# R02 — Keyword discovery and evidence collection

Status: initial methodology. Source checkpoint: 2026-11-18.

## Objective

Build a reproducible corpus of candidate phrases and demand observations without confusing suggested keywords, measured site visibility, relative popularity, paid-market estimates and search-result evidence.

## Understand source semantics

| Source | Measures or provides | Limitation |
|---|---|---|
| Google Search Console | Recorded search performance of verified property | Not total market demand; hidden anonymized queries, truncated rows, aggregation and date effects |
| Bing Webmaster Tools Keyword Research | Bing keyword ideas, volumes and trends | Bing-specific, filters and coverage must be recorded |
| Google Trends | Sampled, normalized interest index (0–100) | Not absolute counts; low-volume terms can appear as zero |
| Google Ads Keyword Planner | Historical estimates with close variants and location/network/date settings; forecasts conditional on ads inputs | Rounded; advertising competition is not organic difficulty; regional/account eligibility matters |
| Autocomplete/related searches/question features | Candidate phrasing and questions | May vary by locale, time, personalization and platform policy; not volume |
| Sales, support, interviews and site search | User vocabulary and problems among observed populations | Not representative search frequencies; sanitize personal content |
| Manual SERP inspection | Current result types, competing pages, features and potential intent | Snapshot conditioned by market, device, time; not volume |
| Third-party keyword databases | Vendor estimates and discovery suggestions | Provider/model coverage varies, especially smaller languages; do not claim exact demand |

## Collection protocol

1. Derive seeds from approved or provisional R01 audience/problem groups: product/category, problem, outcome, comparison, questions, configuration, cost, compatibility and implementation. Preserve a separate list of brand terms and excluded intents.
2. Record raw phrases exactly as observed. Associate observations with stable query IDs; never overwrite raw text with normalized variants. Normalize in a separate field for analysis. A brainstormed phrase is a hypothesis, not observed demand.
3. Collect first-party query/page data for comparable selected date ranges when authorized. Record property, search type, geography, device, dates, dimensions, filters, aggregation and extraction date. Use longer periods when necessary for sparse or seasonal data. Avoid exporting sensitive query content publicly. Search Analytics API returns a bounded set of rows; pagination does not guarantee exhaustiveness. Reconcile aggregate and filtered data with scope limitations.
4. Use permitted external discovery tools. For Trends compare terms in the same request with identical settings, distinguish topic vs search term, and record geography, period, category and search type. Across runs the scale can change; do not add or average incompatible indices. For ad estimates record close-variant behavior, period, location, network, and whether value is rounded or a range; never sum overlapping estimates as exact demand.
5. Check platform availability and target-market coverage before collection. Google Ads official country restrictions include Iran and other sanctioned territories; do not assume Keyword Planner supports Iran-targeted estimates or attempt to bypass restrictions. Use authorized local evidence, Trends where available, Bing where supported, and qualitative discovery; report missing quantitative data.
6. Capture actual SERP observations for representative phrases; record observed engine, country/language if established, device, date, result type and URL. Do not label generic web search as a localized rank check. Use later intent review (R03) rather than deciding based on wording alone.
7. De-duplicate identical observation records, not potentially meaningful different queries. Keep multiple source observations independently; do not fill nulls with zero. Label status: observed, estimated, hypothesis, unavailable. Confidence reflects source fit and corroboration, not ranking probability.
8. Produce an initial corpus and investigate gaps rather than chasing arbitrary keyword counts. Stop when important audience/problem groups have evidence or explicit unknowns and marginal expansion yields little new useful intent.

## Quality controls

- Every numeric observation has metric, unit, source, scope, date range and collection date.
- Zero as reported differs from no data, privacy omission and uncollected.
- Do not equate paid competition, third-party difficulty, current rank and business value.
- Do not treat GSC impressions as population search volume or Bing volume as Google volume.
- Do not sum values across overlapping periods, conflicting scopes or close variants.
- Retain original evidence securely; do not publish raw private customer/site data.
- If a tool's access or legal eligibility is unknown, record the blocker and use lawful alternatives.

## Outputs

[Keyword observations template](../../templates/keyword-observations.csv) stores one row per source observation. [Keyword map](../../templates/keyword-map.csv) stores later intent/page decisions, not raw metrics. Use [SERP observations](../../templates/serp-observations.csv) for result evidence. Export source records separately; use evidence IDs to link decisions.

## Primary sources checked 2026-11-18

- [Search Console dimensions and data grouping](https://support.google.com/webmasters/answer/17011259)
- [Search Analytics API limitations](https://developers.google.com/webmaster-tools/v1/searchanalytics/query)
- [Google Trends data FAQ](https://support.google.com/trends/answer/4365533)
- [Keyword Planner forecasts and historical metrics](https://support.google.com/google-ads/answer/3022575)
- [Google Ads country restrictions](https://support.google.com/google-ads/answer/6163740)
- [Autocomplete predictions](https://support.google.com/websearch/answer/7368877)
- [Bing keyword research](https://www.bing.com/webmasters/help/keyword-research-628070b6)

This module describes evidence collection only; no live project metrics, rank claims, or final keyword recommendations are included.
