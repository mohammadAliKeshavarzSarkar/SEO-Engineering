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

## Distinct feature decisions

- Product rich results target a particular product or variants of that product, not generic category lists. Merchant listing eligibility requires the ability to buy on the page's site; an editorial affiliate review may instead be relevant to product snippets. Merchant listings require a genuine Offer rather than AggregateOffer alone. Check actual feature-specific required data, currency-specific URLs and current availability; do not invent price or stock for a lead-generation page. Initial HTML product markup is recommended for merchants, especially changing offers; verify source, completed render and freshness.
- Review snippets require genuine specific-item, user-visible evidence. Do not aggregate ratings from other sites, fabricate ratings or conceal incentives. Self-controlled Organization or LocalBusiness reviews are ineligible for Google star review features even with a third-party widget. This is not a ban on displaying truthful testimonials or a rule that all product reviews on merchant sites are ineligible.
- Breadcrumb markup continues to be supported on desktop Google Search; Google removed visible mobile search breadcrumbs beginning January 2025. Keep useful on-site navigation regardless; verify actual feature context rather than claim mobile display from valid markup.
- General guidelines recommend consistent representative markup on equivalent duplicate pages, not only the canonical. Do not copy one entity's markup onto distinct products or localized offers with different facts. Markup-specific manual actions can remove rich-result eligibility; Google's general guideline separates that from ordinary web ranking. Other policy issues may have other consequences. A warning, syntax success or appearance change does not prove a penalty.

Check exact feature guides before implementing: [merchant listings](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing), [product snippets](https://developers.google.com/search/docs/appearance/structured-data/product-snippet), [review snippets](https://developers.google.com/search/docs/appearance/structured-data/review-snippet), [mobile breadcrumbs update](https://developers.google.com/search/blog/2025/01/simplifying-breadcrumbs), [general structured data policy](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).

Validate schema syntax with Schema Markup Validator; Google-supported features with Rich Results Test; verify visible parity and URL Inspection on production. Record exact errors/warnings, eligibility and release. Use `og:title`, `og:description`, `og:image` and `og:url` consistently for sharing; social tags are not a ranking guarantee.

Sources: [Search gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery), [Article](https://developers.google.com/search/docs/appearance/structured-data/article), [Schema.org](https://schema.org/), [changelog — FAQ removal](https://developers.google.com/search/updates).

For typed generation, actual source/render comparisons, safe JSON-LD serialization and layered validation see [T08](../03-technical/t08-metadata-structured-data.md). The local article profile is an internal convention, not Google's required-property list. Never equate local syntax or literal checks with semantic validity or feature eligibility.
