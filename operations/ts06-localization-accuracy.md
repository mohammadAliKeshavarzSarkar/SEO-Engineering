# TS06.4 — International and Persian knowledge accuracy

Date: 2026-11-19. Reviewed source 8ac4d36d3113b9d8d71b45e3a12633bc9ded8fc6. [TS06.3 CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44473792745) passed 301 tests and verified 216 packaged files. Previous archive SHA-256 6dab174d8a6ee98723691fff56fd8a185c78e3edff33c2b88a6b7bd90057b06c.

| ID | Area | Disposition |
|---|---|---|
| L01 | Locale identity | HTML/BCP47 vs search-specific supported codes, language vs market |
| L02 | Alternate graph | Generic language alias, x-default, cross-domain, partial reciprocity |
| L03 | Canonical handling | Actual localized bodies vs untranslated duplicates; manual exceptions |
| L04 | Persian match keys | Preserve raw strings, ZWNJ, code points, meaningful models and tasks |
| L05 | Unicode | NFC vs compatibility normalization; runtime version independent |
| L06 | URL serialization | Reader display vs request identity, component-aware percent encoding |
| L07 | Locale-adaptive crawling | Default US IP/no Accept-Language, actual regional testing and no bypass |
| L08 | RTL and accessibility | Root dir, scoped bidi, logical layout, runtime text/form QA |
| L09 | Local checker boundary | Added three regression tests for strict-profile limitations, no checker/schema change |

References: docs/08-learning/sources.md and R09. Selected review; W3C ALReq is a draft note, not a normative SEO standard. Three new offline regression methods exercise documented strict-profile behavior, including intentionally not validating official code membership. No actual page, keyword demand, browser, regional provider or external agent checked. Preserve prior candidate bytes and approvals; changed portable documentation yields a new hash once CI confirms. Existing 0.3.0-dev.12 is unreleased. No privacy/rights/source-completeness approval. Next TS06.5 measurement and conversion engineering.
