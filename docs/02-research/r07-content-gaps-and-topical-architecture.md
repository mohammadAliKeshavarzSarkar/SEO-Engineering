# R07 — Content gaps and topical architecture

Status: initial agent-ready methodology and offline graph utility; behavioral evaluations pending. Source checkpoint: 2026-11-18.

## WHAT

Topical architecture is the deliberate organization of useful pages and their relationships around audience tasks. A topic is a subject domain, a task is what a person wants to accomplish, a page is a destination and a link is a navigable relationship. A hub (sometimes called a pillar) provides an independently useful overview or navigation for a broad task. Supporting pages provide distinct detail, tools, products, comparisons or documentation. A topic cluster is a planning convention, not a required search-engine structure or a ranking score.

Content gap analysis asks whether an audience task is not adequately served. It includes missing information, functionality, evidence, findability, or appropriate content formats. A missing competitor keyword alone is not a gap. A content graph records page identities as nodes and directed navigable links as edges; topic relationships and proposed links are stored separately from observed links.

## WHY

Logical architecture helps people locate, understand and use content. Google describes links as discovery and relevance signals and recommends contextual internal links to useful pages. Its ecommerce guidance discusses link relationships, not URL folder names alone, as evidence of site structure and relative importance. Original usefulness, trustworthy evidence and audience fit matter; publishing more pages, arranging all pages into silos or achieving a vendor topical-authority score does not guarantee rankings.

## WHEN / WHEN NOT

Use after R01–R06 for site launches, navigation design, content audits, resource hubs, documentation, product/category hierarchies, internal linking improvements and reviewed lifecycle changes. Iterate when map evidence changes. Skip broad restructuring for unrelated narrow defects. Do not fabricate missing topics, force a pillar for every theme, manufacture exact-match links, change dates without meaningful revisions, delete useful low-traffic pages for freshness, or publish at scale primarily to manipulate rankings.

## INPUTS

Authorized scope and mode; audience tasks and business constraints; reviewed R03/R04 task clusters, R05 opportunities and R06 page registry/mappings/briefs; editorial inventory, actual page content and ownership; source/rendered link observations, menu/breadcrumb/context links, sitemap and authorized public crawl or exports; current approved claims, first-party search and outcome data when available; language/locale, accessibility, review and maintenance requirements. Specify snapshots, entry points, collection coverage, limitations, evidence and privacy boundaries. A missing observation is unknown, not a proven defect.

## HOW

### 1. Build a task coverage matrix

Define subject boundaries from real offering, purpose, expertise and audience. List useful task units (learn, compare, do, transact, navigate, local) plus meaningful prerequisites, decision criteria, support and post-purchase needs. Do not add topics merely because competitors rank for them or an embedding model regards them as related.

Map each task to existing independently useful destinations, based on R06. Inspect actual content rather than titles alone. Record adequate, partial, absent-in-verified-scope, not assessed, blocked, out-of-scope and uncertain. When inventory is incomplete, say 'not found in observed sample', not 'missing from website'. Record unique value and required evidence (product proof, source, reviewer, original examples, accurate tools). Keep useful low-search-volume support and conversion content where justified.

### 2. Choose the smallest suitable action

| Observed situation | Proposal |
|---|---|
| Adequate existing page | Keep and maintain; no unnecessary rewrite |
| Incomplete answer or outdated facts | Improve/refresh existing content and verify claims |
| Good answer difficult to discover | Improve navigation and contextual links; diagnose eligibility separately |
| New independent task with evidence, offering fit and feasible proof | Propose new page, resource or tool with owner and links |
| Near-duplicate answers to same task | Review differentiation or approved consolidation under R06; preserve unique value |
| Distinct useful tasks share wording | Keep separate; link appropriately |
| Obsolete offering/content | Review historical value, safety and replacement; controlled retirement only if justified |
| Unsupported claim, topic or service | Reject or defer until genuine evidence/capability exists |
| Unknown data or incomplete crawl | Investigate; preserve useful pages meanwhile |

No universal word count, cluster size, publishing cadence, link count or required number of supporting pages. Depth means sufficient information/functionality for the task, not article length. Content format follows user needs. Use real expertise and appropriate expert review, especially for sensitive topics. Do not create pages just to cover every keyword or every entity-related phrase.

### 3. Organize the user journeys

