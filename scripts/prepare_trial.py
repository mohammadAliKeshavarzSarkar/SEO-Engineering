#!/usr/bin/env python3
"""Local TS04 staging and artifact checks, not an agent sandbox or runner."""
import argparse
import json
import os
import re
import stat
import subprocess
from pathlib import Path
from zipfile import ZipFile

if __package__:
    from .control_benchmark import check_schedule, ledger_index, fingerprint, ensure, blind_packet, finalize
    from .verify_package import verify, digest, ROOT, PREFIX
    from .score_benchmark import load, grade_items, EXPECTED, DISQUALIFIERS
else:
    from control_benchmark import check_schedule, ledger_index, fingerprint, ensure, blind_packet, finalize
    from verify_package import verify, digest, ROOT, PREFIX
    from score_benchmark import load, grade_items, EXPECTED, DISQUALIFIERS

RUBRIC_PREFIX=PREFIX+"references/library/evaluations/"
LABEL=re.compile(r"r-[0-9a-f]{32}")
MAX_ARTIFACT=16*1024*1024
# Explicit runtime installation layouts, not claims of discovery.
SKILL_LAYOUTS={"codex":".agents/skills/", "cursor":".cursor/skills/"}


def regular_bytes(path, limit=MAX_ARTIFACT):
    path=Path(path)
    ensure(stat.S_ISREG(path.lstat().st_mode),"not a regular file")
    with path.open("rb") as stream:
        raw=stream.read(limit+1)
    ensure(len(raw)<=limit,"file size limit")
    return raw


def fresh_write(path, raw):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)


def stage(root, suite, control, blind_id, archive, context, target, runtime_kind="codex"):
    """Stage one slot; parent paths must be trusted and stable."""
    ensure(runtime_kind in SKILL_LAYOUTS,"unsupported pilot runtime layout")
    check_schedule(suite,control)
    found=[s for s in control["slots"] if s["blind_id"]==blind_id]
    ensure(len(found)==1,"unknown slot")
    slot=found[0]
    cfg=control["plan"]["config"]
    # This narrow workspace implements the complete-toolkit comparison only.
    ensure(cfg["treatment"]=="complete_toolkit","instruction-only staging needs a separately matched tool setup")
    raw=regular_bytes(context)
    ensure(digest(raw)==cfg["task_context_sha256"],"common context digest mismatch")
    raw.decode("utf-8",errors="strict")
    receipt=verify(root,archive)
    ensure(receipt["archive_sha256"]==cfg["archive_sha256"],"candidate archive mismatch")
    target=Path(target)
    ensure(not target.exists() and not target.is_symlink(),"fresh target required")
    # Read and verify all selected bytes before creating files.
    selected={}
    omitted=[]
    if slot["arm"]=="skill":
        with ZipFile(archive) as z:
            for record in receipt["files"]:
                name=record["path"]
                if cfg["candidate_variant"]=="rubric_restricted" and name.startswith(RUBRIC_PREFIX):
                    omitted.append(name)
                    continue
                data=z.read(name)
                ensure(digest(data)==record["sha256"],"archive changed during stage")
                selected[SKILL_LAYOUTS[runtime_kind]+name]=data
        ensure(cfg["candidate_variant"]!="rubric_restricted" or
               RUBRIC_PREFIX+"cases.json" in omitted,"expected bundled rubric not excluded")
    target.mkdir()
    files={"context.txt":raw,**selected}
    for name,data in files.items():
        fresh_write(target/name,data)
    expected={name:digest(data) for name,data in files.items()}
    ensure(tree_hashes(target)==expected,"staged membership or bytes differ")
    return {"schema_version":"1","control_sha256":fingerprint(control),"blind_id":blind_id,
            "arm":slot["arm"],"candidate_variant":cfg["candidate_variant"],
            "source_commit_declared":cfg["skill_commit"],
            "runtime_kind":runtime_kind,
            "installed_skill_root":SKILL_LAYOUTS[runtime_kind]+"seo-engineering" if slot["arm"]=="skill" else None,
            "source_matched_archive_sha256":receipt["archive_sha256"],
            "context_sha256":digest(raw),"installed_files":expected,
            "omitted_archive_paths":omitted,"target_tree_sha256":fingerprint(expected),
            "runtime_activation":"not_tested","runtime_isolation":"not_verified",
            "rubric_leakage_review":"required","actual_model_run":False}


