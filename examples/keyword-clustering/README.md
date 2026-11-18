# R04 synthetic worked example
All inputs are fictional, not measured Google data. The input file contains three same-scope, same-task records deliberately creating a bridge. A and B share five URLs (union eight, J=0.625); B and C likewise; A and C share two (union eight, J=0.25). At threshold 0.5 the greedy candidate output is [a,b], [c]. B could instead be reviewed with C; the algorithm does not resolve that ambiguity. A candidate is not authorization to create or merge pages.

From repository root:
```sh
python3 scripts/cluster_keywords.py --input examples/keyword-clustering/input.json --output candidate-report.json
```
The output file must not already exist. Review the pairs and source provenance; no network access occurs.

Persian example: كفش ورزشي and کفش ورزشی may have the same match key in the Persian normalization policy. خرید کفش ورزشی and تعمیر کفش ورزشی retain different modifiers. No comparable snapshots means no automatic group even for exact match keys.

See [R04](../../docs/02-research/r04-keyword-normalization-and-clustering.md) and [review protocol](../../decision-engine/keyword-clustering.md).
