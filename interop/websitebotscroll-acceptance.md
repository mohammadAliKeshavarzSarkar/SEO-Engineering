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
