# P04 — Traffic loss and recovery review

Offline fictional incident on a separate hypothetical history of three existing P01 route identities: home, guide and protected dashboard. See [P01](../p01-react-vite/README.md) and [registry](registry.json). No real release or collection; do not contact the reserved host. All response, search, account-access, analytics and business counts are invented. The words production, pass and complete refer solely to the supplied simulation. Mode audit/plan and review only; no deployment, tracking changes, credential use or incident response on an actual target.

## Timeline and competing explanations

[Timeline](timeline.json) supplies two declared equal seven-day fictional reporting windows, same home+guide scope, and an incomplete recovery day. Clicks fall 1000 to 600; impressions 20000 to 16000; organic sessions 800 to 300; recorded lead events 40 to 15; accepted leads 40 to 25. These numbers do not establish real comparability or a shared metric denominator. The different relative declines invite measurement review, not subtraction of clicks from sessions or attribution of all loss to technical causes. Demand, presentation, reporting lag, attribution and collection remain hypotheses. No recovery percentage can be calculated from unknown recovery values.

[Observation catalogue](observations.json) records initial and recovery subjects, exact assertion verification, scope, quality and invented timestamps. It is a human-readable crosswalk, not a new provider schema. A guide sample has HTTP noindex; a same-subject repeat does not. Preserve both and investigate gateway/cache/request variability. A preview observation cannot resolve the production claim; incomplete collection evidence is excluded from definite causal support. T12 gateway state conflicting, measurement and demand unresolved. The separate T06 guide projection uses the adverse sample, not a claim that every request was affected; later mock current evidence has no unexpected directive but processing evidence predates the recovery change. Healthy home serves as a narrow supplied observation, not a site-wide control.

## Three review states

| State | T12 | T11 | Remaining boundary |
|---|---|---|---|
| Initial | investigate; no recovery subject | not assessed | cause unresolved |
| Partial | HTTP pass, render unmatched assertion, access missing; investigate | HTTP pass, render stale, access missing; hold | wrong assertion cannot satisfy render |
| Later review | all three fictional technical checks pass; technical_recovery_review | ready_for_owner_review | no real authority, root cause, closure, or search recovery |

Partial retains an incomplete render capture but deliberately supplies the HTTP evidence against the render assertion to show that matching revision alone is insufficient. The later state adds separate exact render and access assertions. No mock evidence is a real passing gate. An additional regression injects a **fictional** credible exposure reference into both later ledgers: escalation overrides otherwise passing checks (no sensitive data present). This is an adverse scenario, not a report of actual exposure.

## Run

From library root, set OUT to an existing fresh private directory. All commands execute existing offline utilities on authored records. No network.

~~~sh
LAB=examples/practice-projects/p04-traffic-incident
for STATE in initial partial review; do
  python3 scripts/review_incident.py --input "$LAB/$STATE/incident.json" --output "$OUT/$STATE-incident.json"
done
for STATE in partial review; do
  python3 scripts/review_release_gates.py --input "$LAB/$STATE/gates.json" --output "$OUT/$STATE-gates.json"
done
for STATE in initial review; do
  python3 scripts/audit_index_evidence.py --input "$LAB/$STATE/index.json" --output "$OUT/$STATE-index.json"
done
~~~

Expected exit 0 for all seven reports: structurally processed, not verified real state. Tests check actual dispositions, blockers, assertion identity, recency and false authorization/closure flags. No new T10 coordinator run: this focused incident uses direct T06, T11 and T12 reports, with SEARCH_DATA and ANALYTICS reviewed manually. Actual provider retrieval and conversion QA unavailable. No additional composite needed.

## Decision and handoff

D1 preserve original conflicting headers and compare equivalent GET requests with controlled route, configuration, revision, profile and timestamps; establish actual coverage before a scoped correction. D2 independently review actual report completeness, cohort filters, business acceptance and consent/collection; no indiscriminate tracking changes. D3 require exact HTTP, render and protected access assertions before technical recovery review; use appropriate authorization and separate rollback plan with access and eligibility checks. D4 keep search/outcome follow-up pending; use matched complete windows and current processed evidence; technical recovery cannot prove search or revenue recovery. D5 credible exposure interrupts discretionary investigation and goes to authorized security/privacy owner regardless of other passes. Proposed owners: delivery maintainer, analytics/privacy owner, authorized security owner and search owner; no actual assignments. No automatic reopening of public access, no forced migration, no promise of rankings, no actual incident closure.

See [T12 procedure](../../technical-incident/README.md), [T11](../../deployment-regression/README.md), [cross-module review](../../../decision-engine/cross-module-review.md), [search platforms](../../../docs/05-measurement/search-platforms.md), [analytics](../../../docs/05-measurement/analytics.md). This exercise is not a benchmark answer or independently evaluated behavior.
