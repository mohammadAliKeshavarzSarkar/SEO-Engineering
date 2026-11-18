# Operating principles

**Goal:** match useful, trustworthy public pages to real search demand and business outcomes. Search is a pipeline: discovery → crawling → rendering → indexing → canonical selection → retrieval/ranking → presentation → visit → outcome. Diagnose earlier stages first. Search engines do not guarantee any stage.

## Classify recommendations

| Class | Example | Decision rule |
|---|---|---|
| Eligibility requirement | Googlebot access, valid response and indexable content | Resolve for intended indexable pages |
| Official recommendation | Crawlable anchors, helpful titles | Apply where relevant |
| Project policy | One trailing-slash convention, one clear H1 | Document and enforce consistently |
| Experiment | Alternative CTA or title wording | Define test, metric and rollback |

SEO is not a checklist of universal ranking factors. E-E-A-T is a quality framework, not a standalone score. Structured data is not a ranking guarantee. A sitemap enables discovery, not guaranteed indexing. Accessibility matters for people even where not a ranking signal. Technical rendering strategy should follow page needs and real validation.

## Priority

P0: widespread loss of access/indexability, security or privacy risk. P1: important templates fail eligibility or business outcomes cannot be measured. P2: relevance, internal architecture, performance and trust gaps. P3: optional enhancements and experiments. Assign owner, confidence, affected URLs and dependency to each issue. Stop unsafe releases; do not delay a critical fix for an experiment.

## Sources

- [Google Search Essentials](https://developers.google.com/search/docs/essentials)
- [How Search works](https://developers.google.com/search/docs/fundamentals/how-search-works)
- [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a)
