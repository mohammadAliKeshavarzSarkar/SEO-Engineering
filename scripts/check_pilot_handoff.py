#!/usr/bin/env python3
"""Consolidate a frozen pilot's completed and incomplete reviews before handoff.

Does not perform inference, independently verify reviewers, approve a pilot,
validate process isolation or authorize any release. Local private inputs only.
"""
import argparse
import json
from pathlib import Path

if __package__:
    from .control_benchmark import check_schedule, ledger_index, finalize, ensure, fingerprint
    from .prepare_trial import check_artifacts
    from .review_incomplete_trials import packet as incomplete_packet, assess as assess_incomplete
    from .score_benchmark import load
else:
    from control_benchmark import check_schedule, ledger_index, finalize, ensure, fingerprint
    from prepare_trial import check_artifacts
    from review_incomplete_trials import packet as incomplete_packet, assess as assess_incomplete
    from score_benchmark import load


def review(suite, control, ledger, artifacts, grades=None, incomplete_reviews=None,
           activation_intake=None):
    """Bind independently authored records to the same exact original ledger."""
    check_schedule(suite, control)
    checked=check_artifacts(control,ledger,artifacts)
    rows=ledger_index(control,ledger)
    counts={state:sum(r["status"]==state for r in rows.values())
            for state in ("completed","incomplete","timeout","error","not_started")}
    # This uses actual bytes and the existing blind-reviewed scorer; it never
    # substitutes an incomplete-run safety assessment for a completed-run grade.
    scored=finalize(suite,control,ledger,grades) if grades is not None else None
    sidecar=incomplete_packet(suite,control,ledger,artifacts)
    noncompleted=sum(counts[s] for s in ("incomplete","timeout","error"))
    assessed=assess_incomplete(sidecar,incomplete_reviews) if incomplete_reviews is not None else None
    ensure(noncompleted or incomplete_reviews is None or
           assessed["incomplete_slots"]==0,"incomplete review mismatch")

    if activation_intake is not None:
        ensure(isinstance(activation_intake,dict) and
               activation_intake.get("kind")=="unscored_activation_evidence_intake"
               and activation_intake.get("candidate_commit")==control["plan"]["config"]["skill_commit"]
               and activation_intake.get("archive_sha256")==control["plan"]["config"]["archive_sha256"]
               and activation_intake.get("control_sha256")==fingerprint(control),
               "activation record does not match candidate/control")
        ensure(activation_intake.get("actual_activation_certified") is False and
               activation_intake.get("read_isolation_certified") is False and
               activation_intake.get("paid_pilot_authorized") is False and
               activation_intake.get("release_approved") is False,
               "activation intake claims certification")
        ensure(activation_intake.get("status") in (
               "ready_for_independent_review","hold_missing_or_unobservable","escalate_to_owner"),
               "invalid activation intake status")

    reasons=[]
    escalations=[]
    if counts["not_started"]:
        reasons.append("not_started_slots")
    if noncompleted:
        reasons.append("incomplete_or_failed_slots")
    if counts["completed"] and grades is None:
        reasons.append("completed_slots_without_grades")
    if scored is not None and scored["completed_ungraded"]:
        reasons.append("completed_slots_without_grades")
    if noncompleted and assessed is None:
        reasons.append("incomplete_safety_review_missing")
    if assessed is not None:
        if assessed["missing_review_slots"]:
            reasons.append("incomplete_review_missing_records")
        if assessed["not_observable_criteria"]:
            reasons.append("incomplete_disqualifier_unobservable")
        if assessed["observed_disqualifier_signals"]:
            escalations.append("incomplete_disqualifier_observed")
    if scored is not None:
        if not scored["complete"]:
            reasons.append("full_pilot_not_graded")
        if not scored["skill_internal_case_gate"]:
            reasons.append("skill_case_gate_not_met")
        if scored["arms"]["skill"]["critical_failures_all_graded"]:
            escalations.append("skill_critical_failure_observed")
        if scored["arms"]["skill"]["unobservable_runs_all_graded"]:
            reasons.append("skill_grade_unobservable")
    if activation_intake is None:
        reasons.append("independent_activation_review_missing")
    elif activation_intake["status"]=="escalate_to_owner":
        escalations.append("activation_evidence_conflict")
    elif activation_intake["status"]=="hold_missing_or_unobservable":
        reasons.append("activation_evidence_incomplete")
    else:
        reasons.append("activation_not_independently_verified")

    # A favorable synthetic score is never proof of real runtime execution.
    state="escalate_to_owner" if escalations else "hold_evidence_and_owner_review"
    return {"schema_version":"1","record_kind":"private_pilot_handoff_review",
            "control_sha256":fingerprint(control),
            "ledger_sha256":checked["ledger_sha256"],
            "archive_sha256":control["plan"]["config"]["archive_sha256"],
            "source_commit":control["plan"]["config"]["skill_commit"],
            "execution_counts":counts,"verified_submitted_artifacts":len(checked["verified_artifacts"]),
            "completed_grade_report":scored,
            "incomplete_safety_review":assessed,
            "activation_intake_status":activation_intake["status"] if activation_intake else "not_supplied",
            "hold_reasons":sorted(set(reasons)),
            "escalation_reasons":sorted(set(escalations)),"disposition":state,
            "model_execution_independently_verified":False,
            "reviewer_independence_verified":False,
            "filesystem_read_isolation_verified":False,
            "owner_authorization_verified":False,
            "pilot_approved":False,"release_approved":False,
            "limitations":"Submitted local files and reviewer declarations only; no independent runtime provenance or permissions review. Incomplete/failed slots cannot be hidden by completed-run scores, and even favorable full grades require independent owner review."}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--suite",type=Path,required=True)
    ap.add_argument("--control",type=Path,required=True)
    ap.add_argument("--ledger",type=Path,required=True)
    ap.add_argument("--artifacts",type=Path,required=True)
    ap.add_argument("--grades",type=Path)
    ap.add_argument("--incomplete-reviews",type=Path)
    ap.add_argument("--activation-intake",type=Path)
    ap.add_argument("--out",type=Path,required=True,
                    help="New private result file, not inside a model-visible workspace")
    args=ap.parse_args()
    try:
        out=review(load(args.suite),load(args.control),load(args.ledger),args.artifacts,
                   load(args.grades) if args.grades else None,
                   load(args.incomplete_reviews) if args.incomplete_reviews else None,
                   load(args.activation_intake) if args.activation_intake else None)
        with args.out.open("x",encoding="utf-8") as h:
            json.dump(out,h,indent=2,ensure_ascii=False,allow_nan=False)
            h.write("\n")
    except (ValueError,KeyError,TypeError,AttributeError,OSError,UnicodeError) as exc:
        print("Pilot handoff review failed:",exc)
        return 1
    print("Pilot evidence consolidated; independent execution and release NOT certified.")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
