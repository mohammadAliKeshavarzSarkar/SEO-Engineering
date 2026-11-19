# R09 — Persian and multilingual search engineering

Status: initial agent-ready methodology and offline locale-manifest validator. Behavioral evaluation pending. Source checkpoint: 2026-11-18.

## WHAT

International SEO adapts website discovery and usefulness to real language, script and market needs. Multilingual means several languages; multi-regional means several geographic markets. These can overlap but are not interchangeable. Persian (fa) is a language, Arabic-derived script generally flows right to left, and Iran (IR) is one market. A Persian speaker may live elsewhere. Locale identifiers for HTML, application localization, analytics and search annotations can differ in supported syntax; do not reuse them without checking.

## WHY

Separate accessible locale URLs and clear localized content allow users and search crawlers to discover appropriate versions. Google determines page language from content, not HTML lang attributes; lang and dir nonetheless matter for accessibility and presentation. Hreflang communicates relationships among equivalent variants, not a guaranteed ranking boost or canonical-selection override.

## WHEN / WHEN NOT

Use for native-language research, genuinely localized content, market expansion, locale route architecture, international migrations and language-specific diagnostics. A single-language site needs no hreflang merely because it targets a country. Avoid creating empty translations, duplicate country pages without real audience value, mandatory IP redirects, or rewriting established URL slugs solely for SEO. Respect service availability, consent and access restrictions.

## INPUTS

R01 audience and real offerings, explicit target languages/scripts/regions, native-language reviewer, authorized market evidence, R02–R06 query/task/page records, route inventory, current and desired locale URLs, source/rendered HTML, status/canonical/index observations, alternate annotations, language selector, locale-specific product proof, delivery and measurement conditions. Unknown geography or unavailable evidence remains unknown.

## HOW

### 1. Establish the locale-market matrix

Record language, script, direction, actual geographic audience, regional offering, terms, currency, support, proof, accessibility, available search/measurement sources, authority and maintenance separately. Use fa for broad Persian-language equivalents, fa-IR only where Iran-specific targeting is genuinely intended. A Persian/English site may have Persian-speaking Canadian users; a country/language combination is not proof of residence. Country-only codes are not valid hreflang language identifiers. Google documents supported language, region and script forms; check valid codes and platform support rather than assuming all BCP 47 tags are supported. Do not assume an HTML application locale automatically qualifies for Google hreflang.

Keep a separate mapping for HTML language tags (BCP 47 / IANA registry), document direction, framework locale keys, search-specific hreflang values and analytics geography. Google uses a supported subset of language/region/script combinations; use the current guide rather than an arbitrary BCP 47 parser. For example, fa and fa-IR may be meaningful for different audience scopes; fa-CA can describe a genuinely localized Persian-language version serving Canada, not every Persian-speaking user there. IR alone lacks a language component. Google does not support es-419 and ignores reserved region components such as UK, EU and UN; use GB where the intended region is the United Kingdom. Language tags are case-insensitive, with conventional casing for readability. Google also supports documented script forms such as zh-Hant and zh-Hans-US. Never infer a user's residence or a language code solely from script. Validate the actual audience and offering before proposing any new alternate.

### 2. Research native search behavior

Start with actual user tasks and local terminology, not automatic translation of a foreign keyword list. Collect native phrases, formal and informal variants, spelling, transliteration, loanwords and mixed-script product names. Record raw text, locale and requested versus observed search context. Use authorized Search Console data, permitted local observations and available research tools; preserve metric definitions and time windows. GSC country dimension is a reported geography, not language. Trends values are relative, not absolute monthly demand. Google Ads officially restricts Iran availability/targeting; verify provider and regional access and do not bypass restrictions. Do not fabricate local volume, rankings or tool availability. If only generic or foreign search evidence exists, classify as provisional and request suitable evidence; preserve null values.

Example synthetic Persian seed variants: ضربان‌سنج, ضربان سنج, ضربانسنج, حسگر ضربان قلب, سنسور ضربان قلب, heart rate monitor. These are possible terms, not verified demand or equivalent intent. An explicit purchase or repair modifier must remain distinct.

### 3. Normalize for analysis, not publication or routing

Reuse R04 cluster_keywords.py to preserve original queries and generate conservative candidate keys. For explicitly Persian text only, NFC, Arabic yeh/kaf to Persian forms, digit normalization and ZWNJ-to-space matching are useful for candidate retrieval. Retain original ZWNJ, punctuation, digits, English codes and transliterations. NFC does not itself equate Arabic and Persian letter variants. Joined and separated forms may need additional reviewed aliases, not global whitespace removal. Do not collapse Arabic or other languages under Persian rules; protect numbers, negation, product model and task differences. Never use keyword match keys as automatic URL rewrites or as editorial spelling. Validate false merges with a native reviewer and R03/R04 evidence.

