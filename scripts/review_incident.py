#!/usr/bin/env python3
"""Validate a supplied incident ledger; no causal inference or live actions."""
import argparse
import json
from pathlib import Path

SUBJECT = {"scope_ref", "revision", "artifact", "environment", "profile", "config_ref"}


def exact(obj, keys):
    if not isinstance(obj, dict) or set(obj) != keys:
        raise ValueError("unexpected object fields")


def string(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("nonempty string required")


def subject(value, scope):
    exact(value, SUBJECT)
    for v in value.values():
        string(v)
    if value["scope_ref"] != scope:
        raise ValueError("subject outside incident scope")


def array(value):
    if not isinstance(value, list) or len(value) > 1000:
        raise ValueError("invalid array")


def unique_id(item, seen):
    string(item)
    if item in seen:
        raise ValueError("duplicate identifier")
    seen.add(item)


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
    exact(data, {"schema_version", "incident_id", "scope_ref", "subject", "recovery_subject",
                 "evidence", "hypotheses", "checks", "exposure_ref", "search_follow_up"})
    if data["schema_version"] != "2":
        raise ValueError("unsupported schema")
    scope = data["scope_ref"]
    string(scope)
    string(data["incident_id"])
    current, recovery = data["subject"], data["recovery_subject"]
    subject(current, scope)
    if recovery is not None:
        subject(recovery, scope)
    if data["search_follow_up"] not in ("pending", "not_applicable", "unknown"):
        raise ValueError("invalid search follow-up")
    if data["exposure_ref"] is not None:
        string(data["exposure_ref"])
    for key in ("evidence", "hypotheses", "checks"):
        array(data[key])
    if not data["hypotheses"]:
        raise ValueError("at least one hypothesis required")
    evidence = {}
    seen = set()
    for item in data["evidence"]:
        exact(item, {"id", "subject", "ref", "quality", "verification"})
        unique_id(item["id"], seen)
        subject(item["subject"], scope)
        string(item["ref"])
        if item["quality"] not in ("complete", "partial"):
            raise ValueError("invalid evidence quality")
        v = item["verification"]
        if v is not None:
            exact(v, {"check_id", "assertion", "outcome"})
            string(v["check_id"])
            string(v["assertion"])
            if v["outcome"] not in ("pass", "fail", "incomplete"):
                raise ValueError("invalid verification outcome")
        evidence[item["id"]] = item

    def lookup(ref):
        string(ref)
        if ref not in evidence:
            raise ValueError("unknown evidence id")
        return evidence[ref]

    hypotheses = []
    seen = set()
    for h in data["hypotheses"]:
        exact(h, {"id", "claim", "falsifier", "assessments"})
        unique_id(h["id"], seen)
        string(h["claim"])
        string(h["falsifier"])
        array(h["assessments"])
        links, support, refute, inconclusive, excluded = set(), [], [], [], []
        for a in h["assessments"]:
            exact(a, {"evidence_id", "relation"})
            ident = a["evidence_id"]
            unique_id(ident, links)
            item = lookup(ident)
            relation = a["relation"]
            if relation not in ("supports", "refutes", "inconclusive"):
                raise ValueError("invalid relationship")
            if item["subject"] != current or item["quality"] != "complete":
                excluded.append(ident)
            elif relation == "supports":
                support.append(ident)
            elif relation == "refutes":
                refute.append(ident)
            else:
                inconclusive.append(ident)
        state = ("conflicting" if support and refute else "support_only" if support
                 else "refute_only" if refute else "unresolved")
        hypotheses.append({**h, "state": state, "support_ids": support, "refute_ids": refute,
                           "inconclusive_ids": inconclusive, "excluded_ids": excluded})
    if recovery is None and data["checks"]:
        raise ValueError("checks require recovery subject")
    checks, blockers, optional, seen = [], [], [], set()
    count = 0
    for c in data["checks"]:
        exact(c, {"id", "required", "assertion", "evidence_id", "outcome"})
        unique_id(c["id"], seen)
        string(c["assertion"])
        if type(c["required"]) is not bool:
            raise ValueError("invalid required flag")
        count += c["required"]
        ident, outcome = c["evidence_id"], c["outcome"]
        if ident is None:
            if outcome is not None:
                raise ValueError("missing evidence cannot have outcome")
            state = "missing"
        else:
            item = lookup(ident)
            if outcome not in ("pass", "fail", "incomplete"):
                raise ValueError("invalid check outcome")
            if item["subject"] != recovery or item["quality"] != "complete":
                state = "unmatched_or_partial"
            elif item["verification"] != {"check_id": c["id"], "assertion": c["assertion"], "outcome": outcome}:
                state = "unmatched_assertion"
            else:
                state = outcome
        checks.append({**c, "state": state})
        if state != "pass":
            (blockers if c["required"] else optional).append(c["id"])
    if recovery is not None and not count:
        raise ValueError("recovery needs required checks")
    if data["exposure_ref"] is not None:
        disposition = "escalate"
    elif recovery is None or blockers:
        disposition = "investigate"
    elif optional:
        disposition = "review_optional"
    else:
        disposition = "technical_recovery_review"
    return {**data, "method": "T12-v2", "hypotheses": hypotheses, "checks": checks,
            "required_blockers": blockers, "optional_review": optional,
            "disposition": disposition, "root_cause_confirmed": False,
            "evidence_independently_verified": False, "incident_closed": False,
            "search_recovery_established": False}


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
        report = review(data)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(report, stream, indent=2, ensure_ascii=True, allow_nan=False)
            stream.write("\n")
    except (OSError, UnicodeError, ValueError, RecursionError):
        print("Incident review failed: invalid input or output")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
