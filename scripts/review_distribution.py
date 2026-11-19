#!/usr/bin/env python3
"""Maintainer-only offline content triage and review bookkeeping.

Signals are heuristics, not confirmed exposures. Never emit matched values.
No network, remediation, licensing decision, or release authorization.
"""
import argparse
import hashlib
import json
import re
import stat
import subprocess
from pathlib import Path
from zipfile import ZipFile

if __package__:
    from .verify_package import ROOT, verify, digest
    from .score_benchmark import fingerprint, load
else:
    from verify_package import ROOT, verify, digest
    from score_benchmark import fingerprint, load

METHOD="distribution-pre-review-v1"
LIMIT=8*1024*1024
RULES={
    "private_key_marker":re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"),
    "token_shape":re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{35,}|sk-(?:proj-)?[A-Za-z0-9_-]{24,}|AKIA[A-Z0-9]{16})\b"),
    "credential_assignment":re.compile(r"""(?i)\b(?:password|passwd|client_secret|api[_-]?key|access[_-]?token|refresh[_-]?token)\s*["']?\s*[:=]\s*["'][^"'\r\n]{8,}["']"""),
    "url_userinfo":re.compile(r"(?i)\bhttps?://[^/\s@]+:[^/\s@]+@"),
    "url_sensitive_query":re.compile(r"(?i)[?&](?:token|access_token|api_key|signature|sig|password|auth|x-amz-signature)=[^&\s\"'<>]+"),
    "email_shape":re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "local_user_path":re.compile(r"(?i)(?:/Users/[^/\s]+/|/home/[^/\s]+/|[A-Z]:\\Users\\[^\\\s]+\\)"),
    "private_network_url":re.compile(r"(?i)\bhttps?://(?:localhost\b|127\.\d+\.\d+\.\d+|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+|\[::1\])"),
}
DISPOSITIONS={"synthetic_or_public_reference","approved_for_scope","requires_correction","unresolved"}
FILE_STATES={"reviewed_no_issue","reviewed_with_findings","requires_correction","unreviewed"}


def require(ok,message):
    if not ok:
        raise ValueError(message)


def tracked(root):
    raw=subprocess.check_output(["git","ls-files","-z"],cwd=root)
    names=raw.decode("utf-8",errors="strict").split("\0")
    names=[n for n in names if n]
    require(len(names)==len(set(names)),"duplicate tracked path")
    return sorted(names)


def safe_path(root,name):
    require(isinstance(name,str) and name and "\\" not in name and
            not name.startswith("/") and all(p not in ("",".","..") for p in name.split("/")),
            "unsafe tracked path")
    current=root
    for part in name.split("/"):
        current=current/part
        require(not current.is_symlink(),"symlink in tracked path")
    require(stat.S_ISREG(current.lstat().st_mode),"nonregular tracked resource")
    return current


def scan_bytes(raw):
    if len(raw)>LIMIT:
        return "size_limit",[]
    try:
        text=raw.decode("utf-8",errors="strict")
    except UnicodeError:
        return "non_utf8",[]
    if "\0" in text:
        return "binary_or_nul",[]
    signals=[]
    for number,line in enumerate(text.splitlines(),1):
        for rule,pattern in RULES.items():
            if pattern.search(line):
                signals.append({"rule":rule,"line":number})
    return "scanned",signals


def record(scope,path,raw):
    state,signals=scan_bytes(raw)
    fid=fingerprint({"scope":scope,"path":path,"sha256":digest(raw)})
    for signal in signals:
        signal["id"]=fingerprint({"file":fid,**signal})
    return {"id":fid,"scope":scope,"path":path,"sha256":digest(raw),
            "bytes":len(raw),"scan_status":state,"signals":signals}


def summarize(records):
    return {"files":len(records),"scanned":sum(r["scan_status"]=="scanned" for r in records),
            "unscanned":sum(r["scan_status"]!="scanned" for r in records),
            "signals":sum(len(r["signals"]) for r in records),
            "flagged_files":sum(bool(r["signals"]) for r in records)}


