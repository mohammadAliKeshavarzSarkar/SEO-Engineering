# R05 synthetic worked exercise

All entities, domains, query IDs, results and counts are fictional. No actual ranking, traffic or revenue claims.

Use [fixture](sample.json). One snapshot per query; include only complete snapshots in synthetic-CA-en-mobile-web. Count domain once per included query. Exclude partial q5 from all denominators.

| Comparator | Coverage | Interpretation |
|---|---|---|
| publisher.example | 4/4 (100%) | Search/content benchmark |
| marketplace.example | 3/4 (75%) | Ecosystem/search benchmark |
| vendor.example | 2/4 (50%) | Potential business and search rival |
| direct.example | 0/4 in sample | Named commercial comparator; retain |

Repeated marketplace result in q1 does not inflate count. These values are not market share, search volume or traffic.

Fictional inventory-monitoring SaaS: publication has a useful installation tutorial; target supports installation but its documentation lacks troubleshooting. Propose original, verified troubleshooting steps on existing documentation if need is evidenced. Competitor advertises an unsupported integration: reject speculative target page. Public request returns 403: coverage unknown, no bypass. Existing useful commercial page: retain if adequate.

Vendor A 80,000 estimated USA monthly visits versus vendor B 50,000 worldwide estimates are noncomparable without alignment. Mobile origin-level field LCP and a desktop URL lab result are also noncomparable. Preserve separate scopes, not a league table.

See [methodology](../../docs/02-research/r05-competitor-intelligence.md) and [decision protocol](../../decision-engine/competitor-intelligence.md). Behavioral evaluations must run separately.
