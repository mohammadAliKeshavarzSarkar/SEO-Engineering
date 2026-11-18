# Performance, mobile and accessibility

Core Web Vitals good thresholds at 75th percentile of field visits: LCP ≤ 2.5 s; INP ≤ 200 ms; CLS ≤ 0.1. Field and lab data answer different questions. Use CrUX/PageSpeed and search CWV reports when available, and instrument privacy-aware RUM by route/device. No field data does not prove good performance.

| Metric | Diagnose | Typical fixes |
|---|---|---|
| LCP | TTFB, resource discovery, download, render delay | cache, prioritize actual LCP resource, efficient hero, useful initial HTML |
| INP | input delay, processing, presentation | split long tasks, reduce JS, defer noncritical work, optimize handlers |
| CLS | unstable media, fonts, injected UI | reserve dimensions, compatible font metrics, avoid unexpected layout changes |

Use route-level bundles, responsive images, deliberate font preloading and font-display, appropriate caching, reduced-motion support, and lazy loading below fold. Never lazy-load a known critical LCP image as a default. Test animations and main-thread work on representative mobile devices. Respect keyboard, focus, landmarks, contrast, labels and touch targets. Preserve content and links across layouts; ensure mobile content parity for indexing.

Acceptance: record baseline and after lab tests with same settings; monitor field distributions across representative traffic after release; test accessibility and real journeys. Do not remove valuable content solely to chase Lighthouse 100.

Sources: [web.dev vitals](https://web.dev/articles/vitals), [mobile-first indexing](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing), [WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/).

For detailed field/lab provenance, bottleneck attribution, retained motion and matched regression comparisons see [T09](t09-performance.md). No field values are created from lab observations. Preserve explicit origin/URL scope, missing INP and actual provider assessment separately. Local three-metric completeness is not PSI's assessment rule.
