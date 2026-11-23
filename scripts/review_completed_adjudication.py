#!/usr/bin/env python3
"""Validate two blinded completed-run reviews against adjudicated grades.

Private maintainer-side structural check only. No actual reviewer identity,
independence, trace semantics, safety or release authorization is verified.
"""
import argparse
import json
from pathlib import Path

if __package__:
    from .control_benchmark import ensure, exact, fingerprint
    from .prepare_trial import compare_reviewers
    from .score_benchmark import load, nonempty, grade_items, EXPECTED, DISQUALIFIERS
else:
    from control_benchmark import ensure, exact, fingerprint
    from prepare_trial import compare_reviewers
    from score_benchmark import load, nonempty, grade_items, EXPECTED, DISQUALIFIERS

TYPES = {"expected": EXPECTED, "disqualifiers": DISQUALIFIERS}


def indexed(packet, grades):
    """Validate each submitted private grade against the exact blind packet."""
    exact(grades, {"packet_sha256", "records"})
    ensure(grades["packet_sha256"] == fingerprint(packet), "review packet mismatch")
    ensure(isinstance(packet, dict) and packet.get("schema_version") == "1" and
           isinstance(packet.get("records"), list), "invalid blind packet")
    available = {r["blind_id"]: r for r in packet["records"]}
    ensure(len(available) == len(packet["records"]), "duplicate blind packet slot")
    ensure(isinstance(grades["records"], list), "invalid grade records")
    result = {}
    for row in grades["records"]:
        exact(row, {"blind_id", "reviewer", "output_sha256", "trace_sha256",
                    "expected", "disqualifiers"})
        ident = row["blind_id"]
        ensure(isinstance(ident, str) and ident in available and ident not in result,
               "unknown or duplicate grade slot")
        expected = available[ident]
        ensure(nonempty(row["reviewer"]) and
               row["output_sha256"] == expected["output_sha256"] and
               row["trace_sha256"] == expected["trace_sha256"],
               "review artifact mismatch")
        normalized = {}
        for kind, allowed in TYPES.items():
            items = row[kind]
            ensure(isinstance(items, list) and
                   all(isinstance(item, dict) and
                       set(item) == {"criterion", "status", "evidence"} for item in items),
                   "invalid criterion fields")
            grade_items(items, len(expected[kind]), allowed)
            normalized[kind] = {item["criterion"]: item["status"] for item in items}
        result[ident] = {"reviewer": row["reviewer"], "statuses": normalized}
    return result


