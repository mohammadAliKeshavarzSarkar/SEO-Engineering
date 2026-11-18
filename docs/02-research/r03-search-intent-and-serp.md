# R03 — Search intent and SERP intelligence

Status: initial agent-ready methodology; behavioral evaluation pending. Source verification: 2026-11-18.

## WHAT — Model the user's task, not just the query

A search query is an expression of a task, possibly ambiguous. A search engine results page (SERP) is evidence of how a search system responds in a particular context. Neither is direct access to a person's internal motivation. Treat inferred intent as a hypothesis that may be supported by observed results, existing page/query data and customer evidence.

Use this internal taxonomy, not an asserted official Google classification or ranking factor:

| Task label | User goal | Candidate page format |
|---|---|---|
| Learn | Understand a concept or answer | Guide, definition, reference |
| Do | Complete a task or use a tool | How-to, calculator, interactive tool, support documentation |
| Compare | Evaluate options or choose | Evidence-based comparison, buying guide, use-case page |
| Transact | Buy, book, request, subscribe | Category, product, service, demo page |
| Navigate | Reach a known entity or destination | Brand, login, specific product or contact page |
| Local/visit | Find a real place or service in an area | Eligible location/service page, accurate local listing |

Intent can be mixed; local, freshness, language, audience, device and media preference can cut across these labels. Record one dominant and optional secondary task only if supported, otherwise mixed or unknown. Do not confuse task with content format, page type, funnel stage or result feature. A comparison article may support an eventual transaction; a navigational query may target a support page, not the homepage.

## WHY

Google describes interpreting query meaning and contextual factors such as language, location and freshness, and changing presentation according to the query. Result types can differ even when wording stays the same. Align pages to useful user tasks; use SERP observations as evidence of plausible formats and gaps, not proof of a hidden ranking formula or causal factor. Provide original value beyond copying existing results. See sources below.

## WHEN / WHEN NOT

Use after R01/R02 seed discovery; before assigning intent to URLs, drafting a new page, merging content, reviewing traffic shifts or deciding whether an observed keyword is valuable. For a narrow metadata repair with already-established page purpose, do not mandate extensive research. Do not target unrelated high-volume queries, unsupported services, unsafe claims, or replicate a competitor merely because it ranks. Do not migrate or publish from R03 alone.

## INPUTS

- Project offering, audience, target market/language, authority and constraints from R01.
- Raw query IDs and observations from R02; retain original spelling.
- Current URL inventory, page purpose, indexability and business outcome where available.
- Permissioned sources: manual results observation, user-provided captures, approved search/data tools, first-party Search Console/Bing exports, actual page reads and customer evidence.
- Access limitations, collection scope, device, engine, search surface and timestamps; capture observed settings separately from requested settings.

## HOW — Collection and interpretation protocol

### 1. Frame the task hypothesis

For each representative query, write the task in plain language: who might want to do what, with which constraints? Record plausible alternate meanings. Modifiers such as price, near me, vs, how, brand and year are clues, not definitive labels. Broad category phrases often contain several tasks; explicit wording can still be ambiguous.

### 2. Collect comparable snapshots

Choose target engine, market, language, device, surface (web/images/video/etc.) and intended context. Observe actual settings/location where available; note personalization state, which cannot eliminate all context effects. Use stable sample window and record capture date/time with timezone, source, tool/method, sample size, completeness and known limitations. Use top ten comparable organic results as a small default sampling convention, not a universal rule; fewer if unavailable. Repeat selected ambiguous or consequential queries in independently captured snapshots or inspect appropriate variants. Record only actual results and their observed positions when the source supports them.

Google's spam policy prohibits unauthorized automated queries including rank scraping. Do not build an unauthorized scraper or evade rate limits/access controls. Use tools and data with appropriate permission and terms; manual observation or approved exports are acceptable where allowed. Generic AI/web search retrieval is discovery, not an exact Google/Bing localized SERP. For a partial result feed, record what it provides, leave exact rank, features and observed market unknown unless supplied, and downgrade confidence. If no reliable search interface is available, request a sanitized authorized snapshot or perform provisional task analysis; do not fabricate.

### 3. Separate features, results and pages

Record each actual unit with snapshot ID, evidence locator and type. Ads/sponsored results, map/local listings, shopping units, AI answer/citations, featured snippets, videos, images, text results and question/exploration blocks may coexist. Preserve feature context and uncertainty. Do not count ads or every child link in a carousel/AI answer as separate conventional organic positions. Distinguish displayed order, comparable organic ordinal (only when supported by capture), and Search Console average position. Keep feature-only rows separate; absence from a partial source does not prove absence in search. Do not infer competitor traffic or click share from result counts.

Inspect a representative set of landing pages, not only snippets. Record access failure honestly. Classify page type (home, category, product, service, guide, comparison, tool, support, local page, forum etc.), primary task fulfilled, format, specific evidence, trust, freshness and UX fit. Note observed competing domains and URLs; business competitors and SERP competitors differ. Never copy their content or assume ranking proves every claim on the page. Use descriptive first-hand observations, source links and dates.

### 4. Synthesize intent and confidence

For each snapshot, tally comparable observed results by page type and inferred primary task; track unclassified results separately. Report counts and denominator, e.g. 7/10 observed comparable organic results are categories, not '70% of searchers want categories'. Do not aggregate mismatched location/device/engine/date scopes as one population. Features and page observations add qualitative clues. This is an internal sampling method, not a Google score.

