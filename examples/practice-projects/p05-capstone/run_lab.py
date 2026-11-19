#!/usr/bin/env python3
"""P05 trusted offline exercise: patch disposable copies, run native checks, write receipt."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

LAB = Path(__file__).resolve().parent
ROOT = LAB.parents[2]
P03 = LAB.parent / "p03-persian-service"
PATCH_FILES = {"fa/guide/index.html", "fa/service/index.html", "en/service/index.html"}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def replace_once(text, old, new):
    require(text.count(old) == 1, "patch precondition failed")
    return text.replace(old, new, 1)


def hashes(root):
    files = {}
    for p in sorted(root.rglob("*")):
        require(not p.is_symlink(), "symlink in trusted fixture tree")
        if p.is_file():
            files[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return files


class Doc(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.root = None
        self.canonicals = []
        self.alternates = []
        self.links = []
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.root = a
        if tag == "link" and a.get("rel") == "canonical":
            self.canonicals.append(a["href"])
        if tag == "link" and a.get("rel") == "alternate":
            self.alternates.append({"tag": a["hreflang"], "url": a["href"]})
        if tag == "a":
            self.links.append(a.get("href"))


def apply(root, registry):
    """Fixed P03-A patch only. Validate all anchors before writing any file."""
    r = {p["id"]:p for p in registry["routes"]}
    gp, sp, ep = (root / r[i]["file"] for i in ("guide","service","service-en"))
    require({p.relative_to(root).as_posix() for p in (gp,sp,ep)} == PATCH_FILES,
            "unexpected fixture paths")
    g,s,e = (p.read_text(encoding="utf-8") for p in (gp,sp,ep))
    g = replace_once(g, '<html lang="fa" dir="ltr">', '<html lang="fa" dir="rtl">')
    g = replace_once(g, '<link rel="canonical" href="'+r["service"]["url"]+'">',
                     '<link rel="canonical" href="'+r["guide"]["url"]+'">')
    s = replace_once(s, '<button type="button">راهنما</button>',
                     '<a href="'+r["guide"]["path"]+'">'+r["guide"]["title"]+'</a>')
    en = '<link rel="alternate" hreflang="en" href="'+r["service-en"]["url"]+'">'
    fa = '<link rel="alternate" hreflang="fa" href="'+r["service"]["url"]+'">'
    default = '<link rel="alternate" hreflang="x-default" href="'+r["service"]["url"]+'">'
    e = replace_once(e, en, "\n".join((fa,en,default)))
    for p, text in ((gp,g),(sp,s),(ep,e)):
        p.write_bytes(text.encode("utf-8"))


def project(artifacts, registry):
    """Project explicit local declarations into existing fixture manifests.
    Retain mock status/intent; never claim these are HTTP observations."""
    ids = {r["id"]:r for r in registry["routes"]}
    docs = {i:Doc((artifacts/r["file"]).read_text(encoding="utf-8"))
            for i,r in ids.items() if r["state"]=="public"}
    loc = load(P03/"p03-a/locale.json")
    by_url = {r["url"]:i for i,r in ids.items() if i in docs}
    for row in loc["pages"]:
        d = docs[by_url[row["url"]]]
        require(len(d.canonicals)==1,"unexpected canonical count")
        row.update(canonical=d.canonicals[0],alternates=d.alternates)
    graph = load(P03/"p03-a/graph.json")
    # Only reviewed edge is changed; other synthetic graph observations preserved.
    edge = next(e for e in graph["links"] if e["from"]=="service" and e["to"]=="guide")
    if ids["guide"]["path"] in docs["service"].links:
        edge["kind"] = "crawlable"
    return loc,graph,docs


def run():
    registry=load(P03/"registry.json")
    ids={r["id"]:r for r in registry["routes"]}
    source=P03/"p03-a/artifacts"
    original=hashes(source)
    receipts={}
    with tempfile.TemporaryDirectory(prefix="p05-lab-") as name:
        work=Path(name)
        target=work/"artifacts"
        shutil.copytree(source,target)
        require(hashes(target)==original,"copy mismatch")

        def call(label,script,args,expected=0,report=False):
            cmd=[sys.executable,"-B",str(ROOT/"scripts"/script),*map(str,args)]
            out=work/(label+".json")
            if report:
                cmd += ["--output",str(out)]
            result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,encoding="utf-8",
                                  timeout=30)
            require(result.returncode==expected,"unexpected native exit: "+label)
            # Do not retain environment-dependent absolute paths or raw traces.
            entry={"script":script,"exit_code":result.returncode}
            if report:
                entry["report"]=load(out)
            else:
                entry["stdout"]=result.stdout
            receipts[label]=entry
            return entry.get("report",entry.get("stdout"))

        def save(name,data):
            p=work/name
            p.write_text(json.dumps(data,ensure_ascii=False,allow_nan=False),encoding="utf-8")
            return p

        q=call("clusters","cluster_keywords.py",["--input",P03/"queries.json"],report=True)
        pair=next(p for p in q["pairs"] if p["a"]=="Q1" and p["b"]=="Q7")
        require(pair["status"]=="candidate","unexpected clustering result")
        h=call("handoff","validate_research.py",["--input",P03/"handoff.json"],report=True)
        require(h["provisional"]==["U3","U4"],"unexpected research disposition")
        mapping={u["id"]:u for u in load(P03/"mapping.json")["units"]}
        require(mapping["U1"]["primary"]=="service" and mapping["U2"]["primary"]=="guide"
                and mapping["U5"]["status"]=="excluded","unexpected task ownership")
        pending=load(LAB/"backlog.json")
        before=call("priority-before","prioritize_opportunities.py",["--input",LAB/"backlog.json"],report=True)
        lanes={r["id"]:r["lane"] for r in before["rows"]}
        require(lanes["review-guide-copy"]=="blocked" and lanes["unsupported-hours"]=="excluded",
                "unexpected initial priorities")
        smoke_args=["--manifest",P03/"static-routes.json","--root",target]
        smoke=call("html-before","audit_html.py",smoke_args,expected=1)
        require("4 manifest entries; 1 findings" in smoke and "canonical mismatch" in smoke,
                "unexpected baseline local smoke")
        for rev, expected in (("before",3),):
            loc,graph,docs=project(target,registry)
            l=call("locale-"+rev,"audit_locale_manifest.py",["--input",save("locale-"+rev+"-input.json",loc)],1,True)
            require(len(l["findings"])==expected,"unexpected baseline locale findings")
            graph_before=call("graph-"+rev,"audit_topic_graph.py",["--input",save("graph-"+rev+"-input.json",graph)],report=True)
            require(next(p for p in graph_before["pages"] if p["id"]=="guide")["priority_unreachable"],
                    "unexpected baseline graph")
            require(docs["guide"].root=={"lang":"fa","dir":"ltr"},"unexpected baseline direction")

        apply(target,registry)
        revised=hashes(target)
        require(set(revised)==set(original),"file inventory changed")
        changed={k for k in original if original[k]!=revised[k]}
        require(changed==PATCH_FILES,"unexpected changed paths")
        smoke=call("html-after","audit_html.py",smoke_args)
        require("4 manifest entries; 0 findings" in smoke,"unexpected revised local smoke")
        loc,graph,docs=project(target,registry)
        require(docs["guide"].root=={"lang":"fa","dir":"rtl"} and
                docs["guide"].canonicals==[ids["guide"]["url"]],"guide acceptance failed")
        expected_alt=[{"tag":"fa","url":ids["service"]["url"]},
                      {"tag":"en","url":ids["service-en"]["url"]},
                      {"tag":"x-default","url":ids["service"]["url"]}]
        require(docs["service"].alternates==docs["service-en"].alternates==expected_alt,
                "alternate acceptance failed")
        l=call("locale-after","audit_locale_manifest.py",["--input",save("locale-after-input.json",loc)],1,True)
        require({(r["url"],r["reason"]) for r in l["findings"]}==
                {(ids[i]["url"],"alternate_set_differs_from_group") for i in ("service","service-en")},
                "unexpected remaining locale findings")
        gr=call("graph-after","audit_topic_graph.py",["--input",save("graph-after-input.json",graph)],report=True)
        guide=next(p for p in gr["pages"] if p["id"]=="guide")
        require(guide["depth"]==2 and not guide["priority_unreachable"],"guide graph acceptance failed")

        # Only local assertions just checked become verified, never actual external QA.
        verified={"repair-guide","repair-link","repair-alternates"}
        for item in pending:
            if item["id"] in verified:
                item["status"]="verified"
        priority=call("priority-after","prioritize_opportunities.py",["--input",save("backlog-after.json",pending)],report=True)
        after={r["id"]:r["lane"] for r in priority["rows"]}
        require(all(after[i]=="verified" for i in verified) and
                after["review-guide-copy"]=="growth" and after["actual-browser-qa"]=="review",
                "unexpected post-patch priorities")
        # Native T11: bind only actual local assertion; remaining requirements absent.
        subject={"stage":"candidate","scope_ref":"P05-four-local-public-documents",
                 "revision":"p05-local-patch","artifact":"sha256:"+hashlib.sha256(
                     json.dumps(revised,sort_keys=True).encode()).hexdigest(),
                 "environment":"disposable-offline-copy","profile":"explicit-head-fixture",
                 "config_ref":"P05-local-policy"}
        assertion="Four local public HTML documents pass explicit-head project-policy smoke"
        policy="P05-local-only-policy"
        # Hash actual recorded local result, not a fabricated runtime receipt.
        smoke_hash=hashlib.sha256(json.dumps(receipts["html-after"],sort_keys=True).encode()).hexdigest()
        gates={"schema_version":"2","release_id":"P05-local-review","subject":subject,
               "policy_ref":policy,"exposure":None,"gates":[
                   {"id":"local-html","required":True,"rationale":"Local smoke only","assertion":assertion,
                    "evidence":{"subject":subject,"outcome":"pass","ref":"receipt:html-after:sha256:"+smoke_hash,
                                "policy_ref":policy,"gate_id":"local-html","assertion":assertion}},
                   *[{"id":i,"required":True,"rationale":"Actual evidence absent","assertion":a,"evidence":None}
                     for i,a in (("browser-locale","Actual matched HTTP/browser locale and accessibility review"),
                                 ("access","Actual protected route and data authorization"),
                                 ("measurement","Actual consent/collection and outcome verification"))]]}
        gate=call("gate","review_release_gates.py",["--input",save("gate-input.json",gates)],report=True)
        require(gate["disposition"]=="hold" and not gate["deployment_authorized"] and
                set(gate["blockers"])=={"browser-locale","access","measurement"},
                "unexpected gate result")
        business=load(P03/"business-review.json")
        require(business["after"]["accepted_leads"]==business["before"]["accepted_leads"] and
                business["after"]["lead_events"]>business["before"]["lead_events"] and
                business["consent_network_verification"] is None,"unexpected business evidence")
        require(hashes(source)==original,"original fixture changed")
        result={"project_id":"P05","scope":"actual offline checks and edits on fictional local files only",
                "initial_hashes":original,"candidate_hashes":revised,"changed_files":sorted(changed),
                "source_unchanged":True,"local_verified_items":sorted(verified),
                "reports":receipts,"remaining_locale_profile_review":l["findings"],
                "business_evidence":business,"actual_external_verification":False,
                "deployment_authorized":False,"search_or_business_growth_established":False}
    result["disposable_copy_removed"]=not work.exists()
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    try:
        require(not a.out.resolve().is_relative_to(ROOT.resolve()),"output must be outside library")
        require(not a.out.exists() and not a.out.is_symlink(),"new output file required")
        result=run()
        with a.out.open("x",encoding="utf-8") as out:
            json.dump(result,out,ensure_ascii=False,allow_nan=False,indent=2)
            out.write("\n")
    except (OSError,ValueError,KeyError,TypeError,StopIteration,subprocess.SubprocessError) as exc:
        print("P05 lab failed:",exc)
        return 1
    print("P05 local exercise receipt written; external verification and release held.")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
