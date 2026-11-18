# Persian, multilingual and international SEO

For the detailed agent workflow, evidence limitations, decision gates, offline checks and QA templates, see [R09 — Persian and multilingual search engineering](r09-multilingual-search-engineering.md). This page is the concise overview.

## Persian research procedure

Collect real Persian variants with and without ZWNJ (e.g. ضربان‌سنج / ضربان سنج), Arabic and Persian forms of ی/ي and ک/ك, digits ۰–۹ / 0–9, transliteration, spacing, informal terms and English loanwords. Normalize for analysis while retaining original queries and editorially correct spelling. Verify whether variants share intent through actual SERPs rather than generating duplicate pages. Preserve descriptive natural Persian anchors and titles; no mechanical repetition.

For Persian URLs, choose a stable readable slug, percent-encode non-ASCII characters as required in links and HTTP requests, normalize at URL boundaries consistently and test copies, redirects and canonical/sitemap values. Persian slugs can be useful to readers; they do not guarantee an SEO boost over English slugs. Avoid switching established slugs merely for SEO aesthetics.

Use `lang="fa"` and `dir="rtl"` for Persian pages, bidi isolation for mixed numbers and product names, accessible labels and mobile line wrapping. Test real devices and network conditions in the target market where authorized. Check regional availability, legal/privacy and actual delivery of analytics services; never assume identical collection in all markets.

## International sites

Use stable separate locale URLs when offering genuinely localized content. Use reciprocal hreflang including self and valid language/region values, and optionally `x-default` for a neutral fallback. Canonicalize each distinct language page to its own preferred URL; for same-language duplicates decide canonical strategy with current guidance. Provide crawlable locale links; avoid mandatory IP/language redirects that prevent access. Localize intent, currency, proof and support—not just words.

Validate every hreflang target returns 200 and reciprocal annotations resolve; check mobile and locale fallback. A one-language website does not need hreflang solely because it targets a country.

Sources: [International sites](https://developers.google.com/search/docs/specialty/international/), [localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions), [URL structure](https://developers.google.com/search/docs/crawling-indexing/url-structure).
