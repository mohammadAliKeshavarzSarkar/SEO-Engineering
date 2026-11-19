"""Offline P03 native tool tests and explicit fixture crosswalk; no live locale or market QA."""
import json
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from scripts.build_skill import collect

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples/practice-projects/p03-persian-service"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.root = None
        self.alternates = []
        self.links = []
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.root = a
        if tag == "link" and a.get("rel") == "alternate":
            self.alternates.append({"tag":a["hreflang"],"url":a["href"]})
        if tag == "a":
            self.links.append(a.get("href"))


class PracticeP03Tests(unittest.TestCase):
    def cli(self, script, *args):
        return subprocess.run([sys.executable,"-B",str(ROOT/"scripts"/script),*map(str,args)],
                              cwd=ROOT,capture_output=True,text=True,timeout=20)

    def report(self, script, path, code=0):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/"report.json"
            p = self.cli(script,"--input",LAB/path,"--output",output)
            self.assertEqual(p.returncode,code,p.stdout+p.stderr)
            return load(output)

    def test_query_keys_and_candidates_do_not_override_business_fit(self):
        r = self.report("cluster_keywords.py","queries.json")
        keys = {q["id"]:q for q in r["queries"]}
        pairs = {(p["a"],p["b"]):p for p in r["pairs"]}
        for a,b in (("Q1","Q2"),("Q3","Q4")):
            self.assertNotEqual(keys[a]["raw_query"],keys[b]["raw_query"])
            self.assertEqual(keys[a]["match_key"],keys[b]["match_key"])
            self.assertEqual(pairs[a,b]["status"],"candidate")
        self.assertIn("scope_missing_or_different",pairs["Q1","Q6"]["reasons"])
        self.assertIn("insufficient_comparable_results",pairs["Q1","Q5"]["reasons"])
        self.assertEqual(pairs["Q1","Q7"]["status"],"candidate")
        units = {u["id"]:u for u in load(LAB/"mapping.json")["units"]}
        self.assertEqual(units["U5"]["status"],"excluded")
        self.assertIsNone(units["U5"]["primary"])
        self.assertEqual((units["U1"]["primary"],units["U2"]["primary"]),("service","guide"))
        self.assertTrue(all(units[i]["primary"] is None for i in ("U3","U4","U5")))
        self.assertEqual(r["status"],"review_required")

    def test_handoff_unknown_not_zero_and_provisional(self):
        r = self.report("validate_research.py","handoff.json")
        self.assertTrue(r["valid_structure"])
        self.assertEqual((r["evidence_count"],r["decision_count"]),(5,5))
        self.assertEqual(r["provisional"],["U3","U4"])
        e = {e["id"]:e for e in load(LAB/"handoff.json")["evidence"]}
        self.assertIsNone(e["E2"]["value"])
        self.assertEqual(e["E3"]["value"],0)
        self.assertTrue(r["review_required"])

    def test_graph_actual_before_after_reports(self):
        a,b = [self.report("audit_topic_graph.py",rev+"/graph.json") for rev in ("p03-a","p03-b")]
        ra,rb = ({p["id"]:p for p in r["pages"]} for r in (a,b))
        self.assertTrue(ra["guide"]["priority_unreachable"])
        self.assertIsNone(ra["guide"]["depth"])
        self.assertEqual(rb["guide"]["depth"],2)
        self.assertFalse(rb["guide"]["priority_unreachable"])
        self.assertEqual(rb["guide"]["unique_inbound_sources"],1)
        self.assertNotIn("account",rb)
        self.assertNotIn("planned",rb)

    def test_locale_profile_findings_and_local_html(self):
        reg = {r["id"]:r for r in load(LAB/"registry.json")["routes"]}
        a,b = [self.report("audit_locale_manifest.py",rev+"/locale.json",1) for rev in ("p03-a","p03-b")]
        def findings(r):
            return {(x["url"],x["reason"]) for x in r["findings"]}
        expected = {(reg[i]["url"],"alternate_set_differs_from_group") for i in ("service","service-en")}
        self.assertEqual(findings(a),expected|{(reg["guide"]["url"],"non_self_canonical_review")})
        self.assertEqual(findings(b),expected)
        for rev,code,n in (("p03-a",1,1),("p03-b",0,0)):
            p = self.cli("audit_html.py","--manifest",LAB/"static-routes.json","--root",LAB/rev/"artifacts")
            self.assertEqual(p.returncode,code,p.stdout+p.stderr)
            self.assertIn(f"4 manifest entries; {n} findings",p.stdout)
            if code:
                self.assertIn(reg["guide"]["url"]+": canonical mismatch",p.stdout)

    def test_registry_crosswalk_html_literals_and_packaging(self):
        reg = load(LAB/"registry.json")
        ids = {r["id"]:r for r in reg["routes"]}
        pub = {r["id"]:r for r in reg["routes"] if r["state"]=="public"}
        self.assertEqual({r["url"]:r["file"] for r in load(LAB/"static-routes.json")},
                         {r["url"]:r["file"] for r in pub.values()})
        mapping = load(LAB/"mapping.json")
        self.assertEqual({p["id"]:p["url"] for p in mapping["pages"]},{i:r["url"] for i,r in ids.items()})
        self.assertEqual({u["id"] for u in mapping["units"]},{d["id"] for d in load(LAB/"handoff.json")["decisions"]})
        self.assertEqual({q for u in mapping["units"] for q in u["query_ids"]},{q["id"] for q in load(LAB/"queries.json")})
        for rev in reg["revisions"]:
            locale = {p["url"]:p for p in load(LAB/rev/"locale.json")["pages"]}
            graph = load(LAB/rev/"graph.json")
            self.assertEqual(set(locale),{r["url"] for r in pub.values()})
            self.assertEqual({r["id"] for r in graph["pages"]},set(ids))
            for ident,r in pub.items():
                doc = Document(LAB/rev/"artifacts"/r["file"])
                direction = "ltr" if r["locale"]=="en" or (rev=="p03-a" and ident=="guide") else "rtl"
                self.assertEqual(doc.root,{"lang":r["locale"],"dir":direction})
                self.assertEqual(doc.alternates,locale[r["url"]]["alternates"])
                self.assertEqual(set(doc.links),{ids[e["to"]]["path"] for e in graph["links"]
                                 if e["from"]==ident and e["kind"]=="crawlable"})
        package = collect(ROOT)
        for p in LAB.rglob("*"):
            if p.is_file():
                self.assertIn("seo-engineering/references/library/"+p.relative_to(ROOT).as_posix(),package)

    def test_business_review_preserves_outcome_and_claim_uncertainty(self):
        r = load(LAB/"business-review.json")
        self.assertGreater(r["after"]["lead_events"],r["before"]["lead_events"])
        for key in ("accepted_leads","search_clicks","organic_sessions"):
            self.assertEqual(r["after"][key],r["before"][key])
        self.assertIsNone(r["consent_network_verification"])
        self.assertIsNone(r["provider_receipt_verification"])
        c = next(c for c in r["claims"] if c["id"]=="CL1")
        self.assertEqual(c["disposition"],"defer")
        self.assertIsNone(c["approved_wording"])


if __name__ == "__main__":
    unittest.main()
