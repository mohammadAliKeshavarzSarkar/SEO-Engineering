#!/usr/bin/env python3
"""Read-only, fail-closed integrity check of the initial staged pilot pair.

Operator-side tool. This checks local file identities only: no model invocation,
skill activation, process isolation, reviewer independence or release certification.
"""
import argparse
import json
import subprocess
from pathlib import Path

if __package__:
    from .build_skill import ROOT
    from .control_benchmark import check_schedule, ensure, fingerprint, ledger_index
    from .prepare_trial import (SKILL_LAYOUTS, RUBRIC_PREFIX, initial_ledger,
                                regular_bytes, tree_hashes)
    from .score_benchmark import load
    from .start_public_pilot import separate
    from .verify_package import digest, verify
else:
    from build_skill import ROOT
    from control_benchmark import check_schedule, ensure, fingerprint, ledger_index
    from prepare_trial import (SKILL_LAYOUTS, RUBRIC_PREFIX, initial_ledger,
                               regular_bytes, tree_hashes)
    from score_benchmark import load
    from start_public_pilot import separate
    from verify_package import digest, verify


def inspect(root, operator, workspaces):
    """Review a trusted source checkout and a private, unexecuted pilot packet."""
    root,operator,workspaces = (Path(x).resolve() for x in (root,operator,workspaces))
    separate((root,operator,workspaces))
    ensure(operator.is_dir() and not operator.is_symlink(), "invalid operator root")
    ensure(workspaces.is_dir() and not workspaces.is_symlink(), "invalid staged workspace root")
    suite=load(root/"evaluations/cases.json")
    control=load(operator/"control.json")
    check_schedule(suite,control)
    frozen=control["plan"]["config"]
    ensure(load(operator/"config.json")==frozen, "operator config differs from frozen plan")
    candidate=verify(root,operator/"candidate.zip")
    receipt=load(operator/"candidate-receipt.json")
    ensure(candidate["archive_sha256"]==receipt["archive_sha256"] and
           candidate["files"]==receipt["files"] and
           candidate["file_count"]==receipt["file_count"],
           "candidate receipt does not match source/archive")
    ensure(frozen["archive_sha256"]==candidate["archive_sha256"],
           "candidate digest differs from control")
    context=regular_bytes(operator/"context.txt")
    ensure(digest(context)==frozen["task_context_sha256"],
           "operator task context changed")
    ledger=load(operator/"ledger.json")
    ledger_index(control,ledger)
    ensure(ledger==initial_ledger(control), "pilot ledger no longer all-not-started")
    launch=load(operator/"launch.json")
    kind=launch["runtime_kind"]
    ensure(kind in SKILL_LAYOUTS,"unsupported staged runtime kind")
    ensure(launch["control_sha256"]==fingerprint(control) and
           launch["candidate_commit"]==frozen["skill_commit"] and
           launch["archive_sha256"]==candidate["archive_sha256"],
           "pilot launch identity mismatch")
    ensure(launch["actual_agent_runs"]==0 and
           launch["staged_slots"]==2 and launch["planned_slots"]==len(control["slots"]) and
           launch["runtime_activation_observed"] is False and
           launch["runtime_isolation"]=="not_verified",
           "pilot execution or activation cannot be inferred")
    pair=control["slots"][:2]
    ensure(len(pair)==2 and pair[0]["case_id"]==pair[1]["case_id"]
           and pair[0]["repeat"]==pair[1]["repeat"]
           and pair[0]["prompt"]==pair[1]["prompt"]
           and {s["arm"] for s in pair}=={"baseline","skill"},
           "first two frozen slots are not a matched pair")
    launch_rows=launch["first_pair_in_launch_order"]
    ensure(isinstance(launch_rows,list) and len(launch_rows)==2,
           "unexpected launch record count")
    recorded=[]
    for slot,record in zip(pair,launch_rows):
        ident=slot["blind_id"]
        target=workspaces/ident
        expected_prompt=operator/(ident+".prompt.txt")
        expected_receipt=operator/(ident+".staging.json")
        ensure(record=={"blind_id":ident,"arm":slot["arm"],
                        "case_id":slot["case_id"],
                        "workspace":str(target.resolve()),
                        "prompt_file":str(expected_prompt.resolve()),
                        "staging_receipt":str(expected_receipt.resolve())},
               "launch record differs from intended fixed slot paths")
        ensure(target.is_dir() and not target.is_symlink(),
               "invalid staged slot directory")
        text=regular_bytes(expected_prompt).decode("utf-8")
        expected_text=("Read context.txt in this workspace, then answer the following task.\n\n"
                       +slot["prompt"]+"\n")
        ensure(text==expected_text, "staged prompt changed")
        saved=load(expected_receipt)
        ensure(saved["blind_id"]==ident and saved["arm"]==slot["arm"]
               and saved["runtime_kind"]==kind and
               saved["control_sha256"]==fingerprint(control) and
               saved["source_matched_archive_sha256"]==candidate["archive_sha256"] and
               saved["source_commit_declared"]==frozen["skill_commit"] and
               saved["context_sha256"]==digest(context),
               "staging receipt identity mismatch")
        prefix=SKILL_LAYOUTS[kind]
        expected_files={"context.txt":digest(context)}
        omitted=[]
        if slot["arm"]=="skill":
            for item in candidate["files"]:
                name=item["path"]
                if frozen["candidate_variant"]=="rubric_restricted" and name.startswith(RUBRIC_PREFIX):
                    omitted.append(name)
                else:
                    expected_files[prefix+name]=item["sha256"]
            ensure(prefix+"seo-engineering/SKILL.md" in expected_files,
                   "skill entrypoint absent from staged treatment")
        ensure(saved["installed_skill_root"]==(prefix+"seo-engineering" if slot["arm"]=="skill" else None)
               and saved["omitted_archive_paths"]==omitted
               and saved["installed_files"]==expected_files
               and saved["target_tree_sha256"]==fingerprint(expected_files),
               "staging receipt does not match source-selected member identities")
        ensure(tree_hashes(target)==expected_files, "staged files changed or unexpected")
        ensure(saved["runtime_activation"]=="not_tested" and
               saved["runtime_isolation"]=="not_verified" and
               saved["actual_model_run"] is False,
               "staging receipt claims an unsupported runtime observation")
        recorded.append({"blind_id":ident,"arm":slot["arm"],
                         "context_sha256":digest(context),
                         "tree_sha256":fingerprint(expected_files),
                         "files":len(expected_files)})
    ensure(recorded[0]["context_sha256"]==recorded[1]["context_sha256"],
           "matched pair did not receive the same task context")
    return {"schema_version":"1","kind":"local_pilot_pair_integrity",
            "runtime_kind":kind,"candidate_commit_declared":frozen["skill_commit"],
            "archive_sha256":candidate["archive_sha256"],
            "control_sha256":fingerprint(control),"planned_slots":len(control["slots"]),
            "verified_unstarted_pair":recorded,
            "matched_task_and_prompt":True,
            "stage_bytes_matched_to_source_archive":True,
            "agent_runs_observed":0,
            "runtime_discovery_verified":False,
            "filesystem_read_isolation_verified":False,
            "independent_grading_verified":False,
            "release_approved":False,
            "status":"ready_for_operator_isolation_and_activation_review",
            "limitations":"Private local staging integrity only. Verify clean checkout, exact runtime version, actual permitted filesystem/network reads, activation, paid access, permission boundaries and reviewer authority separately. Re-review if files or candidate change."}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--operator",type=Path,required=True)
    ap.add_argument("--workspaces",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True,
                    help="New operator-private report file, outside source/agent workspace")
    args=ap.parse_args()
    try:
        source=ROOT.resolve()
        root=Path(args.workspaces).resolve()
        report_path=args.out.resolve()
        ensure(not report_path.is_relative_to(source) and
               not report_path.is_relative_to(root),
               "report must be outside source and agent workspace")
        actual=subprocess.check_output(["git","rev-parse","HEAD"],cwd=source,text=True).strip()
        ensure(not subprocess.check_output(["git","status","--porcelain","--untracked-files=all"],
                                          cwd=source,text=True).strip(),
               "clean checkout required")
        report=inspect(source,args.operator,args.workspaces)
        ensure(report["candidate_commit_declared"]==actual,
               "source checkout revision differs from candidate")
        with args.out.open("x",encoding="utf-8") as out:
            json.dump(report,out,ensure_ascii=False,allow_nan=False,indent=2)
            out.write("\n")
    except (OSError,ValueError,KeyError,TypeError,AttributeError,
            UnicodeError,subprocess.SubprocessError) as exc:
        print("Pilot first-pair review failed:",exc)
        return 1
    print("Offline pair integrity checked. Actual isolation, discovery and inference NOT tested.")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
