# A.2.4 — WebsiteBotScroll observation-platform handoff checkpoint

Date: 2026-11-23. SEO Engineering baseline before this review: `14d43a7fb1986f2db1d007d35a091df52782afa4`. Producer source inspected at exact commit `8e3ca8fc83e69379ca499e112742c1ec264e4dea` (short: `8e3ca8f`).

## Verified source facts

- WebsiteBotScroll's source includes a real worker path, persisted observation-platform records, parity checks, snapshot freezing, projection and evidence/manifest export and verification. The team's CI runs [45166108810](https://github.com/mohammadAliKeshavarzSarkar/WebsiteBotScroll/actions/runs/45166108810) and [45165683594](https://github.com/mohammadAliKeshavarzSarkar/WebsiteBotScroll/actions/runs/45165683594) were marked successful; 277 tests and 13 migrations are **team-reported**, not independently reproduced in this consumer environment.
- `packages/crawler/src/evidence/definitions.ts` declares observation/collector definitions `1.1.0`. `packages/evidence-producer/src/build-document.ts` accepts both `1.0.0` and `1.1.0` observation definitions but still emits the canonical `seo-crawl-evidence/0.1.0` contract.
- The exchange profile remains `seo-crawl-evidence-exchange-profile/0.1.0`; producer `SCHEMA_SHA256` remains `8e06803f254b863a670418491aa85856208e75ae70b6bb77dcfde71cbc8787e8`. No evidence contract upgrade was evidenced by this review.

## Blocking incompatibility — manifest.contract

`packages/evidence-producer/src/exchange-manifest.ts` emits:

```json
{"contract":"seo-crawl-evidence/0.1.0"}
```

The exact previously accepted sidecar convention in `interop/exchange-manifest-layout.md` and the independent Python validator in `interop/verify_exchange.py` requires:

```json
{"contract":{"name":"seo-crawl-evidence","version":"0.1.0"}}
```

The producer's own `verify-exchange.ts` checks for the string, so producer self-verification cannot detect this cross-repository mismatch. The rest of the 17-field manifest is **not** certified compatible by this source check. The consumer therefore rejects the producer-shaped string without running downstream canonical or profile checks; do not accept alternate shapes, rewrite submitted bytes, or silently change the pinned format.

## Producer remediation requested

1. Correct the exported sidecar field **and** the producer-side verifier to the previously accepted object shape, preserving the other exact lexical conventions and 17-key set. Add a producer regression demonstrating acceptance of the canonical object and rejection of the old string.
2. Independently run the Python consumer on the **actual exported serialized bytes** (not a constructed surrogate). Confirm canonical/profile results and equivalent semantic fields; record any remaining divergence before publication.
3. After owner-authorized bounded synthetic collection, privately deliver unchanged `evidence.json` and manifest files, full producer commit, schema checksum, evidence SHA-256/byte length, producer exact-byte replay result, authorization reference, run scope, terminal coverage and limitations, snapshot/projection/artifact identity and confirmation of persisted bytes. Do not commit private files.
4. The consumer runs `python -m interop.verify_exchange` against the reviewed local schema and immutable pair with `--reviewed-producer-commit` set to the exact corrected producer revision. Review the report and provenance separately before any A.2.4 acceptance claim.

## Status

**Stage A.2.4: HOLD — producer/consumer manifest mismatch and no privately delivered real authorized synthetic export yet.** This is not a claim against successful internal producer tests, production-worker implementation, or migrations. REST/MCP, strategy adapters, release, distribution, and live-site authorization remain separate gates. The independent SEO Engineering package and legacy canonical schema/fixture pin remain unchanged.

## Follow-up — corrected in producer `3e11019e57882c25462c43ed8706cd4a9af5d3cd`

The above incompatibility is retained as a historical source finding for `8e3ca8f`. WebsiteBotScroll corrected the exact manifest object representation in both producer emission and verification at `3e11019e57882c25462c43ed8706cd4a9af5d3cd`; this specific format blocker is now **resolved**. See [corrected producer checkpoint](producer-3e11019-checkpoint.md). An actual authorized frozen exchange still has not been submitted or independently accepted.
