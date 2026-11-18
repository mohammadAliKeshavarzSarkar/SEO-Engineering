# Task routing

## Locate library root L

In a portable installation, use the references/library directory inside this skill if its docs/01-foundations/operating-principles.md exists. Otherwise, for a full SEO-Engineering checkout, use the repository root two levels above the skill directory. Confirm expected docs/, templates/ and decision-engine/ exist. If neither is present, report missing resources; do not pretend the skill is complete. Paths in the table are relative to L, not the target website.

Read docs/01-foundations/operating-principles.md and docs/01-foundations/evidence-and-decisions.md for material decisions. Do not load the entire library by default.

| Task or trigger | Load relative to L |
|---|---|
| New website, broad strategy | workflows/new-website.md; docs/02-research/r01-business-and-positioning.md; docs/06-operations/audit-and-release.md |
| Keyword discovery | docs/02-research/r01-business-and-positioning.md; docs/02-research/r02-keyword-discovery.md; docs/02-research/research-roadmap.md |
| Search intent, SERP analysis | docs/02-research/r03-search-intent-and-serp.md; decision-engine/search-intent.md; templates/serp-snapshots.csv; templates/serp-results-v2.csv; templates/intent-assessments.csv |
| Keyword normalization and clustering | docs/02-research/r04-keyword-normalization-and-clustering.md; decision-engine/keyword-clustering.md; templates/keyword-cluster-review.csv; scripts/cluster_keywords.py |
| Competitor intelligence and competitive gaps | docs/02-research/r05-competitor-intelligence.md; decision-engine/competitor-intelligence.md; templates/competitor-register.csv; templates/competitor-search-footprint.csv; templates/competitor-page-benchmark.csv; templates/competitor-opportunities.csv |
| Keyword-to-page mapping, ownership and overlap | docs/02-research/r06-keyword-to-page-mapping.md; decision-engine/page-mapping.md; templates/page-registry.csv; templates/task-page-mapping.csv; templates/page-seo-brief.md |
| Topical gaps, internal linking and content lifecycle | docs/02-research/r07-content-gaps-and-topical-architecture.md; decision-engine/topical-architecture.md; templates/topic-task-coverage.csv; templates/internal-link-plan.csv; templates/content-lifecycle.csv; scripts/audit_topic_graph.py |
| Prioritization, backlog and opportunity scoring | docs/02-research/r08-opportunity-prioritization.md; decision-engine/opportunity-prioritization.md; templates/opportunity-backlog.csv; templates/priority-review.md; scripts/prioritize_opportunities.py |
| Persian, multilingual and international SEO | docs/02-research/r09-multilingual-search-engineering.md; decision-engine/localization.md; templates/locale-market-register.csv; templates/locale-page-matrix.csv; templates/localization-qa.md; scripts/audit_locale_manifest.py |
| Research automation, imports and validation | docs/02-research/r10-research-automation-and-validation.md; workflows/research-pipeline.md; templates/research-run-manifest.md; scripts/validate_research.py |
| Crawl accessibility, robots, sitemap discovery and crawl-budget evidence | docs/03-technical/t05-crawling-robots.md; decision-engine/crawl-discovery.md; implementation-patterns/crawl-discovery.md; templates/crawl-evidence-inventory.csv; scripts/audit_crawl_evidence.py |
| Crawl/index/status/robots/sitemap | docs/03-technical/crawl-and-index.md; docs/06-operations/troubleshooting.md |
| Architecture discovery, technology and delivery detection | docs/03-technical/t01-architecture-detection.md; decision-engine/architecture-detection.md; templates/architecture-inventory.csv; scripts/inspect_architecture.py |
| JS rendering, hydration, source/render discrepancies | docs/03-technical/t02-javascript-rendering.md; decision-engine/rendering.md; implementation-patterns/rendering-validation.md; templates/rendering-evidence.csv; scripts/audit_rendering.py |
| React, Vite, SPA routing, prerender or static deployment | docs/03-technical/t03-react-vite-spa.md; decision-engine/spa-delivery.md; implementation-patterns/react-vite-spa.md; templates/spa-route-build-plan.csv; scripts/audit_spa_build.py |
| Next.js, App/Pages Router, ISR, Cache Components or hybrid delivery | docs/03-technical/t04-nextjs-hybrid.md; decision-engine/next-delivery.md; implementation-patterns/nextjs-delivery.md; templates/next-route-cache-inventory.csv; scripts/audit_next_delivery.py |
| Rendering strategy or SPA/SSR architecture | decision-engine/rendering.md; docs/03-technical/rendering-and-architecture.md; implementation-patterns/route-delivery.md |
| URL, canonical, redirect, migration | docs/03-technical/urls-and-migrations.md |
| Content, trust, metadata | docs/04-content/on-page-and-editorial.md |
| Structured data/social/entity | docs/04-content/structured-data.md |
| Images, video, Discover | docs/04-content/media.md |
| Performance, mobile, accessibility | docs/03-technical/performance.md |
| Search platform data, logs | docs/05-measurement/search-platforms.md |
| Analytics, lead, ecommerce events, consent | docs/05-measurement/analytics.md; docs/05-measurement/privacy-and-qa.md |
| Local, ecommerce, SaaS or programmatic | docs/07-specialties/site-types.md |
| AI search | docs/07-specialties/ai-search.md |
| Traffic loss or diagnostic | docs/06-operations/troubleshooting.md; relevant evidence guides |
| Authority | docs/04-content/authority.md |
| Experiment/monitoring | docs/06-operations/experiments.md |
| Implementation and QA | implementation-patterns/README.md; docs/06-operations/audit-and-release.md; templates/release-checklist.md |
| Skill updates/competence | docs/01-foundations/module-standard.md; docs/08-learning/stabilization.md; docs/08-learning/distribution-privacy-review.md; templates/skill-release-review.md; evaluations/README.md |

If multiple triggers are relevant, resolve dependencies (privacy/security -> eligibility -> research/intent -> implementation -> measurement; baseline measurement can begin earlier). For narrow tasks do not mandate unrelated modules. If a future specialized document is not present, use the existing foundations and current evidence and report the gap.
