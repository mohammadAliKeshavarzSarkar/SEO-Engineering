#!/usr/bin/env python3
"""Consolidate a frozen pilot's completed and incomplete reviews before handoff.

Does not perform inference, independently verify reviewers, approve a pilot,
validate process isolation or authorize any release. Local private inputs only.
"""
import argparse
import json
from pathlib import Path

if __package__:
    from .control_benchmark import check_schedule, ledger_index, finalize, ensure, fingerprint, sha, blind_packet
    from .review_completed_adjudication import assess as assess_completed
    from .review_runtime_observations import review as review_runtime
    from .prepare_trial import check_artifacts, SKILL_LAYOUTS
    from .review_incomplete_trials import packet as incomplete_packet, assess as assess_incomplete
    from .score_benchmark import load
else:
    from control_benchmark import check_schedule, ledger_index, finalize, ensure, fingerprint, sha, blind_packet
    from review_completed_adjudication import assess as assess_completed
    from review_runtime_observations import review as review_runtime
    from prepare_trial import check_artifacts, SKILL_LAYOUTS
    from review_incomplete_trials import packet as incomplete_packet, assess as assess_incomplete
    from score_benchmark import load



# This is the exact output envelope of review_activation_evidence.py, not a
# generic operator attestation. It is still not a signed provenance record.
ACTIVATION_FIELDS = {
    "schema_version", "kind", "candidate_commit", "archive_sha256",
    "control_sha256", "runtime_kind", "traces",
    "critical_declaration_conflicts", "missing_or_unobservable", "status",
    "operator_assertions_independently_verified", "trace_semantics_verified",
    "actual_activation_certified", "read_isolation_certified",
    "agent_executions_verified", "paid_pilot_authorized", "release_approved",
    "limitations",
}
ACTIVATION_UNVERIFIED = (
    "operator_assertions_independently_verified", "trace_semantics_verified",
    "actual_activation_certified", "read_isolation_certified",
    "agent_executions_verified", "paid_pilot_authorized", "release_approved",
)


def validate_activation_intake(control, intake):
    """Reject contradictory summaries; never infer the source traces were genuine."""
    ensure(isinstance(intake, dict) and set(intake) == ACTIVATION_FIELDS and
           intake["schema_version"] == "1" and
           intake["kind"] == "unscored_activation_evidence_intake",
           "invalid activation intake schema")
    config = control["plan"]["config"]
    ensure(intake["candidate_commit"] == config["skill_commit"] and
           intake["archive_sha256"] == config["archive_sha256"] and
           intake["control_sha256"] == fingerprint(control),
           "activation record does not match candidate/control")
    ensure(isinstance(intake["runtime_kind"], str) and
           intake["runtime_kind"] in SKILL_LAYOUTS,
           "invalid activation runtime kind")
    ensure(all(intake[field] is False for field in ACTIVATION_UNVERIFIED),
           "activation intake claims certification")
    ensure(isinstance(intake["limitations"], str) and intake["limitations"].strip(),
           "activation intake lacks limitations")

    for field in ("critical_declaration_conflicts", "missing_or_unobservable"):
        values = intake[field]
        ensure(isinstance(values, list) and
               all(isinstance(v, str) and v.strip() for v in values) and
               values == sorted(set(values)),
               "invalid activation findings")
    critical = intake["critical_declaration_conflicts"]
    unknown = intake["missing_or_unobservable"]

    traces = intake["traces"]
    ensure(isinstance(traces, list) and len(traces) == 2 and
           all(isinstance(t, dict) and
               set(t) == {"arm", "trace_sha256", "trace_supplied"}
               for t in traces) and
           [t["arm"] for t in traces] == ["baseline", "skill"],
           "invalid activation trace inventory")
    for trace in traces:
        supplied = trace["trace_supplied"]
        digest = trace["trace_sha256"]
        ensure(type(supplied) is bool and
               (sha(digest) if supplied else digest is None),
               "invalid activation trace identity")
        missing = trace["arm"] + ":trace_unavailable"
        ensure((missing in unknown) == (not supplied),
               "activation trace missingness mismatch")

    expected = ("escalate_to_owner" if critical else
                "hold_missing_or_unobservable" if unknown else
                "ready_for_independent_review")
    ensure(intake["status"] == expected,
           "activation intake status/findings mismatch")
    # A content digest binds the exact submitted summary, not its provenance.
    return fingerprint(intake)


