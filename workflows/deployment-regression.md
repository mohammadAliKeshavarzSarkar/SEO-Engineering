# Deployment regression review workflow

Use [T11](../docs/03-technical/t11-deployment-regression.md) and the [release checklist](../templates/release-checklist.md).

1. Confirm scope, authority, environment and release owner; identify changed route intents and baseline.
2. Review mandatory and optional gates, exact subject/configuration profile, method and sample coverage before running checks. Record excluded scope and rationale.
3. Collect authorized local and preview evidence; use relevant standalone diagnostics or [T10](technical-audit.md). Do not treat exit codes as issue resolution.
4. Evaluate the candidate manifest with scripts/review_release_gates.py. Retain required blockers, optional gaps and exposure escalation. Obtain explicit owner decision; no automatic deployment.
5. After authorized deployment, collect separate production evidence against the actual deployed identity. Review disposition and unresolved risk. Never transfer a preview pass to production.
6. For incidents, contain and consult the owner; choose compatible rollback or forward fix. Re-run evidence collection on the new subject.
7. Track search and field outcomes separately and disclose incomplete coverage.

Store project manifests, reports, decision records and evidence outside public library files. No deployment tool is implied.
