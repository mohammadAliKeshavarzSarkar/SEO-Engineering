# Strategy, market, keywords and competitors

## Advanced research series (introduced during v0.2.0 development)

- [Research roadmap](research-roadmap.md)
- [R01 — Business objectives and search positioning](r01-business-and-positioning.md)
- [R02 — Keyword discovery and evidence collection](r02-keyword-discovery.md)
- [R03 — Search intent and SERP intelligence](r03-search-intent-and-serp.md)
- [R04 — Keyword normalization and clustering](r04-keyword-normalization-and-clustering.md)
- [R05 — Competitor intelligence](r05-competitor-intelligence.md)
- [R06 — Keyword-to-page mapping](r06-keyword-to-page-mapping.md)
- [R07 — Content gaps and topical architecture](r07-content-gaps-and-topical-architecture.md)
- [R08 — Opportunity scoring and prioritization](r08-opportunity-prioritization.md)
- [R09 — Persian and multilingual search engineering](r09-multilingual-search-engineering.md)
- [R10 — Research automation and validation](r10-research-automation-and-validation.md)
- [Integrated research pipeline](../../workflows/research-pipeline.md)

## Research workflow

1. Define product, audiences, market, business objectives, funnel and primary conversion. Identify whether search demand is informational, navigational, comparison, transactional or local; mixed intent is possible.
2. Collect seed terms from customer interviews, support/sales questions, product terminology, Search Console, Bing, Trends, keyword tools and manually observed autocomplete. Record source, date, locale, device and metric type. No-data does not mean zero demand; third-party estimates are not observed volume.
3. Normalize variants without deleting meaningful language distinctions. Group queries by task and inspect representative SERPs. Record page types, dominant intent, freshness, SERP features, real competitors and evidence gaps. Search-result competitors can differ from business competitors.
4. Map reviewed cluster/task units to intended existing or proposed destinations; leave uncertain or unsuitable units unassigned. Strategic assignment is distinct from technical canonicalization. Do not force one page per wording or cluster. Note overlapping pages and evaluate their actual tasks and evidence before consolidation.
5. Compare competitors by answer quality, user journey, original proof, topical coverage, technical access, brand trust and relevant citations. Do not copy competitor text or infer their revenue/traffic without evidence.
6. Prioritize clusters by business relevance, unmet need, intent fit, feasible evidence and estimated effort; volume is a secondary signal. Define success by qualified discovery and outcomes.

For demand and competitive evidence, apply [R02](r02-keyword-discovery.md) and [R05](r05-competitor-intelligence.md): Trends interest, ad estimates, first-party impressions, vendor traffic models and difficulty scores are not interchangeable. Preserve report/model context and investigate broken time series before comparing. [R03](r03-search-intent-and-serp.md) separates organic ordinal, compound result features and reported average position. [R04](r04-keyword-normalization-and-clustering.md) treats threshold-sensitive groups as provisional. [R08](r08-opportunity-prioritization.md) keeps unsupported opportunities unscored and critical repairs outside growth scoring.

## Deliverables

Use [keyword map](../../templates/keyword-map.csv), [SERP snapshots](../../templates/serp-snapshots.csv) and [results v2](../../templates/serp-results-v2.csv) and [project brief](../../templates/project-brief.md). Retain raw query and normalized cluster separately. Record source and confidence for every numerical value. Recheck the SERP before approving new commercial pages. If no first-party data exists, label initial mapping as hypothesis and establish a baseline after launch.

## Sources

- [Search Console performance report](https://support.google.com/webmasters/answer/7576553)
- [Google Trends help](https://support.google.com/trends/)
- [Google people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
