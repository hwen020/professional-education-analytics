import streamlit as st

from analytics import ROOT, load, scenario
from market import market
from public_education import STATE, observations, public_findings

st.set_page_config(page_title="Professional Education Analytics", layout="wide")
st.title("Professional Education Analytics")
page = st.sidebar.radio("Workspace", ["Portfolio", "Instructor recruitment", "Instructor services",
                                     "Qualitative insights", "Market intelligence", "Business case",
                                     "Delivery & governance", "Public education evidence"])
st.header(page)

if page in ("Portfolio", "Instructor recruitment", "Instructor services", "Qualitative insights"):
    needs = {
        "Portfolio": "Cohort capacity, enrollment, outcomes, tuition and direct costs",
        "Instructor recruitment": "Requisition dates and stage events by applicant and channel",
        "Instructor services": "Ticket dates, SLA thresholds and escalation status",
        "Qualitative insights": "Approved feedback text and a documented sampling protocol",
    }
    st.info("No verified operational observations are available for this view.")
    st.write(needs[page])
elif page == "Public education evidence":
    cdcp, provider = observations()
    findings = public_findings(cdcp,provider)
    st.info("Public observations · California public agencies")
    st.write(findings["state"])
    district = st.selectbox("Select state or district", [STATE,*sorted(set(cdcp.district)-{STATE})])
    selected = cdcp[cdcp.district.eq(district)]
    st.subheader("Public noncredit CDCP FTES by fiscal year")
    st.line_chart(selected.set_index("fiscal_year").ftes)
    st.dataframe(selected,hide_index=True,width="stretch")
    st.download_button("Download public FTES CSV",selected.to_csv(index=False),file_name="public-cdcp-ftes.csv")
    st.subheader("Public Calbright headcount and awards")
    st.write(findings["provider"])
    st.caption("June 30 headcount and annual awards use different time grains. No completion rate is calculated.")
    st.dataframe(provider,hide_index=True,width="stretch")
    st.download_button("Download public outcomes CSV",provider.to_csv(index=False),file_name="public-calbright-outcomes.csv")
    st.dataframe(load("education_sources"),hide_index=True,width="stretch")
elif page == "Market intelligence":
    st.subheader("Public Market Evidence")
    st.caption("Public data. BLS annual openings and California EDD decade totals have different units.")
    for frame, file in [(market(), "public-market.csv"), (load("sources"), "source-registry.csv")]:
        st.dataframe(frame, width="stretch")
        st.download_button("Download CSV", frame.to_csv(index=False), file_name=file)
elif page == "Business case":
    st.caption("Enter your own inputs to calculate contribution and break-even. Inputs stay in this session.")
    price = st.number_input("Tuition per paid seat", min_value=0, value=None)
    variable = st.number_input("Variable cost per paid seat", min_value=0, value=None)
    fixed = st.number_input("Fixed direct costs", min_value=0, value=None)
    seats = st.number_input("Paid seats", min_value=0, value=None, step=1)
    if all(value is not None for value in (price, variable, fixed, seats)):
        result = scenario(price, variable, fixed, seats)
        st.metric("Contribution before overhead", f"${result['contribution']:,}")
        st.write("Break-even seats", result["break_even"] if result["break_even"] is not None else "Unavailable")
    st.dataframe(market()[["candidate", "benchmark", "benchmark_usd"]])
else:
    st.markdown((ROOT/"docs/governance.md").read_text(encoding="utf-8"))
    for file in ("executive-summary.pdf", "integrated-report.pdf", "management-executive-brief.pdf", "public-education-case-study.pdf", "analysis-workbook.xlsx"):
        path = ROOT/"deliverables"/file
        if path.is_file():
            st.download_button(file, path.read_bytes(), file_name=file)
