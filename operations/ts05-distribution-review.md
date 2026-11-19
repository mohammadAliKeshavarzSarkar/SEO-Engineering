# TS05.1 — Distribution privacy pre-review

Status: offline pre-review and review accounting; no completed human review, privacy approval, license or stable release. The behavioral pilot and WebsiteBotScroll exchange remain independent. Keep this maintainer work outside the portable package so it does not change the pilot candidate bytes.

## Boundaries

Review both exact source-matched archive and every current tracked public repository file independently. A path excluded from the ZIP may still be publicly visible. The current repository is public with no assigned license as of the 2026-11-19 checkpoint. Public visibility itself is not redistribution permission. Historic commits, deleted files and untracked files need separate review. Do not change visibility, rewrite history, publish assets or assign a license without owner approval.

The offline scanner looks for limited patterns: private key markers, token-like forms, credential assignments, URL userinfo, sensitive query keys, email-like strings, local user paths and private-network URLs. Pattern matches are leads, not proof of secrets. Documentation and fixtures can trigger expected false positives. It does not detect all PII, secrets, encoded data, contextual reidentification or third-party copyright. Review actual file content and context manually, not just signals. Non-UTF-8, NUL-containing and over-limit files are marked unscanned; review these manually. Never paste a matched value into a public log, issue or grade record.

## Run privately

From a clean pinned checkout, use a source-matched verified archive and fresh output paths outside the checkout.

```sh
python3 scripts/review_distribution.py scan --archive /private/candidate.zip --out /private/pre-review.json
python3 scripts/review_distribution.py prepare-review --report /private/pre-review.json --out /private/manual-review.json
python3 scripts/review_distribution.py check-review --report /private/pre-review.json --review /private/manual-review.json --out /private/review-status.json
```

Scan output has per-file scope, path, byte count, SHA-256, scan status and rule/line identifiers; no matched text. Keep it private (paths can still be sensitive). CI runs the same scan in a temporary directory and prints only aggregate counts, not private records; it checks completeness of inventory, not zero heuristic signals. No automatic remediation.

For each file in the manual review, use state reviewed_no_issue, reviewed_with_findings, requires_correction or unreviewed, with an evidence reference for reviewed files. Explicitly classify each signal as synthetic_or_public_reference, approved_for_scope, requires_correction or unresolved. Record rationale without copying the value. Use the owner's authorization reference and actual reviewer identity. A record marked complete remains an attestation, not independent review proof or approval. The verifier checks record membership, hashes of the report/record, states and presence of evidence; it cannot establish reviewer independence, actual inspection or authority. Correct issues, rebuild and rerun against the exact replacement revision. For suspected exposure stop distribution and use owner-approved incident handling; no history rewrite without authorization.

## Remaining TS05 work

- Source currency: map material claims to exact official source sections and record verification, applicability and unresolved changes.
- Ownership: confirm authorship, third-party rights, licensing and intended distribution scope with the owner. No license selected automatically.
- Candidate: consolidate exact-revision CI, installed-tree acceptance, independent model activation and behavioral results, actual content review, source review and owner decisions.
- Promotion: only after all mandatory gates and explicit owner approval; no unsupported stable version, public asset or release tag.

The package remains 0.3.0-dev.12. TS04 real agent results and A.2.4 evidence exchange are not manufactured by release preparation.

## First execution finding

[CI 44470186709](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44470186709) executed 295 tests; 294 passed and the scanner assertion failed because the synthetic URL with userinfo also matched the email heuristic. Both signals intentionally remain visible. Corrected the expected test set, not the scanner; content pre-review step was skipped in the failed run. Recheck exact next revision before claiming actual screening results.
