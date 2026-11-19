#!/usr/bin/env python3
"""Synthetic differential comparison, never an operational evidence adapter."""
import argparse
import copy
import json
import re
import sys
from pathlib import Path

from interop.validate_crawl_evidence import digest, load_pin, load_validator, read_local, validate
from interop.exchange_profile import PROFILE_ID, PROFILE_AGREEMENT, profile


def write_json(path, data):
    with path.open("x", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=True, allow_nan=False, indent=2)
        f.write("\n")


def prepare(root, work):
    pin = load_pin()
    work.mkdir()
    cases = []
    def add(name, raw, expected, mode="required"):
        path = work / (name + ".json")
        with path.open("xb") as s:
            s.write(raw)
        cases.append({"id": name, "file": path.name, "sha256": digest(raw),
                      "expected": expected, "mode": mode})
    for fixture in pin["fixtures"]:
        path = root / fixture["path"]
        raw = read_local(path)
        if digest(raw) != fixture["sha256"]:
            raise ValueError("fixture checksum mismatch")
        add("fixture-" + path.stem, raw, fixture["expected"])
    fixtures = root / "packages/evidence-contract/fixtures/valid"
    base = json.loads(read_local(fixtures / "complete-page.json"))
    cross = json.loads(read_local(fixtures / "cross-page-diagnostic.json"))
    redirects = json.loads(read_local(fixtures / "redirect-repeated-headers.json"))
    def mutate(name, fn, expected="invalid", source=base, mode="required"):
        doc = copy.deepcopy(source)
        fn(doc)
        add(name, json.dumps(doc, ensure_ascii=True, allow_nan=False).encode(), expected, mode)
    def obs(d, key):
        return d["pages"][0]["observations"][key]
    def canonical(d, u):
        obs(d,"metadata")["value"]["canonical_urls"] = [u]
    def headers(d):
        return obs(d,"http")["value"]["transactions"][-1]["headers"]
    def override(d, paths):
        o = obs(d,"metadata")
        o["field_overrides"] = [{"path": p, "provenance":o["provenance"]} for p in paths]
    def wrong_scope(d):
        d["diagnostics"]["value"][0].update(evidence_scope="subject_page", related_page_ids=[])
    def unrelated(d):
        d["diagnostics"]["value"][0]["related_page_ids"] = ["missing-page"]
    def duplicate_tx(d):
        ts = obs(d,"http")["value"]["transactions"]
        ts[1]["id"] = ts[0]["id"]
    def discontinuity(d):
        obs(d,"http")["value"]["transactions"][0]["redirect_to"] = "https://example.com/elsewhere"
    def reverse_time(d):
        d["run"]["finished_at"] = "2026-11-18T09:59:59Z"
    def fractional_time(d):
        d["run"].update(started_at="2026-11-18T10:00:00.000900Z",
                        finished_at="2026-11-18T10:00:00.000100Z")
    mutate("secret-encoded-key", lambda d:canonical(d,"https://example.com/?%74oken=synthetic"))
    mutate("secret-userinfo", lambda d:canonical(d,"https://user:synthetic@example.com/"))
    mutate("secret-header-relative", lambda d:headers(d).append({"name":"location","values":["/login?access_token=synthetic"]}))
    mutate("secret-link-header", lambda d:headers(d).append({"name":"link","values":["</fa?sig=synthetic>; rel=alternate"]}))
    mutate("bad-header-url", lambda d:headers(d).append({"name":"location","values":["http://[broken"]}))
    mutate("ordinary-query", lambda d:canonical(d,"https://example.com/?page=2&lang=fa"),"valid")
    mutate("ordinary-relative-header",lambda d:headers(d).append({"name":"location","values":["/new?lang=fa"]}),"valid")
    mutate("pointer-valid",lambda d:override(d,["/title","/canonical_urls/0"]),"valid")
    mutate("pointer-missing",lambda d:override(d,["/missing"]))
    mutate("pointer-duplicate",lambda d:override(d,["/title","/title"]))
    mutate("pointer-overlap",lambda d:override(d,["/canonical_urls/0","/canonical_urls"]))
    mutate("pointer-invalid-escape",lambda d:override(d,["/title~2"]))
    mutate("pointer-leading-zero",lambda d:override(d,["/canonical_urls/00"]))
    mutate("unknown-reason",lambda d:obs(d,"rendering").update(reasons=["unknown_reason"]))
    mutate("cross-page-scope",wrong_scope,source=cross)
    mutate("cross-page-dangling",unrelated,source=cross)
    mutate("duplicate-transaction",duplicate_tx,source=redirects)
    mutate("redirect-discontinuity",discontinuity,source=redirects)
    mutate("reverse-run-time",reverse_time)
    mutate("finish-required",lambda d:d["run"].update(finished_at=None))
    mutate("coverage-mismatch",lambda d:d["run"]["coverage"].update(collected=0))
    mutate("integer-not-boolean",lambda d:d["run"]["limits"].update(max_pages=True))
    mutate("missing-policy",lambda d:d["diagnostics"]["value"][0].pop("policy_version"))
    mutate("invalid-header",lambda d:headers(d).append({"name":"set-cookie","values":["synthetic"]}))
    mutate("diagnostic-unavailable",lambda d:d["diagnostics"]["value"][0].update(observation_ids=[obs(d,"rendering")["id"]]))
    raw = json.dumps(base,ensure_ascii=True).encode()
    add("duplicate-escaped-key", b'{"\\u0063ontract": {},'+raw[1:], "invalid")
    add("malformed-json",b'{"\\q":1}',"invalid")
    add("nonfinite-json",b'{"x":NaN}',"invalid")
    # These are deliberately measured, not assumed matches or accepted canonical behavior.
    mutate("submillisecond-time-order",fractional_time,None,mode="review")
    mutate("unsafe-integer",lambda d:d["run"]["limits"].update(max_pages=9007199254740993),None,mode="review")
    mutate("unpaired-surrogate",lambda d:obs(d,"metadata")["value"].update(title=chr(0xD800)),None,mode="review")
    mutate("backslash-header",lambda d:headers(d).append({"name":"location","values":["https://example.com\\path"]}),None,mode="review")
    mutate("header-url-port",lambda d:headers(d).append({"name":"location","values":["https://example.com:99999/"]}),None,mode="review")
    mutate("uri-unicode-host",lambda d:canonical(d,"https://مثال.test/"),None,mode="review")
    mutate("timestamp-leap-second",lambda d:d["run"].update(finished_at="2026-12-31T23:59:60Z"),None,mode="review")
    mutate("del-in-link-header",lambda d:headers(d).append({"name":"link","values":["</fa>; title="+chr(127)]}),None,mode="review")
    mutate("control-in-link-parameter",lambda d:headers(d).append({"name":"link","values":["</fa>; title="+chr(9)]}),None,mode="review")
    mutate("fractional-integer-spelling",lambda d:d["run"]["limits"].update(max_pages=10.0),None,mode="review")
    add("negative-zero-spelling",re.sub(rb'("max_pages"\s*:\s*)[0-9]+',rb'\g<1>-0',raw,count=1),None,mode="review")
    add("utf8-bom",b"\xef\xbb\xbf"+raw,None,mode="review")
    write_json(work/"manifest.json", {"producer_commit":pin["producer_commit"], "cases":cases})
    print("Prepared",len(cases),"immutable synthetic input files")


