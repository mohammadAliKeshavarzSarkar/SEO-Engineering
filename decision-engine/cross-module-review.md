# Cross-module decision and dependency review

Use when multiple selected routes share evidence, produce competing recommendations, or require one another's decisions. For a narrow independent task use its own protocol instead. This is a review procedure, not a decision engine executable, a provider mapping, or authorization.

## 1. Separate the claims before resolving a conflict

Record what each source actually establishes, including the asserted subject, stage, revision, environment, configuration, locale, collection time, method, coverage and limitations as relevant. Distinguish intended policy from observed behavior. Primary documentation establishes applicable platform behavior, not site state. A tool's local finding does not establish a search-platform penalty. Compare assertions, not only matching IDs, dates or labels.

Classify each apparent conflict:

| Class | Example | Response |
|---|---|---|
| Different subject/scope | Local build HTML vs CDN response | Preserve both; inspect actual deployment and match subjects |
| Different stage or time | Current redirect vs earlier indexed canonical | Preserve both; check last crawl/config/release and processing lag |
| Different assertion | Crawl permitted vs index eligible | Check each independently; neither entails the other |
| Different metric/population | Search clicks vs accepted leads | Match scope and denominators where possible; no forced numeric reconciliation |
| Policy vs evidence | Strict locale profile flags a documented alias | Review actual platform applicability and project policy separately |
| Actual disagreement | Comparable same-subject, same-stage captures disagree | Preserve contradicting records; examine collection method, variance and discriminating test |
| Competing objectives | Faster initial delivery vs required interaction or accessibility | Compare alternatives and acceptance/rollback; no universal maximization |

Do not average categorical observations, choose the most convenient result, assume newest is necessarily applicable, or convert missingness to negative evidence. If a source is superseded, preserve the old record and justify applicability of its replacement. Where evidence is not comparable, call it noncomparable, not refuted.

## 2. Define the dependency graph at decision level

Use specific proposed decisions or assertions as nodes, not whole modules. Include the decision ID, responsible route/owner, scope, exact expected assertion, required evidence, actual status and next check. An edge from prerequisite A to dependent B means B needs the reviewed result of A for a specified decision. Classify edges as:

- Hard: progress on the dependent decision would be unjustified without the prerequisite assertion and evidence.
- Conditional: hard only if an explicitly recorded condition holds; unknown material conditions require investigation, not automatic removal.
- Advisory: helpful but not necessary for this decision; record omission when material.

Do not make all possible module links hard prerequisites. Resolve cycles by inspecting the decision definitions: split discovery from implementation or choose a safe independent discriminating test. Never mark a node passed to break a cycle. A prerequisite can be adequate for a preliminary decision while still inadequate for later execution. A proposed or approved decision is not an observed verified prerequisite; bind what is needed to the actual acceptance assertion and context. Reuse a reviewed observation only after checking relevance and scope again.

## 3. Propagate uncertainty without hiding urgent risk

| Prerequisite condition | Dependent action |
|---|---|
| Relevant current assertion verified | Continue evaluating remaining evidence and permissions |
| Failed assertion | Hold actions requiring that assertion; choose correction or supported alternative |
| Missing, incomplete, stale, contradictory or blocked | Hold the dependent conclusion/action; identify next minimum safe check |
| Genuinely inapplicable | Remove edge only after reasoned review of its condition |
| Independent urgent credible harm | Escalate to responsible authorized owner even when causal evidence or other prerequisites remain unresolved |

A failed dependency is not proof the dependent hypothesis is false. It may prevent an implementation decision yet leave a separate exploration possible. Hold only the decisions that rely on it. Do not lower risk merely because confidence is low; do not treat escalation as permission to edit production. Use R08 for reviewed backlog lanes and dependencies, T11 for actual deployment gate assertions, and T12 for causal hypotheses and recovery checks. Those native contracts remain unchanged.

## 4. Reconcile proposed actions

Before recommending action, list the actual tradeoff: expected user/business benefit, security/privacy, eligibility, accessibility/function, compatibility, cost and reversibility. Preserve valid URLs and working functionality unless a supported decision justifies change. Use no-change, limited experiments, scoped fixes, and staged rollout as alternatives where appropriate. Reject any option that violates scope or safety regardless of its growth score. If two acceptable options still depend on missing evidence, choose a bounded investigation, not both edits simultaneously.

Select a sequence whose acceptance conditions can be verified. If a relevant input changes (revision, artifact, policy, scope, evidence coverage, or a material assumption), reopen affected decisions and dependent assertions; do not reuse stale approval. Preserve independent completed work and actual failures.

## 5. Record the handoff

Use [decision record](../templates/decision-record.md) and, for complex work, [dependency review](../templates/decision-dependency-review.csv). The latter records one reviewed prerequisite relationship per row; independent nodes remain in the decision record. Keep actual evidence privately with original identifiers. No schema conversion, runtime enforcement or automatic approval. Finalize explicit decisions, dependencies, held work, independent safe work, owner, rollback and verification stages. See [worked synthetic examples](../examples/cross-module-review/README.md). Choose the [technical handoffs](../docs/03-technical/technical-handoffs.md) for the exact technical assertion contracts.

This is an internal reasoning method. It does not establish source truth or guarantee a search/business outcome.
