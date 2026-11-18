# Synthetic R08 exercise

All items, impact bands and effort estimates are invented, not data from a real website. Assume a single objective and planning horizon.

Run from repository or bundled library root:
```sh
python3 scripts/prioritize_opportunities.py --input examples/opportunity-prioritization/sample.json --output priority-report.json
```
Use a new output filename. Expected lanes: incident (urgent triage regardless of missing evidence); repair (material verified issue, no estimate required); links and guide (growth); migration (risk review); new-market (investigate); new-page (blocked until repair verified); unrelated-content (excluded). Links mid = 4/3, range 1–2. Guide mid = 2.5/4 = 0.625, range 2.5/6–1.25. Ranges overlap; sensitivity review is required. Migration is not ranked ahead merely because of high impact; policy and risk review precede scores. The output order is not a calendar. Resolve incidents/repair and blockers with owner approval; verified prerequisite is an attested acceptance state, not simply planned work.

See [method](../../docs/02-research/r08-opportunity-prioritization.md) and [decision protocol](../../decision-engine/opportunity-prioritization.md).
