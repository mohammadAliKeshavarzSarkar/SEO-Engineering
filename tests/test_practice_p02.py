"""Actual offline CLI output on coherent fictional P02, not Next.js or model tests."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.build_skill import collect

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples/practice-projects/p02-next-hybrid"


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def native(report, module):
    return next(x["native_report"] for x in report["modules"] if x["module"] == module)


def row(report, module, key, ident):
    return next(x for x in native(report,module)[key] if x["id"] == ident)


class PracticeP02Tests(unittest.TestCase):
    def run_report(self, script, rev, name, out):
        proc = subprocess.run([sys.executable, "-B", str(ROOT/"scripts"/script),
                               "--input", str(LAB/rev/name), "--output", str(out)],
                              cwd=ROOT, capture_output=True, text=True, timeout=20)
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
        return load(out)

    def reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            return [self.run_report("audit_technical.py", rev,"technical.json",Path(tmp)/(rev+".json"))
                    for rev in ("p02-a","p02-b")]

    def test_registry_crosswalk_and_packaging(self):
        reg = load(LAB/"registry.json")
        ids = {r["id"]:r for r in reg["routes"]}
        self.assertEqual(len(ids),5)
        public = {i for i,r in ids.items() if r["index_intent"]}
        perf = {r["record_id"]:r for r in reg["performance_crosswalk"]}
        self.assertIsNone(perf["field-origin"]["route_id"])
        for rev in reg["revisions"]:
            manifest = load(LAB/rev/"technical.json")
            self.assertEqual(manifest["reviewed_revision"],rev)
            for mod,key,want in (("T01","routes",set(ids)),("T04","routes",set(ids)),
                                 ("T06","urls",public),("T08","pages",public)):
                rows = manifest["tasks"][mod]["input"][key]
                self.assertEqual({r["id"] for r in rows},want)
                for r in rows:
                    if mod=="T06":
                        self.assertEqual(r["url"],ids[r["id"]]["url"])
                    if mod=="T08":
                        self.assertEqual(r["plan"]["canonical"],ids[r["id"]]["url"])
            p = manifest["tasks"]["T09"]["input"]
            for r in p["field"]:
                self.assertEqual(r["subject"],perf[r["id"]]["subject"])
            for r in p["lab"]:
                self.assertEqual(perf[r["id"]]["subject"],ids[perf[r["id"]]["route_id"]]["url"])
                self.assertEqual([r["baseline_revision"],r["candidate_revision"]],reg["revisions"])
        package = collect(ROOT)
        for path in LAB.rglob("*"):
            if path.is_file():
                self.assertIn("seo-engineering/references/library/"+path.relative_to(ROOT).as_posix(),package)

    def test_actual_coordinator_and_delivery_comparability(self):
        a,b = self.reports()
        for report in (a,b):
            self.assertEqual(report["coverage"]["module_counts"],
                             {"processed":5,"blocked":2,"not_applicable":2,"failed":0})
            self.assertEqual(report["grouping_status"],"not_requested")
            self.assertTrue(report["authorization_required"])
            self.assertIn("authorization_unverified",row(report,"T01","routes","account")["findings"])
        cat = row(a,"T04","routes","catalogue")
        self.assertIn("static_export_runtime_strategy_conflict_review",cat["review_findings"])
        self.assertIn("static_export_runtime_features_review",cat["review_findings"])
        cat = row(b,"T04","routes","catalogue")
        self.assertEqual(cat["review_findings"],[])
        self.assertEqual(cat["samples"][0]["freshness"],"not_assessed")
        self.assertIn("sample_context_mismatch",cat["samples"][0]["deferred_checks"])
        samples = row(a,"T04","routes","product")["samples"]
        self.assertEqual([s["freshness"] for s in samples],
                         ["different_before_deadline","different_at_or_after_deadline"])
        self.assertIn("freshness_target_not_observed_by_deadline_review",samples[1]["review_findings"])
        self.assertEqual(row(b,"T04","routes","product")["samples"][0]["freshness"],"target_observed")

    def test_metadata_and_index_scope_remain_separate(self):
        a,b = self.reports()
        self.assertIn("declared_canonical_differs_from_preference_review",
                      row(a,"T06","urls","product")["review_findings"])
        self.assertNotIn("declared_canonical_differs_from_preference_review",
                         row(b,"T06","urls","product")["review_findings"])
        for r in (a,b):
            self.assertIn("processed_sample_predates_change",row(r,"T06","urls","product")["deferred_checks"])
        old = row(a,"T08","pages","product")["captures"]["source"]["review_findings"]
        self.assertTrue({"title","canonical"} <= {x["field"] for x in old if x["code"]=="observed_metadata_differs_from_plan_review"})
        self.assertEqual(row(b,"T08","pages","product")["captures"]["source"]["review_findings"],[])
        self.assertIn("capture_incomplete",row(b,"T08","pages","catalogue")["captures"]["rendered"]["deferred_checks"])

    def test_performance_tradeoff_and_no_field_substitution(self):
        a,b = self.reports()
        self.assertEqual(native(a,"T09")["lab"],[])
        product = row(b,"T09","lab","product-lcp")
        self.assertEqual((product["baseline"]["median"],product["candidate"]["median"],product["delta"]),(2200,2600,400))
        self.assertEqual(product["status"],"regression_review")
        other = row(b,"T09","lab","catalogue-lcp")
        self.assertEqual(other["status"],"deferred")
        self.assertIsNone(other["delta"])
        self.assertIn("candidate:incomplete_or_mismatched_run",other["deferred_checks"])
        field = row(b,"T09","field","field-origin")
        self.assertEqual(field["level"],"origin")
        self.assertEqual(field["local_summary"],"incomplete")
        self.assertIsNone(field["p75"]["inp_ms"]["classification"])

    def test_actual_gate_review_holds_both_revisions(self):
        with tempfile.TemporaryDirectory() as tmp:
            for rev in ("p02-a","p02-b"):
                r = self.run_report("review_release_gates.py",rev,"gates.json",Path(tmp)/(rev+".json"))
                self.assertEqual(r["disposition"],"hold")
                self.assertEqual(len(r["blockers"]),5)
                self.assertTrue(all(g["state"]=="missing" for g in r["gates"]))
                self.assertFalse(r["deployment_authorized"])
                self.assertFalse(r["evidence_independently_verified"])


if __name__ == "__main__":
    unittest.main()
