import streamlit as st

from analytics import ROOT, load, scenario
from market import market

st.set_page_config(page_title="Professional Education Analytics", layout="wide")
st.title("Professional Education Analytics")
page = st.sidebar.radio("Workspace", ["Portfolio", "Instructor recruitment", "Instructor services",
                                     "Qualitative insights", "Market intelligence", "Business case",
                                     "Delivery & governance"])
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
elif page == "Market intelligence":
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
    for file in ("executive-summary.pdf", "integrated-report.pdf", "analysis-workbook.xlsx"):
        path = ROOT/"deliverables"/file
        if path.is_file():
            st.download_button(file, path.read_bytes(), file_name=file)
