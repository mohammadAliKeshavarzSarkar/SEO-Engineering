# TS09.4 — Pilot staging integrity and runtime-specific installation

Date 2026-11-21. Base `fdd92b32afd582be1067ae0a5c98876847eed76b`. [Prior verified core CI](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44898843912) passed source tests; [Python matrix](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44898843976) passed 3.10 and 3.13 offline tests. The reviewed build has 284 portable skill resources. No real agent runtime was invoked.

## Observed staging gap and closure

The original launcher targeted `.agents/skills` for all agents, regardless of a Cursor setup guide choosing `.cursor/skills`. TS09.4 made `start_public_pilot.py --runtime-kind` mandatory, which stages the initial treatment in the runtime-specific project directory, while keeping the baseline skill-free. This checkpoint also requires explicit runtime kind for later individual slots staged by `prepare_trial.py stage`; otherwise later Cursor sessions could silently receive Codex layout. The matched prompt, common context, original case order and evaluator's scoring protocol remain unchanged.

The new `check_pilot_staging.py` is a read-only operator verification layer, **not a new scheduler or model runner**. It rechecks the current trusted source/archive, source-selected members, first paired slots, treatment vs baseline file inventories, rubric exclusions, exact prompt text, stable identities, staging receipts, context hash and fully not-started ledger. It refuses modified files or mismatched control records. It neither establishes real process read boundaries nor starts a model. Operator must keep it private, pinned to exact candidate, and run actual fresh-session discovery/activation and permissions review separately.

## Private operator workflow

From a reviewed clean source checkout and prepared private settings:

~~~sh
python3 scripts/start_public_pilot.py --runtime-kind cursor \
  --settings /private/runtime-settings.json \
  --operator /private/pilot-operator \
  --workspaces /isolated/pilot-workspaces

python3 scripts/check_pilot_staging.py \
  --operator /private/pilot-operator \
  --workspaces /isolated/pilot-workspaces \
  --out /private/pilot-pair-integrity.json
~~~

For Codex, change **only** runtime kind and provide matching settings. Both commands operate solely on a fictional, approved task and do not run an agent. Do not mount operator packet or grading rubrics into agent environment. The checker rejects no-longer-unstarted packets; preserve execution evidence rather than resetting a run to "not_started". Actual pilot execution is blocked until a correctly isolated external CLI, authorized inference, verified discovery and independent review are established. Do not retroactively change a frozen run; derive a separately pinned new candidate and record its own archive.

Four added test methods check both installation paths, matched-pair integrity and distinct tampering; one lower-level CLI requirement is enforced. CI for this revision must be checked before claiming pass. Privacy/source/rights, full public and held-out evaluation and release decisions remain open. No changes to SEO algorithms, actual site, WebsiteBotScroll or BeatFit.
