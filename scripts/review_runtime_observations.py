#!/usr/bin/env python3
"""Review private operator runtime-capture declarations against frozen pilot bytes.

Does not execute a model, interpret provider-specific events or independently
verify session identity, user authorization, isolation or runtime behavior.
"""
import argparse
import json
from pathlib import Path

if __package__:
    from .control_benchmark import (check_schedule, ledger_index, ensure, exact,
                                     fingerprint, real_text, sha)
    from .prepare_trial import check_artifacts, regular_bytes, SKILL_LAYOUTS
    from .score_benchmark import load
    from .verify_package import digest
else:
    from control_benchmark import (check_schedule, ledger_index, ensure, exact,
                                   fingerprint, real_text, sha)
    from prepare_trial import check_artifacts, regular_bytes, SKILL_LAYOUTS
    from score_benchmark import load
    from verify_package import digest


TOP = {"schema_version", "record_kind", "control_sha256", "source_commit",
       "archive_sha256", "runtime_kind", "runs"}
RUN = {"blind_id", "status", "session_ref", "environment_ref",
       "runtime_version", "model", "inference_settings", "permission_mode",
       "prompt_sha256", "terminal_event", "exit_code", "elapsed_ms",
       "read_isolation", "skill_activation", "output_sha256", "trace_sha256",
       "capture_ref", "capture_sha256"}
STARTED = {"completed", "incomplete", "timeout", "error"}
TERMINALS = {"success", "failure", "timeout", "unobservable"}
OBSERVATIONS = {"observed", "absent", "unknown"}
ISOLATION = {"verified_by_operator", "failed", "unknown"}
PROMPT_PREFIX = "Read context.txt in this workspace, then answer the following task.\n\n"


