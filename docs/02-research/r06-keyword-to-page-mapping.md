# R06 — Keyword-to-page mapping

Status: initial agent-ready methodology; behavioral evaluation pending. Primary-source checkpoint: 2026-11-18.

## WHAT

A map assigns reviewed search tasks to useful website destinations and documents how the site should serve them. A cluster is a research entity, not a URL. A page can serve several compatible clusters, and a broad cluster may require several distinct task-level assignments. An intended primary page is an internal planning choice, not a command to a search engine.

Distinguish:
- Query/cluster: observed language and reviewed relationships (R02–R04).
- Mapping unit: cluster ID + specific task + market/language scope; split a mixed cluster into task units only where evidence supports the distinction.
- Page identity: stable page ID independent of its current URL; record planned pages separately from existing pages.
- Primary intended destination: best currently justified indexable destination for a mapped unit; supporting pages can serve related or distinct tasks. A unit may remain unassigned.
- Canonical URL: preferred representative of duplicate or very similar content. Declared canonical and engine-selected canonical are different observations.
- Actual owner: avoid this ambiguous term; report observed query/page visibility and planned destination separately. Multiple URLs receiving impressions can be normal.

One intended primary destination per resolved mapping unit is an internal coordination convention, NOT a rule that only one page can rank, that every keyword needs a page, or that different useful pages must be canonicalized together. Keep fallback/secondary relationships explicit and do not enforce a primary on unresolved mixed intent.

## WHY

A map turns research into a coherent page strategy and helps teams avoid competing briefs, redundant pages, orphan content and unnecessary URL changes. Logical navigation and useful links connect pages; URL hierarchy alone does not establish site structure. Preserve serving pages where appropriate. Search engines determine which content to show; neither mapping nor canonical hints guarantee selection, ranking or traffic.

## WHEN / WHEN NOT

Use after business scope (R01), discovery (R02), intent (R03), clustering (R04) and relevant competitive review (R05); iterate when new evidence emerges. Use for launches, page briefs, architecture changes, content refreshes and investigation of query overlap. For a narrow metadata fix, do not force a whole-site remap. Do not use keyword mapping to justify fake services, doorway pages, synonym pages, indiscriminate redirects, forced keyword repetition or indexing private surfaces.

## INPUTS

Authorized target and mode; locale/market, offerings, audiences, business goals and evidence constraints; R03/R04 reviewed or provisional tasks/clusters and evidence IDs; R05 opportunities; current route inventory and page purpose; canonical/status/robots/sitemap/render observations where authorized; internal links; available first-party query/page reports and actual outcome data; known dependencies, owner and release constraints. Missing evidence remains unknown. Do not fabricate query volumes or visibility.

## HOW

### 1. Establish an inventory and eligibility

List existing pages and variants from authorized route registry, CMS, sitemaps, navigation/crawl sample, search reports and historical URLs as available. Assign stable page IDs, current URLs, locale, purpose, audience, page type, unique value, business action, expected index policy, observed HTTP status, declared/selected canonical (separate), evidence and owner. Record coverage gaps; absence in a sitemap or limited crawl does not establish nonexistence. Record planned pages with proposed URLs, not observed 200s. Keep utility/authenticated/admin/checkout/thank-you routes in functional scope without making them organic landing pages. Protect private routes with real authorization, not robots.txt.

If an intended public page is inaccessible, miscanonicalized, noindexed or otherwise broken, record repair separately from its potential task fit. Never choose a worse content destination merely because it is currently indexed, or assert that the repaired page will immediately rank. Address material eligibility faults before growth work.

### 2. Define each mapping unit

From reviewed cluster and intent assessment, record ID, primary task, secondary meanings, target language and market, audience and constraints, source query IDs and evidence. Do not merge different product specifications, locales, or opposing intents just to simplify mapping. When evidence is mixed, preserve alternatives and mark unresolved; avoid prematurely enforcing a single URL. Several related variants can share one task-level mapping. One broad cluster may be split by actual task (e.g. learn how to choose a product versus shop available products) without rewriting raw evidence.

### 3. Find and compare existing candidates

Inspect actual pages and relevant templates before proposing new ones. Compare task completeness, content format and functionality, offering fit, locale, unique proof, usability, accessibility, crawl/index eligibility and established URL value. Include links and historic search/traffic evidence when authorized, but do not select solely by volume, current rank, URL text or backlinks. A high-impression page can be a poor intent fit; the appropriate answer may need repair or differentiation.

