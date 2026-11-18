# R04 — Keyword normalization and clustering

Status: initial agent-ready methodology and offline candidate utility. Behavioral evaluations pending. Source checkpoint: 2026-11-18.

## WHAT
A raw query is observed text; a normalized match key is a deliberately lossy comparison aid; an intent cluster is a reviewed set of queries that may share a useful page or task. These are different entities. A cluster is not a URL, a search-engine rule, a ranking factor or a mandatory page. Preserve the distinction between raw observations, query IDs, match keys, pairwise evidence, cluster membership and later R06 ownership.

## WHY
Spelling, synonyms, morphology and phrasing can obscure related demand. Grouping reduces arbitrary synonym pages and enables coherent planning; overly aggressive grouping can erase meaningful needs and lead to poor content or damaging redirects. Unicode NFC handles canonical equivalence; compatibility normalization can remove meaningful distinctions. Search-engine canonicalization concerns duplicate or very similar pages, not the fact that different pages appear for the same query.

## WHEN / WHEN NOT
Use after R02 discovery and R03 intent research, before page mapping, editorial planning or architecture changes. Do not use identical words, embedding similarity, a vendor cluster, or overlapping impressions alone to merge pages. Do not cluster unrelated locales or unverified SERP scopes as if equivalent. A narrow repair to an existing page may not need clustering.

## INPUTS
Raw query IDs and observations; actual language/market; authorized comparable SERP samples (with snapshot IDs, date, device, engine, surface, comparable organic URLs and completeness); R03 intent assessments; product/brand/attribute constraints; existing URL inventory and page/query reports if available. Missing evidence is unknown. Preserve source rows and metrics separately; do not sum close-variant estimates or mixed scopes.

## HOW

### A. Normalize conservatively
1. Preserve original text and ID exactly. Make a separate match key using Unicode NFC, whitespace collapse and Unicode casefold where useful for candidate discovery. Casefold can also collapse meaningful case distinctions; never conclude equivalence from it alone.
2. For explicitly Persian language only, optionally map Arabic yeh/kaf to Persian forms, Persian and Arabic-Indic digits to ASCII, and ZWNJ to a space in the match key. Do not edit source text or public copy with this key. Do not apply Persian mappings to Arabic queries. Preserve spacing, joined-word and transliteration alternatives as separate raw queries even when keys match. No accent/diacritic stripping, blanket NFKC, stemming, stopword deletion or word sorting by default.
3. Protect negation, numbers, product/model codes, brand, audience, geography, dates, price, comparison, purchase, support and safety modifiers. Examples: 'with arms' vs 'without arms'; '2 kg' vs '20 kg'; خرید versus تعمیر. Similar topic is not identical task.
4. Record normalization rules/version and Unicode data version; flag collisions. Language-dependent synonyms or stemming require validated additional configuration. Match keys are for retrieval and review, not ranking decisions.

### B. Generate candidates
- Exact match-key matches: spelling candidates, not evidence of shared intent.
- Lexical token/character similarity: useful for candidate retrieval but sensitive to word order and negation; no universal cutoff.
- Semantic embeddings: optional multilingual model with evaluation of locale, model version, contrastive negative examples, privacy and cost. Similarity is not intent or rank probability. Do not send private raw queries to external services without approval.
- SERP overlap: compare sets of observed, unique comparable organic landing URLs from matched scopes and sampling windows. Exclude ads and unrelated feature children. Use exact observed URLs unless verified equivalent URL mapping is recorded; do not drop query parameters blindly. Domain-only overlap is weaker; a publisher can serve different needs.
- If a sample is missing or incomplete, record unknown; do not treat it as zero overlap. Require adequate comparable denominators, repeat important ambiguous samples and keep independent snapshots distinguishable.

### C. Review pair evidence
For sets A and B, Jaccard J = |A intersection B| / |A union B|. Example: two 10-result samples share 6 URLs, union 14, J = 6/14 ≈ 0.43. This is an overlap measure, not search volume or percentage of searchers. Report shared count, denominators, settings and sample date. The offline utility defaults to J >= 0.5 and at least 5 unique URLs per complete sample; these are internal provisional review defaults, not Google rules. With equal ten-result samples, J >= 0.5 needs at least seven shared URLs. Calibrate on reviewed project cases and inspect sensitivity, not universal thresholds.
Require consistent primary task, actual scope and business fit before concluding a group. High URL overlap may reflect a dominant site or mixed intent. Low overlap may reflect geographic differences, transient results or sample choice.