Unicode normalization and language-specific match rules are separate operations. NFC combines canonically equivalent sequences; it does not equate Persian yeh (U+06CC) with Arabic yeh (U+064A), or Persian kaf (U+06A9) with Arabic kaf (U+0643). ZWNJ (U+200C, often called نیم‌فاصله) deliberately controls letter joining and must survive in correct editorial text. It is not ordinary whitespace, ZWJ (U+200D), or disposable formatting noise. Do not strip all invisible characters: inspect unexpected bidi overrides or other controls separately for display/security issues, and preserve the original evidence. NFC does not establish semantic or query equivalence. Compatibility folding may erase distinctions, e.g. superscripts or presentation forms; do not apply it blindly to product identifiers, codes or quantities.

Fictional review cases (no demand assertions):

| Raw input distinction | Candidate review | Preserve |
|---|---|---|
| ضربان‌سنج / ضربان سنج | May share the lossy Persian match key | Raw strings and correct native spelling |
| ضربانسنج / ضربان‌سنج | Review a possible alias, not automatic equality | Word boundary and separate observations |
| كیف / کیف | Language-scoped letter mapping if actually Persian | Original code points; do not transform Arabic data globally |
| مدل ۲ / مدل ۲۰ | Different numbers | Exact model/quantity identity |
| خرید حسگر / تعمیر حسگر | Different tasks | Purchase vs repair |
| fa vs fa-IR | Separate market evidence where applicable | Real language, region and source scope |

Store normalization version and actual runtime Unicode database version; Unicode 18.0.0 UAX #15 is the reviewed reference, not a claim that the local Python runtime uses that database.

### 4. Select a stable URL strategy

Compare subdirectories, subdomains and country domains using actual locale scope, current URL value, maintenance, infrastructure, eligible domain registration and migration risks. A language subdirectory on a generic domain often simplifies maintenance, but is not mandatory. Google recommends distinct URLs for localized versions instead of relying on cookies or browser language; locale-adaptive delivery can hide variants from crawlers. Use descriptive audience-language words or transliterations, UTF-8 and percent-encoding where necessary in hrefs. Persian slugs are valid; do not claim they necessarily outperform English slugs. Preserve useful current URLs. Test direct entry, copy/paste, UTF-8 roundtrips, route matching, canonical/sitemap consistency, percent-encoding exactly once, trailing slash/case, historical aliases and server redirects. Do not decode reserved separators or apply query normalization blindly to paths. New URL mapping requires R06 migration approval.

For newly authored URLs use a reviewed stable slug registry and component-aware UTF-8 serialization. Google recommends localized readable words, percent encoding non-ASCII in hrefs and hyphens between words where feasible. Keep display slug separate from serialized href and request evidence; a browser may display the decoded form. Under RFC 3986 percent-escape hex case can normalize, but reserved delimiters must not be decoded indiscriminately (e.g. %2F is not generally interchangeable with /). Do not encode an already percent-encoded URL again or force path case changes without actual route policy. For internationalized hosts, retain reviewed host identity and validate IDN handling separately. Test actual browser/router/server behavior, source anchors, canonical, sitemap XML escaping, alternate URLs and redirects. A matching normalized label or Unicode appearance is not proof two request URLs serve the same resource.

For locale-adaptive delivery, Google documents that its default crawler IPs appear US-based and requests do not set Accept-Language, although geo-distributed crawling exists. Do not rely on this distribution to discover every variant. No special locale crawler UA should be inferred; verify identity using approved methods and treat a verified crawler consistently with ordinary visitors from the same location. Test authorized direct entry with no locale cookie or Accept-Language, user-selected locale transitions, and real regional access where permitted. Never bypass geographic/access restrictions. Country domains are a potential geographic signal, but some vanity ccTLDs are treated as generic; inspect actual platform guidance. Hosting location alone is not decisive, and neither ccTLD nor target language determines where users live.

### 5. Localize the task and the experience

Translate main content, not just chrome. Adapt wording, product applicability, audience examples, proof, imagery, currency, units, local terms, support, dates, forms, contact methods and meaningful conversion steps. Allow native editorial review and subject expert review where needed. Do not invent country offices or shipping availability. Distinct useful pages can coexist; unrelated locale pages need not be paired. Use clear language switch links to actual equivalents; if no equivalent exists, communicate the limitation instead of marking a generic homepage as equivalent. Avoid forced redirects based on IP/browser language; offer a choice and preserve direct entry. Keep private areas protected.

