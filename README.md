# Professional Education Analytics & Workforce Intelligence

An independent continuing-education decision-support project built on the existing Python and Streamlit demo. The analysis uses public BLS projections and wages, California EDD Sacramento occupation statistics, O*NET skills and published continuing education fees. Operational data is unavailable in this release.

Data Analytics ranks first under the stated demand weights. Project Management has the largest annual U.S. openings and Sacramento decade openings of the three occupations. These occupational signals justify discovery. Buyer demand, delivery costs and instructor availability remain gate evidence.

| Deliverable | Location |
|---|---|
| Executive summary | [One-page PDF](deliverables/executive-summary.pdf) |
| Integrated decision report | [Nine-page PDF](deliverables/integrated-report.pdf) |
| Excel analysis workbook | [Workbook](deliverables/analysis-workbook.xlsx) |
| Public input and SQLite output | [Source snapshot](data/public_market.csv), [analysis CSV](deliverables/market-evidence.csv), [source registry](data/sources.csv) |
| Governance and task tracker | [Governance](docs/governance.md), [import CSV](data/tasks.csv) |
| Methods and hiring alignment | [Methods](docs/methods.md), [requirements traceability](docs/requirements_traceability.md) |

## Reproduce with Python 3.11

```sh
python -m pip install -r requirements.txt
python build.py
python -m pytest -q
python -m streamlit run app.py
```

The pipeline reads curated, attributed snapshots offline. Repeating the research step requires visiting the registry URLs and reviewing source vintages before updating the CSV. Scenario fields are empty until entered. Contribution excludes indirect costs. The dashboard includes data requirements for portfolio, recruiting, services and feedback so a future authorized operational data release can extend this project.
