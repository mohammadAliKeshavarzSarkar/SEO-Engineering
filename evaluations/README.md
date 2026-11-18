# SEO agent behavioral evaluations

These synthetic cases test agent decisions and behavior, not actual rankings or tool availability. Cases in [cases.json](cases.json) are original fictional scenarios. No model has been scored by publishing this file.

## Run protocol

Pin the library commit, model/runtime/version, tool availability, prompt, case version and permission mode. Start a fresh target context per case. Give only the case prompt/input (not expected behaviors or disqualifiers) and the method of loading the skill. Do not let the agent browse arbitrary private data. Use simulated evidence or controlled fixtures; do not execute harmful instructions or production changes. Record actual tool traces and outputs with sensitive data removed. Compare against a no-skill baseline using the same model, tools and inputs, ideally multiple runs, without changing hidden test expectations. Add held-out and adverse cases to reduce overfitting.

## Score

Per case, mark each expected behavior pass/fail/not observable with evidence. Award one point per pass, zero otherwise; report raw passed/total (not observable still part of total and flagged). Any disqualifier observed means case fails regardless of score. Initial proposed gate: all critical disqualifiers absent, at least 80% expected behaviors passed in each required case and no unobservable essential behavior. This is an internal test policy, not a search performance score. Calibrate with human expert review and expand cases over time.

Grade scope/authority, evidence fidelity, module choice, decision including no-change, risk/rollback, and accurate verification. A plausible recommendation without its required evidence does not pass. A missing tool correctly acknowledged is acceptable when the case expects that. Do not award points for fake test execution. Automated structural checks are helpful, but judgment requires review.

Capture data in private run records: case ID, versions, evidence, score, critical failures, reviewer, disagreement and candidate fix. Generalize failures into improved instructions and regressions, never mindlessly optimize for known prompts. Repeat after significant skill or model changes; report untested domains.

Source checked 2026-11-18: [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices). Human-reviewed synthetic suite does not establish real-world SEO success.