For Persian HTML use lang="fa" and dir="rtl" at document level where appropriate; use bdi or direction markup for embedded mixed-script names and identifiers. CSS logical properties can simplify RTL layout. Inspect numerals, phone numbers, form fields, charts, punctuation, dates, text truncation, localized title/description, font loading, focus and keyboard navigation, mobile parity and accessible control labels. Do not mirror meaningful icons or number order blindly. Verify actual page language in visible content and ensure browser/assistive technology can identify language and direction. This is usability/accessibility validation, not an asserted ranking factor.

For RTL content, set base direction in HTML markup (root document dir="rtl" and the appropriate lang), not only CSS. Use CSS logical spacing/alignment properties for layout; do not reverse strings, digits or identifiers in storage. For known opposite-direction phrases use tightly scoped dir="ltr" or dir="rtl" markup; for unknown direction of runtime text use bdi or a tightly scoped dir="auto" element. Form free-text inputs may use dir="auto"; known-direction emails, serial numbers and URLs need appropriate field-specific handling. Check copy/paste, caret movement, punctuation adjacent to product codes, mixed-language accessible names, focus order, numeric units, dates, and correct font shaping. Test on actual browsers and assistive technologies, not by visually mirroring the entire UI. The W3C Arabic & Persian Layout Requirements source is a Group Draft Note (work in progress); use it for layout context alongside W3C direction guidance, not as a normative SEO requirement.

Illustrative markup (not executed browser tests):
~~~html
<html lang="fa" dir="rtl">
  <!-- Document head and body omitted -->
  <p>مدل <bdi dir="ltr">HR-20</bdi>، مناسب تمرین</p>
  <p>نظر کاربر: <bdi>Sample name</bdi></p>
  <label for="question">سؤال شما</label>
  <input id="question" name="question" dir="auto">
</html>
~~~
In the actual document keep main-language markup, meaningful labels, and valid document structure. Isolate dynamic values and escape them for their actual HTML context. Direction controls solve text display, not search ranking.

### 6. Canonicals and hreflang

Build equivalent-page groups with real corresponding main content and stable preferred URLs. Distinct translated content should generally have its own same-language representative. Similar same-language regional duplicates may require a separate preferred representative decision; use canonical and hreflang consistently with Google guidance and verify rather than blanket-cross-canonicalizing all locales. Declared and engine-selected canonical are distinct evidence fields.

Use one maintained annotation method (HTML head, HTTP Link header for appropriate resources, or sitemap). Google treats these methods equivalently; multiple methods are unnecessary and can drift. Use fully qualified URLs and supported language/script/region codes, each member listing itself and its equivalents, with reciprocal links. x-default is optional for meaningful fallback, not a language code or requirement. A partial set with reciprocal pairs can be processed according to Google guidance; the utility below deliberately enforces a stricter full-set project contract for representative groups. Do not annotate unavailable, unrelated, private, redirected or erroneous destinations as if they were equivalent live representatives. For same-language canonical exceptions and fallback combinations, review manually and document reason.

Google recommends a generic language catchall when multiple regional variants of that language exist; one existing regional URL can also serve that language-level tag where genuinely suitable. This differs from x-default for unmatched language preferences. A fallback can reuse an existing URL; do not create a redundant locale page just to satisfy the local validator's one-tag-per-URL model. Cross-domain alternates are supported, subject to real correspondence and authorization. Missing reciprocal pairs are ignored or not interpreted correctly; maintain the full set where feasible but distinguish valid partial reciprocal configurations from broken return links. Google documents alternate annotations even for some pages that share untranslated main content and localize only template chrome; that does not establish independently useful acquisition pages or justify mass creation. A genuinely translated main body is not a duplicate solely because its meaning is equivalent. Review same-language duplicates using actual content and canonical policy.

The strict local manifest intentionally reports review findings for valid configurations outside its profile, including catchall aliases, x-default aliases, partial reciprocal sets, and non-self representatives. Do not “repair” such findings by adding thin pages or changing established canonical preferences. Retain source evidence and handle documented exceptions manually; no blanket compliance claim from a zero-finding report.

Illustrative paired HTML (each page uses its own canonical; alternate lines identical on both):
```html
<link rel="alternate" hreflang="fa" href="https://example.org/fa/guide/">
<link rel="alternate" hreflang="en" href="https://example.org/en/guide/">
```
No x-default is necessary in this two-language example. Do not point every Persian page to the English homepage.

### 7. Validate delivery and measure by locale

Use authorized direct GET, source and rendered DOM, header and sitemap inspection for whichever method is chosen. Verify actual status, crawl/index policy, canonical and reciprocal equivalents; test language switch and no-cookie entry without forced geographic redirects. Review sample pages for each template and exceptions. Use URL Inspection or equivalent authorized data to assess selected canonical and indexed states separately. Check real regional delivery and permitted analytics, consent, privacy, form completion and event deduplication. Do not collect personal or sensitive data in public records. A successful local check cannot establish regional service availability or search visibility.