def compare(root, work, ts_path, out):
    pin=load_pin()
    schema=read_local(root/pin["contract"]["schema_path"])
    validator=load_validator(schema,pin)
    manifest=json.loads(read_local(work/"manifest.json"))
    ts=json.loads(read_local(ts_path))
    if manifest["producer_commit"] != pin["producer_commit"]:
        raise ValueError("wrong manifest identity")
    cases=manifest["cases"]
    if len({c["id"] for c in cases}) != len(cases):
        raise ValueError("duplicate case identity")
    if set(ts["results"]) != {c["id"] for c in cases}:
        raise ValueError("missing or extra TypeScript results")
    rows=[]
    for case in cases:
        raw=read_local(work/case["file"])
        if digest(raw)!=case["sha256"]:
            raise ValueError("input changed")
        py,doc=validate(raw,validator)
        t=ts["results"][case["id"]]
        if t["sha256"] != case["sha256"]:
            raise ValueError("TypeScript read different input")
        both_valid=py["status"]==t["status"]=="valid"
        preserved=None if not both_valid else (
            t.get("preservation") is True and doc==t.get("document") and doc==json.loads(raw))
        matched=py["status"]==t["status"] and py["status"] in ("valid","invalid") and preserved is not False
        if case["mode"]=="required":
            status="pass" if matched and py["status"]==case["expected"] else "fail"
        else:
            status="review_match" if matched else "review_difference"
        p = profile(raw)
        candidate = both_valid and preserved is True and p["status"] == "within_profile"
        expected_candidate = case["mode"] == "required" and case["expected"] == "valid"
        profile_ok = candidate == expected_candidate
        rows.append({"id":case["id"],"mode":case["mode"],"expected":case["expected"],
                     "profile":p,"joint_candidate":candidate,"profile_expected":expected_candidate,
                     "profile_gate_pass":profile_ok,
                     "input_sha256":case["sha256"],"typescript":t["status"],"python":py["status"],
                     "preservation":preserved,"result":status,
                     "typescript_codes":t.get("codes",[]),
                     "python_codes":[x["code"] for x in py["issues"]]})
    summary={k:sum(row["result"]==k for row in rows) for k in ("pass","fail","review_match","review_difference")}
    summary["profile_pass"] = sum(row["profile_gate_pass"] for row in rows)
    summary["profile_fail"] = len(rows)-summary["profile_pass"]
    summary["joint_candidates"] = sum(row["joint_candidate"] for row in rows)
    report={"profile_id":PROFILE_ID,"profile_agreement":PROFILE_AGREEMENT,
            "producer_commit":pin["producer_commit"],"schema_sha256":pin["contract"]["schema_sha256"],
            "node":ts["node"],"python":sys.version.split()[0],"summary":summary,"cases":rows,
            "actual_exchange_verified":False,"operational_integration_approved":False,
            "edge_review_required":True}
    write_json(out,report)
    for row in rows:
        print(row["id"],row["typescript"],row["python"],row["result"],"preservation="+str(row["preservation"]))
    print("DIFFERENTIAL_SUMMARY",json.dumps(summary,sort_keys=True))
    return 1 if summary["fail"] or summary["profile_fail"] else 0


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("operation",choices=("prepare","compare"))
    ap.add_argument("--producer-root",required=True,type=Path)
    ap.add_argument("--work",required=True,type=Path)
    ap.add_argument("--typescript-results",type=Path)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    if args.operation=="prepare":
        prepare(args.producer_root,args.work)
        return 0
    if args.typescript_results is None or args.output is None:
        ap.error("compare needs --typescript-results and --output")
    return compare(args.producer_root,args.work,args.typescript_results,args.output)


if __name__=="__main__":
    raise SystemExit(main())
