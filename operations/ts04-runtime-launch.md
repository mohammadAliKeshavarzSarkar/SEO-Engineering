# TS04.3 — Run the actual pilot

Status: first real runtime execution required. No agent calls, ratings or activation claims in this checkpoint. The maintainer-side launcher is outside the skill distribution. Use the latest independently verified source checkout and archive checksum for the real experiment.

## 1. Pick ONE runtime

Start with either Cursor CLI or Codex CLI, not one for baseline and the other for treatment. Check the installed version, authenticated access, exact available model, inference settings and remaining budget locally. Never paste API keys into the repository, prompts, traces or grading records. Paid usage is possible. The initial 32-slot experiment has only two sessions staged; run those before starting the remaining 30.

Examples (check your installed version's help before invoking):

```sh
agent --version
agent --help
agent models
# or
codex --version
codex exec --help
```

Cursor Ask mode is intended for read-only analysis; enable sandbox and explicitly review actual permissions, network policy and tool access. Do not use --force, --yolo, automatic MCP approval or automatic trust. Codex exec supports JSON events and read-only sandbox; read-only is not read isolation. Neither flag makes files outside the workspace inaccessible by itself. Use dedicated isolated user/container/VM or equivalent verified controls; expose only one staged target, necessary runtime files and login channel. Disable unrelated global skills, memory, plugins, MCP, web/shell network access and external project access; distinguish inference transport from agent tool network access. Verify no other private directories accessible to the model. Never mount the operator packet, source checkout or other staged workspace inside the active agent environment. No customer site or change authorization.

## 2. Prepare the first pair

Use a clean checkout at the chosen exact revision. The existing source-verified archive builder creates the candidate; the launcher derives the actual commit and archive/context SHA-256 instead of accepting made-up values.

Copy the example settings [JSON](ts04-runtime-settings.example.json) outside the repository. Fill every REPLACE string with actual values (including model identifier, exact version/settings and equal budget, actual isolation and review protocol). Keep the same configuration for both arms. The operator and workspace parent paths must exist, and the two new roots must be separate, non-nested and outside the checkout.

```sh
python3 scripts/start_public_pilot.py \
  --settings /private/runtime-settings.json \
  --operator /private/pilot-operator \
  --workspaces /isolated/pilot-workspaces
```

The tool creates the complete 32-slot randomized control and all-not-started ledger; builds and verifies the candidate; stages just the first matched pair; and writes private launch.json in actual randomized order. The operator-only prompts contain the same context instruction and exact task, no arm label. Use the staged folder only, not an IDE window with this source repo open. Do not expose launch.json, staging receipts or original archive. Separate the agent account from the operator account; the directories alone do not enforce isolation.

## 3. Non-scored activation check BEFORE running

In separate disposable copies of both staged environments, verify baseline cannot discover SEO Engineering and treatment can discover and read it. Start fresh sessions, inspect discovery metadata and actual tool/skill-loading trace or observed file reads; a model saying it used the skill is insufficient. Ask to identify locally visible skills and, only in the treatment activation check, explicitly request the SEO Engineering entrypoint and a routed resource. This is not the scored task. Record exact evidence, check for access to an intentionally harmless sentinel outside the permitted workspace, do not attempt to access real secrets. Stop if the runtime cannot enforce isolation or if skill visibility is wrong. Do not reuse activation sessions or their altered workspace for scored runs. Stage fresh copies for the real first pair if necessary; preserve the original task and settings. Verify actual skill discovery/activation during the scored run too; record unobservability rather than pretending a file was read. Do not explicitly request the skill in only one scored prompt.

## 4. Execute exactly one staged slot at a time

Use launch.json privately, select IDs in its declared order. Set WORKSPACE to the isolated target path, PROMPT to the operator prompt file, MODEL to the exact frozen model, RAW to a fresh private output directory outside the agent workspace. Supply the prompt through the launcher/terminal while preventing the agent from reading the operator directory. The raw logs and response must not be directly available as model input. The following examples assume a trusted operator shell with appropriate OS isolation already configured; running them alone is not a sandbox. Check actual flags for your runtime/version. Enforce the agreed equal time/tool/token budget externally; retain timeouts or early failures, never silently retry.

Codex (same command for each arm):
```sh
(cd "$WORKSPACE" && codex exec --model "$MODEL" --sandbox read-only \
  --skip-git-repo-check --json --output-last-message "$RAW/response.txt" - \
  < "$PROMPT" > "$RAW/events.jsonl" 2> "$RAW/stderr.txt")
```
Record actual exit status and elapsed time. Use fresh session, no resume. Confirm no approvals beyond reviewed permissions. If output-last-message would expose the private operator folder, omit it and extract final output from the structured events externally. Do not mount the operator directory to make this flag work.

Cursor CLI (same command for each arm):
```sh
(cd "$WORKSPACE" && agent --print --mode ask --sandbox enabled \
  --model "$MODEL" --output-format stream-json "$(cat "$PROMPT")" \
  > "$RAW/events.jsonl" 2> "$RAW/stderr.txt")
```
Record actual exit status, elapsed time, session/init model and terminal result. Extract final response from the terminal success result; no terminal result or tool/permission anomaly can be silently counted as a normal completion. Do not use resume / continue. If the local command is named cursor-agent, verify its own help and flags; don't assume CLI versions are interchangeable.

These examples are source-checked on 2026-11-19, not executed in our environment. Documentation: [Cursor parameters](https://cursor.com/docs/cli/reference/parameters), [Cursor CLI](https://cursor.com/docs/cli/overview), [Cursor output events](https://docs.cursor.com/en/cli/reference/output-format), [Codex non-interactive](https://developers.openai.com/codex/noninteractive), [Codex CLI reference](https://developers.openai.com/codex/cli/reference). No runtime/model is endorsed by name; pick what is authorized and available.

## 5. Return the actual evidence

Keep unredacted original traces private. Sanitize copies without changing evidence meaning; inspect traces for secrets, model/arm hints, and activation evidence. Use the fixed arm-neutral file layout and actual byte hashes in [pilot execution](../evaluations/pilot-execution.md), update ledger from actual outcomes. Preserve both failures and successes; if the first pair is incomplete, hold and record why, no replacement. Verify artifacts with prepare_trial.py before blind review. Do not claim independent grading from automated checks or from the tested agent's self-assessment. Record no writes or note unexpected changes with before/after hashes. Prompt, raw result, stderr, session identity, runtime/model/version, elapsed time, exit code and relevant tool trace matter.

Only after the first real pair and independent reviewer calibration/quality review, consider running the remaining frozen slots. First-pair logs and private artifacts are the next required input. Do not request another feature merely to avoid actual execution. The first two runs are part of the 32-slot pilot and not sufficient for generalization. WebsiteBotScroll exchange, complete public benchmark, held-out evaluation and TS05 release approval remain separate.

TS07.6: use the separate incomplete-session review before deciding whether to continue after an aborted or failed run. See [operator instructions](ts07-instruction-evaluation.md). Partial traces can reveal adverse actions even without a final response. No-signal in the available portion does not establish safety. Preserve the normal completed-run scorer, and hold pending independent review. A structural CI pass cannot substitute for the first real isolated pair.
