# Structured data, entities and search appearance

Structured data represents real page content; it may establish eligibility for supported features, never guarantees display or ranking. Maintain stable entity IDs and canonical URLs; connect organization, website, authors and pages when accurate. Use JSON-LD where suitable; do not duplicate contradictory graphs.

| Page | Candidate types | Check |
|---|---|---|
| Organization/home | Organization, WebSite | Real identity/name/logo and verified profiles |
| Nested pages | BreadcrumbList | Actual hierarchy and valid URLs |
| Editorial | Article or BlogPosting | Visible authorship, dates, headline, representative images |
| Product | Product and eligible offer/review properties | Genuine product, accurate price/availability/reviews |
| Main video watch page | VideoObject | Crawlable video/thumbnail and real metadata |
| Eligible local business | LocalBusiness | Real location and business details |

Schema.org vocabulary and Google rich-result support are different. Check current feature-specific docs and eligibility before implementation. Google discontinued FAQ rich results beginning May 7, 2026; FAQs can still help users, and FAQPage may have non-Google uses if valid, but no Google FAQ rich-result objective. Do not use fake ratings, hidden claims or generic software schema on pages that do not represent the entity.

Validate schema syntax with Schema Markup Validator; Google-supported features with Rich Results Test; verify visible parity and URL Inspection on production. Record exact errors/warnings, eligibility and release. Use `og:title`, `og:description`, `og:image` and `og:url` consistently for sharing; social tags are not a ranking guarantee.

Sources: [Search gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery), [Article](https://developers.google.com/search/docs/appearance/structured-data/article), [Schema.org](https://schema.org/), [changelog — FAQ removal](https://developers.google.com/search/updates).
