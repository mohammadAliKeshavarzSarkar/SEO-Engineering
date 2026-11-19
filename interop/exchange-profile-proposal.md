# First synthetic exchange — proposed compatibility profile

Status: **producer review pending**. Applies only to the first bounded A.2.4 synthetic file exchange. Not a revision of the accepted canonical schema, not a universal validator-equivalence claim and not a production export policy.

## Actual A.2.3 baseline

Consumer commit `0c0276245564a757896af7ed177c6a47aed70d37`, producer commit `bd45aa69c141deffed50c8d2ea57e28cea552cb8`. [Differential run 44466140687](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44466140687) passed, 55 identical-byte cases, 48 required passes, 0 required failures, 2 exploratory matches, 5 exploratory differences; 12 jointly valid required cases preserved parsed content. [Core run 44466140674](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44466140674) passed. Original results remain historical.

| Probe | TypeScript | Python | Proposed first-exchange decision |
|---|---|---|---|
| Submillisecond reverse chronology | valid | invalid | No timestamp fractions beyond three digits; do not truncate an existing observation to change the outcome |
| Unsafe integer | valid | blocked | All numbers must use integer JSON spelling, fit the JavaScript safe integer range; never round an existing value |
| Unpaired Unicode surrogate | valid | blocked | Export valid Unicode scalar strings in UTF-8; preserve Persian and other legitimate Unicode unchanged |
| Backslash header URL | valid | blocked | Exclude backslashes and control characters in URL fields and extracted URL-bearing header values; no silent normalization |
| Invalid URL port | invalid | invalid | Keep invalid, no change |
| Unicode domain in URI field | invalid | invalid | Keep invalid; producer may use an honestly recorded URI representation, not fabricated rewriting |
| Leap second | valid | invalid | No leap-second timestamp in first exchange; report unsupported collection/representation rather than inventing time |

The timestamp restriction is an intentional limited exchange policy, not a determination that RFC 3339 disallows these strings. The numeric spelling rule is conservative: the current schema uses integer fields, but JSON Schema may accept an integer-valued decimal or exponent; preserve that distinction. The profile also inherits consumer byte, depth and strict JSON/Unicode boundaries. It is not a general URL parser equivalence or secret detection guarantee.

## Proposed acceptance sequence

1. WebsiteBotScroll explicitly agrees to the profile or suggests alternatives; canonical schema and source pin stay unchanged unless a separate version review is warranted.
2. Consumer executes profile checks on the shared suite without modifying either validation verdict. Every required accepted input must be eligible for joint review; no invalid data or exploratory difference may be promoted.
3. Producer exports actual observations from an authorized bounded synthetic target, with exact schema pin, producer/export revision, input SHA-256, run scope and authorization/coverage limitations. No hand-authored fixture substitutes for actual collection.
4. Independently validate those exact bytes with producer and consumer and run agreed preflight. For the first exchange, restrict to readily representable evidence; if unavailable, use the contract's honest unavailable states where supported or stop export. No data coercion, inferred success or strategic adapters.
5. Jointly record actual observation coverage and restrictions before A.2.4 closure. Actual exchange, provenance, authorization and operational integration remain unverified until evidence exists.

Broader cross-language behavior (including additional URI/date/number edge cases and resource limits) remains explicit future contract work. The local preflight is a proposal and does not authorize collection or release.
