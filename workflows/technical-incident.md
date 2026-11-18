# Technical incident workflow

Read [T12](../docs/03-technical/t12-technical-troubleshooting.md), [incident decision procedure](../decision-engine/technical-incident.md) and [incident record](../templates/incident-record.md).

1. Establish authority, exact symptom, expectation, onset and comparison quality. Escalate reported exposure promptly to the proper owner, without copying sensitive material.
2. Scope affected/control cohorts and freeze evidence references. Review recent releases and data freshness; separate live and processed sources.
3. Propose competing hypotheses with falsifiers. Select low-risk discriminating tests; reuse T01–T10 and research/measurement modules as applicable.
4. Review native observations and enter the incident ledger. Run scripts/review_incident.py if useful; preserve contradictory and stale observations. A report does not establish causality.
5. Record reviewed cause or unresolved hypotheses, response alternatives, authorized decision, owner and recovery risks. Use [T11](../docs/03-technical/t11-deployment-regression.md) for release verification.
6. Recheck the actual recovery subject; keep technical recovery, security closure, search processing and business trends separate.
7. Record owner disposition, residual risks, follow-up and recurrence-prevention action. Do not auto-close or auto-deploy.

All private records remain outside the public skill.
