"""Generate the public market decision package."""
import sqlite3
from xml.sax.saxutils import escape

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from analytics import ROOT, load
from market import demand_score, market
from education_package import build_evidence, write_evidence

OUT = ROOT / "deliverables"


def pdf(path, pages, source=None):
    styles = getSampleStyleSheet()
    styles["BodyText"].fontSize = 11
    styles["BodyText"].leading = 16
    styles["Title"].textColor = colors.HexColor("#173854")
    body = []
    for index, (title, paragraphs, grid) in enumerate(pages):
        if index:
            body.append(PageBreak())
        body.extend([Paragraph("PROFESSIONAL EDUCATION ANALYTICS", styles["Normal"]),
                     Paragraph(escape(title), styles["Title"]), Spacer(1, 15)])
        for paragraph in paragraphs:
            body.extend([Paragraph(escape(paragraph), styles["BodyText"]), Spacer(1, 12)])
        if grid:
            table = Table([[Paragraph(escape(str(value)), styles["BodyText"]) for value in row]
                           for row in grid], repeatRows=1, hAlign="LEFT",
                          colWidths=[450/len(grid[0])]*len(grid[0]))
            table.setStyle(TableStyle([("BACKGROUND", (0,0),(-1,0),colors.HexColor("#D4E8EE")),
                                       ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F3F6F7")]),
                                       ("VALIGN",(0,0),(-1,-1),"TOP"),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
            body.append(table)

    def footer(canvas, document):
        canvas.setFont("Helvetica", 9)
        canvas.drawString(72, 42, source or "Independent decision-support demonstration")
        canvas.drawRightString(document.pagesize[0]-72, 42, str(document.page))

    SimpleDocTemplate(str(path), title=pages[0][0], author="Professional Education Analytics", invariant=True).build(
        body, onFirstPage=footer, onLaterPages=footer)



def main():
    OUT.mkdir(exist_ok=True)
    build_evidence(pdf, OUT)
    evidence = market()
    ranks = demand_score()
    sources = load("sources")
    assert evidence.soc.is_unique and evidence.notna().all().all()
    with sqlite3.connect(":memory:") as db:
        evidence.to_sql("public_market", db, index=False)
        db.executescript((ROOT/"views.sql").read_text(encoding="utf-8"))
        pd.read_sql_query("SELECT * FROM market_evidence", db).to_csv(OUT/"market-evidence.csv", index=False)

    lead = ranks.iloc[0]
    decision = f"Prioritize {lead.candidate} for discovery based on the published occupation indicators and the screening weights. Hold investment until Finance approves costs, the academic owner validates curriculum scope, and paid-seat evidence supports break-even."
    table = [["Candidate / SOC","U.S. growth","U.S. annual openings","Sacramento decade openings","Tuition"]]+[
        [f"{x.candidate} / {x.soc}",f"{x.bls_growth_pct:g}%",f"{x.bls_annual_openings:,}",
        f"{x.edd_decade_openings:,}",f"${x.benchmark_usd:,}"] for x in evidence.itertuples()]
    lack = "Verified continuing education cohort, recruitment, service and feedback observations were unavailable for this project. The operating sections provide measurement definitions and implementation steps."
    pdf(OUT/"executive-summary.pdf", [("Executive summary",[decision,lack,
        "U.S. projections cover 2025–2035. Sacramento projections cover 2023–2033. Openings are occupational estimates. The figures cannot establish learner demand or enrollment.",
        "By day 15, the analyst should validate buyer demand. By day 25, the program manager should confirm staffing. On day 30, the director should review evidence and record a go or hold decision."],table)])
    pdf(OUT/"integrated-report.pdf", [
        ("Integrated decision report",[decision,lack,
         "The analysis compares Data Analytics, Cybersecurity and Project Management as candidate short courses. Each candidate maps to a standard occupation and a publicly priced continuing education offering."],[]),
        ("Portfolio performance design",[
         "The proposed cohort grain ties together census enrollments, capacity, withdrawals, completions, tuition, refunds, direct costs and a target. Collect quarter and modality to preserve comparability.",
         "Use enrolled divided by capacity for fill and completed divided by enrolled for completion. Track paid tuition net of refunds. Deduct direct cost for contribution before overhead. Pool counts across selected cohorts and withhold undefined rates.",
         "Reconcile census counts with the registrar and direct costs with Finance. Review deviations against approved targets before deciding whether to expand, redesign or discontinue an offering. No baseline is available."],[]),
        ("Instructor recruitment measurement",[
         "Track sourcing, outreach, screening, interview, offer and hire with one first-entry timestamp per application and stage. Preserve closed and still-open requisitions in separate counts.",
         "Use hires divided by sourced for channel conversion. Use hire date minus requisition opening date for fill time. Report completed transition dwell and pending cases separately.",
         "Ask Instructor Services and the academic reviewer to agree on the screening rubric and handoff ownership. Validate unique application-stage keys and strictly ordered stage sequences before interpreting conversion."],[]),
        ("Instructor service and qualitative analysis",[
         "Use on-time closed tickets divided by closed tickets for the resolution SLA. Report backlog at cutoff with age since open, escalation counts and tracked effort. Separate contract, onboarding and classroom support queues.",
         "Predefine the feedback sample and codebook. Proposed codes include contract clarity, onboarding access, schedule flexibility and applied practice. Record inclusion criteria and review coding disagreements.",
         "Compare coded themes with ticket categories where dates and populations align. Require approved feedback and quote consent or documented de-identification before release. No themes or quotes were observed."],[]),
        ("Labor market and competition",[
         "BLS national projections are for 2025–2035. California EDD Sacramento projections are for 2023–2033. Annual BLS counts and EDD decade totals enter the score as separate normalized factors.",
         "Program tuition is a published amount for a credential or sequence. Compare duration, eligibility and fees before using it as a price anchor for a short pilot."],table),
        ("Skills and candidate ranking",[
         "The screening score uses 50% relative national growth, 25% relative national annual openings and 25% relative Sacramento decade openings. Each factor divides by the highest observed value in this set.",
         "Proposed curriculum maps programming to a Python module, problem solving to an analytics capstone and decision making to an options memo. Cybersecurity maps critical thinking and systems analysis. Project management maps coordination, time management and decision making.",
         "Skills and listed prices inform the qualitative review. Role proxies, self-selection and differences in training depth limit inference. Repeat the ranking with new evidence."],
         [["Candidate","Evidence score"]]+[[x.candidate,f"{x.score:.3f}"] for x in ranks.itertuples()]),
        ("Business case and decision gates",[
         "Leave proposed tuition, variable spending, fixed spending and low, base and high paid seats blank until an owner provides inputs. Contribution equals paid seats times tuition less variable cost per paid seat, minus fixed direct costs.",
         "Break-even rounds fixed costs divided by positive contribution per seat up to the next whole seat. Review refunds, marketing costs, staffing and overhead before approval.",
         "Days 15, 25 and 30 are planning deadlines from kickoff for demand evidence, instructor readiness and the director decision. Use the workbook to test exposure across the three seat levels."],[]),
        ("Governance and privacy",[
         "34 CFR 99.31(a)(1)(i)(A) and (a)(1)(ii) address qualifying school officials and reasonable methods to limit access. Section 99.31(b)(1) addresses de-identified disclosures.",
         "Have the responsible institution determine applicable privacy and records policies before onboarding. The proposed workflow assigns separate responsibilities for approvals, record access and publication.",
         "Release aggregate data only after disclosure review. Confirm legal holds and deletion policy with Records. Use the governance plan and task tracker for workshop and implementation planning."],[]),
        ("Sources and limitations",[
         "The source registry records the direct BLS, California EDD, O*NET, continuing education and regulation URLs and their retrieval dates, units and reuse notes.",
         "Run python build.py to regenerate the reports, evidence CSV and workbook. The market snapshot is a curated transcription. The SQLite view preserves the reported national and local units.",
         "Obtain buyer signals, employer validation, comparable offerings and verified operating data before expanding this case to an institutional decision. Occupational openings do not measure education market share."],[])
    ])
    with pd.ExcelWriter(OUT/"analysis-workbook.xlsx", engine="xlsxwriter") as writer:
        book = writer.book
        book.set_calc_mode("auto")
        book.set_properties({"created": pd.Timestamp(sources.retrieved.max()).to_pydatetime()})
        for name, frame in {"Public market":evidence,"Sources":sources,"Demand summary":ranks}.items():
            frame.to_excel(writer,sheet_name=name,index=False)
            ws = writer.sheets[name]
            ws.freeze_panes(1,1)
            ws.autofilter(0,0,len(frame),len(frame.columns)-1)
            ws.set_column(0,len(frame.columns)-1,22)
        demand = writer.sheets["Demand summary"]
        demand.set_column("C:E",18)
        weight_format = book.add_format({"bg_color":"#D4E8EE","num_format":"0%"})
        demand.write_row("A7",["Growth weight","U.S. openings","Local openings"])
        for col, weight in enumerate([.50,.25,.25]):
            demand.write_number(7,col,weight,weight_format)
        demand.data_validation("A8:C8",{"validate":"decimal","criteria":"between","minimum":0,"maximum":1})
        for index, row in enumerate(ranks.itertuples(),start=2):
            source_row = int(evidence.index[evidence.soc.eq(row.soc)][0])+2
            formula = "+".join(f"${weight}$8*'Public market'!{metric}{source_row}/MAX('Public market'!{metric}$2:{metric}$4)"
                               for weight,metric in zip("ABC","DEH"))
            demand.write_formula(f"C{index}","="+formula,None,row.score)
        demand.write("A10","Weight total")
        demand.write_formula("B10","=SUM(A8:C8)",weight_format,1)
        demand.write("A11","Summary table; sort again after changing weights.")
        ws = book.add_worksheet("Pilot inputs")
        ws.set_column("A:A",30)
        ws.set_column("B:D",19)
        entry = book.add_format({"bg_color":"#D4E8EE","num_format":"0"})
        cash = book.add_format({"num_format":"$#,##0;($#,##0)"})
        for i, title in enumerate(["Tuition per paid seat","Variable cost per paid seat","Fixed direct costs"]):
            ws.write(i,0,title)
            ws.write_blank(i,1,None,entry)
        ws.write_row("A5",["Scenario","Paid seats","Contribution","Break-even seats"])
        for i,name in enumerate(["Low","Base","High"],start=6):
            ws.write(f"A{i}",name)
            ws.write_blank(f"B{i}",None,entry)
            ws.write_formula(f"C{i}",f'=IF(COUNT(B$1:B$3,B{i})=4,(B$1-B$2)*B{i}-B$3,"")',cash,"")
            ws.write_formula(f"D{i}",'=IF(AND(COUNT(B$1:B$3)=3,B$1>B$2),ROUNDUP(B$3/(B$1-B$2),0),"")',None,"")
        ws.data_validation("B1:B3",{"validate":"decimal","criteria":">=","value":0})
        ws.data_validation("B6:B8",{"validate":"integer","criteria":">=","value":0})
        chart = book.add_chart({"type":"column"})
        chart.add_series({"name":"Scenario contribution","categories":"='Pilot inputs'!$A$6:$A$8",
                          "values":"='Pilot inputs'!$C$6:$C$8"})
        chart.set_title({"name":"Contribution by paid-seat scenario"})
        ws.insert_chart("A11",chart)
        matrix = book.add_worksheet("Price cost sensitivity")
        matrix.set_column("A:F",20)
        matrix.write_row("A1",["Alternative","Price per seat","Unit direct cost","Base seats","Fixed direct cost","Contribution"])
        for i, label in enumerate(["Alternative A","Alternative B","Alternative C"], start=2):
            matrix.write(f"A{i}",label)
            matrix.write_blank(f"B{i}",None,entry)
            matrix.write_blank(f"C{i}",None,entry)
            matrix.write_formula(f"D{i}",'=IF(COUNT(\'Pilot inputs\'!B7),\'Pilot inputs\'!B7,"")',None,"")
            matrix.write_formula(f"E{i}",'=IF(COUNT(\'Pilot inputs\'!B3),\'Pilot inputs\'!B3,"")',cash,"")
            matrix.write_formula(f"F{i}",f'=IF(COUNT(B{i}:E{i})=4,(B{i}-C{i})*D{i}-E{i},"")',cash,"")
        matrix.data_validation("B2:C4",{"validate":"decimal","criteria":">=","value":0})
        qa = book.add_worksheet("QA")
        qa.set_column("A:A",34)
        qa.write("A1","Missing SOC values")
        qa.write_formula("B1","=COUNTBLANK('Public market'!B2:B4)",None,0)
        qa.write("A2","Candidate rows")
        qa.write_formula("B2","=COUNTA('Public market'!A2:A4)",None,len(evidence))
        guide = book.add_worksheet("Read me")
        guide.write("A1","Public observations are on the market sheet. Demand summary is a summary table.")
        guide.write("A2","Blue scenario cells accept your own data. Background data remains blank until entered.")
        write_evidence(writer)


if __name__ == "__main__":
    main()
