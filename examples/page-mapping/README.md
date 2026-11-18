# R06 synthetic worked example

All URLs and research units are fictional; no real search observations, rankings or traffic are asserted. See [fixture](sample.json). The fictional office-furniture shop already has a chair category and selection guide. A duplicate category alias is genuinely equivalent; a private checkout remains private.

| Unit | Intended primary | Action |
|---|---|---|
| U1: browse chairs | P1 /chairs/ | Keep |
| U2: compare stocked chair options within category | P1 /chairs/ | Improve existing filters/details if verified gap |
| U3: learn how to choose a chair | P2 /guides/choose-chair/ | Keep; link to suitable category |
| U4: configure an independently useful sizing tool (validated need, assumed feasible) | P3 /tools/chair-fit/ | Propose new, not published |
| U5: broad mixed phrase, insufficient task evidence | Unassigned | Investigate; retain P1/P2 candidates |
| U6: repair service not offered | Unassigned | Exclude |

P1 and P2 may both receive impressions for a broad phrase; keep if they serve distinct tasks. P2 may also support U1 without becoming the primary shopping destination. P4 /office-chairs/ is assumed a verified duplicate; review canonical if it must stay available, or permanent redirect to P1 if approved for retirement. This is separate URL treatment, not an intent-mapping mandate. P5 /checkout/ is functional/private, not a primary organic destination. These are hypothetical decisions pending actual project evidence.

Fixture assertions: each resolved unit has exactly one existing/planned primary page ID; P1 serves more than one unit; U5 and U6 have none; P3 planned, not live; P5 not primary. The two distinct task pages are not canonicalized together. A real project must confirm evidence and authority before implementation.

See [R06](../../docs/02-research/r06-keyword-to-page-mapping.md) and [decision protocol](../../decision-engine/page-mapping.md).
