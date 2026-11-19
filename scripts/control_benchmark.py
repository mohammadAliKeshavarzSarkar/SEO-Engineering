#!/usr/bin/env python3
"""Maintainer-only trial control: no inference or grading performed here."""
import argparse
import hashlib
import json
import random
import re
from pathlib import Path
if __package__:
    from .score_benchmark import prepare, score, fingerprint, cases_index, load, nonempty
else:
    from score_benchmark import prepare, score, fingerprint, cases_index, load, nonempty

ARMS=("baseline","skill")
STATES=("completed","incomplete","timeout","error","not_started")
SHA=re.compile(r"[0-9a-f]{64}")
COMMIT=re.compile(r"[0-9a-f]{40}")
REQUIRED={"model","runtime","inference_settings","tool_config","permission_mode",
          "skill_commit","archive_sha256","launch_protocol","review_protocol",
          "suite_kind","repeats","treatment","task_context_sha256","seed",
          "budget","rubric_access_policy","candidate_variant"}
CONFIG_TEXT=REQUIRED-{"repeats","seed"}


def ensure(condition,message):
    if not condition:
        raise ValueError(message)


def exact(obj,keys):
    ensure(isinstance(obj,dict) and set(obj)==set(keys),"invalid record fields")


def sha(value,pattern=SHA):
    return isinstance(value,str) and pattern.fullmatch(value) is not None


def real_text(value):
    return nonempty(value) and not any(t in value.lower() for t in ("replace","placeholder","todo","<fill"))


def validate_config(config):
    exact(config,REQUIRED)
    for k in CONFIG_TEXT:
        ensure(real_text(config[k]),"missing reviewed config: "+k)
    ensure(sha(config["skill_commit"],COMMIT) and sha(config["archive_sha256"])
           and sha(config["task_context_sha256"]),"commit, archive and context identities required")
    ensure(type(config["seed"]) is int and 0<=config["seed"]<2**64,"invalid seed")
    ensure(config["suite_kind"] in ("public_regression","held_out"),"invalid suite kind")
    ensure(config["treatment"] in ("instruction_only","complete_toolkit"),"invalid treatment")
    ensure(config["candidate_variant"] in ("unmodified","rubric_restricted"),"invalid candidate variant")
    ensure(config["suite_kind"]!="held_out" or config["candidate_variant"]=="unmodified",
           "held-out requires unmodified candidate")
    ensure(config["suite_kind"]!="public_regression" or config["candidate_variant"]=="rubric_restricted",
           "public regression requires rubric-restricted access with disclosed treatment")


def frozen_subset(suite,ids):
    index=cases_index(suite)
    ensure(isinstance(ids,list) and ids and all(isinstance(i,str) for i in ids)
           and len(ids)==len(set(ids)) and set(ids)<=index.keys(),"invalid cohort")
    return {"version":suite["version"],"cases":[index[i] for i in ids]}


def schedule(suite,config,ids):
    validate_config(config)
    cohort=frozen_subset(suite,ids)
    plan=prepare(cohort,config)
    prng=random.Random(config["seed"])
    tasks=list(plan["tasks"])
    prng.shuffle(tasks)
    # Within each pair, alternate launch order after randomizing pair order.
    # This balances the two arms to within one pair even for odd cohorts.
    first=prng.randrange(2)
    slots=[]
    for index,t in enumerate(tasks):
        arms=ARMS if (index+first)%2==0 else ARMS[::-1]
        for arm in arms:
            blind_id="r-"+format(prng.getrandbits(128),"032x")
            slots.append({"blind_id":blind_id,"case_id":t["case_id"],"repeat":t["repeat"],
                          "arm":arm,"prompt":t["prompt"]})
    ensure(len({x["blind_id"] for x in slots})==len(slots),"duplicate blind id")
    presentation=[s["blind_id"] for s in slots]
    prng.shuffle(presentation)
    return {"schema_version":"1","full_suite_sha256":fingerprint(suite),
            "cohort_ids":ids,"plan":plan,"plan_sha256":fingerprint(plan),
            "slots":slots,"presentation_order":presentation,
            "actual_runs_executed":False,"independent_grading_completed":False}


def check_schedule(suite,control):
    expected=schedule(suite,control["plan"]["config"],control["cohort_ids"])
    ensure(control==expected,"control differs from frozen suite/config")


def dispatch(control,blind_id):
    found=[s for s in control["slots"] if s["blind_id"]==blind_id]
    ensure(len(found)==1,"unknown dispatch slot")
    return {"prompt":found[0]["prompt"]}
    # Operator separately applies the arm's environment. Never hand the
    # control record, rubric, blind label or arm name to the model.


