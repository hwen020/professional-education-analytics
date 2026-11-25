"""Export independently labeled public education evidence."""
from xlsxwriter.utility import xl_col_to_name

from analytics import load
from public_education import STATE, observations, public_findings


def build_evidence(pdf, out):
    cdcp, provider = observations()
    cdcp.to_csv(out/"public-cdcp-ftes.csv",index=False)
    provider.to_csv(out/"public-calbright-outcomes.csv",index=False)
    facts = public_findings(cdcp,provider)
    decision = "Use these aggregates for context and trend review. Require matched cohort, cost and capacity records before making a program-level decision."
    pdf(out/"management-executive-brief.pdf",[
        ("Public education management brief",[facts["state"],facts["provider"],decision,
         "Headcount is a point-in-time measure; awards are a calendar-year flow. The workbook keeps the two measures and statewide FTES separate.",
         "Assign the analyst to validate cohort definitions and the program director to own the decision gate. The case contains published education records only."],
         [["Metric family","Coverage"],["Public trend and awards","State, selected districts and published provider totals"],
          ["Program operations","Requires approved program and event records"]])
    ],source="Public Education Evidence")
    state = cdcp[cdcp.district.eq(STATE)]
    district = cdcp[cdcp.district.ne(STATE) & cdcp.fiscal_year.eq(state.fiscal_year.iloc[-1])]
    pdf(out/"public-education-case-study.pdf",[
        ("Public education analytics case study",[facts["state"],facts["provider"],decision],[]),
        ("Sources and analysis grains",[
         "The California Community Colleges Chancellor's Office CDCP report provides fiscal-year attendance equivalents. Tables 1 and 2 provide district and statewide values.",
         "The California Legislative Analyst's Office reports Calbright point-in-time enrollment and annual award counts in Figure 11 of its 2026-27 budget analysis. Public source details and URLs are in data/education_sources.csv.",
         "The district comparison is the first 16 eligible rows in published table order. Selection is a reproducibility choice and cannot estimate a statewide district distribution."],[]),
        ("Statewide noncredit attendance trend",[facts["state"],
         "Use fiscal-year FTES as the attendance-volume unit. Year-over-year change divides change by prior-year FTES when that base is positive."],
         [["Fiscal year","FTES","YoY change"]]+[[r.fiscal_year,f"{r.ftes:,.2f}",f"{r.yoy_rate:+.1%}" if r.yoy_rate==r.yoy_rate else "Unavailable"]
                                               for r in state.itertuples()]),
        ("Selected district comparisons",[
         "Compare levels and percentage changes together. An increase from a small base can produce a large percentage without adding much volume. A zero base yields an unavailable growth rate.",
         "The workbook and CSV include the full 16-district cut. The largest six current-year totals in that cut are displayed below."],
         [["District","Current-year FTES","Absolute change"]]+[[r.district,f"{r.ftes:,.2f}",f"{r.change_ftes:+,.2f}"]
             for r in district.nlargest(6,"ftes").itertuples()]),
        ("Online provider headcount and awards",[facts["provider"],
         "Divide each change by its own previous-year count. The cohorts for June headcount and calendar awards do not align, so no completion rate is calculated."],
         [["Year","June 30 headcount","Calendar-year awards"]]+[[r.year,r.june_30_enrollment,r.calendar_year_awards] for r in provider.itertuples()]),
        ("Portfolio decisions and missing data",[
         "A course-health score needs comparable course-level objectives, capacity and learner outcomes. These datasets do not include those denominators. They also do not measure course applications, withdrawals, tuition, refunds or direct costs.",
         decision,"For future authorized analysis, measure fills against capacity, completion against the defined start cohort and contribution against net tuition. Review like-for-like periods with Finance and Academic owners."],[]),
        ("Recruitment, services and qualitative scope",[
         "No verified public applicant histories, teaching coverage records, service timestamps or attributable feedback records are included. Recruiting funnel conversion, fill time, service SLA, backlog and theme prevalence remain unavailable.",
         "Agree on event timestamps and analyst access before collection. Pilot an auditable coding protocol and use a defined eligible population for any eventual interview or survey."],[]),
        ("Governance and decision gates",[
         "By day 30, confirm scope, source ownership and cohort definitions. By day 60, validate an authorized intake and report missingness with denominators. By day 90, record whether a pilot has adequate buyer, staffing and cost evidence.",
         "The governance plan provides approval and privacy controls. Roadmap actions are proposals. The public labor-market forecasts and hypothetical pilot calculator remain independent of the education observations."],[])
    ],source="Public Education Evidence")