def scan(root,archive,commit,names=None):
    """Trusted stable checkout; names override is for synthetic tests only."""
    root=Path(root)
    require(isinstance(commit,str) and re.fullmatch(r"[0-9a-f]{40}",commit),"invalid commit")
    receipt=verify(root,archive)
    package=[]
    with ZipFile(archive) as z:
        for r in receipt["files"]:
            data=z.read(r["path"])
            require(digest(data)==r["sha256"],"archive changed")
            package.append(record("archive",r["path"],data))
    require(digest(Path(archive).read_bytes())==receipt["archive_sha256"],"archive changed")
    public=[]
    for name in tracked(root) if names is None else sorted(names):
        path=safe_path(root,name)
        # Hash every tracked file even if too large to scan; do not load large blobs.
        if path.stat().st_size>LIMIT:
            h=hashlib.sha256()
            size=0
            with path.open("rb") as stream:
                for chunk in iter(lambda:stream.read(65536),b""):
                    h.update(chunk)
                    size+=len(chunk)
            sha=h.hexdigest()
            public.append({"id":fingerprint({"scope":"tracked","path":name,"sha256":sha}),
                           "scope":"tracked","path":name,"sha256":sha,"bytes":size,
                           "scan_status":"size_limit","signals":[]})
        else:
            public.append(record("tracked",name,path.read_bytes()))
    require(len({r["id"] for r in package+public})==len(package+public),"duplicate record")
    return {"method":METHOD,"candidate_commit":commit,"archive_sha256":receipt["archive_sha256"],
            "summary":{"archive":summarize(package),"tracked":summarize(public)},
            "files":package+public,"human_review_required":True,
            "privacy_approved":False,"release_approved":False,
            "limitations":"Current tracked working tree and verified archive only; no history, untracked files, external sources, contextual identification or guaranteed secret detection."}


def blank_review(report):
    return {"report_sha256":fingerprint(report),"reviewer":"","authorization_ref":"",
            "files":[{"file_id":r["id"],"state":"unreviewed","evidence":""} for r in report["files"]],
            "findings":[{"signal_id":s["id"],"disposition":"unresolved","evidence":""}
                        for r in report["files"] for s in r["signals"]]}


def index(rows,key,expected):
    require(isinstance(rows,list),"invalid review rows")
    out={}
    for row in rows:
        ident=row[key]
        require(ident in expected and ident not in out,"unexpected or duplicate review identity")
        out[ident]=row
    require(set(out)==expected,"incomplete review inventory")
    return out


def review_status(report,review):
    require(review["report_sha256"]==fingerprint(report),"review report mismatch")
    files=index(review["files"],"file_id",{r["id"] for r in report["files"]})
    signals=index(review["findings"],"signal_id",{s["id"] for r in report["files"] for s in r["signals"]})
    for r in files.values():
        require(r["state"] in FILE_STATES,"invalid file review state")
        require(isinstance(r["evidence"],str),"invalid evidence")
        require(r["state"]=="unreviewed" or r["evidence"].strip(),"review evidence required")
    for r in signals.values():
        require(r["disposition"] in DISPOSITIONS,"invalid signal disposition")
        require(isinstance(r["evidence"],str),"invalid evidence")
        require(r["disposition"]=="unresolved" or r["evidence"].strip(),"finding evidence required")
    missing=sum(r["state"]=="unreviewed" for r in files.values())
    corrections=sum(r["state"]=="requires_correction" for r in files.values())
    unresolved=sum(r["disposition"] in {"unresolved","requires_correction"} for r in signals.values())
    # A file with signals cannot be declared reviewed_no_issue without explicit dispositions.
    inconsistent=sum(files[r["id"]]["state"]=="reviewed_no_issue" and bool(r["signals"]) for r in report["files"])
    reviewer=review.get("reviewer")
    grant=review.get("authorization_ref")
    complete=not(missing or corrections or unresolved or inconsistent) and all(
        isinstance(v,str) and v.strip() for v in (reviewer,grant))
    return {"report_sha256":fingerprint(report),"review_sha256":fingerprint(review),
            "unreviewed_files":missing,"files_requiring_correction":corrections,
            "unresolved_or_correction_signals":unresolved,"inconsistent_file_states":inconsistent,
            "review_record_complete":complete,"reviewer_independence_verified":False,
            "authorization_independently_verified":False,"privacy_approved":False,
            "release_approved":False}


def write(path,value):
    with path.open("x",encoding="utf-8") as s:
        json.dump(value,s,ensure_ascii=True,indent=2,allow_nan=False)
        s.write("\n")


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode",choices=("scan","prepare-review","check-review"))
    for k in ("archive","report","review","out"):
        p.add_argument("--"+k,type=Path)
    a=p.parse_args()
    try:
        if a.mode=="scan":
            commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
            require(not subprocess.check_output(["git","status","--porcelain","--untracked-files=no"],
                                               cwd=ROOT,text=True).strip(),"clean tracked checkout required")
            out=scan(ROOT,a.archive,commit)
            print("Distribution pre-review counts:",json.dumps(out["summary"],sort_keys=True))
        elif a.mode=="prepare-review":
            out=blank_review(load(a.report))
        else:
            out=review_status(load(a.report),load(a.review))
        write(a.out,out)
        print("Review record written; no privacy or release approval.")
    except (OSError,ValueError,TypeError,KeyError,AttributeError,subprocess.CalledProcessError):
        print("Distribution review failed; inspect inputs privately.")
        return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())