Choose hubs where users genuinely benefit from overview, categories or navigation. Alternatives include flat useful navigation for small sites, product taxonomies, multi-axis documentation, chronological archives, topic collections and localized variants. Avoid strict SEO silos that prohibit useful cross-topic navigation. The hub itself needs a real function; not a thin list created for ranking. An independent detailed page should not duplicate its parent.

For each important subject, document core task, destination, supporting tasks, prerequisites, next steps, related topics and maintenance owner. Assign links from relevant established entry points and contextual pages. Use explicit directed edges: from page ID, to page ID, relationship (prerequisite, detail, comparison, evidence, product, support, parent/child, next step), placement (navigation/breadcrumb/body/footer), descriptive anchor intent, existence/plan status, observed markup and evidence. Relationship need not be reciprocal. Keep editorial topic relationships (semantic relevance) separate from actual link edges. Review links across topics where they help users; no artificial all-to-all graph.

For ecommerce, provide discoverable category/subcategory/product links and crawlable pagination where needed; don't rely only on onsite search or interaction-generated results for important pages. For multilingual sites, preserve useful locale links and review canonical/hreflang separately. Functional private or intentionally nonindexed pages are not organic acquisition targets. Never expose confidential surfaces for graph completeness.

### 4. Audit the observed link graph

For an authorized snapshot use stable page IDs and entry points (e.g. homepage and explicitly justified other public entries). Distinguish existing public, private and proposed nodes. Record intended indexability separately from observed status/index state. Collect actual links from source and rendered DOM with context; links inserted by JS can be valid when they resolve to real anchor hrefs. Classify crawlable/interaction-only/proposed/unknown; 'crawlable' input is an observed link-form classification, not proof that a target can be fetched or indexed. Verify HTTP responses, robots, access, canonical and redirect behavior separately; do not infer indexed state from graph metrics.

Use directed graph traversal (breadth-first search) to compute shortest observed crawlable-link distance from selected entry points. Count unique inbound source pages rather than multiple same-page links. Flag:
- Priority intended public pages unreachable in supplied graph (depth unknown).
- Intended indexable pages with no observed crawlable inbound link, excluding declared entry points. These are orphan candidates, not proven full-site orphans.
- Disconnected groups may have inbound links from one another while remaining unreachable from entries.
- Existing public link pointing at a registry-planned page warrants review, not automatic proof of a 404.

A sitemap-discovered URL can be known yet have no observed internal path. Distinguish actual entry assumptions, full and partial collection, source/render mismatches and stale inventory. Extend capture if necessary; never count planned links as observed, nor allow private-only or interaction-only navigation to satisfy public graph reachability. No universal three-click rule; choose project-specific reachability objectives appropriate to navigation and user experience. Link depth is not a ranking score. A link count does not measure PageRank, authority or search demand.

The [offline graph utility](../../scripts/audit_topic_graph.py) consumes a prepared JSON graph, does no network requests, and reports these structural diagnostics. It includes existing public nodes regardless of intended indexability as potential paths; actual fetchability/access/redirect and nofollow or robots effects must be checked separately. It ignores self-links and deduplicates edges; it does not compute PageRank, infer semantics, detect every cycle, or decide which page to link. Partial or inaccurate inputs create partial or inaccurate findings.

### 5. Propose context-aware internal links

Use standard anchor elements with resolvable hrefs for navigable page links. Make visible anchor text descriptive, natural, accessible and relevant; avoid repeated forced exact matches, bundles of links with no context or hidden links. Avoid unnecessary redirect intermediates and noncanonical targets where a preferred stable destination is appropriate; respect planned URL migrations and genuine alternate locales. Ensure readers can reach important destinations from relevant pages; links should serve an understandable next task. Measure useful navigation, not arbitrary link density. Do not add all pages to the global footer simply to reduce depth.

Record edge proposals separately, confirm destination exists or is approved and schedule dependencies so users do not encounter broken paths. Check rendered navigation, keyboard focus, mobile parity, visible anchors, status, index policy and actual route availability. Use templates for large sites, review representative pages and exceptions.

### 6. Manage the editorial lifecycle

Assign content owner, sources/reviewer, version, meaningful update date and review trigger. Maintain evergreen content, fix verified factual changes, retain useful archival content where appropriate, and keep commercial claims consistent with current offering. Decide keep, update, expand, differentiate, consolidate, retire, or defer with evidence of actual purpose and risk. Low traffic, age or a competitor's page count is not alone a reason to delete. Consolidate or retire only through approved R06 migration treatment: preserve unique content and real replacements, check historical search/referrals and functionality, update affected links/sitemap, plan rollback. Do not fake freshness; evaluate quality at pace the team can maintain.

