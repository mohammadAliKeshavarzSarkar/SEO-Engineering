# Technical audit workflow

Use [T10](../docs/03-technical/t10-audit-automation.md) and [audit and release](../docs/06-operations/audit-and-release.md). Read-only unless scoped implementation explicitly approved.

1. Record objective, target origin/environment, revision, route intent, authorized sources, evaluated capabilities and collection limits. Review security first.
2. Prepare existing local module envelopes; choose ready/blocked/not_applicable with reason for each T01–T09. Do not manufacture inputs. Retain underlying source refs and capture context.
3. Run the local coordinator against a trusted checkout and explicit trusted artifact root if T03 selected. Synthetic exercise:

```sh
python3 scripts/audit_technical.py --input examples/technical-audit/sample.json --artifact-root examples/spa-build/artifacts --output technical-report.json
```

4. Inspect native outputs and signal pointers. Record execution states and underlying coverage, escalate suspected private exposure, investigate gaps. Compare actual sources rather than infer actual site health.
5. Review each related set, record rationale and member exact signal IDs in groups on a separate manifest copy. Include reviewed R08 inputs and owner/next check. Rerun unchanged input context with new output; stale references rejected. Unassigned candidates remain visible. If no group reviewed, leave groups empty; no priority fabricated.
6. Prepare decision and acceptance/rollback using [review inventory](../templates/technical-audit-review.csv). Report independent checks and actual status, review limitations and required approvals. No automatic deployment or issue closure. Verify authorized changes separately and preserve history; search outcomes need actual platform evidence.

TS02: If grouping is rejected, T10-v2 writes the native diagnostics and ungrouped candidates, rejects the entire reviewed grouping batch and returns exit 2. Review any suspected exposure independently; correct grouping against the current signals and rerun to obtain reviewed triage. Do not interpret partial report or exit zero as release approval.

For complex handoffs use [delivery quality](../docs/01-foundations/deliverable-quality.md) and optional [delivery summary](../templates/delivery-summary.md). Lead with reviewed scope and urgent issues, distinguish examined samples from planned coverage and list actual native execution/review states separately from recommendations. Do not convert a partial offline audit into a site-wide score or completion claim.
