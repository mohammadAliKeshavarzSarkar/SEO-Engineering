# Search intent to page decision protocol

Use after R03. This produces a scoped proposal, not authorization to write, publish or redirect.

| Evidence / condition | Recommended next decision |
|---|---|
| Query is unrelated to offerings or cannot be responsibly satisfied | Out of scope; document why; investigate better-matched intent |
| Evidence is incomplete, generic, mismatched by market, or conflicting | Investigate; preserve provisional labels; do not make destructive changes |
| Existing useful page already fulfills task | Retain; improve only for evidence-backed gaps |
| Existing page matches task but fails completeness, accessibility, trust or practical next step | Improve existing page first, preserve stable URL |
| No existing page fulfills a genuinely distinct, valuable task, with actual expertise and offering fit | Propose new useful page with proof, maintenance owner and links |
| Multiple tasks can be answered coherently by a single page | Consider existing page with clear sections and descriptive links |
| Distinct tasks require different content or functionality | Consider separate pages when each independently serves a real need |
| Several pages repeat the same task or have overlapping query visibility | Investigate content equivalence, query/page trends, useful unique value and backlinks in R04/R06; propose consolidation only if evidence supports a true replacement |

Before recommending a new page, record: user task, evidence IDs and confidence, actual audience/offering fit, existing alternatives, proposed independent useful contribution, page format, why no-change is insufficient, risks and verification. A high-volume keyword without these is not a page requirement. Do not generate city/variant/near-identical pages solely for discovery. Do not canonicalize or redirect different useful pages solely due to overlapping queries.

Acceptance: [intent assessments template](../templates/intent-assessments.csv) records decision, owner, evidence and limitations; proceed to clustering and architecture work, not directly to publication. If consolidation or URL change is approved later, follow [URL migration guide](../docs/03-technical/urls-and-migrations.md) for mapping, redirects and rollback; review crawl/index and search performance separately. For missing context keep existing useful pages unchanged pending evidence.

Related: [R03](../docs/02-research/r03-search-intent-and-serp.md), [decision framework](README.md).