Use R08 to prioritize a backlog of reviewable tasks with dependencies, impact, evidence, effort and risk. Do not interpret a coverage matrix as authorization to publish or change URLs. Each proposed new page needs a page brief, actual user value, evidence, owner, useful incoming/outgoing links and a verification plan.

## VERIFY

- All tasks trace to R01–R06 evidence; observed, provisional and unsupported tasks separated.
- Existing adequate pages preserved, missing content not inferred solely from keyword gaps or incomplete inventory.
- Every proposed hub/new page has independent usefulness, actual offering fit, evidence, approval and maintenance plan; no scale abuse or artificial topical-authority claim.
- Graph contains unique registry IDs, known entry points, resolvable node references and observed versus proposed edges distinct. Privacy/authority respected.
- Check orphan candidates/unreachable priority pages against actual sampled URL inventory, source/render links, direct GET, canonical, index policy and sitemap; use offline diagnostic only as evidence about supplied graph.
- Verify proposed links after implementation for markup, accessible anchors, meaningful next step, target reachability, mobile/keyboard behavior and HTTP status. Confirm no broken link regression or unauthorized exposure.
- Run utility tests and synthetic fixture; evaluate E23–E26 independently with model inputs and reviewer. These checks do not prove live crawling, indexing, rankings or agent competence.

## MEASURE

Track task coverage by reviewed units (adequate / partially served / unresolved, with defined denominator), content review status, observed public-link reachability, priority depths, candidate orphan count, verified correct destinations and actual user outcomes. Use comparable snapshot scopes before/after graph changes. Report partial coverage and unknowns. Use authorized GSC/Bing query/page cohorts, search traffic and meaningful engagement/conversion outcomes where available, allowing for reporting/recrawl latency and confounders. A decline in link depth or increase in page count is not a ranking result. No arbitrary topical authority score or promised traffic. Reassess lifecycle based on evidence and ownership.

## ADAPT

Small sites: simple navigation may be enough; never invent pillars. Ecommerce: browseable hierarchy, pagination and real attributes; avoid uncontrolled facets. SaaS: solution/use-case/docs/support journeys, authenticated surfaces protected. Publishers: editorial taxonomy, sources, review/archival policy and no artificial dates. Local: real services/locations, no city doorway permutations. Multilingual/Persian: native tasks and useful locale navigation; RTL and translated content quality, not word-for-word topical templates. Health/finance: credible evidence and qualified review; no unsafe calculator or unsupported diagnosis. Large sites: inventory partitioning, sampled technical validation and reviewed template link rules; no uncontrolled generation.

## RECOVER

If coverage assumptions are wrong, reopen inventory and raw evidence, revise topic/page relationship records without rewriting observations. If proposed links fail, revert relevant link changes and assess target status before reattempting. If content consolidation harms users or eligibility, apply approved migration rollback and investigate affected cohort. Correct inaccurate claims promptly and stop unsafe/unauthorized collection or publishing. For incomplete crawl, label findings candidate-only and request bounded authorized additional evidence.

## OUTPUTS

[Topic-task coverage](../../templates/topic-task-coverage.csv), [internal-link plan](../../templates/internal-link-plan.csv), [content lifecycle](../../templates/content-lifecycle.csv), [decision protocol](../../decision-engine/topical-architecture.md), [synthetic graph exercise](../../examples/topical-architecture/README.md), [graph utility](../../scripts/audit_topic_graph.py). Use R06 page briefs and R08 prioritization for approved handoff. Project evidence stays private.

## SOURCES — checked 2026-11-18

- [Google helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content): people-first usefulness, original value, no preferred word count, no artificial freshness.
- [Google crawlable links and anchor text](https://developers.google.com/search/docs/crawling-indexing/links-crawlable): resolvable anchors, contextual links and no magical ideal link count.
- [Google ecommerce site structure](https://developers.google.com/search/docs/specialty/ecommerce/help-google-understand-your-ecommerce-site-structure): navigation/link relationships and product discoverability.
- [Google spam policies](https://developers.google.com/search/docs/essentials/spam-policies): scaled content and doorway abuse.

Topic architecture, task coverage, graph thresholds and lifecycle statuses are internal engineering methods, not Google requirements. No real target website or competitor crawl was performed.
