# Task routing

## Locate library root L

In a portable installation, use the references/library directory inside this skill if its docs/01-foundations/operating-principles.md exists. Otherwise, for a full SEO-Engineering checkout, use the repository root two levels above the skill directory. Confirm expected docs/, templates/ and decision-engine/ exist. If neither is present, report missing resources; do not pretend the skill is complete. Paths in the table are relative to L, not the target website.

Apply the execution contract before selecting tools. Read docs/01-foundations/operating-principles.md and docs/01-foundations/evidence-and-decisions.md for material decisions. Select only relevant rows and necessary dependencies, not every keyword match. Templates and utilities are optional deliverable aids; inspect an applicable module before using its utility. Do not load evaluation rubrics for ordinary target tasks.

## Select by requested decision, not keyword

1. Determine mode and authorized target first. A general explanation needs no target access; an implementation needs actual scope. If unrelated or generic copywriting, do not activate this workflow.
2. Choose the primary route by the outcome the user requests, not the technology or metric mentioned. For combined tasks, identify one primary route per independently requested outcome. A broad onboarding or incident/audit workflow coordinates subroutes; it does not require all modules.
3. Add a dependency only when its evidence or decision is needed. Unknown delivery architecture before a stack-specific change calls for T01. A known source/render discrepancy calls for T02; add T06 only for index/canonical decisions. A named technology in unrelated research is not a dependency.
4. Distinguish initial guidance from optional support. For each selected row start with the relevant methodology/protocol; open implementation patterns, templates or scripts only as needed for the requested output. A listed utility is not a command to execute. Use the common contract and preserve native evidence boundaries.
5. Record primary IDs, necessary dependency IDs with reasons, conditional/blocked decisions and material exclusions for multi-step work. If intent is ambiguous, use bounded orientation or ask only the question that changes the decision. Do not infer authorization, framework, locale, data availability or cause from trigger words.
6. If serious exposure, a widespread eligibility failure or harmful rollout is credible, interrupt discretionary work; route incident triage (T12) where appropriate. Preserve uncertainty and continue independent safe analysis. Use MAINTAIN only for authorized library/operator work, never to seek answers during evaluation.