### 8. Offline locale manifest tool

scripts/audit_locale_manifest.py consumes an explicit JSON manifest: allowed_tags (reviewed project language tags), pages (url, group, locale, status, index_intent, canonical, alternates array of tag/url). It checks the strict internal representative contract: unique page URLs, valid project-approved tag shape/allowlist, unique tag per group, exact full reciprocal/self sets, known targets and same-group membership, declared status 200, intended indexability and self-canonical representatives. Language-only singletons need no alternates. The syntax check only accepts a narrow two-letter language, optional script and region shape; it is NOT an ISO/BCP 47 registry validator. Review codes against current search guidance. x-default is allowed as a manifest representative, but real implementations may reuse a language URL for fallback; such aliases, partial sets and same-language canonical exceptions require manual review. Findings are structural review items, not proof of platform errors. No network, extraction, content-language detection, actual indexability check or mutation. Exact URL comparison requires consistent encoding by the collector.

## VERIFY

- Market and language explicitly separated, native wording reviewed and raw search evidence retained.
- Measured local data has appropriate scope and source; missing data is not zero.
- Existing URLs preserved unless approved migration, roundtrip/direct-entry tested; no forced localization redirect.
- Content genuinely localized; accurate offering; correct lang/dir, readable RTL, keyboard/mobile and mixed-script checks.
- Equivalent alternate groups, supported tags, self/reciprocal URLs and canonical policy reviewed; selected canonical separate from declared.
- Offline tool tests and synthetic fixture run, real HTTP/HTML/headers/sitemap verified separately where authorized.
- Locale outcomes and data collection consent checked. Behavioral E31–E34 require independent model evaluation, not merely publishing cases.

## MEASURE

Compare aligned locale page/query cohorts by region/device/date/search type. Track intended-variant visibility, unexpected locale destinations, accepted conversions, useful task completion, regional performance and localization defects. Country does not equal language. Account for canonical attribution, hidden query data, actual regional access, seasonality, changed query mix and crawl/report delay. Define baseline and review windows per locale; technical validity and hreflang do not guarantee ranking. Revisit source restrictions and offerings before major decisions.

## ADAPT

Single-language: preserve simple architecture, no mandatory locale pairs. Multiple languages: equivalent-page clusters and native editorial review. Multiple countries in one language: verify genuine regional differences and canonical policy. Mixed scripts: local direction markup and appropriate script identifiers. Ecommerce: actual currency, stock, shipping and regional terms; no fictitious offer. SaaS: localized support and capabilities with genuine service access. Health/finance: qualified review, local claims and legal constraints. New site: no invented history. Incomplete localization: prioritize useful existing versions, not empty placeholders. At scale use a maintained route/locale registry and template tests with exceptions, not mass automatic translations for search traffic.

## RECOVER

If language mismatch appears, inspect actual content, direct URLs, redirects, metadata and alternate groups before changing URLs. If annotations drift, repair maintained registry and verify source/rendered delivery; roll back risky rollout if necessary. If query normalization merges distinct tasks, restore raw records and revise candidate rules. If provider access is blocked, document it and use permitted alternatives; never bypass. Correct unsupported local claims, preserve private evidence, and do not change valid pages solely because a language report fluctuates.

## OUTPUTS

[Locale-market register](../../templates/locale-market-register.csv), [locale page matrix](../../templates/locale-page-matrix.csv), [localization QA](../../templates/localization-qa.md), [decision protocol](../../decision-engine/localization.md), [offline tool](../../scripts/audit_locale_manifest.py), [synthetic example](../../examples/locale-audit/README.md). Project-specific data remains outside the public skill.

## SOURCES — checked 2026-11-18

- [Google multi-regional/multilingual sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites): URL, language and market distinction, locale switching and same-language duplicates.
- [Google localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions): hreflang, supported tags, reciprocity and x-default.
- [Google locale-adaptive crawling](https://developers.google.com/search/docs/specialty/international/locale-adaptive-pages): limitations of dynamic locale delivery.
- [Google URL structure](https://developers.google.com/search/docs/crawling-indexing/url-structure): descriptive localized slugs and encoding.
- [W3C right-to-left structural markup](https://www.w3.org/International/questions/qa-html-dir.en.html) and [bidirectional HTML](https://www.w3.org/International/docs/bp-html-bidi/): language/direction separation and RTL.
- [Google Ads country restrictions](https://support.google.com/google-ads/answer/6163740): regional availability and targeting.
- R02 and R04 contain prior source references on measurement and Unicode normalization; their scope and provenance still apply.

The locale schema, strict alternate-set contract and comparison method are internal conventions, not universal ranking rules. No real target website or localized search data has been collected.
