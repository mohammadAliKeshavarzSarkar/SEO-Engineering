# SEO experiments and maintenance

Record hypothesis, mechanism, cohort, baseline, primary metric, guardrails, duration/decision threshold, risks and rollback. Use comparable page groups when feasible, stagger changes and annotate releases. Avoid changing every title, URL, schema and layout at once. Search is observational and noisy; account for seasonality, updates, query mix, crawl lag and selection bias. Do not claim causality from simple before/after comparisons. Critical repairs are not optional experiments.

Measure eligibility, visibility, useful visits and verified conversion separately. Sample size and time depend on baseline volume and recrawl speed; avoid arbitrary universal time windows. Report absolute and relative results with denominators; low-data results are inconclusive. Keep negative results and superseded hypotheses. No ranking guarantee.

Cadence (adapt): weekly during releases — errors, indexing, changes and alerts; monthly — intent/page trends, lead quality, content decay and field performance; quarterly — crawl, source updates, schema, internal links and editorial reviews; annually — architecture, policy/access and inventory. Health-sensitive content may need expert-defined shorter review intervals. Refresh actual substance, not dates only.

Automation: use official APIs within quota, paginate where supported, store extraction date and query parameters, retry with backoff, avoid PII and credentials in Git. Schedule reports only after ownership and consent approval. Use [experiment template](../../templates/experiment.md).
