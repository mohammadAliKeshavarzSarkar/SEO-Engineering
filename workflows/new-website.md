# New website onboarding and SEO workflow

For connected R01–R10 research stages, use the [integrated research pipeline](research-pipeline.md); select appropriate stages and retain evidence separately from decisions.

## Applicability

Use for a new or unfamiliar target website, including already-live sites. For a narrow task, select only relevant stages. Requires explicit target and permission; no blanket access across accounts.

| Stage | Action | Exit gate / artifact |
|---|---|---|
| 0 Scope | Identify actual website, owner, target repo/origin, mode, exclusions, release/control boundaries | Project brief and authority; stop unauthorized writes |
| 1 Discover | Understand site type, business model, audience, market, language, product proof, conversion | R01 audience/problem map; hypotheses labeled |
| 2 Baseline | Use [T01 architecture detection](../docs/03-technical/t01-architecture-detection.md); inspect scoped site templates, URL inventory, statuses, source/rendered HTML, index and tracking availability | Evidence-backed current-state inventory, severity, unknowns |
| 3 Research | Collect actual search observations (R02), intent/competitors and page gaps | Provenance-aware corpus, proposed query-to-page mapping |
| 4 Decide | Classify rules vs recommendations vs policy vs experiments; choose smallest suitable action | Prioritized decision records with evidence, owners and tests |
| 5 Implement | Approved work only; preserve valid URLs, unrelated UI/features, privacy | Reviewable changes, backups/rollback for risky changes |
| 6 Verify | Offline, browser, deployed HTTP, platform inspection and analytics checks as feasible | Actual results, blocked/not-run separately, release gates |
| 7 Measure | Baseline, outcomes, cohort, timeframe, uncertainty, alert owner | Dated report; do not imply ranking from eligibility |
| 8 Learn | Identify reusable lesson, generalize away target identity, propose update and eval | Reviewed skill change or private project note |

Security or broad indexing failures should be handled first; measurement planning starts at baseline. No final keyword or architecture decision until supporting evidence is sufficient. No forced replatforming or blanket new pages. For greenfield sites, record not-yet-available production metrics and design testable contracts rather than inventing baseline. For migrations, inventory existing URLs and redirects before changing them. For ecommerce, localized, local or regulated content, load specialty and privacy references.

Artifacts: [brief](../templates/project-brief.md), [audience map](../templates/audience-problem-map.csv), [URL inventory](../templates/url-inventory.csv), [keyword observations](../templates/keyword-observations.csv), [decision](../templates/decision-record.md), [run record](../templates/agent-run-record.md), [release checklist](../templates/release-checklist.md). Keep private data out of shared skill and reviewable public commits.
