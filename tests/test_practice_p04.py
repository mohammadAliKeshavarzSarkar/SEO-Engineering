"""Native CLI regression on fictional incident records; not real incident verification."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.build_skill import collect
from scripts.review_incident import review as incident_review
from scripts.review_release_gates import review as gate_review

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples/practice-projects/p04-traffic-incident"


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


class PracticeP04Tests(unittest.TestCase):
    def report(self, script, name):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "report.json"
            r = subprocess.run([sys.executable, "-B", str(ROOT/"scripts"/script),
                                "--input", str(LAB/name), "--output", str(out)],
                               cwd=ROOT, capture_output=True, text=True, timeout=20)
            self.assertEqual(r.returncode, 0, r.stdout+r.stderr)
            return load(out)

    def test_registry_crosswalk_and_packaging(self):
        reg = load(LAB/"registry.json")
        base = load(LAB.parent/"p01-react-vite/registry.json")
        urls = {r["id"]:r["url"] for r in base["routes"]}
        self.assertTrue(all(urls[r["id"]]==r["url"] for r in reg["routes"]))
        catalogue = load(LAB/"observations.json")
        obs = {e["id"]:e for e in catalogue["observations"]}
        ids = {r["id"] for r in reg["routes"]}
        for o in obs.values():
            self.assertTrue(set(o["route_ids"]) <= ids)
        for folder in ("initial","partial","review"):
            ledger = load(LAB/folder/"incident.json")
            self.assertEqual(ledger["subject"],reg["subjects"][0])
            for e in ledger["evidence"]:
                self.assertEqual(e,{k:obs[e["id"]][k] for k in e})
            for c in ledger["checks"]:
                self.assertEqual(c["assertion"],catalogue["assertions"][c["id"]])
        for folder in ("partial","review"):
            ledger = load(LAB/folder/"incident.json")
            gates = load(LAB/folder/"gates.json")
            self.assertEqual(gates["subject"],{"stage":"production",**ledger["recovery_subject"]})
            self.assertEqual({g["id"]:g["assertion"] for g in gates["gates"]},
                             {c["id"]:c["assertion"] for c in ledger["checks"]})
        for folder in ("initial","review"):
            index = load(LAB/folder/"index.json")
            self.assertEqual({r["id"]:r["url"] for r in index["urls"]},
                             {r["id"]:r["url"] for r in reg["routes"]})
        package = collect(ROOT)
        for p in LAB.rglob("*"):
            if p.is_file():
                self.assertIn("seo-engineering/references/library/"+p.relative_to(ROOT).as_posix(),package)

    def test_initial_conflicting_hypotheses_and_excluded_evidence(self):
        r = self.report("review_incident.py","initial/incident.json")
        hypotheses = {h["id"]:h for h in r["hypotheses"]}
        self.assertEqual(hypotheses["gateway"]["state"],"conflicting")
        self.assertEqual(hypotheses["gateway"]["excluded_ids"],["preview-a"])
        self.assertEqual(hypotheses["gateway"]["inconclusive_ids"],["search-loss-a"])
        self.assertEqual(hypotheses["measurement"]["state"],"unresolved")
        self.assertEqual(hypotheses["measurement"]["excluded_ids"],["collection-gap-a"])
        self.assertEqual(hypotheses["demand"]["state"],"unresolved")
        self.assertEqual(r["disposition"],"investigate")
        self.assertFalse(r["root_cause_confirmed"])

    def test_partial_wrong_assertion_blocks_both_reviews(self):
        r = self.report("review_incident.py","partial/incident.json")
        g = self.report("review_release_gates.py","partial/gates.json")
        self.assertEqual({c["id"]:c["state"] for c in r["checks"]},
                         {"http-guide":"pass","render-guide":"unmatched_assertion","access-dashboard":"missing"})
        self.assertEqual({c["id"]:c["state"] for c in g["gates"]},
                         {"http-guide":"pass","render-guide":"stale","access-dashboard":"missing"})
        self.assertEqual(set(r["required_blockers"]),{"render-guide","access-dashboard"})
        self.assertEqual(set(g["blockers"]),set(r["required_blockers"]))
        self.assertEqual(r["disposition"],"investigate")
        self.assertEqual(g["disposition"],"hold")
        # The partial capture cannot satisfy the render check even if used directly.
        inp = load(LAB/"partial/incident.json")
        c = next(c for c in inp["checks"] if c["id"]=="render-guide")
        c.update(evidence_id="guide-render-partial-b",outcome="incomplete")
        self.assertEqual(next(c["state"] for c in incident_review(inp)["checks"]
                              if c["id"]=="render-guide"),"unmatched_or_partial")

    def test_all_mock_assertions_pass_but_no_closure_or_authority(self):
        r = self.report("review_incident.py","review/incident.json")
        g = self.report("review_release_gates.py","review/gates.json")
        self.assertEqual(r["required_blockers"],[])
        self.assertEqual(g["blockers"],[])
        self.assertTrue(all(c["state"]=="pass" for c in r["checks"]))
        self.assertEqual(r["disposition"],"technical_recovery_review")
        self.assertEqual(g["disposition"],"ready_for_owner_review")
        for k in ("root_cause_confirmed","incident_closed","search_recovery_established",
                  "evidence_independently_verified"):
            self.assertFalse(r[k])
        self.assertEqual(r["search_follow_up"],"pending")
        self.assertFalse(g["deployment_authorized"])
        self.assertFalse(g["evidence_independently_verified"])

    def test_exposure_overrides_otherwise_passing_mock_checks(self):
        i = load(LAB/"review/incident.json")
        g = load(LAB/"review/gates.json")
        i["exposure_ref"]="P04/MOCK/credible-exposure-review"
        # Old-subject report must not be suppressed by later passing gates.
        g["exposure"]={"subject":{"stage":"production",**i["subject"]},"ref":i["exposure_ref"]}
        ir,gr = incident_review(i),gate_review(g)
        self.assertEqual(ir["disposition"],"escalate")
        self.assertEqual(gr["disposition"],"escalate")
        self.assertEqual(gr["exposure_state"],"stale_reported")
        self.assertFalse(ir["incident_closed"])
        self.assertFalse(gr["deployment_authorized"])

    def test_index_recency_and_incomplete_outcome(self):
        a,b = ({r["id"]:r for r in self.report("audit_index_evidence.py",folder+"/index.json")["urls"]}
               for folder in ("initial","review"))
        self.assertIn("intended_representative_noindex_review",a["guide"]["review_findings"])
        self.assertIn("processed_representative_not_indexed_review",a["guide"]["review_findings"])
        self.assertEqual(b["guide"]["review_findings"],[])
        self.assertIn("processed_sample_predates_change",b["guide"]["deferred_checks"])
        self.assertEqual(a["guide"]["processed_ref"],b["guide"]["processed_ref"])
        self.assertEqual(a["home"]["review_findings"],[])
        self.assertIn("current_capture_incomplete",b["dashboard"]["deferred_checks"])
        periods = load(LAB/"timeline.json")["periods"]
        self.assertEqual(periods[0]["days"],periods[1]["days"])
        self.assertEqual(periods[0]["scope"],periods[1]["scope"])
        self.assertLess(periods[1]["clicks"],periods[0]["clicks"])
        self.assertLess(periods[1]["accepted_leads"],periods[0]["accepted_leads"])
        self.assertEqual(periods[2]["search_status"],"partial_mock")
        self.assertTrue(all(periods[2][k] is None for k in
                            ("clicks","impressions","organic_sessions","lead_events","accepted_leads")))


if __name__ == "__main__":
    unittest.main()
