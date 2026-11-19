# A.2.4 — accepted sidecar field layout

The teams agreed the bounded profile identifier `seo-crawl-evidence-exchange-profile/0.1.0` and semantic manifest contents, on 2026-11-19. WebsiteBotScroll accepted the field layout at consumer commit f08a73d40942edbfcb67566de7cab267433df359 with the final lexical conventions below, on 2026-11-19.

| Field | Convention |
|---|---|
| contract | object with name seo-crawl-evidence and version 0.1.0 |
| exchange_profile | agreed identifier above |
| contract_source_commit | bd45aa69c141deffed50c8d2ea57e28cea552cb8 (canonical pin) |
| producer_commit | exact lowercase full 40-hex commit of actual export implementation; separately reviewed, not assumed to equal canonical pin |
| schema_sha256 | 8e06803f254b863a670418491aa85856208e75ae70b6bb77dcfde71cbc8787e8 |
| evidence_sha256 | exact delivered UTF-8 bytes digest |
| checksum_algorithm | SHA-256 |
| evidence_filename | explicit safe basename ending in .json; never used to locate an input |
| evidence_bytes | positive safe integer exact byte length |
| run_id | exact run.id |
| authorization_ref | nonempty restricted reference, verified separately by responsible owner |
| authorized_scope | exact copy of run.scope for this narrow first exchange; broader grants require separate review |
| started_at, finished_at | exactly equal run timestamps; terminal run only |
| coverage_limitations | exact copy of run.limitations; other coverage fields remain in evidence |
| producer_validation | pass or fail declaration, only pass eligible |
| producer_preflight | pass or fail declaration, only pass eligible |

No extra manifest keys in this accepted initial layout. No new fields in canonical evidence. producer.version equals actual reviewed export revision. Unknown data, limitations and provenance in the evidence remain unchanged. Manifest hash verifies only correspondence to supplied bytes, not authenticity; producer status declarations, authorization and collection truth require independent evidence and owner review. Keep both files private unless reviewed for redistribution. No customer crawl.

Consumer command (from repository root, optional environment):

```sh
python -m interop.verify_exchange --schema /trusted/pinned/schema.json \
  --manifest /private/manifest.json --evidence /private/evidence.json \
  --reviewed-producer-commit REVIEWED_FULL_EXPORT_COMMIT --output /private/receipt.json
```

The input filenames are explicitly supplied; the consumer checks checksum and byte length before evidence parsing. Local consumer result, profile result and producer declarations remain separate. Exit 0 candidate for joint review, 2 hold with receipt, 1 setup/read/write failure. Fresh output path required. No receipt claims actual exchange, authorization, origin or producer verification. No network or automated adapter.

The profile checks valid RFC 3339 representations with at most three fractional digits and no leap seconds, safe integer JSON spelling, Unicode scalar strings, and URL fields/entire URL-bearing Link and Location values free of backslash, C0 and DEL. Local byte/depth limits remain independently applied. No rewrite. Integer spelling is ordinary decimal JSON only; fractional and exponent spellings and negative zero are ineligible. Serialize zero as 0 at collection/export, never repair delivered bytes.

Testing uses hand-authored mutations of authoritative fixtures only, never actual collection. Real export receipt and independent replay of producer canonical validation/preflight against delivered bytes are still required for A.2.4 closure.

## Frozen lexical and processing conventions

Both SHA-256 members are 64 lowercase hex characters. The checksum algorithm is exactly SHA-256. The evidence is UTF-8 without BOM (consumer also rejects a sidecar BOM), without newline normalization or reserialization. Compare the informational basename against the explicitly supplied input name, never use it to select a file. Producer status strings are exactly pass or fail. Binding comparison preserves JSON types and array order. Select both local regular files independently, check positive byte length, check hash, decode strict UTF-8 without BOM, reject duplicate JSON members, check evidence/manifest consistency, then canonical validation followed by profile preflight. Early failures hold with skipped checks shown as not_run. Consumer limits may hold inputs before later checks. The producer must replay canonical validation and producer preflight on the actual serialized bytes delivered; prior object validation is insufficient. The receipt records declarations only, not independent producer replay or proof of origin. No permission implied to access or change a site.
