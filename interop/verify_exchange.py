#!/usr/bin/env python3
"""Verify an explicitly supplied sidecar and evidence file offline.

Field layout is a consumer proposal, subject to producer agreement.
A receipt is not proof of origin, authorization, real collection or approval.
"""
import argparse
import re
import sys
import json
from pathlib import Path

from interop.validate_crawl_evidence import (
    BoundaryError, InvalidJson, digest, load_pin, load_validator, parse, read_local, validate,
)
from interop.exchange_profile import PROFILE_ID, PROFILE_AGREEMENT, profile

FIELDS = {"contract", "exchange_profile", "producer_commit", "contract_source_commit",
          "schema_sha256", "evidence_sha256", "checksum_algorithm", "evidence_filename",
          "evidence_bytes", "run_id", "authorization_ref", "authorized_scope",
          "started_at", "finished_at", "coverage_limitations", "producer_validation",
          "producer_preflight"}
SHA = re.compile(r"[0-9a-f]{64}")
COMMIT = re.compile(r"[0-9a-f]{40}")
FILENAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\.json")


def text(value):
    return isinstance(value,str) and bool(value.strip())


def verify(manifest_raw, raw, filename, validator, pin, reviewed_producer_commit):
    result = {"method":"synthetic-exchange-receipt-dev.1","profile_id":PROFILE_ID,
              "profile_agreement":PROFILE_AGREEMENT,"manifest_sha256":digest(manifest_raw),
              "input_sha256":digest(raw),"input_bytes":len(raw),
              "checksum_verified":False,"manifest_binding_verified":False,
              "producer_validation":"not_assessed","producer_preflight":"not_assessed",
              "consumer_validation":"not_run","consumer_preflight":"not_run",
              "authorization_verified":False,"provenance_verified":False,
              "producer_validation_independently_verified":False,
              "actual_exchange_verified":False,"operational_integration_approved":False,
              "disposition":"hold","issues":[]}
    def fail(code):
        result["issues"].append(code)
        return result

    try:
        m=parse(manifest_raw)
    except (BoundaryError, InvalidJson):
        return fail("manifest.invalid_json_or_boundary")
    if not isinstance(m,dict) or set(m)!=FIELDS:
        return fail("manifest.field_layout")
    if not isinstance(reviewed_producer_commit,str) or not COMMIT.fullmatch(reviewed_producer_commit):
        return fail("manifest.reviewed_producer_revision_required")
    if m["contract"]!={"name":pin["contract"]["name"],"version":pin["contract"]["version"]}:
        return fail("manifest.contract_mismatch")
    if (m["exchange_profile"]!=PROFILE_ID or m["schema_sha256"]!=pin["contract"]["schema_sha256"]
            or m["contract_source_commit"]!=pin["producer_commit"]):
        return fail("manifest.profile_or_schema_pin_mismatch")
    if m["producer_commit"]!=reviewed_producer_commit:
        return fail("manifest.producer_commit_mismatch")
    if (not isinstance(m["evidence_filename"],str) or not FILENAME.fullmatch(m["evidence_filename"])
            or m["evidence_filename"]!=filename):
        return fail("manifest.filename_mismatch")
    if (m["checksum_algorithm"]!="SHA-256" or not isinstance(m["evidence_sha256"],str)
            or not SHA.fullmatch(m["evidence_sha256"]) or type(m["evidence_bytes"]) is not int
            or m["evidence_bytes"]!=len(raw) or m["evidence_sha256"]!=digest(raw)):
        return fail("manifest.evidence_checksum_or_length_mismatch")
    result["checksum_verified"]=True
    # Only after the delivered bytes have been authenticated against the
    # supplied checksum declaration do we parse evidence. No signature implied.
    result["producer_validation"]="declared_pass" if m["producer_validation"]=="pass" else "not_declared_pass"
    result["producer_preflight"]="declared_pass" if m["producer_preflight"]=="pass" else "not_declared_pass"
    v,doc=validate(raw,validator)
    p=profile(raw)
    result["consumer_validation"]=v["status"]
    result["consumer_validation_issues"]=v["issues"]
    result["consumer_preflight"]=p
    if doc is None or p["status"]!="within_profile":
        return fail("evidence.validation_or_profile_hold")
    run=doc["run"]
    # Exact equality to the evidence scope is a deliberately narrow first-run
    # convention: no inference that a broader authorization covers a target.
    if (not text(m["authorization_ref"]) or not text(m["run_id"])
            or m["run_id"]!=run["id"] or doc["producer"]["name"]!=pin["contract"]["owner"]
            or doc["producer"]["version"]!=reviewed_producer_commit
            or m["authorized_scope"]!=run["scope"]
            or m["started_at"]!=run["started_at"] or m["finished_at"]!=run["finished_at"]
            or m["coverage_limitations"]!=run["limitations"]
            or run["lifecycle"] not in {"completed","partial","failed","cancelled"}
            or run["finished_at"] is None):
        return fail("manifest.evidence_semantic_binding_mismatch")
    result["manifest_binding_verified"]=True
    if result["producer_validation"]!="declared_pass" or result["producer_preflight"]!="declared_pass":
        return fail("manifest.producer_checks_not_passed")
    result["disposition"]="candidate_for_joint_review"
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for name in ("schema","manifest","evidence","output"):
        ap.add_argument("--"+name,type=Path,required=True)
    ap.add_argument("--reviewed-producer-commit",required=True)
    args=ap.parse_args()
    try:
        pin=load_pin()
        validator=load_validator(read_local(args.schema),pin)
        m=read_local(args.manifest,limit=1024*1024)
        raw=read_local(args.evidence)
        report=verify(m,raw,args.evidence.name,validator,pin,args.reviewed_producer_commit)
        with args.output.open("x",encoding="utf-8") as f:
            json.dump(report,f,indent=2,ensure_ascii=True,allow_nan=False)
            f.write("\n")
        return 0 if report["disposition"]=="candidate_for_joint_review" else 2
    except (OSError,ValueError,ImportError,RecursionError):
        print("Exchange setup/read/write failed; no acceptance inferred.",file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
