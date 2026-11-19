# Independent crawl evidence consumer (A.2.2)

Development-only, optional component. See [accepted pin](websitebotscroll-0.1.0-pin.json) and [acceptance decision](websitebotscroll-acceptance.md). The canonical schema and fixtures remain upstream; no vendored material or runtime network dependency. Obtain a trusted local checkout of the accepted producer revision separately. No schema or fixture is fetched by the validator or tests. Install requirements in a dedicated environment; direct dependency pinned, transitive dependencies not yet locked (record actual resolved versions for parity). The standalone SEO skill is unchanged.

From SEO Engineering root, after reviewing dependencies:

```sh
python3 -m venv .venv-interop
. .venv-interop/bin/activate
python -m pip install -r interop/requirements.txt
export WBS_FIXTURE_ROOT=/path/to/reviewed/WebsiteBotScroll
python -m unittest interop.test_crawl_evidence -v
python interop/validate_crawl_evidence.py --schema "$WBS_FIXTURE_ROOT/packages/evidence-contract/schema/seo-crawl-evidence/0.1.0/schema.json" --input "$WBS_FIXTURE_ROOT/packages/evidence-contract/fixtures/valid/complete-page.json" --output /path/to/private/receipt.json
```

Use a fresh output file and trusted stable local paths. The CLI verifies the schema SHA-256; parses strict UTF-8, rejects duplicate members and nonfinite constants; validates Draft 2020-12 with formats, then local semantic rules. No coercion, rewriting or default values. Return 0 valid, 2 invalid, 3 consumer-blocked with receipt; 1 setup/IO failure without a new valid receipt. Receipts include input identity and declared coverage/observation status counts only, not raw values or arbitrary error messages. Do not publish private receipts. Input remains unchanged. A valid result means the implemented checks passed, not that observations are true, safe, authorized, exhaustive or strategically correct.

Consumer boundaries: 16 MiB, nesting limit 128, safe integer range and valid Unicode scalar values. Boundary failures are explicitly distinct from canonical invalidity. Python urllib URL handling and datetime/jsonschema format behavior are not identical to WHATWG URLs, JavaScript Date and Ajv. The implementation conservatively blocks ambiguous control/backslash URLs and unsupported timestamp comparisons; broader cross-language edge parity is not established. Pointer rules, diagnostic evidence ownership, ID namespaces, coverage and ordered redirects are independently implemented. No automatic adapters, real export or deployment authorization. A.2.3 requires actual paired TypeScript/Python differential tests and resolution of disagreements, including numeric and time precision, URL parsing, and format checker differences. The optional CI checks fixture outcomes against the accepted expectations; producer CI separately validates TypeScript. Those are not a direct differential run for new mutations.

No public redistribution of the upstream schema/fixtures or stable release approved. The optional interop workflow uses the pinned public checkout in a disposable hosted job for compatibility tests only.

## A.2.3 actual differential harness

The optional compatibility workflow now prepares immutable synthetic input bytes from the 20 checksum-verified fixtures and 35 additional cases, executes the exact pinned producer TypeScript validator with a test-only Vitest bridge in a disposable checkout, then runs Python over those same input bytes. Every row binds the SHA-256; compares actual status, and for jointly accepted cases checks parsed content and ordered arrays against the original document. Required cases must match their reviewed expectation; exceptions, blocked results or preservation failures are not passes. Seven edge probes measure potential differences separately, without marking them compatible. Any differences require review before claiming broad parity; a green required-case CI alone is not A.2.3 closure. The report contains sanitized codes, case IDs and hashes, not input content; the intermediate producer output contains synthetic data only and is not uploaded. Never use this harness to publish a real crawl.

Reproduce using the commands in [workflow](../.github/workflows/interop.yml), with pinned producer checkout and dedicated Node/Python environments. The optional Python comparison uses a version lock observed in prior successful hosted Linux/Python 3.12.3 execution; not a universal or hash-locked dependency guarantee. The main dependency-free SEO library is unchanged.

## First-exchange profile proposal

See [exchange profile](exchange-profile-proposal.md) and `exchange_profile.py`. The proposed profile is checked independently of both actual validator outcomes. It holds input outside the bounded representability rules and cannot change a canonical verdict. Differential reporting now includes a distinct profile gate and joint-candidate count. Producer agreement and a real authorized synthetic crawl export are still required; no automatic promotion from profile eligibility to actual exchange or operational readiness.

## Accepted profile and A.2.4 intake

The producer accepted the bounded profile on 2026-11-19. The earlier proposal is historical; the agreed identifier is `seo-crawl-evidence-exchange-profile/0.1.0`. The consumer now checks DEL and entire URL-bearing header values in addition to previous restrictions. See [proposed sidecar protocol](exchange-manifest-layout.md) and `python -m interop.verify_exchange --help`. Manifest exact field names and export commit require coordination; real producer declaration and authorization are not independently established by a checksum. Actual evidence exchange remains pending. The new differential suite adds three probes (58 total) without erasing the original 55-case record.
