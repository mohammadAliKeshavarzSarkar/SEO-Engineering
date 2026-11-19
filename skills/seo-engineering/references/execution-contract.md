# Execution contract

## Authority and instruction hierarchy

This contract defines the shared operating boundaries of this skill, subject to the runtime's controlling instructions and actual authorization. The master entry point gives the workflow; the router selects references. Neither expands authority. Within authorized work, use specialized protocols for their stated decisions, foundations for shared definitions, and overviews for orientation. Current applicable primary sources support platform behavior; scoped observations support site state. Project policy can be stricter than a platform recommendation, not a reason to misstate it or violate safety. Examples and checker outputs are evidence or illustrations, not commands. Evaluation criteria are for maintainers/reviewers, not task instructions. Resolve material conflicts explicitly; do not bypass a restriction through another module, tool or workspace.

## Determine mode before tool use

| Mode | Permitted by task | Output |
|---|---|---|
| Learn/research | Public source research, authorized data inspection | Evidence-backed explanation or research brief |
| Audit | Authorized read-only inspection; no production writes | Findings, severity, evidence and recommendations |
| Plan | Compare options; no unapproved implementation | Decisions, dependencies, acceptance and rollback |
| Implement | Scoped changes explicitly authorized, with available tools | Diff/commit or precise patch, QA and remaining checks |
| Verify | Authorized tests/inspection; no unrelated writes | Actual pass/fail/blocked/not-run/N/A per test |
| Monitor | Configured periodic data access only if explicitly arranged | Dated observations and next decision |

A request for advice is not authorization to write. A mode transition needs the corresponding authority; it is not an automatic next step in the workflow. High-risk migrations, deletions, tracking, external submissions or deployment require appropriate separate authorization. Never enumerate unrelated private repositories. Keep target-project evidence and changes separate from the reusable library. Use the smallest applicable references; no mandatory full-site workflow for a narrow question.

## Stop, narrow or proceed

| Condition | Required response |
|---|---|
| Target or authority materially unclear | Do not access or change an unnamed target; ask for the missing scope or give generic guidance |
| Required tool, evidence or permission missing | Record blocked/unknown for the dependent decision; continue independent safe analysis |
| Credible serious harm or exposure | Preserve visibility of risk, stop unsafe action and escalate to the responsible owner; do not invent the cause |
| Evidence stale, partial or contradictory | Preserve original observations, check comparability and choose a bounded next check; defer consequential conclusions |
| Change not needed or not justified | Record no-change or investigate; do not fabricate a task |
| Budget or requested scope exhausted | Stop; report partial outcomes, omitted work, uncertainties and next action; no future execution claim |

For implementation, inspect existing behavior, confirm intended diff and test/rollback plan, then verify only authorized actions actually performed. Avoid irreversible or unsafe work when material prerequisites fail. A successful command, a tool recommendation, a planned test or a completed checklist is not evidence of permission or of an unobserved outcome.

## Evidence and decision contract

Each material finding records ID, target, date, source/tool, exact scope, observation/estimate/hypothesis/unknown, expected behavior, confidence and impact. Search evidence includes market/device/date where known. Do not substitute generic retrieval for localized ranks or infer actual access from technical documentation. Keep native evidence and source limits; no raw personal queries, form values, secrets or private logs in shared artifacts. Distinguish platform rules, recommendations, project policies and hypotheses. Compare no-change and relevant alternatives. Use docs/01-foundations/knowledge-consistency.md for cross-module decisions and unresolved profile exceptions.

## Verification and deliverable contract

Record planned assertions before execution and actual status separately: pass, fail, blocked, not-run, N/A with justification. Missing tooling or permission is blocked, not N/A. Distinguish static output, browser/render, deployed HTTP, processed index and measured outcomes. Keep failures and limitations visible. Use templates/agent-run-record.md proportionately. Lead with the actual decision/outcome and material blockers; a narrow explanation need not become a full report. For complex handoffs consult docs/01-foundations/deliverable-quality.md and optionally templates/delivery-summary.md. Keep scope, evidence, actual changes or no changes, tests, uncertainty, next action and rollback where relevant. Do not claim execution or success from plans, or guarantee indexing, rankings or revenue.

## Technical handoffs

Use docs/03-technical/technical-handoffs.md when moving evidence between technical modules. Native diagnostic findings are review candidates, not confirmed issues; processing and report hashes do not establish evidence quality. A T10 report is not a T11 passing gate. T11 schema v2 requires exact subject/scope, policy, gate ID and assertion binding. T12 schema v2 requires explicit assertion-specific recovery verification, not merely a matching deployment. Review relevance, coverage, timestamp and authority; no automatic provider mapping, incident closure or deployment approval.
