"""Actual offline CLI and crosswalk checks of fictional P01 input, not runtime evaluation."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.build_skill import collect
from scripts.review_release_gates import review

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples/practice-projects/p01-react-vite"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def row(report, module, ident):
    native = next(m["native_report"] for m in report["modules"] if m["module"] == module)
    return next(r for r in native.get("routes", native.get("urls", [])) if r["id"] == ident)


class PracticeP01Tests(unittest.TestCase):
    def run_cli(self, script, *args):
        return subprocess.run([sys.executable, "-B", str(ROOT / "scripts" / script),
                               *map(str, args)], cwd=ROOT, capture_output=True, text=True, timeout=20)

    def smoke(self, revision):
        return self.run_cli("audit_html.py", "--manifest", LAB / "static-routes.json",
                            "--root", LAB / revision / "artifacts")

    def audit(self, revision, out):
        result = self.run_cli("audit_technical.py", "--input", LAB / revision / "technical.json",
                              "--artifact-root", LAB / revision / "artifacts", "--output", out)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return load(out)

    def test_packaged_registry_native_identity_and_scope(self):
        registry = load(LAB / "registry.json")
        ids = {r["id"]:r for r in registry["routes"]}
        self.assertEqual(len(ids), 6)
        public = {i for i,r in ids.items() if r["index_intent"]}
        self.assertEqual({r["url"] for r in load(LAB / "static-routes.json")},
                         {ids[i]["url"] for i in public})
        for rev in registry["revisions"]:
            data = load(LAB / rev / "technical.json")
            self.assertEqual(data["reviewed_revision"], rev)
            for module, expected, key in (("T01", set(ids), "routes"), ("T02", public, "routes"),
                                          ("T03", set(ids), "routes"), ("T05", set(ids), "urls"),
                                          ("T06", public, "urls")):
                rows = data["tasks"][module]["input"][key]
                self.assertEqual({r["id"] for r in rows}, expected)
                for r in rows:
                    if "url" in r:
                        self.assertEqual(r["url"], ids[r["id"]]["url"])
            self.assertEqual(load(LAB / rev / "gates.json")["subject"]["revision"], rev)
        package = collect(ROOT)
        for p in LAB.rglob("*"):
            if p.is_file():
                self.assertIn("seo-engineering/references/library/" + p.relative_to(ROOT).as_posix(), package)

    def test_actual_local_smoke_before_and_revised(self):
        a, b = self.smoke("p01-a"), self.smoke("p01-b")
        self.assertEqual(a.returncode, 1, a.stdout + a.stderr)
        self.assertIn("/guides/getting-started/: missing HTML", a.stdout)
        self.assertIn("/pricing/: canonical mismatch", a.stdout)
        self.assertIn("2 findings", a.stdout)
        self.assertEqual(b.returncode, 0, b.stdout + b.stderr)
        self.assertIn("4 manifest entries; 0 findings", b.stdout)

    def test_native_coordinator_actual_output_before_after(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = self.audit("p01-a", Path(tmp) / "a.json")
            b = self.audit("p01-b", Path(tmp) / "b.json")
        for report in (a,b):
            self.assertEqual(report["coverage"]["module_counts"],
                             {"processed":5,"blocked":2,"not_applicable":2,"failed":0})
            self.assertEqual(report["grouping_status"], "not_requested")
            self.assertTrue(report["authorization_required"])
            self.assertIn("authorization_unverified", row(report,"T01","dashboard")["findings"])
            self.assertIn("paired_comparison_not_performed", row(report,"T02","features")["deferred_checks"])
            self.assertIn("processed_sample_predates_change", row(report,"T06","guide")["deferred_checks"])
            self.assertIn("deployed_routing_headers_and_status_not_checked",
                          row(report,"T03","missing")["deferred_checks"])
        self.assertIn("required_artifact_missing", row(a,"T03","guide")["review_findings"])
        self.assertEqual(row(b,"T03","guide")["artifact_checks"],
                         [{"path":"guides/getting-started/index.html","state":"present"}])
        self.assertIn("client_completion_review",row(a,"T02","guide")["review_findings"])
        self.assertIn("canonicals_changed_review",row(a,"T02","guide")["review_findings"])
        self.assertEqual(row(b,"T02","guide")["review_findings"],[])
        self.assertIn("sitemap_canonical_preference_review",row(a,"T05","pricing")["review_findings"])
        self.assertEqual(row(b,"T05","pricing")["review_findings"],[])
        self.assertIn("missing_route_status_review",row(a,"T01","missing")["findings"])
        self.assertIn("missing_route_status_unknown",row(b,"T01","missing")["findings"])

    def test_gate_cli_and_actual_local_binding_never_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            for rev, state in (("p01-a","fail"), ("p01-b","stale")):
                out = Path(tmp) / (rev + ".json")
                result = self.run_cli("review_release_gates.py", "--input", LAB / rev / "gates.json", "--output", out)
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                report = load(out)
                self.assertEqual(report["disposition"],"hold")
                self.assertEqual(next(g["state"] for g in report["gates"] if g["id"]=="missing-http"),state)
                self.assertFalse(report["deployment_authorized"])
            data = load(LAB / "p01-b/gates.json")
            result = self.smoke("p01-b")
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            receipt = Path(tmp) / "local-smoke.txt"
            receipt.write_text(result.stdout,encoding="utf-8")
            local = next(g for g in data["gates"] if g["id"]=="local-html")
            local["evidence"] = {"subject":data["subject"],"outcome":"pass",
                                 "ref":str(receipt),"gate_id":local["id"],
                                 "policy_ref":data["policy_ref"],"assertion":local["assertion"]}
            report = review(data)
            self.assertEqual(next(g["state"] for g in report["gates"] if g["id"]=="local-html"),"pass")
            self.assertEqual(set(report["blockers"]),{"private-access","missing-http","matched-render"})
            self.assertEqual(report["disposition"],"hold")
            self.assertFalse(report["deployment_authorized"])
            self.assertFalse(report["evidence_independently_verified"])


if __name__ == "__main__":
    unittest.main()
