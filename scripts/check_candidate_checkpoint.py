#!/usr/bin/env python3
"""Validate a held development checkpoint, never authorize distribution."""
import argparse
import json
import re
from pathlib import Path

if __package__:
    from .score_benchmark import load
else:
    from score_benchmark import load

REQUIRED = {
    "offline_tests","archive_identity","reproducibility","relocated_installation",
    "automated_privacy_screen","runtime_activation","supported_runtime_matrix",
    "pilot_behavior","full_public_behavior","held_out_behavior","manual_content_privacy",
    "source_accuracy","ownership_and_rights","license_and_distribution",
    "candidate_handoff","owner_release_approval",
}
OPTIONAL={"websitebotscroll_exchange"}
STATES={"observed_pass","pending","not_run","failed","blocked"}
FLAGS={"release_approved","published","license_assigned","source_review_complete","privacy_approved"}


def require(ok,message):
    if not ok:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value,str) and bool(value.strip())


def validate(record):
    require(record["schema_version"]=="1" and
            record["record_kind"]=="internal_development_review_checkpoint",
            "unsupported checkpoint record")
    candidate=record["candidate"]
    require(set(candidate)=={"source_commit","archive_sha256","version","scope"},
            "candidate identity must be exact")
    require(isinstance(candidate["source_commit"],str) and re.fullmatch(r"[0-9a-f]{40}",candidate["source_commit"]),
            "invalid commit identity")
    require(isinstance(candidate["archive_sha256"],str) and re.fullmatch(r"[0-9a-f]{64}",candidate["archive_sha256"]),
            "invalid archive identity")
    require(isinstance(candidate["version"],str) and re.fullmatch(r"0\.\d+\.\d+-dev\.\d+",candidate["version"]),
            "only development versions supported")
    require(candidate["scope"]=="standalone_portable_skill","unsupported release scope")
    require(record["release_decision"]=="hold" and all(record[k] is False for k in FLAGS),
            "this checker cannot approve or publish releases")
    require(isinstance(record["gates"],list),"invalid gate list")
    index={}
    for g in record["gates"]:
        require(set(g)=={"id","required","state","observation","evidence_refs"},"invalid gate fields")
        ident=g["id"]
        require(ident in REQUIRED|OPTIONAL and ident not in index,"unknown or duplicate gate")
        require(g["required"] is (ident in REQUIRED),"incorrect mandatory gate designation")
        require(g["state"] in STATES and nonempty(g["observation"]),"invalid observation")
        refs=g["evidence_refs"]
        require(isinstance(refs,list) and all(map(nonempty,refs)) and len(refs)==len(set(refs)),
                "invalid evidence references")
        require(g["state"]!="observed_pass" or bool(refs),"pass requires evidence reference")
        index[ident]=g
    require(set(index)==REQUIRED|OPTIONAL,"incomplete gate inventory")
    # This command describes a record only. No input can make it certify a release.
    return {"candidate":candidate,
            "mandatory_gate_count":len(REQUIRED),
            "recorded_passes":sum(index[k]["state"]=="observed_pass" for k in REQUIRED),
            "open_mandatory_gates":[{"id":k,"state":index[k]["state"]} for k in sorted(REQUIRED)
                                    if index[k]["state"]!="observed_pass"],
            "separate_optional_gates":[{"id":k,"state":index[k]["state"]} for k in sorted(OPTIONAL)],
            "evidence_authenticity_verified":False,
            "release_decision":"hold","release_approved":False,
            "limitations":"Record-only consistency check; referenced evidence, review authority and actual archive must be independently verified."}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--record",type=Path,required=True)
    a=p.parse_args()
    try:
        result=validate(load(a.record))
    except (OSError,ValueError,TypeError,KeyError,AttributeError):
        print("Invalid held checkpoint; no release approval.")
        return 1
    print(json.dumps(result,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
