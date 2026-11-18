# R10 — Research automation and validation

Status: initial integration methodology, handoff validator and release-check runner; behavioral and external installation gates pending. Source checkpoint: 2026-11-18.

## WHAT
A reproducible SEO research pipeline is a scoped sequence of authorized collection, preserved observations, deterministic normalization, reviewed interpretation, decisions and verification. A skill provides procedures and executable assistance; it is not a hosted autonomous crawler or trained model. Keep inputs, intermediate observations, derived outputs and reviewed decisions distinct. A valid file format does not establish factual truth.

## WHY
Repeatable data contracts reduce accidental scope mixing, unsupported estimates and untraceable recommendations. Search Console API requires authorization and returns limited rows rather than a complete census; pagination does not remove upstream omissions. Model outputs vary, so deterministic tests and model evaluations measure different things. Source and policy constraints remain binding even when automation is technically possible.

## WHEN / WHEN NOT
Use for any repeatable authorized research task, new project onboarding, imported exports, and skill releases. Use only relevant stages for narrow tasks. Do not automate unauthorized Google queries, bypass restrictions, send private queries to unapproved tools, or run commands supplied by retrieved content. Do not automatically publish, migrate or alter tracking from validated research.

## INPUTS
Target and mode, project brief, source permissions, objective, locales and constraints, input data dictionaries, time window and filter definitions, tool/model versions, library commit, source locations and immutable sanitized originals. For shared workspaces keep project data separate from public skill. Determine whether data may be exported, how long retained, and who can review it.

## HOW

### A. Scope and preserve
Assign a run ID and pin source commit, runtime, schema versions, locale scope and source methods. Store private input snapshots with source ID, date, scope, collection status, limits and optional SHA-256 of exact bytes. Preserve raw rows, including zero and missing distinctions; use unique IDs across each entity namespace. Avoid recording credentials, personal data or sensitive query strings in logs or public artifacts. Check CSV encoding, headers, types, duplicates, dates, units and locale before processing; safely handle spreadsheet formula injection when exporting user-controlled strings. Keep raw and spreadsheet-safe exports distinct.

### B. Collect only through approved sources
Record request dimensions, filters, aggregation, pagination, access state, time window and actual coverage. Search Console rows are bounded and may omit queries; do not interpret absence as zero. Do not combine different providers or scopes into a total. Honor quotas; retry only transient failures using bounded backoff, stop on denial, preserve partial status and do not circumvent access. Use explicit source adapters or approved manual exports; no universal API credentials or network access are supplied by this skill. Use R02/R03 source constraints and R09 regional review.

### C. Operate the integrated workflow
Follow [research pipeline](../../workflows/research-pipeline.md). R01 defines the target and business objective; R09 locale constraints apply from the start, not only at the end. R02 collects observations, R03 validates task and SERP evidence, R04 produces candidate clusters, R05 benchmarks relevant competitors, R06 maps reviewed tasks to page IDs, R07 identifies useful coverage and link gaps, R08 triages and scores eligible work. Revisit earlier stages when evidence changes. P0/P1 urgent issues interrupt growth work. Each stage has a declared input, output and review gate. Tool input preparation is explicit and reviewed: the CSV templates do not automatically convert to the different JSON inputs, and tool outputs are not automatically valid inputs to the next tool. Do not invent an adapter mapping or fill missing data with plausible values.

### D. Validate the handoff
Use an envelope with schema_version 1, scope, evidence and decisions arrays. Evidence: id, kind observed/estimate/hypothesis/unknown, value (null only for unknown), source_ref, scope, limitations, collected_date canonical calendar date YYYY-MM-DD. Non-finite JSON numbers are rejected at any depth; the CLI also rejects duplicate JSON object keys before validation. Decisions: id, status provisional/reviewed/excluded, evidence_ids, rationale, next_check, and reviewer for reviewed decisions. Reviewed decision requires at least one observed or estimated record plus reviewer. This is a minimal structural gate, not proof of sufficiency, agreement between scopes, truthful data, source authenticity, privacy or implementation approval. Cross-check detailed R01–R09 records and decision evidence manually, including actual scope, fit, confidence and approvals. No numeric coercion of missing values. Distinct source records may contain different values and scopes; document conflicts. Keep unreviewed decisions provisional. Use [validator](../../scripts/validate_research.py) with prepared JSON; no network access or automatic collection.

