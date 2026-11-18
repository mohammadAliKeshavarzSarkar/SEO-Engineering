# Execution contract

## Determine mode before tool use

| Mode | Permitted by task | Output |
|---|---|---|
| Learn/research | Public source research, authorized data inspection | Evidence-backed explanation or research brief |
| Audit | Authorized read-only inspection; no production writes | Findings, severity, evidence and recommendations |
| Plan | Compare options; no unapproved implementation | Decisions, dependencies, acceptance and rollback |
| Implement | Scoped changes explicitly authorized, with available tools | Diff/commit or precise patch, QA and remaining checks |
| Verify | Authorized tests/inspection; no unrelated writes | Actual pass/fail/blocked/not-run per test |
| Monitor | Configured periodic data access only if explicitly arranged | Dated observations and next decision |

Treat read-only as default; a request for advice is not authorization to publish or deploy. Ask only for material missing authorization or inputs; otherwise give bounded useful work and list unknowns. High-risk migrations, deletions, tracking or deployment require their own appropriate approval, even when other implementation is authorized. Never enumerate unrelated private repositories. Separate target-project records from the universal library.

## Evidence contract

Each finding has stable ID, target, date, source/tool, exact scope, observed fact (or estimate/hypothesis/unknown), expected behavior, confidence and impact. Search evidence includes market/device/date where known; do not silently substitute global results for local results. Avoid raw personal query text, form values or private logs in shared outputs. Current official sources support platform claims, not unobserved site states.

## Verification contract

Record planned tests before execution and actual status separately: pass, fail, blocked, not-run, N/A. A failure stays visible; a missing tool is blocked. Distinguish static output, browser/render, deployed HTTP, processed index, and measured outcomes. Do not conflate them.

Final output includes scope/mode, relevant references, decision and alternative, changed files (if any), evidence, tests with results, privacy/security notes, unresolved blockers, next action and measurement/rollback. Use the library's templates/agent-run-record.md. A project can be technically eligible while unranked; no success guarantees.
