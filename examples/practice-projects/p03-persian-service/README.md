# P03 — Persian-language bicycle repair service

Offline educational exercise. CycleCare is fictional, all hosts reserved .example domains; no network activity, real business, service promise, localized SERP, advertising access, customer or CRM data. Scope: research, mapping and local artifact audit; no publication, redirects, real tracking or release. The two fixture revisions are handwritten HTML and invented manifests, not deployed pages. See [registry](registry.json) for exact URL-to-local-file mapping.

## Query evidence and decisions

[Queries](queries.json) supply seven invented search observations. Q1/Q2 preserve Arabic/Persian yeh variants; Q3/Q4 preserve ZWNJ versus space. R04 match keys fold these for comparison, not display or URL generation. Q6 has different device, Q5 incomplete/unknown intent. Q7 has the same synthetic result URLs as service variants, but the business has not substantiated 24-hour service. Its high overlap cannot establish business fit or factual claim. Candidate groups stay provisional; do not auto-publish or create pages. This is not actual demand or a representative Iranian SERP.

R06 [mapping](mapping.json) assigns service task U1 to the existing distinct Persian service page and educational U2 to its guide. Keep U3 (pricing uncertainty) and U4 (different device) unresolved; exclude U5 (unsupported hours). The English service page is a real equivalent **within the fictional brief only**. No new English home/guide is justified just to make symmetric groups. R10 [handoff](handoff.json) preserves evidence references, zero in a bounded invented sample versus null unknown market demand. A structurally valid envelope does not verify a reviewer, source truth or authorization.

## Locale, canonical and link changes

P03-A: guide canonical incorrectly points to service; guide root direction ltr; graph has only interaction-only path to guide from public entry and a private source link. English service alternate set omits reciprocal fa and x-default. P03-B: guide gets its own canonical, lang=fa and dir=rtl, public crawlable link from service, and service pair has reciprocal fa/en with x-default pointing to existing Persian service URL. The strict R09 manifest checker reports alternate-set discrepancies on both service URLs even in B because same-URL x-default is not a separate registry representative in its strict model. This is a reviewed profile exception in the fictional context, not automatic proof of a platform violation or live validation. Do not add a thin x-default page, remove useful language alternates, or migrate the Persian URLs to silence the checker. The A English reciprocity omission is a distinct defect. Real applicability and actual served declarations require review.

Raw Persian URL strings remain stable, separate from local ASCII filenames. Browser encoding, bidi, language quality, actual focus/keyboard/assistive technology behavior and route resolution are not verified by the local parser; inspect in an authorized runtime later. The local HTML test checks only its documented explicit-head policy. The regression test also checks the exact root attributes and alternate literals with a small fixture parser, not accessibility conformance.

## Run from the library root

Set OUT to a fresh existing output directory outside the source checkout. Run independently; exit 1 for intentional findings, not an execution failure.

~~~sh
LAB=examples/practice-projects/p03-persian-service
python3 scripts/cluster_keywords.py --input "$LAB/queries.json" --output "$OUT/p03-clusters.json"
python3 scripts/validate_research.py --input "$LAB/handoff.json" --output "$OUT/p03-handoff.json"
python3 scripts/audit_topic_graph.py --input "$LAB/p03-a/graph.json" --output "$OUT/p03-a-graph.json"
python3 scripts/audit_topic_graph.py --input "$LAB/p03-b/graph.json" --output "$OUT/p03-b-graph.json"
python3 scripts/audit_locale_manifest.py --input "$LAB/p03-a/locale.json" --output "$OUT/p03-a-locale.json"
python3 scripts/audit_locale_manifest.py --input "$LAB/p03-b/locale.json" --output "$OUT/p03-b-locale.json"
python3 scripts/audit_html.py --manifest "$LAB/static-routes.json" --root "$LAB/p03-a/artifacts"
python3 scripts/audit_html.py --manifest "$LAB/static-routes.json" --root "$LAB/p03-b/artifacts"
~~~

| Check | Expected narrow result |
|---|---|
| R04 | Q1/Q2 candidate, Q3/Q4 candidate; Q1/Q6 deferred by scope; Q1/Q7 candidate but U5 excluded by reviewed business fit |
| R10 | 5 evidence records, 5 decisions, provisional U3/U4 |
| R07 | Guide unreachable in A; depth 2 in B; private/planned excluded |
| R09 | A: 3 findings; B: 2 alternate-set findings, retained for profile review; both exit 1 |
| Local HTML | A: 1 canonical mismatch; B: 0 findings across 4 public documents |
| Root RTL and alternates | Exact authored attribute/literal changes only |

These are expected tool results, not actual search, browser or authorization receipts. Review all diagnostics, including the remaining strict-profile exception. No T10 composite, live index inspection or release gate execution in this research-focused exercise.

## Editorial and measurement handoff

[Business review](business-review.json) keeps the 24-hour claim deferred; request evidence before use. Do not turn query wording into an availability claim. Fictional equal-window search clicks 200 to 200, recorded sessions 150 to 150, lead events 10 to 15, accepted leads 10 to 10. Event increase is not verified acquisition or business growth; cause unknown. Consent and provider receipt unverified. Do not introduce tracking or submit test leads. Independently review actual collection, retry-safe backend acceptance and comparability only if authorized.

Decision: preserve useful service and guide URLs, improve link and local language semantics, hold new pricing page and unsupported claim. Proposed owners: native editorial reviewer, web maintainer, analytics/privacy owner. Rollback: revert scoped local artifact/link changes if actual acceptance fails, preserve distinct useful content. Before release require actual HTTP and rendered locale checks, native review, browser keyboard/bidi/encoding checks, access-control and consent review where applicable, separate search/outcome verification and appropriate authority. No actual release, real ranking or business impact established.

See [R09](../../../docs/02-research/r09-multilingual-search-engineering.md), [cross-module review](../../../decision-engine/cross-module-review.md), [measurement](../../../docs/05-measurement/analytics.md). Use the existing native schemas; no automatic locale or intent mapping.