def tree_hashes(root):
    root=Path(root)
    ensure(root.is_dir() and not root.is_symlink(),"invalid tree root")
    files={}
    for folder,dirs,names in os.walk(root,followlinks=False):
        for name in dirs:
            ensure(not (Path(folder)/name).is_symlink(),"symlink directory")
        for name in names:
            p=Path(folder)/name
            files[p.relative_to(root).as_posix()]=digest(regular_bytes(p))
    return files


def initial_ledger(control):
    return {"control_sha256":fingerprint(control),"runs":[
        {"blind_id":s["blind_id"],"status":"not_started","session_ref":None,
         "environment_ref":None,"output_ref":None,"output_sha256":None,
         "trace_ref":None,"trace_sha256":None,"failure_reason":"not yet executed"}
        for s in control["slots"]]}


def check_artifacts(control,ledger,root):
    """Verify actual sanitized bytes at fixed arm-neutral paths; no arbitrary refs."""
    rows=ledger_index(control,ledger)
    root=Path(root)
    ensure(root.is_dir() and not root.is_symlink(),"invalid artifact root")
    records=[]
    sessions=set()
    # Keep a complete manifest of referenced evidence. Checking only references
    # would silently ignore undisclosed or stale files inside the artifact root.
    expected_paths=set()
    for ident,row in rows.items():
        ensure(isinstance(ident,str) and LABEL.fullmatch(ident),"invalid blind label")
        if row["status"]=="not_started":
            ensure(all(row[k] is None for k in
                       ("session_ref","environment_ref","output_ref","output_sha256",
                        "trace_ref","trace_sha256")),
                   "not-started slot contains execution references")
        session=row["session_ref"]
        if session is not None:
            ensure(isinstance(session,str) and session.strip() and session not in sessions,
                   "session reference reused or invalid")
            sessions.add(session)
        for kind in ("output","trace"):
            ref,h=row[kind+"_ref"],row[kind+"_sha256"]
            if ref is None and h is None:
                continue
            expected=ident+"/"+kind+".txt"
            ensure(ref==expected and isinstance(h,str) and re.fullmatch(r"[0-9a-f]{64}",h),
                   "invalid fixed artifact reference")
            folder=root/ident
            ensure(folder.is_dir() and not folder.is_symlink(),"invalid artifact directory")
            raw=regular_bytes(root/expected)
            ensure(raw and digest(raw)==h,"artifact missing, empty or changed")
            raw.decode("utf-8",errors="strict")
            expected_paths.add(expected)
            records.append({"blind_id":ident,"kind":kind,"bytes":len(raw),"sha256":h})

    # A fresh, dedicated evidence root must contain no undisclosed files,
    # unrelated slot directories or nested paths. We only inspect names/types;
    # this does not ingest unexpected private content. Empty known slot folders
    # are allowed for failures with no captured artifacts.
    observed_paths=set()
    for folder in root.iterdir():
        ensure(not folder.is_symlink(),"unexpected or symlink artifact root entry")
        ensure(folder.is_dir() and folder.name in rows,
               "unexpected artifact root entry")
        for item in folder.iterdir():
            ensure(not item.is_symlink() and item.is_file(),
                   "unexpected nonregular artifact entry")
            path=folder.name+"/"+item.name
            ensure(path in expected_paths,"undeclared artifact file")
            observed_paths.add(path)
    ensure(observed_paths==expected_paths,"artifact inventory mismatch")
    return {"control_sha256":fingerprint(control),"ledger_sha256":fingerprint(ledger),
            "verified_artifacts":records,"artifact_bytes_verified":True,
            "artifact_inventory_complete":True,
            "actual_execution_verified":False,"review_independence_verified":False}


