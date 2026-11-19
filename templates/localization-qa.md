# Localization QA

Target/locale/group/page IDs, scope, owner, approval and checked date:
- Native intent, terminology, audience, genuine availability and regional constraints
- Local proof, currency, units, dates/time zones, forms, support, expert review where needed
- Source HTML and DOM language and direction; fonts, mixed script text and numerals, focus order, mobile layout
- Stable direct GET URL, UTF-8 encoding, no double encoding, status and authorization
- Canonical/index intent, same-language duplicate review, equivalent alternate URLs and return annotations
- Accessible language selector, direct entry without cookie or IP redirect; fallback behavior
- Consistency of chosen HTML/header/sitemap annotation method, internal links, metadata and schema
- Consent, lawful analytics delivery, measured regional availability and approved conversion QA
- Actual test results, blocked checks, index inspection where authorized, baseline, rollout and rollback

Do not claim a locale is indexed or ranks correctly simply because its annotations validate.

## Extended acceptance cases (TS06.4)

- Separate actual HTML language, direction, locale routing, supported hreflang tags and measured region; check language-only fallback vs x-default. Review valid same-URL aliases and partial reciprocal sets manually against current Google guidance. A strict local contract finding alone is not a defect.
- Preserve correctly authored ZWNJ (U+200C), meaningful model/quantity and negation. Test Arabic/Persian letter variants and digit normalization only on separate scoped candidate keys; do not alter published spelling or stable URL identity.
- Check document dir, scoped opposite-direction text, bdi/dir=auto for runtime values, accessible labels, numerals/currency/units, punctuation, selection/copy and keyboard/assistive-technology order. Inspect font shaping and narrow mobile rendering.
- Validate decoded display versus serialized URL components once; confirm requested path, canonical, hreflang and XML sitemap escaping. Check percent-encoded reserved delimiters, historical aliases, slash/case handling and real direct response before declaring equivalence.
- Test locale selection without a saved cookie or Accept-Language and preserve authorized direct entry. Document actual market evidence; do not infer localized ranking, service availability or legal eligibility from a simulation.

Record actual device/browser, scope, input, observation and blocked checks; no test is assumed run by completing this list.