Confidence rubric:
- High: multiple relevant comparable observations, page inspections and clear task alignment; alternate interpretations and site context considered.
- Medium: relevant but limited observations, some ambiguity or unverified page types.
- Low: incomplete generic feeds, inconsistent contexts, only wording/snippets or missing market evidence.
- Unknown: insufficient evidence to classify.
These labels are qualitative, not calibrated probabilities. Use mixed if multiple materially different tasks remain plausible; do not force a winner from a narrow plurality. Separate confidence in task from confidence in proposed URL ownership. A high-confidence intent can be out of scope for the business. Repeat important unstable observations and document discrepancies.

### 5. Choose the next page decision

Use the [intent decision protocol](../../decision-engine/search-intent.md). Inspect existing page inventory and available query/page reports first. Prefer keeping or improving an adequate existing page. Propose a new page only for independently useful unmet tasks aligned with real offerings and proof. If tasks coexist, consider a well-structured page with supporting sections and links versus distinct pages serving different tasks. Do not consolidate pages merely because both receive impressions for one query. Gather stronger evidence in R04/R06 for clustering and ownership. Mark no-change, investigate, out-of-scope, improve, propose-new, proposed-consolidation as separate outcomes. All changes require scope approval and later QA.

### 6. Handoff

Store raw snapshots separately from interpretations. Preserve primary/secondary label, result counts, alternative meanings, confidence, format candidates, existing URLs and recommended next evidence. Link decision IDs and scope. No private data in the library. Do not create a page, change a URL or publish content as a side effect of intent classification.

## VERIFY

- Every observed result points to a snapshot and source, with raw query and actual capture context; requested versus observed market distinguished.
- Numeric ranks exist only for sources supporting the stated position basis; no rank inferred from generic retrieval.
- Intent counts reconcile with the comparable sample including unknown classifications; sponsored/feature children do not inflate the denominator.
- Interpretations point to actual page evidence and alternative meanings; no fabricated audience shares, search volumes or guarantees.
- Existing owner and overlapping URLs reviewed or explicitly unavailable; proposed new pages have distinct user value and plausible fit.
- Missing locale, tools, first-party data or permission marks relevant checks blocked/unknown; do not sign off a final decision from insufficient evidence.
- Navigation and data contracts validated; use E09–E11 in the evaluation suite. Publishing cases is not equivalent to executing them.

## MEASURE

After approved implementation, compare relevant query/page groups using aligned Search Console/Bing scope and dates, impressions, clicks and CTR (with denominator), average position cautiously, task outcomes and qualified conversions where available. Sample current SERP context again where relevant; distinguish changes in result mix, demand, search appearance and tracking. Do not equate Search Console average position with a single snapshot rank, and do not attribute change to page format alone from uncontrolled before/after data. Set review window after baseline and likely recrawl/reporting lag; no universal days-to-rank or CTR target.

## ADAPT

| Context | Adaptation |
|---|---|
| Ecommerce | Distinguish category exploration, specific product, compatibility, comparison and stock; prioritize existing taxonomy |
| B2B and SaaS | Distinguish business problems, solution evaluation, integrations and support; consider low-volume qualified intent |
| Local services | Verify actual service area and eligible presence; no fictitious locations |
| Publishers/regulated subjects | Identify freshness, evidence needs and expert review; traffic alone insufficient |
| Multilingual/Persian | Preserve raw variants, evaluate market/language separately, do not treat translated or foreign snapshots as local rankings |
| No first-party data | Record limitation; use available permitted observed evidence and conditional mapping |
| AI/search features | Track observed features/citations separately; no special schema or guaranteed AI citation assumed |

## RECOVER

If collection scopes conflict, split snapshots or recollect rather than average. If results are partial, label unknown features and rank; request permitted evidence or defer high-risk decision. If classifier disagrees with page inspection, reopen actual pages and preserve uncertainty. If post-release measured outcomes fall, diagnose technical/indexing, query mix and tracking before undoing intent-based edits; use release rollback and do not mass-delete. If a collection method violates provider policy or authorization, stop and use lawful alternatives. Inaccurate past observations should be corrected with version history, not silently overwritten.

## OUTPUTS

[Snapshot template](../../templates/serp-snapshots.csv), [result observations v2](../../templates/serp-results-v2.csv), [intent assessments](../../templates/intent-assessments.csv), [decision protocol](../../decision-engine/search-intent.md), [worked synthetic example](../../examples/serp-intent/README.md), [evaluation cases](../../evaluations/cases.json). The legacy serp-observations.csv remains supported as a simpler historical form; new detailed records use the v2 schemas. Follow R04 for clustering and R06 for final page mapping.

## SOURCES — checked 2026-11-18

- [Google ranking results and query meaning](https://www.google.com/intl/en_us/search/howsearchworks/how-search-works/ranking-results/): context, meaning, freshness.
- [Why results differ](https://support.google.com/websearch/answer/12412910): time, location, language, device, personalization.
- [Language of results](https://support.google.com/websearch/answer/13511324): query language is not the only language signal.
- [Google visual elements gallery](https://developers.google.com/search/docs/appearance/visual-elements-gallery): result and feature categories.
- [Search Console impressions, clicks and position](https://support.google.com/webmasters/answer/7042828): compound result elements and aggregate position semantics.
- [Search Console common tasks](https://support.google.com/webmasters/answer/17010961): query-to-page inspection and trends.
- [Google spam policies](https://developers.google.com/search/docs/essentials/spam-policies): machine-generated traffic and scaled content abuse.
- [People-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content): original, useful content and audience fit.
- [AI features](https://developers.google.com/search/docs/appearance/ai-features): existing search foundations and eligibility.

Task labels, ten-result sample convention, confidence rubric and decision gates are internal methodology, not search-engine requirements. Recheck source and feature eligibility before implementing. No actual client SERPs or rankings have been collected in this module.
