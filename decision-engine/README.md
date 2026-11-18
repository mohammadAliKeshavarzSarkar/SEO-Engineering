# Evidence-based decision engine (procedure, not executable inference)

1. Confirm the issue and affected URLs using the least intrusive evidence available. If scope or expected behavior is unclear, label provisional.
2. Classify: eligibility requirement, official recommendation, internal project policy, or experiment. Distinguish search eligibility from ranking and UX.
3. Check critical hazards first: privacy/security, widespread broken access, incorrect index policy, destructive URL changes, broken conversions. Stop unsafe release; do not postpone critical remediation for growth research.
4. Identify constraints: site type, locale, stack, scale, hosting, valid current behavior, dependencies, authority, available proof, time/cost and reversibility.
5. Compare at least the current behavior/no change and a plausible alternative; list reasons to reject other options when material. Choose the smallest action that addresses the evidenced problem. Use qualitative priority + confidence; if scoring, define the internal rubric, never imply a probability of ranking.
6. Write a decision record with specific observable assertions, sampling scope, rollback and owner. If evidence is inadequate, choose a bounded discovery step rather than conflicting speculative fixes.
7. If authorized, implement and verify; separate release safety from search performance, preserve remaining uncertainty. Revisit on new evidence.

Specialized protocols: [rendering decisions](rendering.md), [search intent to page decisions](search-intent.md), [keyword clustering](keyword-clustering.md) [competitor intelligence](competitor-intelligence.md) and [page mapping](page-mapping.md). For all other domains apply this shared procedure plus appropriate knowledge and current source guidance. New specialized protocols should follow the [module standard](../docs/01-foundations/module-standard.md). Output via [decision record](../templates/decision-record.md).

This is a reasoning method; it does not autonomously execute actions or replace human approval for consequential changes.
