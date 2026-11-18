# Opportunity prioritization decision protocol

Use [R08](../docs/02-research/r08-opportunity-prioritization.md) for research and implementation backlogs. This is not authorization.

1. Determine actual or credible suspected harm and scope. Keep P0 visible and escalate to appropriate authorized owner, even if evidence, risk or dependencies are unresolved. No discretionary score.
2. Identify P1 material defects. Resolve prerequisite, evidence and risk blockers promptly; do not place them behind unrelated optional work just because their lane is blocked/review.
3. Reject unsuitable or prohibited optional work. Record reasons and reconsider only if real conditions change.
4. For remaining candidates, check fit, evidence and acceptable risk; gather evidence or seek reviewed mitigation if missing. Validate dependency IDs and acceptance, block unverified prerequisites; investigate cycles and excluded prerequisites.
5. Score eligible P2/P3 work under one defined objective/horizon using impact × confidence / effort. Leave unknowns null. Review ranges, tradeoffs, learning value, resources, timing, shared dependencies and no-change. Score is not ranking probability, a budget optimizer or execution permission.
6. Select a feasible batch, document overrides, owner, authorization, acceptance, rollback and outcome review. Preserve rejected/deferred work with reason and trigger. Validate actual implementation and separately measure search/business outcomes.

Use [backlog](../templates/opportunity-backlog.csv) and [review record](../templates/priority-review.md). For urgent defects use [troubleshooting](../docs/06-operations/troubleshooting.md) and [release gates](../docs/06-operations/audit-and-release.md). Do not execute or deploy solely from the utility report.
