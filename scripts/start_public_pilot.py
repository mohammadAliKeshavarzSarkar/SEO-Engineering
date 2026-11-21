#!/usr/bin/env python3
"""Prepare a real public-pilot operator packet without launching paid inference.

Use a dedicated, clean checkout and separate operator/agent directories.
The runtime's filesystem isolation must be established by the operator.
"""
import argparse
import json
import subprocess
from pathlib import Path

if __package__:
    from .build_skill import build, ROOT
    from .verify_package import digest, verify
    from .control_benchmark import schedule, fingerprint, ensure, dispatch
    from .prepare_trial import stage, initial_ledger, regular_bytes, SKILL_LAYOUTS
    from .score_benchmark import load
else:
    from build_skill import build, ROOT
    from verify_package import digest, verify
    from control_benchmark import schedule, fingerprint, ensure, dispatch
    from prepare_trial import stage, initial_ledger, regular_bytes, SKILL_LAYOUTS
    from score_benchmark import load

DERIVED={"skill_commit","archive_sha256","task_context_sha256"}
COMMON_CONTEXT=(
    "Read-only synthetic SEO engineering task. Use only the supplied task and "
    "resources visible in this isolated workspace. Do not contact websites, "
    "edit files, disclose secrets or claim execution not actually observed. "
    "Identify assumptions and limitations. Return your engineering decision "
    "and verification plan; do not invent evidence.\n"
)


def new_json(path,value):
    with path.open("x",encoding="utf-8") as s:
        json.dump(value,s,ensure_ascii=False,allow_nan=False,indent=2)
        s.write("\n")


def separate(paths):
    resolved=[Path(p).resolve() for p in paths]
    ensure(all(a!=b and not a.is_relative_to(b) and not b.is_relative_to(a)
               for i,a in enumerate(resolved) for b in resolved[i+1:]),
           "checkout, operator and workspace roots must be distinct and non-nested")


def prepare(root, commit, config, operator, workspaces, context_bytes=None, runtime_kind="codex"):
    """Prepare the 32-slot public pilot, staging only the first pair."""
    ensure(runtime_kind in SKILL_LAYOUTS,"runtime kind must be codex or cursor")
    ensure(isinstance(config,dict),"invalid operator config")
    # Prevent an obvious runtime/layout mismatch even with a free-text version field.
    declared=config.get("runtime","")
    ensure(isinstance(declared,str),"invalid declared runtime")
    mentioned={kind for kind in SKILL_LAYOUTS if kind in declared.lower()}
    ensure(not mentioned or mentioned=={runtime_kind},
           "declared runtime differs from installation layout")
    root,operator,workspaces=map(Path,(root,operator,workspaces))
    separate((root,operator,workspaces))
    ensure(not operator.exists() and not operator.is_symlink()
           and not workspaces.exists() and not workspaces.is_symlink(),"fresh roots required")
    ensure(operator.parent.is_dir() and workspaces.parent.is_dir(),"parent directories must exist")
    ensure(isinstance(config,dict) and not (DERIVED & config.keys()),
           "omit source, archive and context hashes from operator config; derived from bytes")
    ensure(config.get("suite_kind")=="public_regression" and
           config.get("candidate_variant")=="rubric_restricted" and
           config.get("treatment")=="complete_toolkit" and config.get("repeats")==1,
           "initial pilot must use one-repeat restricted public complete-toolkit treatment")
    suite=load(root/"evaluations/cases.json")
    cohort=load(root/"evaluations/public-pilot.json")
    ensure(len(cohort["case_ids"])==16,"unexpected public pilot cohort")
    context=COMMON_CONTEXT.encode("utf-8") if context_bytes is None else context_bytes
    ensure(context and len(context)<=16*1024*1024,"invalid shared context size")
    context.decode("utf-8",errors="strict")
    # Validate all operator settings before leaving a partial staging directory.
    # Temporary digest is used only to check shape; never used in exported data.
    schedule(suite,config|{"skill_commit":commit,"archive_sha256":"0"*64,
                           "task_context_sha256":digest(context)},cohort["case_ids"])
    operator.mkdir(mode=0o700)
    archive=operator/"candidate.zip"
    build(root,archive)
    receipt=verify(root,archive)
    supplied=operator/"context.txt"
    with supplied.open("xb") as s:
        s.write(context)
    frozen=config|{"skill_commit":commit,"archive_sha256":receipt["archive_sha256"],
                   "task_context_sha256":digest(context)}
    control=schedule(suite,frozen,cohort["case_ids"])
    new_json(operator/"config.json",frozen)
    new_json(operator/"candidate-receipt.json",receipt)
    new_json(operator/"control.json",control)
    new_json(operator/"ledger.json",initial_ledger(control))
    (operator/"artifacts").mkdir()
    (operator/"launch-records").mkdir()
    workspaces.mkdir(mode=0o700)
    pair=control["slots"][:2]
    ensure(len(pair)==2 and pair[0]["case_id"]==pair[1]["case_id"]
           and pair[0]["repeat"]==pair[1]["repeat"]
           and pair[0]["prompt"]==pair[1]["prompt"]
           and {s["arm"] for s in pair}=={"baseline","skill"},
           "first two slots must be an exact matched pair")
    launch=[]
    for s in pair:
        ident=s["blind_id"]
        target=workspaces/ident
        r=stage(root,suite,control,ident,archive,supplied,target,runtime_kind=runtime_kind)
        prompt=dispatch(control,ident)["prompt"]
        # Same fixed context instruction for both arms; no arm indicator.
        with (operator/(ident+".prompt.txt")).open("x",encoding="utf-8") as fp:
            fp.write("Read context.txt in this workspace, then answer the following task.\n\n"+prompt+"\n")
        new_json(operator/(ident+".staging.json"),r)
        launch.append({"blind_id":ident,"arm":s["arm"],"case_id":s["case_id"],
                       "workspace":str(target.resolve()),"prompt_file":str((operator/(ident+".prompt.txt")).resolve()),
                       "staging_receipt":str((operator/(ident+".staging.json")).resolve())})
    report={"control_sha256":fingerprint(control),"candidate_commit":commit,
            "runtime_kind":runtime_kind,
            "runtime_activation_observed":False,
            "archive_sha256":receipt["archive_sha256"],"planned_slots":len(control["slots"]),
            "staged_slots":2,"first_pair_in_launch_order":launch,
            "actual_agent_runs":0,"runtime_activation":"not_tested","runtime_isolation":"not_verified",
            "reviewer_calibration":"not_performed","status":"awaiting_operator_runtime_check"}
    new_json(operator/"launch.json",report)
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--settings",type=Path,required=True)
    p.add_argument("--operator",type=Path,required=True)
    p.add_argument("--workspaces",type=Path,required=True)
    p.add_argument("--context",type=Path)
    p.add_argument("--runtime-kind",choices=sorted(SKILL_LAYOUTS),required=True,
                   help="Explicit project skill installation location; not activation verification")
    args=p.parse_args()
    try:
        actual=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
        ensure(not subprocess.check_output(["git","status","--porcelain","--untracked-files=all"],
                                           cwd=ROOT,text=True).strip(),"clean source checkout required")
        r=prepare(ROOT,actual,load(args.settings),args.operator,args.workspaces,
                  regular_bytes(args.context) if args.context else None,
                  runtime_kind=args.runtime_kind)
        print(json.dumps(r,indent=2))
    except (OSError,ValueError,TypeError,KeyError,AttributeError,subprocess.CalledProcessError) as exc:
        print("Pilot preparation failed:",exc)
        return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())
