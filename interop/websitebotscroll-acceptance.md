# WebsiteBotScroll Stage A.1 consumer acceptance

Review: 2026-11-19. Decision: accepted for pre-stable A.2 independent consumer compatibility, not operational integration or public redistribution approval.

Canonical producer: WebsiteBotScroll at `bd45aa69c141deffed50c8d2ea57e28cea552cb8`, contract seo-crawl-evidence 0.1.0 (Draft 2020-12). The [machine-readable consumer pin](websitebotscroll-0.1.0-pin.json) records exact schema and 20 authoritative fixture hashes and source revision. The previous proposal at 8477cbf83e381b86754d773252ab72f6f486dc29 is superseded, even though its pre-freeze version string was the same. Reject implicit 0.x compatibility or same-version different checksum after acceptance; changes require explicit joint review and version decision.

## Review evidence

Inspected revised canonical schema, TypeScript semantic validator/parser, semantic rules and manifest. Recomputed SHA-256 from retrieved UTF-8 schema and all 20 fixtures; all match (9 valid, 11 invalid, including a raw duplicate-member fixture). Producer CI runs [44464472847](https://github.com/mohammadAliKeshavarzSarkar/WebsiteBotScroll/actions/runs/44464472847) and [44464467633](https://github.com/mohammadAliKeshavarzSarkar/WebsiteBotScroll/actions/runs/44464467633) completed successfully on the exact stated commit. Inspected first job log: 65 contract tests passed, repository lint/typecheck/test/build steps succeeded; some database/application integration tests were skipped. Producer reports 146 repository tests passing. No consumer parity or actual export was executed here.

| Prior finding | Revised disposition |
|---|---|
| IR01 metadata canonical URL secret checks | Covered in URL semantic validator |
| IR02 malformed JSON/URL failures | Structured parser/URL failure handling added |
| IR03 transaction/link identity | Run-local namespace uniqueness enforced |
| IR04 diagnostic relevance | Subject/cross-page scope declared and references checked |
| IR05 field overrides | Resolving RFC 6901 member pointers and overlap rejection |
| IR06 reason vocabulary | Versioned schema enumerations |
| IR07 hosted CI | Both exact-revision runs passed |

Acceptance is scoped to these review findings; not a claim of exhaustive validator correctness. Rule applicability, coverage, authority, redaction, actual provenance, and trust of every supplied observation are not established by passing a schema. The URL secret-name check is heuristic; producers must sanitize, consumers must avoid echoing untrusted contents. Cross-language URL, timestamp, integer and Unicode behavior requires adversarial parity tests; document disagreements and obtain producer review rather than silently changing the canonical schema.

## Stage A.2 work packages

1. A.2.1: freeze this pin; acquire exact source schema and fixtures as reviewed local inputs. No mutable branch, automatic network lookup or live producer repository dependency at runtime. Confirm permission before redistributing upstream contents; public distribution/owner license gate remains pending.
2. A.2.2: independent Python raw JSON parsing (strict UTF-8, duplicate member rejection, no nonfinite values), bounded input handling, verify expected schema checksum, Draft 2020-12 structural validation with formats and no coercion/defaults, then semantic validation matching the authoritative producer. Use a reviewed optional dependency environment rather than adding dependencies to the standalone core. Preserve raw evidence and separate sanitized validation results; no network, crawling, strategy, project change or execution of input content.
3. A.2.3: run the 20 pinned fixtures in Python and compare exact valid/invalid outcomes with producer expectations and actual TypeScript outputs. Include shared additional adversarial cases for nested/escaped duplicate keys, field pointers and overlap, diagnostic ownership, URL secrets, timestamp and numeric interoperability, lifecycle, identity and references. Preserve Persian strings, header order, all seven collection states, partial coverage and distinct URL identities. Compare semantic behavior, not necessarily library error wording. Record runtime/dependencies, commit, schema and fixture hashes, actual test results, disagreements and limits. No adapter promotion.
4. A.2.4: WebsiteBotScroll produces an actual authorized synthetic crawl export from real collected observations (not a hand-authored substitute). Preserve collection gaps, producer identity and export checksum; consumer validates the exact export offline and reports what was observed or unavailable. Joint review of authorization, provenance, coverage and real exchange results closes A.2.

The first mappings remain architecture, internal linking, international SEO; design them only after exchange validation. No REST, MCP, historical comparison, browser/performance/search data fabrication or duplicate crawler. No native diagnostic result automatically becomes a T11/T12 passing assertion, confirmed root cause or implementation authorization.

## Independent SEO Engineering progression

TS03 package verifier correction remains open on the pre-existing main revision; not part of A.1 acceptance. TS04 behavior benchmark and TS05 candidate readiness remain separate gates. This interoperability record is outside the portable skill allowlist pending implementation review and approval. No external runtime activation, consumer execution, or new distribution candidate is claimed.

## A.2.2 execution checkpoint

Consumer revision c259f0abd1627d9a020e32a32ad538e78502902c: [core CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44465690999) and [optional consumer CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44465690916) passed. Logs show 10 consumer test methods, including all 20 authoritative fixture outcomes (9 valid, 11 invalid), preserved parsed values, CLI receipt and overwrite rejection. Corrected TS03 [CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44465554357) passed, 264 core unit tests and installed-tree relocation checks; external activation remains untested.

A.2.3: authored shared-byte differential harness and locked observed optional dependency versions. Required comparisons and explicit exploratory edge probes are separate. Exact-revision outcomes and any divergences must be reviewed before joint parity acceptance. No real export or new contract version is implied.

## A.2.3 actual results and proposed resolution

[Exact differential CI 44466140687](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44466140687): 48/48 required cases passed, 2 exploratory matches, 5 exploratory differences, 55 actual paired inputs in total. All 12 jointly valid required cases preserved parsed content. [Core CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44466140674) passed. See [first-exchange profile proposal](exchange-profile-proposal.md) for the exact disagreements, independent conservative preflight and pending producer agreement. No canonical schema change, no real exchange, no operational approval. New profile test results must be checked on the changed revision.

## Bounded profile agreement

Producer acceptance communicated 2026-11-19. Previous proposal run [44466443407](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44466443407) passed 13 consumer test methods, 48 required comparisons, 55 profile eligibility checks, 12 candidates; five exploratory differences remain. [Core CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44466443395) passed. Agreed profile identifier now seo-crawl-evidence-exchange-profile/0.1.0; canonical pin unchanged. Consumer implements DEL/full URL-bearing header restrictions, exact byte-first sidecar binding under a proposed field layout. New profile/manifest tests pending exact-revision CI. Producer actual preservation/export readiness, manifest layout coordination, independently verified producer outcome and authorization of real synthetic collection remain open. No actual exchange or operational integration approved.

## Final manifest convention agreement

WebsiteBotScroll accepted the exact sidecar field layout at f08a73d40942edbfcb67566de7cab267433df359, with lexical conventions recorded in [accepted layout](exchange-manifest-layout.md). Prior exact CI [44466932995](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44466932995) passed 22 tests, 48 required comparisons and 58 profile checks; 12 joint candidates; 5 exploratory differences and 5 matches. Core CI [44466932914](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44466932914) passed. Consumer now explicitly separates length/hash/parse/binding stages, rejects BOM and negative zero, enforces exact declaration strings and type-sensitive binding; additional tests pending changed-revision CI. Actual collection and serialized producer replay not received. A.2.4 only, no strategic adapters or operational approval.

## A.2.4 producer checkpoint — 2026-11-23

Reviewed WebsiteBotScroll source commit `8e3ca8fc83e69379ca499e112742c1ec264e4dea` and its exact-commit GitHub CI runs [45166108810](https://github.com/mohammadAliKeshavarzSarkar/WebsiteBotScroll/actions/runs/45166108810) and [45165683594](https://github.com/mohammadAliKeshavarzSarkar/WebsiteBotScroll/actions/runs/45165683594), both marked successful. The team reports 13 rehearsed migrations and 277 tests; that count was not independently reproduced as a consumer run. Producer source includes persisted observation-platform collection, projection, export and producer-side verification. It advances **observation definitions** to `1.1.0`, while `build-document.ts` supports both observation definition versions and still emits the separate `seo-crawl-evidence/0.1.0` document contract. The canonical schema SHA-256 and exchange-profile identifier remain pinned.

**Confirmed blocking divergence:** `packages/evidence-producer/src/exchange-manifest.ts` currently emits `"contract": "seo-crawl-evidence/0.1.0"` and `verify-exchange.ts` expects that string. The [accepted 17-field manifest](exchange-manifest-layout.md) and independent Python `verify_exchange.py` instead require `"contract": {"name": "seo-crawl-evidence", "version": "0.1.0"}`. Those representations are not interchangeable, even with matching bytes or a producer-side pass. The consumer must **hold**, not silently rewrite or loosen the accepted agreement. Targeted synthetic regression cases enforce the hold; no actual frozen private export pair has been submitted to SEO Engineering for consumer verification.

The producer should correct its manifest writer/verifier and test the exact emitted pair against the independent Python consumer. After a corrected full producer commit is reviewed, deliver the immutable evidence JSON and 17-field manifest via a private authorized channel with exact byte counts and SHA-256, schema/commit/profile identities, an authorization reference, scope, coverage limitations, producer-side exact-byte verification report and frozen snapshot/projection provenance. Run the independent consumer on those delivered bytes; only then jointly assess A.2.4 closure. No REST/MCP, crawler duplication, diagnosis-to-strategy adapter, live customer crawl or release approval follows automatically.
