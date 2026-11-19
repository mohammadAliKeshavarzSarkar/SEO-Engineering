# A.2.4 — proposed sidecar field layout

The teams agreed the bounded profile identifier `seo-crawl-evidence-exchange-profile/0.1.0` and semantic manifest contents, on 2026-11-19. This document proposes exact JSON member names and value conventions for coordination; confirm producer compatibility before using actual evidence.

| Field | Convention |
|---|---|
| contract | object with name seo-crawl-evidence and version 0.1.0 |
| exchange_profile | agreed identifier above |
| contract_source_commit | bd45aa69c141deffed50c8d2ea57e28cea552cb8 (canonical pin) |
| producer_commit | exact full 40-hex commit of actual export implementation; separately reviewed, not assumed to equal canonical pin |
| schema_sha256 | accepted schema digest |
| evidence_sha256 | exact delivered UTF-8 bytes digest |
| checksum_algorithm | SHA-256 |
| evidence_filename | explicit safe basename ending in .json; never used to locate an input |
| evidence_bytes | integer byte length |
| run_id | exact run.id |
| authorization_ref | nonempty restricted reference, verified separately by responsible owner |
| authorized_scope | exact copy of run.scope for this narrow first exchange; broader grants require separate review |
| started_at, finished_at | exactly equal run timestamps; terminal run only |
| coverage_limitations | exact copy of run.limitations; other coverage fields remain in evidence |
| producer_validation | pass or fail declaration, only pass eligible |
| producer_preflight | pass or fail declaration, only pass eligible |

No extra manifest keys in this proposed initial layout. No new fields in canonical evidence. producer.version equals actual reviewed export revision. Unknown data, limitations and provenance in the evidence remain unchanged. Manifest hash verifies only correspondence to supplied bytes, not authenticity; producer status declarations, authorization and collection truth require independent evidence and owner review. Keep both files private unless reviewed for redistribution. No customer crawl.

Consumer command (from repository root, optional environment):

```sh
python -m interop.verify_exchange --schema /trusted/pinned/schema.json \
  --manifest /private/manifest.json --evidence /private/evidence.json \
  --reviewed-producer-commit REVIEWED_FULL_EXPORT_COMMIT --output /private/receipt.json
```

The input filenames are explicitly supplied; the consumer checks checksum and byte length before evidence parsing. Local consumer result, profile result and producer declarations remain separate. Exit 0 candidate for joint review, 2 hold with receipt, 1 setup/read/write failure. Fresh output path required. No receipt claims actual exchange, authorization, origin or producer verification. No network or automated adapter.

The profile checks valid RFC 3339 representations with at most three fractional digits and no leap seconds, safe integer JSON spelling, Unicode scalar strings, and URL fields/entire URL-bearing Link and Location values free of backslash, C0 and DEL. Local byte/depth limits remain independently applied. No rewrite. The integer-spelling restriction continues the prior proposal; confirm with producer if decimal or exponent representations were intended to be allowed.

Testing uses hand-authored mutations of authoritative fixtures only, never actual collection. Real export receipt and independent replay of producer canonical validation/preflight against delivered bytes are still required for A.2.4 closure.
