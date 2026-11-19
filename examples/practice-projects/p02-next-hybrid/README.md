# P02 — Next.js hybrid catalogue (fictional)

Offline educational exercise for a fictional furniture catalogue. The reserved host catalogue.example is never contacted. Declared Next.js 16 App Router and Cache Components are hypotheses in native inputs, not installed dependencies, a real build, configuration or actual delivery. No product offers, real stock, real prices, customer data, traffic or provider measurements. All source/render, HTTP, search and performance observations are hand-authored; no browser, server, cache invalidation or network execution.

## Brief and identity

Objective: preserve useful distinct catalogue/product URLs and align delivery, content revision, metadata and performance; protect account access. Audit/plan only. No framework migration, actual deployment, new tracking or external submissions. See [registry](registry.json).

| ID | Intended route | Planned use |
|---|---|---|
| home | / | Static public landing |
| catalogue | /chairs/ | Revalidated catalogue, runtime paths needed |
| product | /chairs/arc/ | Hybrid public product content |
| account | /account/ | Protected runtime |
| missing | /chairs/unknown/ | Missing, expected 404 |

Both revisions use the same route identities. T01/T04 cover five routes; T06/T08 cover three intended public pages, including uncollected catalogue records. T09 uses explicit registry performance crosswalk: origin p75 has no route ID; the two lab records refer to named URLs via this reviewed map. T04 delivery is a per-route planning declaration, not proof a single app can mix export/runtime deploy modes; initial catalogue export plan is incompatible with its requirements. Plan for a coherent runtime deployment or separately justify a distinct static deployment. Do not infer actual host architecture from the example.

## Initial and revised hypothetical timeline

P02-A (October 3): product target arc-content-2 due 10:05 UTC. Mock old product revision at 10:04 before deadline and 10:07 after deadline; title and canonical still incorrect relative to current reviewed plan. Static-export proposal for catalogue conflicts with ISR/runtime path needs; no catalogue capture. P02-B (October 4): a new reviewed candidate deadline 10:05 UTC, target mock revision observed 10:07, metadata/canonical literals corrected. This does not erase the previous deadline miss or establish when deployment changed. Catalogue proposed runtime, old-context sample is not comparable. Account has no capture; mock 404 observation is not actual HTTP. Product's search record predates both changes. Source and render values are same-context hypothetical records, not proof of actual rendered behavior. Home is a healthy supplied public observation, not real acceptance.

## Performance tradeoff

The B input adds an explicitly fictional A-to-B lab comparison. Three matched mobile cold runs per arm: product LCP 2100/2200/2300 versus 2500/2600/2700 ms; median rises 2200 to 2600, 400 ms beyond baseline and exceeds the reviewed 100 ms tolerance. Catalogue has one mismatched candidate profile; no comparable delta may be claimed. The same origin mobile p75 record (LCP 3100, INP unknown, CLS .08) predates both candidate deadlines; it cannot be substituted for product URL field evidence or used to claim field improvement. No causal inference or actual performance measurement.

## Run

From library root, set OUT to a new existing private output directory. Commands do not execute Next.js or contact any host.

~~~sh
LAB=examples/practice-projects/p02-next-hybrid
python3 scripts/audit_technical.py --input "$LAB/p02-a/technical.json" --output "$OUT/p02-a-technical.json"
python3 scripts/audit_technical.py --input "$LAB/p02-b/technical.json" --output "$OUT/p02-b-technical.json"
python3 scripts/review_release_gates.py --input "$LAB/p02-a/gates.json" --output "$OUT/p02-a-gates.json"
python3 scripts/review_release_gates.py --input "$LAB/p02-b/gates.json" --output "$OUT/p02-b-gates.json"
~~~

Expected all four exit 0 (reports processed, not verified target). T10 five processed, two blocked (T02/T05 unavailable independent evidence), two not applicable (T03/T07), zero failed, no grouping. T11 all actual candidate assertions missing, hold both; no mock data converted into an actual passing gate. Retain A's native findings even after B changes.

| Native check | Expected A | Expected B |
|---|---|---|
| T04 catalogue | Export strategy/features conflict | Plan conflict absent; old context deferred |
| T04 product | Before-deadline difference and after-deadline review | Target observed at sampled time |
| T06 product | Declaration differs from preference, stale processed sample | Current mock canonical matches, processed still stale |
| T08 product | Title/canonical and share discrepancies | No literal review findings; no product markup eligibility assessment |
| T09 product | No lab comparison | Regression review, +400 ms |
| T09 catalogue | No lab comparison | Deferred; mismatched profile |
| T11 | Hold | Hold |

These are expected outcomes of the actual offline tools on invented inputs. No automatic acceptance, ranking forecasts, field improvement or cache root-cause inference. T08 uses metadata-only profile (article null); product schema/eligibility is not assessed.

## Decisions

D1 reject incompatible export plan, inspect actual deployment capability then choose appropriate runtime or justified independent static plan. D2 diagnose revision freshness using current context, timestamps and cache/deployment evidence; do not purge globally or infer a particular cache layer. D3 align metadata to verified visible facts; no redirect to catalogue because stale canonical is not equivalence evidence. D4 hold performance decision pending matched real runs and review tradeoffs; hypothetical lab regression remains visible. D5 verify actual account authorization and data access independently. D6 require actual browser/source, runtime and search evidence before claiming deployment or index progress. Proposed application owner for D1–D3, performance QA for D4, security owner for D5, search owner for D6. No actual assignments. Consider scoped rollback of delivery changes if real acceptance fails, with independently reviewed content freshness and security consequences. Keep existing useful URLs.

Use [T04](../../../docs/03-technical/t04-nextjs-hybrid.md), [T09](../../../docs/03-technical/t09-performance.md), [T11](../../deployment-regression/README.md) and [cross-module review](../../../decision-engine/cross-module-review.md). The scenario is educational, not model evaluation or actual implementation.
