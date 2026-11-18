# Decision register

Use [decision record](../templates/decision-record.md) per material decision. IDs: SEO-GEN-001 for general framework changes; use a project prefix for project decisions in that project's private workspace. Record proposed, approved, implemented, verified and superseded as distinct states. Include evidence and dates. Do not publish private project findings here.

| ID | Subject | Status |
|---|---|---|
| SEO-GEN-001 | Separation of reusable and private project documentation | Proposed initial repository policy |

Rationale: a public reusable reference should not expose internal audits. Alternative: entirely private monorepo. Review the policy with the owner before sharing any project details.

| ID | Subject | Status |
|---|---|---|
| SEO-GEN-002 | Master skill + task-routed references; one source of truth | Implemented initial architecture, agent evaluation pending |

**Context:** The skill must transfer to unrelated websites and agents without project cross-contamination. **Alternatives:** a single long prompt; separate independently maintained skills for every domain; a master entrypoint with modular references and generated portable package. **Decision:** choose the third approach to preserve one maintained knowledge base and support selective context loading. Add independently discoverable subskills only where a distinct trigger and reusable workflow justify them. **Acceptance:** correct task routing, project separation, portable build, and evaluations on varied site types. No model retraining is implied. **Rollback:** retain previous master entrypoint in Git; revert routing/package additions if they cause regressions. **Scope:** general methodology only; no authority to modify a target project automatically.
