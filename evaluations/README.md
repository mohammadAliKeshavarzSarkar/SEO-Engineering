# SEO agent behavioral evaluations

These synthetic cases test agent decisions and behavior, not actual rankings or tool availability. Cases in [cases.json](cases.json) are original fictional scenarios. No model has been scored by publishing this file.

For the controlled S04 comparison and offline scorer, use [benchmark protocol](benchmark-protocol.md) and [grade schema](benchmark-grades.md). The 58 published cases are public regression scenarios, not held-out evidence; maintain independent held-out cases outside the skill. No benchmark has been executed.

## Run protocol

Pin the library commit, model/runtime/version, tool availability, prompt, case version and permission mode. Start a fresh target context per case. Give only the case prompt/input (not expected behaviors or disqualifiers) and the method of loading the skill. Do not let the agent browse arbitrary private data. Use simulated evidence or controlled fixtures; do not execute harmful instructions or production changes. Record actual tool traces and outputs with sensitive data removed. Compare against a no-skill baseline using the same model, tools and inputs, ideally multiple runs, without changing hidden test expectations. Add held-out and adverse cases to reduce overfitting.

## Score

Per case, mark each expected behavior pass/fail/not observable with evidence. Award one point per pass, zero otherwise; report raw passed/total (not observable still part of total and flagged). Any disqualifier observed means case fails regardless of score. Initial proposed gate: all critical disqualifiers absent, at least 80% expected behaviors passed in each required case and no unobservable essential behavior. The S04 scorer conservatively marks all existing criterion and disqualifier observations essential. This is an internal test policy, not a search performance score. Calibrate with human expert review and expand cases over time.

Grade scope/authority, evidence fidelity, module choice, decision including no-change, risk/rollback, and accurate verification. A plausible recommendation without its required evidence does not pass. A missing tool correctly acknowledged is acceptable when the case expects that. Do not award points for fake test execution. Automated structural checks are helpful, but judgment requires review.

Capture data in private run records: case ID, versions, evidence, score, critical failures, reviewer, disagreement and candidate fix. Generalize failures into improved instructions and regressions, never mindlessly optimize for known prompts. Repeat after significant skill or model changes; report untested domains.

Source checked 2026-11-18: [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices). Human-reviewed synthetic suite does not establish real-world SEO success.

T01 adds E39–E42 (architecture evidence and deployment boundaries). The S04 38-case plan remains a historical checkpoint; a complete 42-case plan with three repeats has 126 paired tasks / 252 individual runs. No independent behavioral runs have been executed.

T02 adds E43–E46 (failed readiness, source/header directives, interaction-dependent discovery and optional provider gaps). The prior 42-case plan is historical; the current 46-case suite at three repeats has 138 pairs / 276 individual runs planned, none executed independently.

T03 adds E47–E50 (router mode, omitted dynamic paths, fallback/asset errors and protected output/metadata). Current 50-case suite at three repeats plans 150 matched pairs / 300 individual runs; prior counts are historical. No independent behavioral runs performed.

T04 adds E51–E54 (export/runtime, Cache Components, streaming/status and freshness/security). Current 54-case suite at three repeats plans 162 matched pairs / 324 individual runs; prior counts historical. None independently run.

T05 adds E55–E58 (robots retrieval and permission, directive visibility, partial discovery and crawl budget). Current 58-case suite at three repeats plans 174 matched pairs / 348 individual runs; none independently executed.
