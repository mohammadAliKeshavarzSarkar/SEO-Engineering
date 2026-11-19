# Localization decision protocol

Use [R09](../docs/02-research/r09-multilingual-search-engineering.md).
1. Establish actual audience language, script, region, service eligibility and authorization separately. When unknown, research rather than infer from IP, language or domain.
2. Keep one useful language version if that meets the project scope; hreflang is not mandatory for a single locale. Do not translate or create country pages solely for traffic.
3. For distinct localized equivalents, prefer stable direct locale URLs and user-selectable links. Compare subdirectory, subdomain and ccTLD maintenance and migration cost; preserve existing useful URLs.
4. For genuinely translated content, keep an appropriate same-language representative. Review same-language duplicates independently; do not cross-canonicalize distinct translations. Annotate equivalent pages only, not unrelated pages or placeholders. Use supported language/script/region codes, fully qualified URLs, reciprocal/self references and optional meaningful x-default.
5. If regional evidence or tool access is missing, mark unknown and use authorized alternatives. Do not bypass restrictions or pretend generic web retrieval is localized ranking data.
6. Validate real HTTP, source/rendered markup, index signals, actual content language, native terminology, RTL/accessibility and conversion paths. Offline manifest findings are candidates for review, not live evidence. Record approval, rollout, rollback, and measured outcomes separately.

Exception routing: a single-language page needs no alternates solely for country targeting. A multilingual group may legitimately reuse one URL for a generic language or x-default fallback, and a partially maintained group may still have valid reciprocal pairs. Review against actual platform guidance and document exceptions rather than force strict local full-set/self-canonical findings to become page changes. Preserve approved URL identity and access. Use R09's source-backed code selection, Unicode and bidi QA before declaring a localized page ready.

See [locale register](../templates/locale-market-register.csv), [page matrix](../templates/locale-page-matrix.csv) and [QA checklist](../templates/localization-qa.md).
