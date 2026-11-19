# P01 — React/Vite-associated workspace marketing scenario

Offline synthetic practice only. Workspace is an invented task-planning product; the reserved example host is never contacted. React/Vite version hints are fictional inputs, not installed dependencies or framework-specific verification. The target consists of **hand-authored HTML**, not actual framework builds. All HTTP/browser/search observations are made-up inputs except where explicitly unavailable. Neither revision is a real deployment. No customer data, authentication secrets, actual authorization test or release approval.

## Brief and identity

Goal: keep four useful public URLs discoverable and distinct while protecting the application and returning a genuine missing-page status. Mode: offline audit/plan plus local fixture comparison only. No migrations, external requests, tracking changes, production or app-data access. See [registry](registry.json). Each native row's id is the registry route id in this specific lab; T02/T05 do not carry actual URL identity, so use this reviewed crosswalk rather than infer same-named IDs elsewhere.

| ID | Route | Intention |
|---|---|---|
| home | / | Public landing |
| features | /features/ | Product exploration |
| guide | /guides/getting-started/ | Educational intent |
| pricing | /pricing/ | Commercial comparison |
| dashboard | /app/dashboard/ | Protected, no acquisition |
| missing | /missing-page/ | HTTP 404, no acquisition |

P01-A has a missing guide file, a pricing canonical incorrectly pointing home, and simulated guide source fallback followed by route content after rendering. The simulated missing path returns HTTP 200. P01-B has a new guide file, corrected pricing canonical and a local error document; the supplied public observations are revised hypothetical observations, not proof of real delivery. No new missing-path HTTP observation exists. Features browser capture absent in both; dashboard authorization unknown in both. Both revisions include the same stale mock search inspection for guide. The timeline is fictional October 2026. The static manifest covers only the four public artifact paths; not the protected/missing routes. T01/T03/T05 cover six rows; T02/T06 cover four public rows. Missing external data is not a negative outcome.

## Run from the library root

Use a new output directory outside the source checkout; set LAB to examples/practice-projects/p01-react-vite and OUT to that existing fresh directory. The code below is POSIX shell; on other systems run equivalent commands. Only trusted local inputs; no network.

~~~sh
LAB=examples/practice-projects/p01-react-vite
# OUT must already name a new private output directory.
python3 scripts/audit_html.py --manifest "$LAB/static-routes.json" --root "$LAB/p01-a/artifacts"
python3 scripts/audit_html.py --manifest "$LAB/static-routes.json" --root "$LAB/p01-b/artifacts"
python3 scripts/audit_technical.py --input "$LAB/p01-a/technical.json" --artifact-root "$LAB/p01-a/artifacts" --output "$OUT/p01-a-technical.json"
python3 scripts/audit_technical.py --input "$LAB/p01-b/technical.json" --artifact-root "$LAB/p01-b/artifacts" --output "$OUT/p01-b-technical.json"
python3 scripts/review_release_gates.py --input "$LAB/p01-a/gates.json" --output "$OUT/p01-a-gates.json"
python3 scripts/review_release_gates.py --input "$LAB/p01-b/gates.json" --output "$OUT/p01-b-gates.json"
~~~

Initial HTML command expected exit 1 (missing guide and pricing canonical mismatch); revised expected exit 0 (four declared public documents checked). Run commands separately or handle the intentional nonzero exit. T10 both expected exit 0: five processed, two blocked (T08/T09 dedicated inputs unavailable), two not applicable (T04/T07), no grouping requested. Native review findings are not processing failures. Both T11 commands expected exit 0 but disposition hold. T11 A missing-http assertion fails from a **synthetic** observation, B it is stale; required private access, browser and local evidence fields missing. Local smoke pass has not been inserted into the saved gate template. During the lab bind actual observed local smoke result to the exact local-html assertion/subject/policy only, recording its real reference; other gates stay held. That local assertion is not authorization to deploy.

## Expected narrow review

| Assertion | A fixture | B fixture |
|---|---|---|
| T03 guide required document | Missing | Present |
| T02 guide mock source/render | Client completion, canonical change | No compared-field review findings |
| T05 pricing mock sitemap canonical preference | Review | No review finding in supplied row |
| T06 guide mock processed crawl | Predates change | Predates change |
| T01 missing path | Status review | Status unknown |
| T02 features | Paired comparison deferred | Paired comparison deferred |
| T01 dashboard | Authorization unverified | Authorization unverified |

These are expected diagnostic results, not independent runtime or agent receipts. Maintainer tests execute the CLI on the actual handwritten files and supplied records. Never infer host, real rendering, search or security success.

## Decisions and handoff

D1: restore the missing guide document at its existing path; D2: correct pricing canonical to its own distinct useful page. No redirect, URL migration or framework rewrite justified by the supplied evidence. D3: plan an explicit missing-route host status rule; the 404 HTML alone cannot verify status. D4: verify access control and data/API behavior separately before any release decision. D5: recheck matched browser output and updated search observations independently; no claim of indexing, ranking or business growth. D3/D4/D5 are held for missing external evidence. Proposed owners: application/hosting maintainer for D1–D3 and browser QA, authorized security owner for D4, search owner for D5; not assigned real people. Revert the changed local artifacts/plan if an approved local assertion fails, preserving unrelated working routes. A revised mock is not an actual implementation or rollback in production.

Reuse [T10 coordinator](../../technical-audit/README.md), [T11 example](../../deployment-regression/README.md), [cross-module review](../../../decision-engine/cross-module-review.md) and [delivery summary](../../../templates/delivery-summary.md). Native IDs are intentionally aligned for this exercise only; no conversion or universal provider schema.