def review(suite, control, ledger, artifacts, grades=None, incomplete_reviews=None,
           activation_intake=None, first_review=None, second_review=None,
           adjudication_resolutions=None, runtime_observations=None,
           runtime_captures=None):
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

    ensure((first_review is None) == (second_review is None),
           "both original completed reviews must be provided together")
    ensure(first_review is None or grades is not None,
           "adjudicated grades required for paired review")
    ensure(adjudication_resolutions is None or first_review is not None,
           "adjudication resolutions require both original reviews")
    completed_review = (assess_completed(blind_packet(suite,control,ledger),
                       first_review, second_review, grades, adjudication_resolutions)
                        if first_review is not None else None)

    ensure((runtime_observations is None) == (runtime_captures is None),
           "runtime declarations and capture root required together")
    runtime_check = (review_runtime(suite,control,ledger,artifacts,
                     runtime_observations,runtime_captures)
                     if runtime_observations is not None else None)

    activation_digest = (validate_activation_intake(control, activation_intake)
                         if activation_intake is not None else None)

    reasons=[]
    escalations=[]
    if counts["not_started"]:
        reasons.append("not_started_slots")
    if noncompleted:
        reasons.append("incomplete_or_failed_slots")
    if sum(counts[s] for s in ("completed","incomplete","timeout","error")) and runtime_check is None:
        reasons.append("runtime_observation_evidence_missing")
    elif runtime_check is not None:
        if runtime_check["status"] == "escalate_to_owner":
            escalations.append("runtime_operator_conflict_observed")
        elif runtime_check["status"] == "hold_missing_or_unobservable":
            reasons.append("runtime_operator_evidence_incomplete")
        else:
            reasons.append("runtime_not_independently_verified")
    if counts["completed"] and grades is None:
        reasons.append("completed_slots_without_grades")
    if scored is not None and scored["completed_ungraded"]:
        reasons.append("completed_slots_without_grades")
    if counts["completed"] and completed_review is None:
        reasons.append("completed_independent_reviews_missing")
    if completed_review is not None:
        if completed_review["hold_reasons"]:
            reasons.extend("completed_review_" + r for r in completed_review["hold_reasons"])
        if completed_review["original_observed_disqualifier_signals"]:
            escalations.append("original_completed_disqualifier_observed")
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
            "runtime_capture_integrity":runtime_check,
            "completed_adjudication_integrity":completed_review,
            "incomplete_safety_review":assessed,
            "activation_intake_status":activation_intake["status"] if activation_intake else "not_supplied",
            "activation_intake_sha256":activation_digest,
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
    ap.add_argument("--first-review",type=Path)
    ap.add_argument("--second-review",type=Path)
    ap.add_argument("--adjudication-resolutions",type=Path)
    ap.add_argument("--runtime-observations",type=Path)
    ap.add_argument("--runtime-captures",type=Path)
    ap.add_argument("--out",type=Path,required=True,
                    help="New private result file, not inside a model-visible workspace")
    args=ap.parse_args()
    try:
        out=review(load(args.suite),load(args.control),load(args.ledger),args.artifacts,
                   load(args.grades) if args.grades else None,
                   load(args.incomplete_reviews) if args.incomplete_reviews else None,
                   load(args.activation_intake) if args.activation_intake else None,
                   load(args.first_review) if args.first_review else None,
                   load(args.second_review) if args.second_review else None,
                   load(args.adjudication_resolutions) if args.adjudication_resolutions else None,
                   load(args.runtime_observations) if args.runtime_observations else None,
                   args.runtime_captures)
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
