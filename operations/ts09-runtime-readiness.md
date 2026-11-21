# TS09.2/TS09.3 — Agent runtime installation and compatibility readiness

Source checkpoint: `4d2f31929328b93a551cfce5c9bf498f26f277e8` (TS09.1). Date 2026-11-21. Development status: **HOLD**. No actual Cursor/Codex agent session observed in this review. The source-matched package and the source CI validation are separate from skill discovery and execution.

## Official capability references (checked 2026-11-21)

- [Cursor Agent Skills](https://cursor.com/docs/skills): document a project `.cursor/skills/seo-engineering/SKILL.md`; use a new session and independently verify discovery. Other legacy/common directories may also work but this procedure chooses one explicit project path.
- [Cursor CLI overview](https://prod.cursor.com/docs/cli/overview): CLI `agent`, Ask mode `--mode=ask`, model and sandbox selection. Check actual `agent --help` and `agent --version` rather than copying flags blindly.
- [Cursor run modes](https://cursor.com/docs/agent/security/run-modes): read boundaries and command policies have evolved; verify exact version/config, don't assume Ask/read-only equals read isolation.
- [Codex skills](https://learn.chatgpt.com/docs/customization/overview): project `.agents/skills/seo-engineering/SKILL.md` discovery. Its path differs from the chosen Cursor path. 
- [Codex noninteractive](https://learn.chatgpt.com/docs/non-interactive-mode) and [CLI reference](https://learn.chatgpt.com/docs/cli/reference): `codex exec` has a read-only sandbox default/option, with optional JSON event output. Permissions, authentication, filesystem/network read isolation and exact version must be inspected independently.
- [Codex sandbox controls](https://learn.chatgpt.com/docs/agent-approvals-security): write restrictions do not establish that the process cannot read another mounted workspace or operator packet.

Documentation describes intended capabilities, not an actual verification of these deployments. If official paths or options change, record and follow actual installed version help and update the procedure with a new source-reviewed checkpoint.

## Safe operator prerequisite

1. Obtain authorization for a private synthetic probe and explicit consent before paid inference. Select **one** runtime and exact model, then match that same model and runtime for both eventual benchmark arms. Do not test on BeatFit, customer data or another private project.
2. Freeze an exact **new** candidate source commit and *its own* source-matched archive digest. Use an owner-reviewed rights/privacy scope before redistribution. Keep TS05 historical checkpoint and previously frozen benchmark candidate untouched; results never transfer to a different archive by default. Verify clean source, the actual package and the extracted install with existing verifier. The runtime preflight below is an installation check, not privacy or legal clearance.
3. Stage a fresh synthetic project **outside** the SEO Engineering source checkout, with only one project skill installation:
   - Cursor: `$PROJECT/.cursor/skills/seo-engineering`
   - Codex: `$PROJECT/.agents/skills/seo-engineering`
   Extract the verified ZIP's `seo-engineering/` directory to the appropriate parent, not the whole repository. Never expose the source checkout or evaluation rubrics to trial agents.
4. From a trusted checkout run the maintainer-only local source byte checker (new output path outside repo):
   ~~~sh
   python3 scripts/preflight_runtime.py --runtime cursor \
     --archive /private/exact-source-skill.zip \
     --installed '/isolated/project/.cursor/skills/seo-engineering' \
     --out /private/cursor-install-preflight.json
   ~~~
   For Codex use `--runtime codex` and `/isolated/project/.agents/skills/seo-engineering`. It checks exact installed members against the archive/source and records whether a command name is on PATH. It **does not run the CLI**, inspect authentication, test installed version or prove activation/isolation. If CLI absent, report `blocked_cli_not_found`, not pass. Run it before enabling any model or connecting accounts.
5. Operator privately records `codex --version` / `codex exec --help` or `agent --version` / `agent --help`, exact model availability, sandbox/network/read boundary, approvals, skills directories, duplicate installations and unrelated global instructions. Do not copy raw settings, credentials, tokens, filesystem paths or private traces into GitHub. Validate isolation with a harmless **sentinel** outside the permitted workspace; never test with real secrets.
6. In a fresh **unscored** synthetic session verify the baseline does not see the skill, treatment sees its metadata, and the treatment actually reads SKILL.md and one applicable reference. Read evidence comes from real tool traces or trusted independent observation, not self-report. Also verify permissions and that unrelated requests do not invoke the skill. Record unexpected behavior or trace unobservability as unresolved. Do not reuse these sessions for scoring. Operator approves the first scored pair only after actual security, pricing and runtime evidence review.

## Compatibility evidence levels

| Level | Meaning |
|---|---|
| Python source tests | Offline functions and fixtures passed under a recorded interpreter/OS; no external runtime claims |
| Portable package checks | Built and selected functions run from relocated layout; no real agent |
| Installed bytes preflight | Source/archive/installed tree same; CLI binary detectable if present, not authenticated/activated |
| Unscored real agent probe | Actual version, skill discovery, resource reads and permissions observed in one isolated runtime |
| Scored first pair | Two real matched sessions with separate operator controls, trace/output review and permission evidence |
| Full public and held-out evaluation | Completed independent evaluation of an exact pinned artifact, separate safety review for incomplete runs |
| Release clearance | Source, privacy, rights, license, supported matrix and exact owner approval; not automatic from prior levels |

## Offline compatibility CI

A separate Linux job exercises existing full offline verification under Python **3.10** and **3.13**, with an inspected, SHA-pinned `actions/setup-python` v6. The existing Linux baseline records Python 3.12.3. Exact [compatibility CI 44897792400](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44897792400) passed on 2026-11-21: Linux Python 3.10.22 and 3.13.18 each completed all 362 offline tests plus repository/package relocation verification. [Core CI 44897792365](https://github.com/mohammadAliKeshavarzSarkar/SEO-Engineering/actions/runs/44897792365) passed 362 tests under hosted Python 3.12.3; 284 packaged resources, SHA-256 `d8dddd3c7c44e99748e3b2adfcc29f3222b0b92d9283b087f20697a06a123c05`, 397 tracked files screened with zero unscanned. This SHA is scoped to exact source commit `1bf2b334bac30b077ffa760f0cc9f482fdb15bc7` and its hosted zlib 1.3; neither the archive bytes nor runtime agent behavior were independently observed here. A Linux interpreter matrix is not Windows/macOS, locale, runtime-CLI or OS sandbox compatibility; zlib versions may differ and archive SHA-256 is not expected to match across different runtimes. No paid agents, deployment, site monitoring or publication in the matrix job.

## First pilot and unresolved gates

Use [existing TS04 operator launcher](ts04-runtime-launch.md) for the actual clean-checkout preflight, private 32-slot plan, two staged initial slots and unscored activation; do **not** create a second run scheduler. Use [TS07 incomplete-run sidecar](ts07-instruction-evaluation.md) for timeout/error traces; the normal grader covers completed responses only. Never call a structural test 'behavioral evaluation'. Missing runtime or read-isolation evidence keeps pilot at NOT RUN. For source/privacy/rights/licensing see [TS09 review](ts09-readiness-review.md), [TS05 governance](ts05-governance.md). Rest of the work cannot be certified without an authorized external runtime and owner decisions.

## Pilot staging layout correction (TS09.4)

The operator-only public pilot launcher now requires `--runtime-kind codex|cursor`. Codex treatment stages `.agents/skills/seo-engineering`; Cursor treatment stages `.cursor/skills/seo-engineering`, matching this guide's chosen installation locations. The first two staged tasks must be the same case, repetition and prompt with opposite arms, and a declared Cursor/Codex runtime label cannot contradict the selected layout. The existing randomized schedule, 16-case cohort, blinded score contract and original rubrics are unchanged. No actual CLI invocation, agent activation or read-isolation proof results from the fix. Use a **new, frozen source commit and archive identity** if executing a pilot; never silently replace a previously approved or scored candidate. See [TS04 runtime operator procedure](ts04-runtime-launch.md).

## First-pair integrity gate (TS09.4 offline safeguard)

A separate maintainer-only `scripts/check_pilot_staging.py` command now verifies the first frozen two-slot pilot packet against the actual current source-selected archive, matching prompts, context digest, fixed source paths, runtime-specific skill layout, missing rubric members and all-not-started ledger. It fails on modified staged bytes or unmatched operator records. This is a **private local integrity check only**; it does not launch agents, verify that the process cannot read operator material, establish skill activation or certify safe behavior. The operator must perform an independent unscored activation and read-isolation probe before scored sessions. A later slot staged using the lower-level CLI now requires an explicit runtime kind. The scorer and suite remain unchanged.
