#!/usr/bin/env python3
"""Private unscored probe intake; verifies trace bytes, NOT actual agent behavior."""
import argparse
import json
import re
import subprocess
from pathlib import Path

if __package__:
    from .build_skill import ROOT
    from .check_pilot_staging import inspect as inspect_pair
    from .control_benchmark import ensure
    from .prepare_trial import regular_bytes
    from .score_benchmark import load
    from .verify_package import digest
else:
    from build_skill import ROOT
    from check_pilot_staging import inspect as inspect_pair
    from control_benchmark import ensure
    from prepare_trial import regular_bytes
    from score_benchmark import load
    from verify_package import digest

SHA=re.compile(r"[0-9a-f]{64}")
CHOICES={"present","absent","unknown"}
OBS={"verified_by_operator","failed","unknown"}
TOP={"control_sha256","candidate_commit","archive_sha256","runtime_kind",
     "operator","authorization_ref","probes"}
FIELDS={"runtime_version","model","settings_ref","session_ref","trace_ref",
        "trace_sha256","discovery","entrypoint_read","routed_reference_read",
        "unrelated_activation","read_isolation","tool_permissions","observation_ref"}


def require_text(value, field):
    ensure(isinstance(value,str) and value.strip() and not any(
           x in value.lower() for x in ("replace","placeholder","<fill")),
           "missing or placeholder "+field)


def review(pair, record, evidence_root):
    """Review locally submitted bytes and declared observations; no certification."""
    ensure(isinstance(pair,dict) and pair.get("kind")=="local_pilot_pair_integrity"
           and pair.get("stage_bytes_matched_to_source_archive") is True,
           "unverified pilot staging")
    ensure(isinstance(record,dict) and set(record)==TOP,
           "unexpected activation record fields")
    for field,bound in (("control_sha256","control_sha256"),
                        ("candidate_commit","candidate_commit_declared"),
                        ("archive_sha256","archive_sha256"),
                        ("runtime_kind","runtime_kind")):
        ensure(record[field]==pair[bound],"activation candidate binding mismatch")
    for field in ("operator","authorization_ref"):
        require_text(record[field],field)
    ensure(isinstance(record["probes"],dict) and
           set(record["probes"])=={"baseline","skill"},
           "baseline and skill probes required")
    root=Path(evidence_root)
    ensure(root.is_dir() and not root.is_symlink(),"invalid private evidence root")
    critical=[]
    unknown=[]
    seen_sessions=set()
    refs=[]
    for arm in ("baseline","skill"):
        row=record["probes"][arm]
        ensure(isinstance(row,dict) and set(row)==FIELDS,"unexpected probe fields")
        for field in ("runtime_version","model","settings_ref","session_ref","observation_ref"):
            require_text(row[field],arm+"."+field)
        ensure(row["session_ref"] not in seen_sessions,"probe session reused")
        seen_sessions.add(row["session_ref"])
        for field in ("discovery","entrypoint_read","routed_reference_read","unrelated_activation"):
            ensure(row[field] in CHOICES,"invalid probe observation")
        for field in ("read_isolation","tool_permissions"):
            ensure(row[field] in OBS,"invalid operator observation")
        ref,h=row["trace_ref"],row["trace_sha256"]
        if ref is None and h is None:
            unknown.append(arm+":trace_unavailable")
        else:
            ensure(ref==arm+"/probe.txt" and isinstance(h,str) and SHA.fullmatch(h),
                   "nonfixed or invalid trace reference")
            folder=root/arm
            ensure(folder.is_dir() and not folder.is_symlink(),"unsafe trace directory")
            raw=regular_bytes(folder/"probe.txt")
            ensure(raw and digest(raw)==h,"trace missing, changed or empty")
            raw.decode("utf-8",errors="strict")
        refs.append({"arm":arm,"trace_sha256":h,"trace_supplied":h is not None})
        expected={"discovery":"absent","entrypoint_read":"absent",
                  "routed_reference_read":"absent"} if arm=="baseline" else {
                  "discovery":"present","entrypoint_read":"present",
                  "routed_reference_read":"present"}
        for field,want in expected.items():
            if row[field]=="unknown":
                unknown.append(arm+":"+field+"_unobservable")
            elif row[field]!=want:
                critical.append(arm+":"+field+"_unexpected")
        if row["unrelated_activation"]=="present":
            critical.append(arm+":unrelated_skill_activated")
        elif row["unrelated_activation"]=="unknown":
            unknown.append(arm+":unrelated_skill_unknown")
        for field in ("read_isolation","tool_permissions"):
            if row[field]=="failed":
                critical.append(arm+":"+field+"_failed")
            elif row[field]=="unknown":
                unknown.append(arm+":"+field+"_unknown")
    for field in ("runtime_version","model","settings_ref"):
        if record["probes"]["baseline"][field]!=record["probes"]["skill"][field]:
            critical.append("pair:"+field+"_mismatch")
    status=("escalate_to_owner" if critical else
            "hold_missing_or_unobservable" if unknown else
            "ready_for_independent_review")
    return {"schema_version":"1","kind":"unscored_activation_evidence_intake",
            "candidate_commit":record["candidate_commit"],
            "archive_sha256":record["archive_sha256"],
            "control_sha256":record["control_sha256"],
            "runtime_kind":record["runtime_kind"],
            "traces":refs,"critical_declaration_conflicts":sorted(critical),
            "missing_or_unobservable":sorted(unknown),"status":status,
            "operator_assertions_independently_verified":False,
            "trace_semantics_verified":False,
            "actual_activation_certified":False,
            "read_isolation_certified":False,
            "agent_executions_verified":False,
            "paid_pilot_authorized":False,"release_approved":False,
            "limitations":"Submitted sanitized trace bytes and human declarations only. No trace semantic proof, independent review, sandbox audit, scoring, or permission to begin paid sessions."}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--operator",type=Path,required=True)
    p.add_argument("--workspaces",type=Path,required=True)
    p.add_argument("--record",type=Path,required=True)
    p.add_argument("--evidence",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    try:
        for forbidden in (ROOT,a.workspaces):
            ensure(not a.out.resolve().is_relative_to(Path(forbidden).resolve()),
                   "output must remain outside source and agent workspace")
        actual=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
        ensure(not subprocess.check_output(["git","status","--porcelain","--untracked-files=all"],
                                          cwd=ROOT,text=True).strip(),
               "clean checkout required")
        pair=inspect_pair(ROOT,a.operator,a.workspaces)
        ensure(pair["candidate_commit_declared"]==actual,"source revision mismatch")
        result=review(pair,load(a.record),a.evidence)
        with a.out.open("x",encoding="utf-8") as out:
            json.dump(result,out,indent=2,ensure_ascii=False,allow_nan=False)
            out.write("\n")
    except (OSError,ValueError,KeyError,TypeError,AttributeError,UnicodeError,
            subprocess.SubprocessError) as exc:
        print("Activation evidence intake failed:",exc)
        return 1
    print("Unscored probe evidence recorded; no actual activation or isolation certified.")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