def review(suite, control, ledger, artifacts, observations, captures):
    """Verify submitted bytes and internal identities; retain unobservables."""
    check_schedule(suite, control)
    checked = check_artifacts(control, ledger, artifacts)
    entries = ledger_index(control, ledger)
    exact(observations, TOP)
    ensure(observations["schema_version"] == "1" and
           observations["record_kind"] == "private_runtime_capture_declarations",
           "invalid runtime capture record kind")
    config = control["plan"]["config"]
    ensure(observations["control_sha256"] == fingerprint(control) and
           observations["source_commit"] == config["skill_commit"] and
           observations["archive_sha256"] == config["archive_sha256"],
           "runtime capture candidate/control mismatch")
    kind = observations["runtime_kind"]
    ensure(isinstance(kind, str) and kind in SKILL_LAYOUTS,
           "invalid runtime kind")
    mentioned = {name for name in SKILL_LAYOUTS if name in config["runtime"].lower()}
    ensure(not mentioned or mentioned == {kind}, "runtime layout differs from control")
    ensure(isinstance(observations["runs"], list), "runtime runs must be an array")

    root = Path(captures)
    ensure(root.is_dir() and not root.is_symlink(), "invalid private captures root")
    slots = {slot["blind_id"]: slot for slot in control["slots"]}
    started = {ident for ident, row in entries.items() if row["status"] in STARTED}
    seen = set()
    captured = []
    critical = []
    unknown = []
    versions = set()
    for row in observations["runs"]:
        exact(row, RUN)
        ident = row["blind_id"]
        ensure(isinstance(ident, str) and ident in started and ident not in seen,
               "capture not bound to one started slot")
        seen.add(ident)
        actual = entries[ident]
        ensure(row["status"] == actual["status"] and
               row["session_ref"] == actual["session_ref"] and
               row["environment_ref"] == actual["environment_ref"] and
               real_text(row["session_ref"]) and
               real_text(row["environment_ref"]),
               "capture status or session binding mismatch")
        ensure(row["output_sha256"] == actual["output_sha256"] and
               row["trace_sha256"] == actual["trace_sha256"],
               "capture sanitized artifact mismatch")
        for field in ("model", "inference_settings", "permission_mode"):
            ensure(row[field] == config[field], "capture frozen settings mismatch: " + field)
        ensure(real_text(row["runtime_version"]), "capture runtime version required")
        versions.add(row["runtime_version"])
        expected_prompt = (PROMPT_PREFIX + slots[ident]["prompt"] + "\n").encode("utf-8")
        ensure(row["prompt_sha256"] == digest(expected_prompt),
               "capture frozen prompt digest mismatch")
        ensure(row["terminal_event"] in TERMINALS and
               (row["exit_code"] is None or
                (type(row["exit_code"]) is int and
                 -255 <= row["exit_code"] <= 255)) and
               type(row["elapsed_ms"]) is int and row["elapsed_ms"] >= 0,
               "invalid terminal event or execution timing")
        if row["status"] == "completed":
            ensure(row["terminal_event"] == "success" and row["exit_code"] == 0,
                   "completed slot lacks successful terminal observation")
        else:
            ensure(row["terminal_event"] != "success" and
                   (row["exit_code"] is None or row["exit_code"] != 0),
                   "failed/partial slot falsely marked successful")
            if row["status"] == "timeout":
                ensure(row["terminal_event"] in ("timeout", "unobservable"),
                       "timeout terminal contradiction")
            if row["status"] == "error":
                ensure(row["terminal_event"] in ("failure", "unobservable"),
                       "error terminal contradiction")
        ensure(row["read_isolation"] in ISOLATION and
               row["skill_activation"] in OBSERVATIONS,
               "invalid operator observations")
        if row["read_isolation"] == "failed":
            critical.append(ident + ":isolation_declared_failed")
        elif row["read_isolation"] == "unknown":
            unknown.append(ident + ":isolation_unobservable")
        arm = slots[ident]["arm"]
        activation = row["skill_activation"]
        if (arm == "baseline" and activation == "observed") or (
                arm == "skill" and activation == "absent"):
            critical.append(ident + ":skill_activation_contradiction")
        elif activation == "unknown":
            unknown.append(ident + ":skill_activation_unobservable")
        if row["terminal_event"] == "unobservable":
            unknown.append(ident + ":terminal_unobservable")

        expected_ref = ident + "/events.txt"
        ensure(row["capture_ref"] == expected_ref and
               sha(row["capture_sha256"]), "invalid fixed capture reference")
        folder = root / ident
        ensure(folder.is_dir() and not folder.is_symlink(),
               "invalid capture slot directory")
        raw = regular_bytes(folder / "events.txt")
        ensure(raw and digest(raw) == row["capture_sha256"],
               "capture missing, empty or changed")
        raw.decode("utf-8", errors="strict")
        captured.append({"blind_id": ident, "capture_sha256": row["capture_sha256"],
                         "bytes": len(raw), "reported_status": row["status"]})

    # Prevent a captured adverse trace from being omitted from the declarations.
    for folder in root.iterdir():
        ensure(not folder.is_symlink() and folder.is_dir() and folder.name in seen,
               "undeclared capture directory or file")
        for item in folder.iterdir():
            ensure(not item.is_symlink() and item.is_file() and item.name == "events.txt",
                   "unexpected runtime capture file")
    if len(versions) > 1:
        critical.append("runtime_version_mismatch_between_sessions")
    missing = sorted(started - seen)
    if missing:
        unknown.append("started_slots_without_capture")
    launch_order = [slot["blind_id"] for slot in control["slots"]]
    reported_order = [item["blind_id"] for item in observations["runs"]]
    if reported_order != [ident for ident in launch_order if ident in seen]:
        unknown.append("capture_records_outside_frozen_launch_order")
    if len(started) < 2 and any(ident not in {s["blind_id"] for s in
                              control["slots"][:2]} for ident in seen):
        unknown.append("later_slot_before_first_pair_observed")
    status = ("escalate_to_owner" if critical else
              "hold_missing_or_unobservable" if unknown else
              "ready_for_independent_review")
    return {"schema_version": "1",
            "record_kind": "private_runtime_capture_integrity_review",
            "control_sha256": fingerprint(control),
            "ledger_sha256": checked["ledger_sha256"],
            "declarations_sha256": fingerprint(observations),
            "source_commit": config["skill_commit"],
            "archive_sha256": config["archive_sha256"],
            "runtime_kind": kind,
            "started_slots": len(started),
            "verified_declared_capture_files": captured,
            "missing_capture_slots": missing,
            "critical_operator_declaration_conflicts": sorted(set(critical)),
            "missing_or_unobservable": sorted(set(unknown)),
            "status": status,
            "runtime_events_semantics_verified": False,
            "actual_model_execution_independently_verified": False,
            "filesystem_isolation_independently_verified": False,
            "paid_pilot_authorized": False,
            "release_approved": False,
            "limitations": "Submitted operator declarations and local UTF-8 event-byte hashes only. No provider event parsing, trustworthy provenance, runtime isolation attestation, inferred budget compliance or authorization."}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for field in ("suite", "control", "ledger", "artifacts",
                  "observations", "captures", "out"):
        ap.add_argument("--" + field, required=True, type=Path)
    args = ap.parse_args()
    try:
        result = review(load(args.suite), load(args.control), load(args.ledger),
                        args.artifacts, load(args.observations), args.captures)
        with args.out.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, ensure_ascii=False, allow_nan=False, indent=2)
            stream.write("\n")
    except (OSError, ValueError, TypeError, KeyError, AttributeError, UnicodeError) as exc:
        print("Runtime capture review failed:", exc)
        return 1
    print("Operator capture bytes checked; external execution NOT verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