def write_evidence(writer):
    cdcp, provider = observations()
    book = writer.book
    percent = book.add_format({"num_format":"0.0%"})
    numeric = book.add_format({"num_format":"#,##0.00"})
    highlight = book.add_format({"bg_color":"#FCE8DE"})
    for name, frame in {"Public CDCP FTES":cdcp,"Public Calbright":provider,"Education sources":load("education_sources")}.items():
        frame.to_excel(writer,sheet_name=name,index=False)
        ws = writer.sheets[name]
        ws.freeze_panes(1,1)
        ws.set_column(0,len(frame.columns)-1,23)
        if name=="Public CDCP FTES":
            ws.add_table(0,0,len(frame),len(frame.columns)-1,
                         {"name":"PublicFTES","columns":[{"header":header} for header in frame.columns]})
            ws.set_column("C:D",18,numeric)
            ws.set_column("E:E",18,percent)
            ws.conditional_format(f"E2:E{len(frame)+1}",{"type":"cell","criteria":"<","value":0,"format":highlight})
            for i,row in enumerate(frame.itertuples(),start=2):
                if i>2 and row.fiscal_year!="2020-21":
                    ws.write_formula(f"D{i}",f"=ROUND(C{i}-C{i-1},2)",numeric,row.change_ftes)
                    ws.write_formula(f"E{i}",f'=IF(C{i-1}>0,C{i}/C{i-1}-1,"")',
                                     percent,row.yoy_rate if row.yoy_rate==row.yoy_rate else "")
        else:
            ws.autofilter(0,0,len(frame),len(frame.columns)-1)
    ws = book.add_worksheet("Public FTES Explorer")
    ws.set_column("A:A",27)
    ws.set_column("B:C",20)
    ws.write("A1","Public observations · CDCP fiscal-year FTES")
    ws.write("A2","Select district or state")
    ws.write("B2",STATE)
    ws.data_validation("B2",{"validate":"list","source":list(cdcp.district.unique())})
    ws.write_row("A4",["Fiscal year","FTES","YoY rate"])
    state = cdcp[cdcp.district.eq(STATE)]
    end = len(cdcp)+1
    for i,row in enumerate(state.itertuples(),start=5):
        ws.write(f"A{i}",row.fiscal_year)
        ws.write_formula(f"B{i}",f"=SUMIFS('Public CDCP FTES'!C2:C{end},'Public CDCP FTES'!A2:A{end},B$2,'Public CDCP FTES'!B2:B{end},A{i})",numeric,row.ftes)
        if i>5:
            ws.write_formula(f"C{i}",f'=IF(B{i-1}>0,B{i}/B{i-1}-1,"")',percent,row.yoy_rate)
    chart = book.add_chart({"type":"line"})
    chart.add_series({"name":"Public CDCP FTES","categories":"='Public FTES Explorer'!$A$5:$A$9",
                      "values":"='Public FTES Explorer'!$B$5:$B$9"})
    chart.set_title({"name":"Public observations: noncredit CDCP FTES"})
    chart.set_y_axis({"min":0,"name":"FTES"})
    ws.insert_chart("E4",chart)
    writer.sheets["Read me"].write("A4","Public education observations have separate tabs; refer to Education sources for data definitions.")
