# Professional Programs Analyst requirements traceability

The requirement categories follow the public UC Davis posting (job 89937). The project is independent. “Demonstrated” refers to artifacts in this repository. [Original public posting](https://careerspub.universityofcalifornia.edu/psc/ucdavis/EMPLOYEE/HRMS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?FOCUS=Applicant&JobOpeningId=89937&Page=HRS_APP_JBPST_FL&PostingSeq=1&SiteId=7&languageCd=ENG)

| Requirement | Evidence and validation | Status or limit |
|---|---|---|
| Minimum · Degree or equivalent | Outside project scope | Degree and equivalent credential or work experience are not established. |
| Minimum · Independently manage complex projects, priorities and dependencies | [Governance](governance.md), [task tracker](../data/tasks.csv) | Documented work plan. Actual delivery with stakeholders is unverified. |
| Minimum · Dashboards, reporting, cases and plans | [Dashboard](../app.py), [workbook](../deliverables/analysis-workbook.xlsx), [brief](../deliverables/executive-summary.pdf), [report](../deliverables/integrated-report.pdf). Page, export and rendering tests. | Demonstrated with public evidence. |
| Minimum · Interpret policies, document procedures and improve operations | [Governance](governance.md) maps 34 CFR §99.31 to proposed workflow and access practices. | Written interpretation and proposed controls. No institutional signoff or outcome. |
| Minimum · Quantitative and qualitative analysis and recommendations | [Public analysis](../deliverables/integrated-report.pdf), [methods](methods.md), export and score tests. | Quantitative analysis demonstrated. Qualitative research protocol only. |
| Minimum · Written and verbal communication, judgment and organization | [Executive brief](../deliverables/executive-summary.pdf), workshop agenda and decision gates. | Written evidence. Verbal facilitation unverified. |
| Minimum · Independent priority management and discretion | [Governance](governance.md), public-only data, missing-data page tests. | Priorities and privacy plan documented. Handling sensitive work records is unverified. |
| Preferred · Measurable education or workforce improvements | [Evaluation plan](governance.md) | No observed improvement or institutional work experience. |
| Preferred · Instructor or specialist recruiting improvements | [Recruitment definitions](methods.md), instructor page smoke test. | Workflow and metric design only. |
| Preferred · Asana, advanced Excel, visualization, Salesforce, Airtable, SIS or financial systems | Excel workbook and actual Excel recalculation, dashboard and CSV import mapping. | Excel and Streamlit artifacts. Actual Asana, Salesforce, Airtable, SIS and financial system usage is unverified. |
| Preferred · Lightcast or comparable labor-market research | [Source registry](../data/sources.csv), [analysis CSV](../deliverables/market-evidence.csv), source and reconciliation tests. | BLS, EDD and O*NET used. Lightcast experience unverified. |
| Preferred · Process-mapping facilitation and workflow documentation | [Swimlanes, RACI and workshop agenda](governance.md) | Proposed process. No workshop facilitated. |
| Preferred · Program portfolios, enrollment, finance and outcomes used for decisions | [Portfolio methods](methods.md), [reports](../deliverables/integrated-report.pdf) | Metric design and public feasibility analysis. Operating dataset unavailable. |
| Preferred · Education structure, approvals, enrollment and online delivery | [Governance](governance.md), [methods](methods.md) | Policy and operating concepts demonstrated. Institution-specific expertise unverified. |
| Responsibility · 30% Program lifecycle | Cohort definitions, planned variance and outcomes, dashboard availability check. | Design coverage only. |
| Responsibility · 30% Instructor services | Recruitment, time-to-fill, SLA, backlog and thematic methods; two page smoke tests. | Design coverage only. |
| Responsibility · 20% Project and process improvement | Governance, RACI, owners, due days, dependency tracker and evaluation plan. | Demonstrated proposal. Implementation impact unverified. |
| Responsibility · 20% Market and analysis | Three SOC mappings, wages, projections, skills, tuition, weighted score and pilot calculator. Verified export reconciliation and PDF rendering. | Demonstrated with public evidence. Buyer demand and pilot economics remain open. |

## Local acceptance

Python 3.11.7 on Windows. Executed `python build.py` and `python -m pytest -q` in the workspace virtual environment. All 14 tests passed. PyMuPDF rendered all ten PDF pages and verified text bounds. Excel 16.0 recalculated the pilot workbook from temporary inputs in read-only mode; demand score, contribution, break-even and sensitivity were verified. Consecutive builds produced identical artifact hashes. The workbook uses summary tables and has no native PivotTables. Data ingestion reproduces the curated snapshot offline. See [GitHub Actions](https://github.com/hwen020/professional-education-analytics/actions) for Linux CI and the [Render service](https://professional-education-analytics.onrender.com) for the hosted dashboard.