| Task or trigger | ID | Reference candidates relative to L |
|---|---|---|
| New website, broad strategy | ONBOARD | workflows/new-website.md; docs/02-research/r01-business-and-positioning.md; docs/06-operations/audit-and-release.md |
| Keyword discovery | R02 | docs/02-research/r02-keyword-discovery.md; docs/02-research/r01-business-and-positioning.md; docs/02-research/research-roadmap.md |
| Search intent, SERP analysis | R03 | docs/02-research/r03-search-intent-and-serp.md; decision-engine/search-intent.md; templates/serp-snapshots.csv; templates/serp-results-v2.csv; templates/intent-assessments.csv |
| Keyword normalization and clustering | R04 | docs/02-research/r04-keyword-normalization-and-clustering.md; decision-engine/keyword-clustering.md; templates/keyword-cluster-review.csv; scripts/cluster_keywords.py |
| Competitor intelligence and competitive gaps | R05 | docs/02-research/r05-competitor-intelligence.md; decision-engine/competitor-intelligence.md; templates/competitor-register.csv; templates/competitor-search-footprint.csv; templates/competitor-page-benchmark.csv; templates/competitor-opportunities.csv |
| Keyword-to-page mapping, ownership and overlap | R06 | docs/02-research/r06-keyword-to-page-mapping.md; decision-engine/page-mapping.md; templates/page-registry.csv; templates/task-page-mapping.csv; templates/page-seo-brief.md |
| Topical gaps, internal linking and content lifecycle | R07 | docs/02-research/r07-content-gaps-and-topical-architecture.md; decision-engine/topical-architecture.md; templates/topic-task-coverage.csv; templates/internal-link-plan.csv; templates/content-lifecycle.csv; scripts/audit_topic_graph.py |
| Prioritization, backlog and opportunity scoring | R08 | docs/02-research/r08-opportunity-prioritization.md; decision-engine/opportunity-prioritization.md; templates/opportunity-backlog.csv; templates/priority-review.md; scripts/prioritize_opportunities.py |
| Persian, multilingual and international SEO | R09 | docs/02-research/r09-multilingual-search-engineering.md; decision-engine/localization.md; templates/locale-market-register.csv; templates/locale-page-matrix.csv; templates/localization-qa.md; scripts/audit_locale_manifest.py |
| Research automation, imports and validation | R10 | docs/02-research/r10-research-automation-and-validation.md; workflows/research-pipeline.md; templates/research-run-manifest.md; scripts/validate_research.py |
| Crawl accessibility, robots, sitemap discovery and crawl-budget evidence | T05 | docs/03-technical/t05-crawling-robots.md; decision-engine/crawl-discovery.md; implementation-patterns/crawl-discovery.md; templates/crawl-evidence-inventory.csv; scripts/audit_crawl_evidence.py |
| General crawl/index orientation (use T05/T06 above/below for actual diagnosis) | CRAWL_OVERVIEW | docs/03-technical/crawl-and-index.md |
| Architecture discovery, technology and delivery detection | T01 | docs/03-technical/t01-architecture-detection.md; decision-engine/architecture-detection.md; templates/architecture-inventory.csv; scripts/inspect_architecture.py |
| JS rendering, hydration, source/render discrepancies | T02 | docs/03-technical/t02-javascript-rendering.md; decision-engine/rendering.md; implementation-patterns/rendering-validation.md; templates/rendering-evidence.csv; scripts/audit_rendering.py |
| React, Vite, SPA routing, prerender or static deployment | T03 | docs/03-technical/t03-react-vite-spa.md; decision-engine/spa-delivery.md; implementation-patterns/react-vite-spa.md; templates/spa-route-build-plan.csv; scripts/audit_spa_build.py |
| Next.js, App/Pages Router, ISR, Cache Components or hybrid delivery | T04 | docs/03-technical/t04-nextjs-hybrid.md; decision-engine/next-delivery.md; implementation-patterns/nextjs-delivery.md; templates/next-route-cache-inventory.csv; scripts/audit_next_delivery.py |
| Rendering strategy or SPA/SSR architecture | RENDER_STRATEGY | decision-engine/rendering.md; docs/03-technical/rendering-and-architecture.md; implementation-patterns/route-delivery.md |
| Index eligibility, canonical conflicts or Search Console indexing evidence | T06 | docs/03-technical/t06-indexing-canonicals.md; decision-engine/index-canonical.md; implementation-patterns/index-canonical.md; templates/index-canonical-inventory.csv; scripts/audit_index_evidence.py |
| URL architecture, redirect chains, domain moves or migration validation | T07 | docs/03-technical/t07-url-migrations.md; decision-engine/url-migration.md; implementation-patterns/url-migration.md; templates/migration-url-map.csv; scripts/audit_migration.py |
| General URL/migration orientation (use T06/T07 for actual decisions) | URL_OVERVIEW | docs/03-technical/urls-and-migrations.md |
| Metadata generation, JSON-LD, entity claims and rich-result QA | T08 | docs/03-technical/t08-metadata-structured-data.md; decision-engine/metadata-entities.md; implementation-patterns/metadata-entities.md; templates/metadata-entity-inventory.csv; scripts/audit_metadata.py |
| Editorial content, claim quality and trust | EDITORIAL | docs/04-content/on-page-and-editorial.md; templates/content-brief.md; templates/editorial-claim-review.csv |
| Structured data/social/entity | SCHEMA_FEATURE | docs/04-content/structured-data.md |
| Images, video, Discover | MEDIA | docs/04-content/media.md |
| Core Web Vitals, lab/field performance, animation or regression evidence | T09 | docs/03-technical/t09-performance.md; decision-engine/performance.md; implementation-patterns/performance-optimization.md; templates/performance-evidence-inventory.csv; scripts/audit_performance.py |
| Performance, mobile, accessibility | PERF_OVERVIEW | docs/03-technical/performance.md |
| Search platform data, logs | SEARCH_DATA | docs/05-measurement/search-platforms.md |
| Analytics, lead, ecommerce events, consent | ANALYTICS | docs/05-measurement/analytics.md; docs/05-measurement/privacy-and-qa.md; templates/event-dictionary-v2.csv |
| Local, ecommerce, SaaS or programmatic | SITE_TYPE | docs/07-specialties/site-types.md |
| AI search | AI_SEARCH | docs/07-specialties/ai-search.md |
| Traffic loss, technical incidents, root cause or recovery | T12 | docs/03-technical/t12-technical-troubleshooting.md; workflows/technical-incident.md; decision-engine/technical-incident.md; templates/incident-record.md; scripts/review_incident.py; docs/06-operations/troubleshooting.md; relevant evidence guides |
| Authority | AUTHORITY | docs/04-content/authority.md |
| Experiment/monitoring | EXPERIMENT | docs/06-operations/experiments.md; templates/experiment.md |
| Coordinated technical audit, evidence consolidation and reviewed triage | T10 | docs/03-technical/t10-audit-automation.md; workflows/technical-audit.md; decision-engine/technical-audit.md; templates/technical-audit-review.csv; scripts/audit_technical.py |
| Release regression prevention, deployment review, pre/post-release gate evidence | T11 | docs/03-technical/t11-deployment-regression.md; workflows/deployment-regression.md; templates/deployment-gate-inventory.csv; scripts/review_release_gates.py |
| Implementation and QA | IMPLEMENT_QA | implementation-patterns/README.md; docs/06-operations/audit-and-release.md; templates/release-checklist.md |
| Maintainer-only: skill updates, competence and evaluation | MAINTAIN | docs/01-foundations/module-standard.md; docs/08-learning/stabilization.md; docs/08-learning/distribution-privacy-review.md; templates/skill-release-review.md; evaluations/README.md |

