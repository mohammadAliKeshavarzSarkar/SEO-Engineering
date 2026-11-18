# Technical module handoffs and status semantics

Status: TS01 reviewed internal architecture. This is a procedural integration contract, not a shared external JSON schema.

| Source | Output and identity | Downstream boundary |
|---|---|---|
| R01–R07/R09 | Reviewed goals, intended routes, locale and page ownership | T01–T09 receive relevant project intent, not estimated demand as technical fact |
| T01–T09 | Module-native observations and review/deferred flags, local scope and method | T10 uses explicit reviewed input projections; do not assume shared IDs or identical scopes |
| T10 | Native reports, bound signal pointers, module states, reviewed groups | R08 may prioritize reviewed candidates; T11 consumes separately checked assertion evidence, not process exit status |
| R08 | Reviewed priority and dependencies | Not a security override, causal diagnosis or implementation authority |
| T11 | Scope/revision/artifact/environment/profile/config, policy and assertion-bound gate checks | Owner chooses release; production must be verified separately from candidate |
| T12 | Competing hypothesis evidence and recovery assertion checks | Owner decides cause, containment and closure; search/field/business follow-up remain separate |

## Preserve distinct axes

- Observation completeness (complete/partial/unknown or native equivalent) and context match are not the same as issue severity.
- T10 processed/blocked/failed/not_applicable describes execution; processed is not pass. Native deferred flags remain unknown. T10 grouping validation errors require rerunning without rejected groups to recover native output; do not silently reuse stale groups.
- Review candidate is not confirmed defect; human review establishes expectations, relevance, affected scope and decision.
- Required gate pass/fail/incomplete/missing/stale and optional gaps are T11 dispositions under reviewed policy, not site-wide health. Exposure is escalated independently when reported.
- T12 support_only/refute_only/conflicting/unresolved are descriptions of assessed evidence, not causal inference. Technical recovery review is not incident closure.
- Verification statuses in the general execution contract apply to actual tests, not module processing. Never translate a missing datum, partial sample or unrun test into a pass. Do not convert one tool's exit zero into another tool's evidence assertion.

For any handoff record exact reviewed scope and provenance, method/schema, observed versus expected assertion, timestamp, environment, revision/artifact/config/profile as applicable, coverage and limitations, and reviewer. Preserve the original evidence references and report hash where relevant. Correct same-name IDs and matching revision strings are insufficient. T11/T12 v2 reject v1 inputs; review old records before constructing new assertion bindings. These checks only compare supplied declarations; no signature, referent or real-world accuracy verification.

For technical authorization, safety and project scope, follow the execution contract; specialized protocols refine older overviews. Keep restricted evidence outside the universal library. WebsiteBotScroll evidence mapping still requires an independently reviewed/versioned contract. No network or provider compatibility implied.
