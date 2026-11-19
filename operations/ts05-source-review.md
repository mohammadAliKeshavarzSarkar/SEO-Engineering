# TS05.2 focused primary-source review

Review date 2026-11-19. Scope: selected change-sensitive assertions from the technical, measurement, localization and AI search guides; sources retrieved directly from official documentation. Not comprehensive independent accuracy, privacy, or legal review. Source URLs and sections recorded in the package's source register. No customer site accessed.

| ID | Claim | Disposition | Primary source and section |
|---|---|---|---|
| SR01 | Domain migration Change of Address | Clarified all old-domain variants for new-domain moves; separate same-domain www switching | Google site move with URL changes, Start the site move, step 4 |
| SR02 | Cache Components dynamic params | Clarified absence of function versus empty result and limited sampled build coverage | Next dynamic segments, With Cache Components; empty generateStaticParams error guidance |
| SR03 | Streaming metadata and status | Retained: full response vs early prefix; metadata may block for HTML-limited bots; streaming can commit 200 before missing content | Next generateMetadata, Streaming metadata; loading.js, Status Codes |
| SR04 | robots retrieval | Retained cautious interpretation: 4xx except 429, 5xx/time/cache behavior; actual provider cache unknown | Google robots-txt-spec, handling HTTP status codes |
| SR05 | FAQ rich results | Retained discontinuation May 7 2026; no feature objective | Google data anomalies, May 7 onwards; June search documentation updates |
| SR06 | Generative AI search | Retained technical eligibility, inclusion control and report limitations; no special AI schema or llms.txt requirement | Google AI optimization guide, technical structure, mythbusting, measure visibility |
| SR07 | CWV thresholds | Retained field LCP <=2.5s, INP <=200ms, CLS <=0.1 at p75, mobile/desktop; not lab release budgets | web.dev Web Vitals, Core Web Vitals |
| SR08 | Locale annotations | Retained reciprocal/self hreflang and valid supported language-region codes, optional fallback; no language detection claim | Google localized versions, Guidelines, Supported language and region codes |
| SR09 | Campaign changes during GA4 sessions | Retained no new session from campaign change; event attribution distinct | GA4 campaigns and traffic sources, processing |
| SR10 | Measurement Protocol success | Retained 2xx receipt not proof of processed data | GA4 Measurement Protocol reference, Transport |
| SR11 | Clarity audience restriction | Retained under-18-targeted site/app exclusion | Microsoft FAQ, restrictions |
| SR12 | Search reporting data defects | Added check of exact report/date anomaly register before causality | Search Console data anomalies; Nov 9–11 2026 generative AI Search logging defect illustrates why |

Sources inspected at this checkpoint; not all linked claims or underlying API/framework versions verified. No independently tested production behavior. The recent Search Console anomaly is a historical example, not evidence of any user's traffic changes. Future work: React Router/Vite modes, Search Analytics API aggregation and limits, indexing/canonical directives, privacy/consent and remaining R/T methods, source rights. Verify source applicability to exact platform version, market and property before implementation.

TS05.1 first CI failed one test due to overlapping synthetic URL-userinfo/email signals; corrected test in 73739604be4c851e35a46e0cddb9e4e87ce1546c, no scanner relaxation. Check its exact CI separately. Privacy heuristic signals and manual inspections remain distinct. Actual model executions, owner privacy approval, license/rights decision and A.2.4 delivery are pending.

This source review changes portable content. Keep already preregistered pilot archive and source commit immutable; record any new candidate checksum and run relevant validation on the replacement before evaluating it. Do not pool results across changed packages. No stable release or tag.