Use qualitative task fit (adequate/partial/mismatch/unknown), eligibility (eligible by checked signals/repair-needed/not intended/unknown), evidence confidence, cost and risk as separate dimensions. Do not combine them into a fabricated SEO score. Compare no-change, improve and candidate new-page options; record why alternatives were rejected. A greenfield site with no history can have a provisional plan supported by real task research, not actual ranking claims.

### 4. Distinguish strategic decision from URL treatment

| Condition | Strategy | URL/index treatment (proposal only) |
|---|---|---|
| Adequate page fits task | Keep; attach compatible cluster units | Preserve stable URL and intended canonical |
| Useful but incomplete page fits task | Improve page; add missing useful sections/function | Preserve URL; repair eligibility separately if needed |
| Existing page satisfies distinct related task | Retain as supporting/distinct page | Preserve distinct indexable URL, not cross-canonical |
| Missing genuinely distinct useful task | Propose new page/tool; verify offering, proof, maintenance and links | Reserve noncolliding URL; planned, not observed |
| Mixed intent / uncertain scope | Defer or investigate; provisional candidates | No destructive URL changes |
| No legitimate offering or user value | Exclude/out of scope | No fabricated organic landing page |
| Actual duplicate/near-duplicate kept accessible | Review representative URL | Appropriate canonical preference, consistent links/sitemap; not a removal guarantee |
| Actual duplicate retired or content moved permanently | Consolidate only with true replacement, approval and preserved value | Relevant permanent redirect; update links, sitemap, metadata; test |
| Content must be removed without real replacement | Retire under approved policy | Genuine 404/410 where appropriate, not generic home redirect |
| Functional but intentionally nonindexable page | Keep functional | Appropriate noindex/security policy; not a keyword owner |

A canonical annotation concerns content equivalence, not keyword competition. Distinct useful pages should not be cross-canonicalized merely because they share keywords. Use a self-referential canonical on intended representative pages where appropriate; align preferred URL, redirects, links and sitemap. Robots.txt and removal tools are not canonicalization methods. A canonical is a preference; Google can choose another URL. Noindex has a different purpose and must be observable by crawlers where applicable. Protect confidential pages via authorization. For localized equivalent content, review hreflang and same-language canonical choices using international guidance; do not send all translations to one language's canonical.

### 5. Diagnose overlapping visibility before changing pages

For authorized Search Console evidence, examine query and page dimensions together with dates, country, device and search type; record export/aggregation method. Compare stable periods and relevant query variants/clusters. Search Console may attribute data to canonical URLs, omit queries and truncate results; page versus property totals may differ. Inspect actual content and index/canonical state separately. Average position is not a fixed daily rank.

Potential explanations include valid mixed intent, genuinely different pages, duplicate URLs, wrong locale, temporary search changes, uneven links, template delivery errors or redundant content. Evaluate user task/outcome and historical trend, not impressions alone. Do not call overlap a penalty or prove that pages compete destructively without evidence.

If distinct content serves useful tasks, keep both and improve differentiation/internal links. If essentially duplicate pages persist, review canonical or consolidation options with page equivalence and migration risk. Keep a redirect proposal separate; no deployment from a mapping worksheet. For a consolidation choose true replacement, retain unique useful content, plan old links, traffic, backlinks, conversion behavior, rollback and monitoring. If scope is missing, leave the decision pending.

### 6. Design page-specific requirements

For each kept/improved/proposed page, document its audience and main user task, supporting units, what users should learn/do, unique contribution and necessary proof, appropriate format, CTA/next step, actual constraints and claims needing review. Define title/topic and heading concept naturally, not keyword density or exact-match repetition. Choose stable descriptive URL only when new or when a justified migration is approved; preserve established URLs by default. Specify expected HTTP/index/canonical policy, source/render expectations, relevant schema if eligible, discoverable internal links from/to real related pages, accessibility/performance checks, event/outcome metric and owner. R07 develops broader topic/link architecture; R08 prioritizes proposals. Do not draft dozens of new pages when useful existing pages can meet tasks.

### 7. Record and hand off

Store page registry, task assignments and page briefs separately from original keyword observations and search data. Keep proposed, approved, implemented and verified states distinct. For resolved mapped units, record a single intended primary destination plus optional supporting relations; no forced assignment for mixed/unreviewed units, nonpublic pages or out-of-scope tasks. Record evidence IDs and competing alternatives. Page briefs and URL-change proposals are not permission to publish. Handoff to content/engineering and authorized release workflow after review.

