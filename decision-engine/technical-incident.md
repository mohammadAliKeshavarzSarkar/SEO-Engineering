# Incident diagnosis decisions

Apply the shared [decision engine](README.md) and [T12](../docs/03-technical/t12-technical-troubleshooting.md).

| Condition | Decision |
|---|---|
| Reported exposure or critical harm | Escalate and plan authorized containment independently of other checks |
| Symptom is expected behavior or incomplete reporting | Document no-change or bounded recheck; avoid speculative fixes |
| Scope or current evidence unclear | Collect matched samples and establish expectations |
| Several plausible causes | Choose discriminating tests; keep contradictions and alternatives visible |
| Reviewed mechanism and sufficient evidence | Compare targeted recovery, monitoring and compatibility-aware rollback |
| Verification absent, failed or mismatched | Hold technical recovery judgment |
| Scoped technical recovery evidence passes | Owner review only; processed search and business results remain separate |

No automatic inference or closure from counts. Keep the original incident scope and separate subject identities for diagnosis and recovery. Record changes, confounders and rejected alternatives in the [incident record](../templates/incident-record.md).