def assess(packet, first, second, adjudicated, resolutions=None):
    """Keep original negative signals visible despite subsequent adjudication."""
    # Existing comparison catches reused reviewer identifiers on overlapping
    # slots, and validates both source reviews against the same packet.
    agreement = compare_reviewers(packet, first, second)
    a, b, final = (indexed(packet, p) for p in (first, second, adjudicated))
    available = {r["blind_id"] for r in packet["records"]}
    overlap = set(a) & set(b)
    disputes = {}
    observed = []
    unobservable = []
    for source, index in (("first", a), ("second", b)):
        for ident, row in index.items():
            for criterion, status in row["statuses"]["disqualifiers"].items():
                if status == "observed":
                    observed.append({"blind_id": ident, "criterion": criterion,
                                     "review": source})
            for kind, items in row["statuses"].items():
                for criterion, status in items.items():
                    if status == "not_observable":
                        unobservable.append({"blind_id": ident, "kind": kind,
                                             "criterion": criterion, "review": source})
    for ident in sorted(overlap):
        for kind in TYPES:
            for criterion, first_status in a[ident]["statuses"][kind].items():
                second_status = b[ident]["statuses"][kind][criterion]
                key = (ident, kind, criterion)
                if first_status != second_status:
                    disputes[key] = {"blind_id": ident, "kind": kind,
                                     "criterion": criterion,
                                     "first": first_status, "second": second_status}
                elif ident in final:
                    ensure(final[ident]["statuses"][kind][criterion] == first_status,
                           "adjudication changes reviewer consensus")

    resolved = set()
    if resolutions is not None:
        exact(resolutions, {"packet_sha256", "first_sha256", "second_sha256",
                            "adjudicated_sha256", "records"})
        ensure(resolutions["packet_sha256"] == fingerprint(packet) and
               resolutions["first_sha256"] == fingerprint(first) and
               resolutions["second_sha256"] == fingerprint(second) and
               resolutions["adjudicated_sha256"] == fingerprint(adjudicated),
               "adjudication resolution source mismatch")
        ensure(isinstance(resolutions["records"], list), "invalid resolution records")
        for row in resolutions["records"]:
            exact(row, {"blind_id", "kind", "criterion", "selected_status",
                        "adjudicator", "rationale"})
            ensure(isinstance(row["blind_id"], str) and
                   isinstance(row["kind"], str) and type(row["criterion"]) is int,
                   "invalid resolution key")
            key = (row["blind_id"], row["kind"], row["criterion"])
            ensure(key in disputes and key not in resolved and key[0] in final,
                   "resolution is not a unique graded disagreement")
            ensure(row["selected_status"] == final[key[0]]["statuses"][key[1]][key[2]],
                   "resolution differs from adjudicated grade")
            ensure(nonempty(row["adjudicator"]) and
                   row["adjudicator"] not in (a[key[0]]["reviewer"], b[key[0]]["reviewer"])
                   and nonempty(row["rationale"]),
                   "independent adjudicator label and rationale required")
            resolved.add(key)

    unresolved = [disputes[key] for key in sorted(disputes.keys() - resolved)]
    missing_first = sorted(available - set(a))
    missing_second = sorted(available - set(b))
    missing_final = sorted(available - set(final))
    unpaired_final = sorted(set(final) - overlap)
    reasons = []
    if missing_first or missing_second:
        reasons.append("original_reviewer_coverage_incomplete")
    if missing_final:
        reasons.append("adjudicated_grades_incomplete")
    if unpaired_final:
        reasons.append("adjudicated_slots_without_two_reviewers")
    if unresolved:
        reasons.append("disagreements_unresolved")
    if unobservable:
        reasons.append("original_review_unobservable")
    status = ("escalate_to_owner" if observed else
              "hold_missing_or_unresolved_review" if reasons else
              "ready_for_independent_review")
    return {"schema_version": "1", "record_kind": "completed_adjudication_integrity",
            "packet_sha256": fingerprint(packet),
            "first_sha256": fingerprint(first),
            "second_sha256": fingerprint(second),
            "adjudicated_sha256": fingerprint(adjudicated),
            "resolutions_sha256": fingerprint(resolutions) if resolutions is not None else None,
            "planned_completed_slots": len(available),
            "first_review_slots": len(a), "second_review_slots": len(b),
            "adjudicated_slots": len(final),
            "agreement_rate": agreement["agreement_rate"],
            "criteria_compared": agreement["criteria_compared"],
            "disagreements": [disputes[key] for key in sorted(disputes)],
            "resolved_disagreements": len(resolved),
            "unresolved_disagreements": unresolved,
            "missing_first_review_slots": missing_first,
            "missing_second_review_slots": missing_second,
            "missing_adjudicated_slots": missing_final,
            "unpaired_adjudicated_slots": unpaired_final,
            "original_observed_disqualifier_signals": observed,
            "original_unobservable_criteria": unobservable,
            "hold_reasons": sorted(set(reasons)),
            "status": status,
            "reviewer_independence_verified": False,
            "adjudicator_independence_verified": False,
            "actual_execution_verified": False,
            "safety_certified": False,
            "release_approved": False,
            "limitations": "Local declared grades and identifiers only. Original adverse signals persist even if adjudicated differently; independent human identity, trace meaning, provenance and approval remain unverified."}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for field in ("packet", "first", "second", "adjudicated", "out"):
        ap.add_argument("--" + field, type=Path, required=True)
    ap.add_argument("--resolutions", type=Path)
    args = ap.parse_args()
    try:
        result = assess(load(args.packet), load(args.first), load(args.second),
                        load(args.adjudicated),
                        load(args.resolutions) if args.resolutions else None)
        with args.out.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write("\n")
    except (OSError, ValueError, TypeError, KeyError, AttributeError, UnicodeError) as exc:
        print("Completed adjudication review failed:", exc)
        return 1
    print("Adjudication integrity checked; human independence NOT certified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
