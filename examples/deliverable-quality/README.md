# Deliverable examples (fictional)

These examples demonstrate proportional reporting under the [deliverable quality method](../../docs/01-foundations/deliverable-quality.md), not actual findings, software results, deployed changes or independently evaluated outputs. All evidence statements below describe hypothetical supplied inputs, not collected data.

## A — Direct explanation

Question: What is a canonical URL?

Appropriate response: A canonical URL identifies the preferred representative of substantially duplicate or equivalent pages. It is a search-engine signal, not a guaranteed indexing instruction or an HTTP redirect. If you are troubleshooting a particular page, compare its declared canonical and the available processed search evidence before changing URLs.

No audit, full release checklist, or invented site-specific diagnosis is needed.

## B — Decision brief: limited audit

Hypothetical input: An authorized sample contains a current deployed response for one route showing unexpected homepage content; no other comparable routes or indexed evidence were provided.

Disposition: Investigate a delivery mismatch on the supplied route. The observation supports a mismatch at the deployed HTTP stage, not a site-wide index failure. Inspect the actual host fallback/routing and matched rendering where relevant. Do not redirect or migrate pages yet; no write authorization.

Next check: Reproduce the direct request using approved access and verify expected status and route-specific content. Scope remains one supplied observation; other routes and search processing unknown. Owner: proposed application/hosting maintainer, not an assigned individual.

## C — Implementation and verification handoff

Hypothetical input: An authorized local patch changes a title-generation function. A supplied local test receipt shows the requested unit assertion passed; no browser or production evidence exists.

Disposition: Local implementation performed within scope in this scenario; deployment not performed. Identify exact changed paths and test receipt if supplied; absent identifiers remain unknown rather than inventing a commit or link.

Verification: local title-generation assertion — pass per supplied receipt; rendered title — not-run; deployed response — blocked if production access or authority is required and absent; processed search title — not-run. No claimed traffic gain. Next: authorized matched render check, review appropriate release gate, then separate production and search observation.

## D — Incident update

Hypothetical input: Credible suspected private data transmission during analytics collection; actual affected requests and cause not yet established.

Disposition: Escalate the suspected exposure to the responsible authorized owner immediately. Hold unsafe collection or changes where within scope; do not claim automatic containment. Preserve restricted evidence safely and investigate actual network/consent behavior. Keep unrelated growth work secondary until risk is reviewed. No sensitive payload in the report; closure requires appropriate owner decision and actual verification.

These examples do not prescribe fixed wording. A real output must reflect its actual scope, permissions, evidence, decision and audience.
