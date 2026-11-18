# SEO Engineering

A reusable, evidence-led SEO engineering system for developers, product teams, content strategists and AI coding agents. Optimize for discoverability, usefulness, performance and measurable business outcomes — not ranking tricks.

**Version:** 0.2.0-rc.1 · **Status:** source release candidate — stable release and independent behavioral validation pending · **Research checkpoint:** 2026-11-18

## Release candidate

See [0.2.0-rc.1 candidate notes](docs/01-foundations/release-candidate.md) and [version metadata](docs/01-foundations/distribution-version.json). This is a source candidate, not a stable release or public binary distribution. Pin the exact candidate commit, verify the archive, and complete the remaining review gates before sharing. No license is assigned.

## For AI agents and new websites

This repository is a reusable **SEO engineering skill system**, not a single website strategy. Use [the master skill](skills/seo-engineering/SKILL.md), [agent architecture](docs/01-foundations/agent-architecture.md), [new website workflow](workflows/new-website.md), [decision protocols](decision-engine/README.md) and [evaluation suite](evaluations/README.md). Only load the relevant references for the task.

To use the entire knowledge base away from this repository, follow [portable skill packaging](docs/01-foundations/skill-installation.md). A skill supplies instructions and resources; it does not train or grant tools to a model, guarantee rankings, or replace project-specific research.

## Start here

1. Read [operating principles](docs/01-foundations/operating-principles.md) and [evidence and decisions](docs/01-foundations/evidence-and-decisions.md).
2. Copy the [project brief](templates/project-brief.md), [URL inventory](templates/url-inventory.csv) and [decision record](templates/decision-record.md) into a project-specific workspace.
3. Establish a baseline and follow the [implementation workflow](docs/06-operations/audit-and-release.md). Fix critical eligibility and measurement defects before growth experiments.
4. Use the [AI-agent skill](skills/seo-engineering/SKILL.md) and [agent instructions](AGENTS.md) when working in a coding agent. The skill is a portable Markdown definition; install it according to the agent's own supported mechanism.
5. Run `python3 scripts/check_docs.py` and `python3 -m unittest discover -s tests` from the repository root. No external packages required.

For integrated research use the [R01–R10 pipeline](workflows/research-pipeline.md). Run `python3 scripts/verify_release.py` from a trusted checkout for repository and portable-package checks; review the [release gates](templates/skill-release-review.md) separately.

See the [stabilization roadmap and S01 audit](docs/08-learning/stabilization.md) for actual verification status and outstanding release gates.

For portable use, see the [installation guide](docs/01-foundations/skill-installation.md) and [portable acceptance procedure](docs/01-foundations/portable-skill-acceptance.md). Build from a reviewed checkout; validate the archive against that source and record its checksum. Candidate status is not a release or measured agent competence.

## Documentation map

| Module | Guide |
|---|---|
| Agent operations | [Documentation standard](docs/01-foundations/module-standard.md), [implementation patterns](implementation-patterns/README.md), [run record](templates/agent-run-record.md) |
| Foundations | [Principles](docs/01-foundations/operating-principles.md), [Evidence & decisions](docs/01-foundations/evidence-and-decisions.md) |
| Research | [Strategy, intent & competitors](docs/02-research/market-and-keywords.md), [Persian & multilingual research](docs/02-research/persian-and-international.md) |
| Technical | [Crawl & index](docs/03-technical/crawl-and-index.md), [Rendering & architecture](docs/03-technical/rendering-and-architecture.md), [URLs & migrations](docs/03-technical/urls-and-migrations.md), [Performance & accessibility](docs/03-technical/performance.md) |
| Content | [On-page & editorial](docs/04-content/on-page-and-editorial.md), [Entities & schema](docs/04-content/structured-data.md), [Images & video](docs/04-content/media.md), [Authority & distribution](docs/04-content/authority.md) |
| Measurement | [Search Console & Bing](docs/05-measurement/search-platforms.md), [GA4 & Clarity](docs/05-measurement/analytics.md), [Privacy & measurement QA](docs/05-measurement/privacy-and-qa.md) |
| Operations | [Audit & release](docs/06-operations/audit-and-release.md), [Troubleshooting](docs/06-operations/troubleshooting.md), [Experiments & monitoring](docs/06-operations/experiments.md) |
| Specialties | [Local, commerce, SaaS & programmatic](docs/07-specialties/site-types.md), [AI search](docs/07-specialties/ai-search.md) |
| Learning | [Competency roadmap](docs/08-learning/competencies.md), [Source register](docs/08-learning/sources.md) |
| Projects | [BeatFit example scope](projects/beatfit/README.md), [New project template](templates/project-brief.md) |
| Governance | [Contributing](CONTRIBUTING.md), [Changelog](CHANGELOG.md), [Decisions](decisions/README.md) |

## Tools

`python3 scripts/audit_html.py --manifest examples/routes.json --root examples/site` checks local static output against declared route expectations. It is not a crawler, browser rendering engine, HTTP probe or indexing test. See [tools documentation](scripts/README.md). A failing sample is documented there.

## Scope and safety

This repository contains universal guidance and a sanitized project scope. Keep customer data, unpublished audits, source-code findings, credentials, raw logs and private analytics outside Git (or in a separate private repository). `private/` is ignored. Never use `git add -f` for private data. Check the staged diff before pushing. No license has been assigned; the repository owner should choose one before granting reuse rights.

This is a maintained initial edition, not an assertion that every platform policy has been independently verified or that any project has been implemented. Revalidate platform guidance and applicability before release.