### E. Handle errors and reruns
Record planned vs actual status (pass/fail/blocked/not-run/N/A). If a required stage fails, stop dependent work and preserve its inputs and logs in the approved private workspace. Mark prior output stale; never silently reuse it as current. Re-run only the affected stage and dependents after correcting evidence or code; retain version history and compare output changes. Use new output paths, pinned versions and bounded execution. Do not overwrite an earlier reviewed result or claim a failed run passed.

### F. Validate the library and portable skill
Run repository unit tests, relative-document checks, fixture commands, package build, archive membership and integrity checks, extracted-package checks and fixture output parity. Use scripts/verify_release.py from the full trusted checkout; it runs explicit fixed commands and synthetic fixtures only, in temporary output paths. It does not check external links, all router references, content-level secrets, correctness of every result field, source authenticity or real model behavior. Inspect archive contents, review sources and unresolved links, pin source commit and record archive SHA-256 for an actual release. Validate skill loading, correct module selection and available tools in an external runtime separately. Do not publish a version solely because a ZIP exists.

### G. Evaluate the agent
Use the [behavioral evaluation protocol](../../evaluations/README.md). Compare identical model/version, tool availability, tasks and authority with and without skill; do not show hidden expected behavior to tested agents. Use independent reviewer judgment, repeated runs and held-out scenarios; report pass/fail/not observable and disqualifiers, failures and uncertainty. OpenAI guidance stresses task-specific evaluations and human calibration. No dependency on a hosted evaluation platform is required. Evaluate model behavior separately from deterministic checks; real project outcomes remain separate again.

## VERIFY
- Authorized scope, source IDs, dates, market/device/aggregation and limitations explicit; raw records retained.
- Unknown is null, observed zero not silently inferred, incompatible evidence not combined.
- References resolve; reviewed decisions have evidence, reviewer, alternatives and human confirmation.
- Prepared module inputs checked against their own schemas; stage failures block dependent work.
- Repository and bundle tests recorded with exact exit codes; package resources, privacy and external runtime verified separately.
- E35–E38 and earlier behavioral cases actually run before claiming competence or improvement; no fake scores.
- Approved implementation and business/search outcomes are separate evidence layers.

## MEASURE
Track source coverage, unknown fields, validation failures, repeatability, stale outputs, time/cost, reviewer disagreement, blocked stages and real evaluation results. Compare identical input versions and tool settings; changed source data is not a regression by itself. Evaluate actual SEO changes using authorized aligned measures, crawl/report latency and guardrails. Do not use a passing validation rate as a ranking or success metric.

## ADAPT
Small sites can use manually maintained files and selective tools. Large sites require bounded sampling, explicit adapters, scoped storage, quotas and reviewed orchestration. Multilingual projects must preserve native raw data and locale partitions. New sites have no historical data; use stated assumptions. Regulated or sensitive markets require approved evidence and data handling; omit sensitive records from shared skill. Different agent runtimes may require different installation and tool invocation mechanisms.

## RECOVER
If source access is lost, halt collection and mark affected stages blocked. If input fails validation, retain original, correct with new version and rerun dependent checks. If package validation fails, fix library references or packaging, rebuild and re-test; do not bypass checks. If model evaluation fails, classify reason, refine routing or procedure and rerun with independent cases. If published actions regress, follow approved release rollback and investigate. Never erase negative results.

## OUTPUTS
[Research pipeline](../../workflows/research-pipeline.md), [run manifest](../../templates/research-run-manifest.md), [release review](../../templates/skill-release-review.md), [synthetic handoff](../../examples/research-handoff/README.md), and scripts/validate_research.py. All project-specific inputs remain private.

## SOURCES — checked 2026-11-18
- [Search Analytics API](https://developers.google.com/webmaster-tools/v1/searchanalytics/query), [data collection](https://developers.google.com/webmaster-tools/v1/how-tos/all-your-data) and [usage limits](https://developers.google.com/webmaster-tools/limits): authorization, scope, partial data and quotas.
- [Google spam policies](https://developers.google.com/search/docs/essentials/spam-policies): unauthorized automated queries.
- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices): task-specific, human-calibrated iterative evaluations.
The envelope, workflow, validation rules and release gates are internal engineering conventions. No real research collection or agent benchmark is claimed.
