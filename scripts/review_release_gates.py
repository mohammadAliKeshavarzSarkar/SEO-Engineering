#!/usr/bin/env python3
"""Review supplied release gate evidence; no deployment or evidence collection."""
import argparse
import json
from pathlib import Path

SUBJECT = {"stage", "revision", "artifact", "environment", "profile", "config_ref"}


def exact(value, keys):
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("unexpected object fields")


def string(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("nonempty string required")


def subject(value):
    exact(value, SUBJECT)
    for v in value.values():
        string(v)
    if value["stage"] not in ("candidate", "production"):
        raise ValueError("invalid stage")


def unique_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON key")
        obj[key] = value
    return obj


def reject_constant(_):
    raise ValueError("non-finite JSON constant")


def review(data):
    exact(data, {"schema_version", "release_id", "policy_ref", "subject", "gates", "exposure"})
    if data["schema_version"] != "1":
        raise ValueError("unsupported schema")
    for key in ("release_id", "policy_ref"):
        string(data[key])
    current = data["subject"]
    subject(current)
    gates = data["gates"]
    if not isinstance(gates, list) or not 1 <= len(gates) <= 1000:
        raise ValueError("invalid gate population")
    seen, results, blockers, optional = set(), [], [], []
    required_count = 0
    for gate in gates:
        exact(gate, {"id", "required", "rationale", "evidence"})
        string(gate["id"])
        string(gate["rationale"])
        if gate["id"] in seen or type(gate["required"]) is not bool:
            raise ValueError("duplicate gate or invalid required flag")
        seen.add(gate["id"])
        required_count += gate["required"]
        evidence = gate["evidence"]
        state = "missing"
        if evidence is not None:
            exact(evidence, {"subject", "outcome", "ref"})
            subject(evidence["subject"])
            string(evidence["ref"])
            if evidence["outcome"] not in ("pass", "fail", "incomplete"):
                raise ValueError("invalid evidence outcome")
            state = evidence["outcome"] if evidence["subject"] == current else "stale"
        results.append({**gate, "state": state})
        if state != "pass":
            (blockers if gate["required"] else optional).append(gate["id"])
    if not required_count:
        raise ValueError("at least one required gate needed")
    exposure = data["exposure"]
    exposure_state = "not_supplied"
    if exposure is not None:
        exact(exposure, {"subject", "ref"})
        subject(exposure["subject"])
        string(exposure["ref"])
        exposure_state = "current_reported" if exposure["subject"] == current else "stale_reported"
    if exposure is not None:
        disposition = "escalate"
    elif blockers:
        disposition = "hold"
    elif optional:
        disposition = "review_optional"
    else:
        disposition = "ready_for_owner_review"
    return {"schema_version": "1", "method": "T11-v1", "release_id": data["release_id"],
            "policy_ref": data["policy_ref"], "subject": current, "gates": results,
            "blockers": blockers, "optional_review": optional, "exposure": exposure,
            "exposure_state": exposure_state, "disposition": disposition,
            "deployment_authorized": False, "evidence_independently_verified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        with args.input.open("rb") as stream:
            raw = stream.read(4 * 1024 * 1024 + 1)
        if len(raw) > 4 * 1024 * 1024:
            raise ValueError("input too large")
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                          parse_constant=reject_constant)
        result = review(data)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2, ensure_ascii=True, allow_nan=False)
            stream.write("\n")
    except (OSError, UnicodeError, ValueError, RecursionError):
        print("Release gate review failed: invalid input or output")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
