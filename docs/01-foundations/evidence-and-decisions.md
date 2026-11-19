# Evidence, decisions and ownership

Distinguish documented behavior from observations and inference. Record primary-source URL, section, date checked, scope and interpretation. Research results from SERPs are observations, not global truths. Community articles can suggest hypotheses; they do not override official docs. A source saying a feature exists does not establish geographic eligibility or product availability.

Evidence tiers: official specs and platform documentation for rules; reproducible HTTP/browser/search inspection and first-party analytics for site observations; peer-reviewed studies and qualified reviewers for health claims; competitor observations for strategy; third-party estimates and hypotheses for exploration.

Decision lifecycle: proposed → reviewed → approved → implemented → verified → superseded. Record alternatives (including doing nothing), costs, risk, affected templates, evidence, validation, owner and rollback. Separate decisions from test results. A decision can be approved but not implemented. A static check can pass while production fails.

Prioritize using severity, business relevance, confidence and effort. Apply [R08](../02-research/r08-opportunity-prioritization.md) before comparing optional work: scope/fit, evidence, risk and dependency gates first; its impact rubric combines reach and importance, so do not multiply reach or volume again. The score is a heuristic, not a claimed SEO score or forecast. Keep P0/P1 visible regardless of missing estimates. Do not use numerical scoring to delay privacy/security or eligibility incidents.

Maintain project inventory, decision log, release annotations, experiment registry and source register. Review change-sensitive claims before implementation and quarterly. Use [decision record](../../templates/decision-record.md) and [source register](../08-learning/sources.md).

For observation records, separate metric/evidence kind (observed, estimate, hypothesis, unknown), review/decision lifecycle, collection status and actual verification result. An approved decision or structurally valid record is not measured success. See the [knowledge consistency guide](knowledge-consistency.md) for cross-module application and exception boundaries.
