#!/usr/bin/env python3
"""Sidecar review for noncompleted benchmark slots; no inference, scoring or approval."""
import argparse
import json
from pathlib import Path

if __package__:
    from .control_benchmark import check_schedule, ledger_index, exact, ensure, fingerprint, cases_index
    from .prepare_trial import check_artifacts
    from .score_benchmark import load, nonempty
else:
    from control_benchmark import check_schedule, ledger_index, exact, ensure, fingerprint, cases_index
    from prepare_trial import check_artifacts
    from score_benchmark import load, nonempty

STATES = {"observed", "no_signal_in_available_evidence", "not_observable"}


def packet(suite, control, ledger, root):
    check_schedule(suite, control)
    checked = check_artifacts(control, ledger, root)
    rows = ledger_index(control, ledger)
    slots = {s["blind_id"]: s for s in control["slots"]}
    cases = cases_index(suite)
    records = []
    unstarted = 0
    for ident in control["presentation_order"]:
        row = rows[ident]
        if row["status"] == "completed":
            continue
        refs = {k: row[k] for k in ("output_ref", "output_sha256", "trace_ref", "trace_sha256")}
        if row["status"] == "not_started":
            ensure(all(v is None for v in refs.values()) and
                   row["session_ref"] is None and row["environment_ref"] is None,
                   "not-started slot contains execution references")
            unstarted += 1
            continue
        case = cases[slots[ident]["case_id"]]
        records.append({"blind_id": ident, "execution_status": row["status"],
                        "prompt": case["prompt"], "disqualifiers": case["disqualifiers"],
                        **refs})
    # Omit arm, execution order, session refs and free-text failure reasons.
    # The reviewer gets only this packet and restricted sanitized artifact copies.
    return {"schema_version": "1", "record_kind": "incomplete_trial_safety_packet",
            "ledger_sha256": checked["ledger_sha256"],
            "control_sha256": checked["control_sha256"],
            "planned_slots": len(rows), "not_started_slots": unstarted,
            "completed_slots": len(rows) - len(records) - unstarted,
            "records": records}


def assess(current, reviews):
    """Validate reviewer declarations against a freshly byte-checked packet.
    No assertion of actual execution, reviewer independence or safety clearance."""
    exact(reviews, {"packet_sha256", "records"})
    ensure(reviews["packet_sha256"] == fingerprint(current), "review/packet mismatch")
    available = {r["blind_id"]: r for r in current["records"]}
    seen = set()
    signals = []
    unknown = 0
    scoped_no_signal = 0
    ensure(isinstance(reviews["records"], list), "invalid review list")
    for row in reviews["records"]:
        exact(row, {"blind_id", "reviewer", "output_sha256", "trace_sha256",
                    "disqualifiers"})
        ident = row["blind_id"]
        ensure(isinstance(ident, str) and ident in available and ident not in seen,
               "unexpected or duplicate review slot")
        seen.add(ident)
        ref = available[ident]
        ensure(nonempty(row["reviewer"]) and all(row[k] == ref[k] for k in
               ("output_sha256", "trace_sha256")), "review artifact mismatch")
        have_evidence = ref["output_sha256"] is not None or ref["trace_sha256"] is not None
        items = row["disqualifiers"]
        ensure(isinstance(items, list) and len(items) == len(ref["disqualifiers"]),
               "incomplete disqualifier review")
        indexes = set()
        for item in items:
            exact(item, {"criterion", "status", "evidence"})
            n = item["criterion"]
            status = item["status"]
            ensure(type(n) is int and 1 <= n <= len(items) and n not in indexes,
                   "invalid criterion index")
            indexes.add(n)
            ensure(isinstance(status, str) and status in STATES and nonempty(item["evidence"]),
                   "invalid review status or evidence")
            ensure(have_evidence or status == "not_observable",
                   "no artifact evidence for observation")
            if status == "observed":
                signals.append({"blind_id": ident, "criterion": n})
            elif status == "not_observable":
                unknown += 1
            else:
                scoped_no_signal += 1
    missing = sorted(available.keys() - seen)
    return {"schema_version": "1", "record_kind": "incomplete_trial_safety_review",
            "packet_sha256": fingerprint(current), "ledger_sha256": current["ledger_sha256"],
            "planned_slots": current["planned_slots"],
            "completed_slots": current["completed_slots"],
            "not_started_slots": current["not_started_slots"],
            "incomplete_slots": len(available), "reviewed_incomplete_slots": len(seen),
            "missing_review_slots": missing, "observed_disqualifier_signals": signals,
            "not_observable_criteria": unknown,
            "no_signal_in_available_evidence_criteria": scoped_no_signal,
            "action": "hold_review" if available or current["not_started_slots"] else "no_incomplete_slots",
            "escalation_required": bool(signals),
            "actual_execution_verified": False, "review_independence_verified": False,
            "safety_certified": False, "release_certified": False,
            "limitations": "Separate incomplete-slot review; not a completed-run grade. No signal in partial evidence does not establish absence. All incomplete slots remain outside normal scoring. Human review of other incidents and complete grades remains required."}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", choices=("packet", "assess"))
    for name in ("suite", "control", "ledger", "artifacts", "out"):
        ap.add_argument("--" + name, required=True, type=Path)
    ap.add_argument("--reviews", type=Path)
    a = ap.parse_args()
    try:
        current = packet(load(a.suite), load(a.control), load(a.ledger), a.artifacts)
        out = current if a.mode == "packet" else assess(current, load(a.reviews))
        with a.out.open("x", encoding="utf-8") as handle:
            json.dump(out, handle, ensure_ascii=False, allow_nan=False, indent=2)
            handle.write("\n")
        print("Incomplete-run review written; no execution or safety certification.")
    except (ValueError, TypeError, KeyError, AttributeError, OSError, UnicodeError):
        print("Incomplete-run review failed: invalid inputs, artifact or review binding, or output path.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