## VERIFY

- Page IDs and current/proposed URLs unique where intended; mapped page IDs resolve in registry; scope and actual locale consistent.
- Every resolved selected unit has one intended primary page, independently useful and planned indexable; supporting relations explicit; unmapped units retain reason and evidence gap.
- Several units can map to one page if task fit and constraints compatible; no automatic synonym pages or one page per keyword.
- Existing usable URLs preserved unless migration separately justified/approved; current and desired states distinct.
- Canonical/redirect plans based on real equivalence or replacement, not overlapping terms; no conflicting destination/chain/loop or generic home fallback.
- New pages require evidence of independent usefulness, supported offering, content/technical requirements, links, maintenance owner, test plan and review.
- Verify actual HTTP, HTML source and rendered DOM, link resolution, intended index policy, sitemap, locale alternates and conversions after approved changes. Search-selected canonical/index and measured outcomes checked separately where tools allow.
- Use synthetic examples and E19–E22 cases for judgment; deterministic reference checks are not live or agent competence tests.

## MEASURE

Before changes, baseline aligned query/page cohorts, relevant impressions, clicks, CTR (with denominators), intended destination visibility, verified business outcomes and technical state. Evaluate after appropriate recrawl/reporting latency; no universal review duration. For approved consolidations compare old and new URL cohorts, not only new URL metrics, and monitor redirects and actual indexed state. Investigate legitimate alternate destinations separately from mismatches. Traffic changes can reflect demand, query mix, ranking, SERP features or tracking rather than mapping itself. Keep no-change as success when it avoids risk. Track mapping review coverage, unresolved units, stale evidence and regressions as operational metrics, not ranking scores.

## ADAPT

Ecommerce: category vs product vs buying guide; preserve variant functions and evaluate facets/pagination independently. SaaS/B2B: audience/problem/use-case versus support/integration task; only create independently useful pages for real capabilities. Local: service and location evidence; no thin city permutations. Publishers: distinguish evergreen reference, timely update and distinct tools; maintain editorial review. Persian/multilingual: native task research per locale, raw spelling preserved; do not rename stable URLs simply for translated keywords. Greenfield: planned registry, no pretended historical search metrics. Large sites: template rules and sampled validation with exceptions, not automatic mass page generation. Health/finance: expertise, safety and supported claims are release gates; no unvalidated calculator or diagnostic promises.

## RECOVER

Record competing/missing evidence and defer structural changes. If mapping changes, version relationships without erasing raw observations. For incorrect assignment, revise briefs and link proposals; do not change URL automatically. For approved migration regressions, follow migration rollback, inspect status, redirect targets, content parity and canonical/index state; preserve unrelated work. Withdraw inaccurate claims and stop unauthorized writes or collection. Escalate data/privacy or security issues. Document blockers rather than fabricating verification.

## OUTPUTS

[Page registry](../../templates/page-registry.csv), [task-to-page assignments](../../templates/task-page-mapping.csv), [page requirements brief](../../templates/page-seo-brief.md), [decision protocol](../../decision-engine/page-mapping.md), [synthetic worked example](../../examples/page-mapping/README.md). Existing keyword-map and URL-inventory templates remain available; new registry and assignments provide stable linked IDs and lifecycle. Use [redirect map](../../templates/redirect-map.csv) separately only when justified.

## SOURCES — checked 2026-11-18

- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide): logical organization, descriptive URLs and duplicate content.
- [Canonical selection](https://developers.google.com/search/docs/crawling-indexing/canonicalization) and [canonical methods](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls): representative URL for equivalent content and aligned preferences.
- [Redirects](https://developers.google.com/search/docs/crawling-indexing/301-redirects) and [site moves](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes): real replacement and migration validation.
- [Search Console performance](https://support.google.com/webmasters/answer/7576553) and [dimensions/grouping](https://support.google.com/webmasters/answer/17011259): query/page analysis and aggregation limitations.
- [Crawlable links](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) and [ecommerce structure](https://developers.google.com/search/docs/specialty/ecommerce/help-google-understand-your-ecommerce-site-structure): links and navigation.
- [Localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions): meaningful locale alternatives.
- [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies): doorway abuse and keyword stuffing.

Mapping units, candidate-fit classes, single intended destination and data schemas are internal engineering conventions. No actual site has been audited or changed in this module.
