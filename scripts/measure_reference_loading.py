#!/usr/bin/env python3
"""Trusted-checkout full-file byte estimates from authored route selections, not runtime traces."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ("skills/seo-engineering/SKILL.md",
         "skills/seo-engineering/references/execution-contract.md",
         "skills/seo-engineering/references/router.md")
MATERIAL = ("docs/01-foundations/operating-principles.md",
            "docs/01-foundations/evidence-and-decisions.md",
            "decision-engine/README.md")
INITIAL_TWO = {"ANALYTICS", "T10", "T11", "T12"}
HEADER = "| Task or trigger | ID | Reference candidates relative to L |"
RESOURCE = re.compile(r"^(?:docs|templates|decision-engine|workflows|implementation-patterns|evaluations|scripts)/[\w./-]+\.(?:md|py|csv|json)$")
MODES = {"learn", "research", "audit", "plan", "implement", "verify", "monitor", "out_of_scope"}


def read_routes(text):
    lines = text.split(HEADER, 1)[1].strip().splitlines()
    if lines[0] != "|---|---|---|":
        raise ValueError("invalid table header")
    routes = {}
    for line in lines[1:]:
        if not line.startswith("| "):
            break
        _, ident, raw = [part.strip() for part in line[1:-1].split("|")]
        refs = []
        for ref in raw.split("; "):
            if ref == "relevant evidence guides" and ident == "T12":
                continue
            if (not RESOURCE.fullmatch(ref) or ".." in ref.split("/") or
                    "." in ref.split("/")):
                raise ValueError("invalid reference")
            refs.append(ref)
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", ident) or ident in routes or not refs or len(refs) != len(set(refs)):
            raise ValueError("invalid route")
        if ident in INITIAL_TWO and len(refs) < 2:
            raise ValueError("missing initial workflow/privacy reference")
        routes[ident] = refs
    if not routes or not INITIAL_TWO <= routes.keys():
        raise ValueError("incomplete catalogue")
    return routes


def unique(paths):
    return list(dict.fromkeys(paths))


def plan(routes, mode, primary, dependencies):
    if mode not in MODES or not isinstance(primary,list) or not isinstance(dependencies,list):
        raise ValueError("invalid mode or selection")
    ids = primary + dependencies
    if any(not isinstance(i,str) or i not in routes for i in ids) or len(ids) != len(set(ids)):
        raise ValueError("unknown or duplicate route")
    if mode == "out_of_scope":
        if ids:
            raise ValueError("out-of-scope routes forbidden")
        return [], [], 0
    if not primary:
        raise ValueError("primary route required")
    if "MAINTAIN" in ids and (ids != ["MAINTAIN"] or mode != "implement"):
        raise ValueError("maintainer profile must be separate")
    common = list(ENTRY) + ([] if mode == "learn" else list(MATERIAL))
    initial, all_refs = common[:], common[:]
    for ident in ids:
        refs = routes[ident]
        if ident != "MAINTAIN" and any(p.startswith("evaluations/") for p in refs):
            raise ValueError("evaluation reference in target route")
        initial.extend(refs[:2 if ident in INITIAL_TWO else 1])
        all_refs.extend(refs)
    return unique(initial), unique(all_refs), (48 if len(ids) == 1 else 80) * 1024


def file_bytes(root, refs):
    """No target or arbitrary external files; trusted library paths only."""
    result = 0
    for ref in unique(refs):
        if ref not in ENTRY and ref not in MATERIAL and (
                not RESOURCE.fullmatch(ref) or ".." in ref.split("/") or "." in ref.split("/")):
            raise ValueError("invalid library path")
        p = root / ref
        if not p.is_file() or p.is_symlink() or not p.resolve().is_relative_to(root.resolve()):
            raise ValueError("missing or unsafe reference")
        result += p.stat().st_size
    return result


def profile(root, cases):
    routes = read_routes((root / ENTRY[-1]).read_text(encoding="utf-8"))
    rows = []
    for c in cases:
        initial, all_refs, budget = plan(routes, c["mode"], c["primary"], c["dependencies"])
        a, b = file_bytes(root, initial), file_bytes(root, all_refs)
        rows.append({"id": c["id"], "mode": c["mode"],
                     "initial_refs": initial, "all_listed_refs": all_refs,
                     "initial_bytes": a, "all_listed_bytes": b,
                     "soft_budget_bytes": budget, "budget_exceeded": a > budget,
                     "operator_only": "MAINTAIN" in c["primary"]})
    target = [r for r in rows if not r["operator_only"] and r["mode"] != "out_of_scope"]
    return {"metric": "unique_full_file_bytes", "route_count": len(routes),
            "cases": rows,
            "target_case_count": len(target),
            "target_initial_bytes_sum": sum(r["initial_bytes"] for r in target),
            "target_all_listed_bytes_sum": sum(r["all_listed_bytes"] for r in target),
            "actual_runtime_measured": False,
            "limitations": "Authored initial selection only; all-listed same-route comparator, not old behavior. Excludes later dependencies, source retrieval, target data and runtime overhead. Soft budget is not a gate; safety/evidence take priority."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="New report file")
    args = parser.parse_args()
    try:
        record = json.loads((ROOT / "operations/ts07-routing-cases.json").read_text(encoding="utf-8"))
        result = profile(ROOT, record["cases"])
        with args.out.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2)
            handle.write("\n")
    except (OSError, ValueError, KeyError, TypeError, IndexError):
        print("Unable to measure trusted reference profile; no runtime claim.")
        return 1
    print("Static byte profile written; no actual runtime measured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