### D. Form and review clusters
Prefer pairwise compatible candidate groups rather than unrestricted connected components. A-B and B-C passing does not prove A-C passes. The utility uses sorted-ID greedy complete-link admission: every member pair must pass the evidence gates. It is deterministic for a fixed input and settings but is not optimal hierarchical clustering; review competing partitions and bridge queries explicitly. Singleton means ungrouped, not necessarily distinct intent. Missing evidence and different intents require review; never assign final page ownership automatically.
For large sets use bounded candidate retrieval and scope partitioning; validate recall across partitions and review bridge pairs. The provided tool supports 1–200 records per batch and is quadratic in pair count, not a production-scale clustering engine. Do not partition so aggressively that meaningful relations disappear.
Use the [decision protocol](../../decision-engine/keyword-clustering.md) to decide keep separate, group provisionally, request evidence, or reject. Review specific audience, task, constraints, page format, actual offering and existing useful pages. Then hand off to R06; no automatic publishing or URL changes.

### E. Investigate cannibalization carefully
Multiple pages with impressions for the same query can be normal: a category and buying guide serve different needs. Diagnose possible harmful overlap using query-page time series, comparable dates/device/market, actual URL purpose, clicks, conversion, indexability and selected canonical where authorized. Look for unstable or mismatched landing pages plus evidence of user or business harm, not merely shared keywords. Alternative explanations include intent mix, seasonality, search changes and technical issues. Retain distinct useful pages; if duplication is real, propose content differentiation or consolidation with mapping, review and rollback. Canonical hints and redirects are for appropriate duplicate/equivalent or moved URLs, not generic keyword conflicts.

## VERIFY
- Raw observations unchanged; rules/version and match keys recorded; Persian transformations scoped.
- Every comparable pair has matching observed scope and sufficient complete unique URLs; input attestations trace to R03 snapshots. Missing values remain null/unknown.
- No cluster accepted just from text similarity, shared domain, a bridge edge or a high-volume estimate. Evaluate pairwise intent and constraints manually.
- Candidate report is deterministic on fixed input; inspect thresholds, false matches and missed relations.
- Compare approved groups to labeled positive/negative examples; report precision (correct accepted pairs / reviewed accepted pairs) and recall (correct accepted pairs / all known relevant pairs) only for a clearly defined reviewed sample; unknown ground truth remains unknown.
- Run new clustering unit tests and synthetic fixtures; use E12–E14 behavioral cases separately. No claim of behavioral success from deterministic utility tests.

## MEASURE
Track reviewed candidate accuracy, unassigned/mixed cases, false merges and false splits, reviewer disagreement, cost and source coverage. After R06 and approved edits, measure aligned query/page cohorts, useful visits and qualified outcomes; do not attribute performance to clustering alone. Review after relevant search or product changes and allow time for crawl/report lag.

## ADAPT
Ecommerce: protect variant attributes, stock and compatibility. SaaS: separate documentation, integration, buyer and problem tasks. Local: preserve service and location constraints. Persian/multilingual: compare within actual language and market; do not turn spelling into public keyword stuffing. Regulated topics: preserve safety and audience distinctions. No search access: produce tentative lexical candidates only, keep evidence gates blocked. Larger samples: use reviewed candidate retrieval, bounded computation and versioned evidence.

## RECOVER
Reopen raw data if a match key loses distinctions. Revert mistaken cluster decisions without rewriting observations. Resample mismatched or partial SERPs. If a published consolidation harms users or eligibility, investigate and use the approved migration rollback. Stop unauthorized data collection or disclosure; keep project records private.

## OUTPUTS
[Cluster review template](../../templates/keyword-cluster-review.csv), [decision protocol](../../decision-engine/keyword-clustering.md), [synthetic example](../../examples/keyword-clustering/README.md), and offline script scripts/cluster_keywords.py (see repository scripts README). Preserve raw R02 and R03 source records. The script consumes prepared evidence, not a search API. No automatic URL assignments or volume aggregation.

## SOURCES
- [Unicode Normalization Forms UAX #15](https://www.unicode.org/reports/tr15/) and [Unicode normalization FAQ](https://www.unicode.org/faq/normalization.html), checked 2026-11-18: canonical versus compatibility equivalence.
- [Google canonicalization guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), checked 2026-11-18: duplicate or very similar pages and canonical signals.
- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide), checked 2026-11-18: duplicate content and URL selection, not an automatic spam violation.

The Jaccard formula, threshold, match-key policy and candidate algorithm are internal methods, not search-engine guidance. Consult [R03](r03-search-intent-and-serp.md) for source and scope limitations.