def ledger_index(control,ledger):
    exact(ledger,{"control_sha256","runs"})
    ensure(ledger["control_sha256"]==fingerprint(control),"ledger/control mismatch")
    ids={s["blind_id"] for s in control["slots"]}
    rows={}
    ensure(isinstance(ledger["runs"],list),"runs must be array")
    for row in ledger["runs"]:
        exact(row,{"blind_id","status","session_ref","environment_ref","output_ref",
                   "output_sha256","trace_ref","trace_sha256","failure_reason"})
        ident=row["blind_id"]
        ensure(ident in ids and ident not in rows,"invalid or duplicate execution slot")
        ensure(row["status"] in STATES,"invalid execution status")
        if row["status"]=="completed":
            ensure(all(nonempty(row[k]) for k in ("session_ref","environment_ref","output_ref","trace_ref"))
                   and sha(row["output_sha256"]) and sha(row["trace_sha256"])
                   and row["failure_reason"] is None,"completed slot lacks artifact identities")
        else:
            ensure(nonempty(row["failure_reason"]),"missing failure reason")
        rows[ident]=row
    ensure(set(rows)==ids,"ledger must account for every planned slot")
    return rows


def blind_packet(suite,control,ledger):
    check_schedule(suite,control)
    rows=ledger_index(control,ledger)
    slots={s["blind_id"]:s for s in control["slots"]}
    cases=cases_index(suite)
    result=[]
    for ident in control["presentation_order"]:
        row=rows[ident]
        if row["status"]!="completed":
            continue
        case=cases[slots[ident]["case_id"]]
        # No arm, repeat, session/environment refs, or order from execution.
        # References must themselves be sanitized and arm-neutral.
        result.append({"blind_id":ident,"prompt":case["prompt"],
                       "expected":case["expected"],"disqualifiers":case["disqualifiers"],
                       "output_ref":row["output_ref"],"output_sha256":row["output_sha256"],
                       "trace_ref":row["trace_ref"],"trace_sha256":row["trace_sha256"]})
    packet={"schema_version":"1","records":result}
    return packet


def finalize(suite,control,ledger,grades):
    packet=blind_packet(suite,control,ledger)
    exact(grades,{"packet_sha256","records"})
    ensure(grades["packet_sha256"]==fingerprint(packet),"grades/packet mismatch")
    records={r["blind_id"]:r for r in packet["records"]}
    slots={s["blind_id"]:s for s in control["slots"]}
    rows=ledger_index(control,ledger)
    seen=set()
    converted=[]
    ensure(isinstance(grades["records"],list),"grades records must be array")
    for g in grades["records"]:
        exact(g,{"blind_id","reviewer","output_sha256","trace_sha256","expected","disqualifiers"})
        ident=g["blind_id"]
        ensure(ident in records and ident not in seen,"grade not bound to completed slot")
        seen.add(ident)
        record=records[ident]
        ensure(g["output_sha256"]==record["output_sha256"] and
               g["trace_sha256"]==record["trace_sha256"],"grade artifact mismatch")
        slot=slots[ident]
        converted.append({k:slot[k] for k in ("case_id","repeat","arm")}|
                         {k:g[k] for k in ("reviewer","expected","disqualifiers")}|
                         {k:record[k] for k in ("output_ref","trace_ref")})
    cohort=frozen_subset(suite,control["cohort_ids"])
    report=score(cohort,control["plan"],{"plan_sha256":control["plan_sha256"],"runs":converted})
    report["control_sha256"]=fingerprint(control)
    report["ledger_sha256"]=fingerprint(ledger)
    report["packet_sha256"]=fingerprint(packet)
    report["execution_counts"]={a:{state:sum(rows[s["blind_id"]]["status"]==state
        for s in control["slots"] if s["arm"]==a) for state in STATES} for a in ARMS}
    report["completed_ungraded"]=len(records)-len(seen)
    report["independent_execution_verified"]=False
    report["independent_review_verified"]=False
    report["release_certified"]=False
    return report


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode",choices=("schedule","dispatch","blind","finalize"))
    for name in ("suite","config","cohort","control","ledger","grades","out"):
        ap.add_argument("--"+name,type=Path)
    ap.add_argument("--blind-id")
    a=ap.parse_args()
    try:
        suite=load(a.suite)
        if a.mode=="schedule":
            result=schedule(suite,load(a.config),load(a.cohort)["case_ids"])
        else:
            control=load(a.control)
            check_schedule(suite,control)
            if a.mode=="dispatch":
                result=dispatch(control,a.blind_id)
            elif a.mode=="blind":
                result=blind_packet(suite,control,load(a.ledger))
            else:
                result=finalize(suite,control,load(a.ledger),load(a.grades))
        with a.out.open("x",encoding="utf-8") as stream:
            json.dump(result,stream,ensure_ascii=False,allow_nan=False,indent=2)
            stream.write("\n")
        print("Written. SHA-256 (canonical JSON):",fingerprint(result))
    except (ValueError,TypeError,KeyError,AttributeError,OSError) as exc:
        print("Benchmark control failed:",exc)
        return 1
    return 0


if __name__=="__main__":
    raise SystemExit(main())
