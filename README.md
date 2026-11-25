# Professional Education Analytics & Workforce Intelligence

Independent public-data decision support for continuing education. Version 1.1.0 adds observed education trends alongside the existing market research and hypothetical pilot calculator. [Live dashboard](https://professional-education-analytics.onrender.com)

**Public Market Evidence.** Three program opportunities compared using BLS and California EDD occupational forecasts and wages, O*NET skills, and listed tuition. Data Analytics ranks first under the documented screening weights. Project Management has the largest annual U.S. openings and Sacramento decade openings. These series use distinct periods and units.

**Public Education Evidence.** The California Community Colleges Chancellor’s Office reported 57,973.64 noncredit CDCP full-time equivalent students in 2024–25, up 12.1% year over year. The California Legislative Analyst’s Office reports 7,660 Calbright students enrolled on June 30, 2025 and 1,019 calendar-year awards. These measures have different grains and do not form a completion rate. No synthetic records are distributed.

| Deliverable | Link |
|---|---|
| Original market research | [Executive summary](deliverables/executive-summary.pdf), [integrated report](deliverables/integrated-report.pdf), [analysis CSV](deliverables/market-evidence.csv), [public sources](data/sources.csv) |
| New public education research | [Management brief](deliverables/management-executive-brief.pdf), [case study](deliverables/public-education-case-study.pdf), [FTES CSV](deliverables/public-cdcp-ftes.csv), [outcomes CSV](deliverables/public-calbright-outcomes.csv), [education sources](data/education_sources.csv) |
| Excel | [Analysis workbook](deliverables/analysis-workbook.xlsx), including a public FTES Explorer and native public FTES PivotTable |
| Governance and evidence | [Original governance](docs/governance.md), [proposed operations roadmap](docs/operations_delivery.md), [public education methods](docs/public_education_methods.md), [role coverage matrix](docs/requirements_traceability.md) |
| Portfolio materials | [English résumé wording](docs/resume.md), [desktop screenshot](docs/screenshots/public-education-1440.png), [390px mobile screenshot](docs/screenshots/public-education-390.png) |

## Reproduce with Python 3.11

```sh
python -m pip install -r requirements.txt
python build.py
python -m pytest -q
python -m streamlit run app.py
```

`build.py` regenerates the reports, CSVs and portable workbook from local curated snapshots. After rebuilding, run `powershell -File tools/refresh_excel.ps1` on Windows with Excel 16.0 to add, refresh and verify the native PivotTable. The shipped workbook includes it.

The browser smoke script uses an optional Playwright installation and an existing browser binary. Run `python tools/browser_acceptance.py URL --edge PATH`. The Render service is read-only. Hypothetical form inputs remain session-local. Course-level finance, staffing, recruiting, SLA and learner feedback are missing from the selected public datasets. Their dashboard sections describe required inputs and methods.