If multiple triggers are relevant, resolve dependencies (privacy/security -> eligibility -> research/intent -> implementation -> measurement; baseline measurement can begin earlier). For narrow tasks do not mandate unrelated modules. The maintainer-only row is for explicitly authorized library work or operator evaluation preparation, not an ordinary target audit or a model sitting a trial. When an evaluator restricts access to evaluation materials, honor that restriction; do not seek expected answers. If a specialized resource is missing, use safe remaining foundations and current evidence, identify the missing resource and mark dependent work blocked where material.

## Progressive reference loading

- Entry: the master skill, execution contract and this router establish scope. For material decisions also read the operating principles, evidence-and-decisions and decision engine overview. A general explanation can stay at orientation. Read the first listed resource for each selected route initially; for ANALYTICS also read its privacy-and-QA reference before evaluating collection. For T10, T11 and T12 also read their workflow (second resource) at initial selection. These are starting references, not complete checklists.
- Before making a consequential decision, read the relevant specialized protocol and any sections or dependencies required to establish evidence quality, authority, acceptance and risk. Choose implementation patterns only for applicable implementation/QA, templates for actual artifacts, and utility interfaces before any tool invocation. Follow a linked source only if its claim is needed. Use the maintained source register selectively rather than load all sources.
- Prefer headings or bounded excerpts for a long guide when available; preserve definitions, prerequisites, exceptions and relevant verification steps. If the relevant section cannot be isolated safely, read the necessary full file or mark the affected decision blocked. Never use a summary as evidence of unseen contents or restrict a necessary safety check just to meet a budget.
- Planning guide: 48 KiB of unique full-file content for single-route initial loading, 80 KiB for multiple initial routes. These are soft editorial budgets for source bytes, not model limits or token counts. A larger required load is permitted with a reason; split a broad task into decision stages and keep unresolved dependencies visible. Do not truncate mandatory safeguards, omit a dependency or redefine task scope to hit a number.
- Keep a small working record of references actually read (full or sections), what decision they support, material unresolved dependencies, and any budget exception. Reuse verified findings instead of repeatedly loading the same document unless currency or scope requires rereading. Do not claim a file was read just because it was listed. Evaluation-only resources remain separate. No agent must access maintainer profiling scripts or scenario answers to perform ordinary work.

## Resolve overlapping triggers

- Indexing problem vs performance data: T06 for index eligibility or selected canonical evidence; SEARCH_DATA for report extraction, aggregation and metric interpretation. Add T05 when crawl/discovery evidence matters. T12 coordinates a material incident; T10 coordinates an explicitly broad technical audit, not every isolated issue.
- Metadata: T08 for declarations, generation or source/render QA; SCHEMA_FEATURE for feature eligibility, EDITORIAL for actual content and claim quality. A title rewrite need not entail a complete structured-data audit.
- Delivery: T03 for React/Vite SPA and static delivery; T04 for Next.js specifics. T02 for matched renders; RENDER_STRATEGY for comparing approaches. T01 resolves uncertain architecture. Do not force SSR or framework migration.
- URLs: R06 for strategic page-task ownership; T06 for canonical/index decisions; T07 for actual redirects or migration planning. R09 for genuine locale decisions. Related keywords alone do not justify redirects or new locales.
- Releases and outcomes: T11 for revision-bound website regression gates; IMPLEMENT_QA for ordinary scoped implementation checks; EXPERIMENT for causal/comparison design; ANALYTICS for event/consent measurement; MAINTAIN for skill distribution/evaluation. Release vocabulary does not itself authorize deployment.
- Research and specialties: use R02–R08 according to the requested research stage, not all stages by default. Add R09 when language/market affects evidence. SITE_TYPE and AI_SEARCH support specialty-specific questions without replacing underlying eligibility/intent evidence. CRAWL_OVERVIEW, URL_OVERVIEW and PERF_OVERVIEW are orientation, not substitutes for specialized diagnosis.
