# Methods and data dictionary

## Evidence at candidate grain

One unique six-digit SOC per candidate. The U.S. series contains BLS 2025–2035 projected growth in percent, annual average openings in positions, and 2025 median annual wage in USD. Sacramento-Roseville-Folsom EDD series includes 2023–2033 growth, total projected openings across the decade, and 2026 Q1 median USD per hour. Annual and decade counts retain distinct units. Occupational openings include growth and separations and differ from postings. SOC codes proxy possible outcomes and cannot predict program enrollment.

O*NET skill names are adapted from National Center for O*NET Development, licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The corresponding occupation profiles use the .00 suffix. Course modules are proposed design elements in the snapshot. Published tuition represents listed program pricing with scope and fees recorded in the source registry. One competitor per candidate is a directional scan.

The ranking adds 50% of relative national growth, 25% of relative annual national openings, and 25% of relative Sacramento decade openings. Within each series, divide by its observed maximum. Weights represent analyst judgment. Skills and tuition inform the narrative review. The model does not infer willingness to pay or placement. Validate demand and instructional prerequisites before investment.

## Operational fields required for future authorized use

| Grain | Required fields | Validation and measures |
|---|---|---|
| Cohort | Program, quarter, modality, capacity, enrollment, withdrawals, completion, tuition and direct costs | Unique cohort, capacity at least enrolled, outcomes reconcile, weighted rates use pooled counts. |
| Applicant-stage | Requisition date, anonymous application key, source channel, stage and date | Unique application-stage, monotonic dates and prefix stages. Measure channel conversion, time-to-fill and transition dwell. |
| Ticket | Category, open, close, time threshold, escalation, effort | Validate date order. Calculate on-time closures over closures. Count open backlog and age at cutoff. |
| Feedback | Anonymous observation, date, program, code and cleared text | Document sampling and independent coding review. Compare themes with related quantitative measures and withhold small cells. |

The workbook models contribution as paid seats multiplied by tuition less per-seat variable costs, minus fixed direct costs. Break-even divides fixed cost by the positive per-seat spread and rounds up. Enter institution-approved figures to test scenarios. No operational benchmark, results, sample feedback or scenario inputs accompany the template.

## Imports

Map Name, Description and Section from tasks.csv in the Asana CSV importer. Map role, dependency, priority, and relative due day as custom fields. Set assignees and real dates in an authorized workspace. For CRM/Airtable-style storage, use separate Cohorts, Requisitions, Applications, Stage Events and Tickets tables with relational IDs and controlled categories. Vendor import remains unverified.