def compare_reviewers(packet, first, second):
    """Agreement measurement, not adjudication or calibration against truth."""
    expected={r["blind_id"]:r for r in packet["records"]}
    def review_index(review):
        ensure(set(review)=={"packet_sha256","records"} and
               review["packet_sha256"]==fingerprint(packet),"review packet mismatch")
        out={}
        for row in review["records"]:
            ensure(set(row)=={"blind_id","reviewer","output_sha256","trace_sha256","expected","disqualifiers"},
                   "invalid review record shape")
            ident=row["blind_id"]
            ensure(ident in expected and ident not in out and
                   isinstance(row["reviewer"],str) and row["reviewer"].strip(),"invalid reviewer slot")
            r=expected[ident]
            ensure(all(row[k]==r[k] for k in ("output_sha256","trace_sha256")),"review artifact mismatch")
            for key,allowed in (("expected",EXPECTED),("disqualifiers",DISQUALIFIERS)):
                grade_items(row[key],len(r[key]),allowed)
            out[ident]=row
        return out
    a,b=review_index(first),review_index(second)
    overlap=sorted(a.keys()&b.keys())
    comparisons=0
    disagreements=[]
    for ident in overlap:
        ensure(a[ident]["reviewer"]!=b[ident]["reviewer"],"same reviewer identifier")
        for kind in ("expected","disqualifiers"):
            x={i["criterion"]:i["status"] for i in a[ident][kind]}
            y={i["criterion"]:i["status"] for i in b[ident][kind]}
            for n in sorted(x):
                comparisons+=1
                if x[n]!=y[n]:
                    disagreements.append({"blind_id":ident,"kind":kind,"criterion":n,
                                          "first":x[n],"second":y[n]})
    return {"packet_sha256":fingerprint(packet),"matched_review_records":len(overlap),
            "first_only":sorted(a.keys()-b.keys()),"second_only":sorted(b.keys()-a.keys()),
            "neither_reviewed":sorted(expected.keys()-(a.keys()|b.keys())),
            "criteria_compared":comparisons,"disagreements":disagreements,
            "agreement_rate":(comparisons-len(disagreements))/comparisons if comparisons else None,
            "adjudication_required":bool(disagreements) or len(overlap)!=len(expected) or not expected,
            "reviewer_independence_verified":False,"calibration_certified":False}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode",choices=("stage","init-ledger","verify-artifacts","blind","finalize","compare-reviewers"))
    for name in ("suite","control","archive","context","target","ledger","artifacts","packet","first","second","grades","out"):
        ap.add_argument("--"+name,type=Path)
    ap.add_argument("--blind-id")
    ap.add_argument("--runtime-kind",choices=sorted(SKILL_LAYOUTS),
                    help="Required for stage mode; use codex or cursor explicitly")
    a=ap.parse_args()
    try:
        if a.mode=="compare-reviewers":
            out=compare_reviewers(load(a.packet),load(a.first),load(a.second))
        else:
            suite,control=load(a.suite),load(a.control)
            check_schedule(suite,control)
            if a.mode=="stage":
                ensure(a.runtime_kind in SKILL_LAYOUTS,
                       "--runtime-kind is required for stage mode")
                actual=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
                ensure(actual==control["plan"]["config"]["skill_commit"],"source revision mismatch")
                ensure(not subprocess.check_output(["git","status","--porcelain","--untracked-files=all"],cwd=ROOT,text=True).strip(),
                       "require clean source checkout")
                out=stage(ROOT,suite,control,a.blind_id,a.archive,a.context,a.target,
                          runtime_kind=a.runtime_kind)
                out["source_checkout_revision_verified"]=True
            elif a.mode=="init-ledger":
                out=initial_ledger(control)
            else:
                ledger=load(a.ledger)
                checked=check_artifacts(control,ledger,a.artifacts)
                if a.mode=="verify-artifacts":
                    out=checked
                elif a.mode=="blind":
                    out=blind_packet(suite,control,ledger)
                else:
                    out=finalize(suite,control,ledger,load(a.grades))
                    out["artifact_verification"]=checked
        with a.out.open("x",encoding="utf-8") as s:
            json.dump(out,s,ensure_ascii=False,allow_nan=False,indent=2)
            s.write("\n")
        print("Written. SHA-256 (canonical JSON):",fingerprint(out))
    except (ValueError,TypeError,KeyError,AttributeError,OSError,UnicodeError,subprocess.CalledProcessError) as e:
        print("Trial preparation failed:",e)
        return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())
