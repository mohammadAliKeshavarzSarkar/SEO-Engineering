# Response and deliverable quality

TS07.5 — internal output method, not a search-platform requirement or model evaluation result. Apply the execution contract first. Choose the smallest useful communication format for the requested task, actual evidence and stakes. Do not make the user read an entire run record to get a simple answer.

## 1. Select output depth

| Level | Use when | Minimum useful content |
|---|---|---|
| Direct | Narrow explanation or independent question | Answer, material qualification, relevant source when needed |
| Decision brief | One scoped finding, recommendation or choice | Outcome, evidence/scope, uncertainty, alternatives if material, recommended next check or action and authorization boundary |
| Work package | Multi-step research/audit, implementation or verification | Executive decision summary, coverage, traceable findings, dependencies and priorities, actual changes/results, risk, next actions and supporting artifacts |
| Incident update | Credible serious harm or time-sensitive failure | Known symptom/scope, independent escalation, current containment/authority, unknowns, held work and next safe check |

These are communication formats rather than task modes. An incident update can be concise even when the investigation is complex. A broad report is not evidence of broad coverage. A request to explain does not require touching the repository or building a formal report. User-specified format and language govern within safety and evidence constraints; provide plain-text alternatives where needed.

## 2. Lead with the decision and the real state

State the answer or disposition first (proposed, held, investigated, implemented within scope, verified at stated stage, or unresolved). Separate a recommendation, its approval, its implementation and its verification. Do not describe unavailable data as zero, a recommendation as a completed fix, or a queued check as passing. Make credible urgent harm and consequential blockers visible in the summary. If nothing should change, say why.

For longer work, state target, task mode, relevant scope and exclusions; reference exact revision/artifact and environment when applicable. Describe what was actually done, observed and omitted. Report mixed results without averaging safety-critical failures into a general positive score.

## 3. Mode-specific handoff

| Mode | Deliverable emphasis |
|---|---|
| Learn/research | Answer the question with scoped primary-source claims; separate raw observations, estimates and inferred intent; show missingness and suggested next evidence |
| Audit | Explain coverage and reviewed findings, separate symptoms and unconfirmed candidates; priority, reproduction, impact/confidence, smallest justified next action |
| Plan | Compare feasible options including no-change, prerequisites, expected value, risk, owner, effort bounds if supported, acceptance and rollback |
| Implement | Provide actual changed files/diff/commit or clearly labeled proposed patch, rationale, exact scope, local tests, blockers and unrun deployment checks |
| Verify | Expected assertion, actual observed result, subject and stage, evidence and status for each applicable check; independent authority decision |
| Monitor | Only actual configured and authorized observations, time window and baseline, anomalies/limitations, uncertainty and next decision; do not promise a future check without a configured mechanism |

Choose the relevant existing artifact rather than invent a new universal format. For detailed work use [agent run record](../../templates/agent-run-record.md) and, if useful, [delivery summary](../../templates/delivery-summary.md). For findings use [audit finding](../../templates/audit-finding.md), for recommendations use [decision record](../../templates/decision-record.md), for release assertions use T11 and for incidents use T12 and their native records. A summary does not replace a native evidence receipt, test report, decision or approval.

## 4. Make every material finding actionable

A finding has a stable reference, target/scope, expected and actual behavior, evidence/source date, observed versus estimated or hypothetical status, severity and confidence, user/business impact and its limits. Cite the actual evidence supporting the claim, not an unrelated reference or a tool's mere existence. Give a reproducible safe next step, proposed owner if not assigned, prerequisites, acceptance assertion, and rollback when an action is proposed. Use code only where it fits the verified target and stack; distinguish illustrative snippets from exact tested patches. Never invent an owner, file, test command result, link, credentials, permissions, rankings or metrics.

For audit coverage, record planned scope versus actual examined routes/templates, omitted or unreachable sections, sampling method, date/environment and remaining unknowns. Use a denominator only when the intended population is known; a sample is not an entire inventory. Preserve unassigned or deferred native findings. Use R08 for backlog scoring; no numerical health score, impact estimate, percentage gain or effort claim without defined method and supporting inputs. P0/P1 must remain visible independently of discretionary scoring.

Keep private evidence in an approved restricted store; use sanitized stable references in shared reports. Do not reproduce sensitive URLs, search queries, form values, traces, health data or credentials. If safe evidence cannot be shared, describe the limitation and authorized verification path.

## 5. Verify at the correct layer

Record planned assertions and actual outcomes separately. Pass, fail, blocked, not-run and N/A (with rationale) describe actual verification; use native tool states where required. No missing evidence becomes a pass. Do not infer an indexed state from a local build, a live state from source files, a business conversion from an event count, a release from a commit, or real agent quality from offline tests. Keep scope, coverage and freshness explicit. Report actual test counts only with a known source, and distinguish previous from current revision results. Link to real delivered artifacts; no fabricated receipt or file link.

For a work package, finish with a small ordered set of next actions, their purpose, owner or proposed owner, required authorization/evidence, and the condition that closes each. Do not turn the list into automatic execution. Group secondary detail in supporting artifacts rather than repeating all earlier decisions. For a narrow question, do not add exhaustive checklists, arbitrary metrics or unnecessary visuals. Provide user-facing language suitable to the actual audience; preserve technical names, units and raw identifiers when needed.

## 6. Final review (before reporting)

- Does the first paragraph answer the actual task and distinguish completed from proposed work?
- Are only material assumptions, evidence limitations and conflicts exposed, with known coverage?
- Are risks, failed/blocked/not-run checks and independent escalation visible?
- Do recommendations include actionable evidence, dependencies and verification, without implied authority?
- Are native evidence and actual file references preserved, sensitive details excluded, and no unsupported outcome claims made?
- Is the output proportional and usable by its audience, without padding or forced metrics?

See [fictional examples](../../examples/deliverable-quality/README.md). They demonstrate format choices only and are not benchmark answers or measured agent performance.
