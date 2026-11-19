import json
import tempfile
import unittest
from pathlib import Path

from scripts.measure_reference_loading import ROOT, ENTRY, read_routes, plan, file_bytes, profile
from scripts.build_skill import collect


class ReferenceLoadingTests(unittest.TestCase):
    def setUp(self):
        self.routes = read_routes((ROOT / ENTRY[-1]).read_text(encoding="utf-8"))
        self.cases = json.loads((ROOT / "operations/ts07-routing-cases.json").read_text(encoding="utf-8"))["cases"]

    def test_all_profiles_use_real_packaged_references(self):
        result = profile(ROOT, self.cases)
        packaged = collect(ROOT)
        self.assertEqual(result["target_case_count"], 14)
        self.assertFalse(result["actual_runtime_measured"])
        self.assertLess(result["target_initial_bytes_sum"], result["target_all_listed_bytes_sum"])
        for row in result["cases"]:
            self.assertLessEqual(row["initial_bytes"], row["all_listed_bytes"])
            self.assertEqual(len(row["initial_refs"]), len(set(row["initial_refs"])))
            for ref in row["all_listed_refs"]:
                path = ("seo-engineering/" + ref.removeprefix("skills/seo-engineering/")
                        if ref.startswith("skills/seo-engineering/") else
                        "seo-engineering/references/library/" + ref)
                self.assertIn(path, packaged)

    def test_initial_privacy_and_incident_workflow_retained(self):
        for ident, needed in (("ANALYTICS", "docs/05-measurement/privacy-and-qa.md"),
                              ("T10", "workflows/technical-audit.md"),
                              ("T11", "workflows/deployment-regression.md"),
                              ("T12", "workflows/technical-incident.md")):
            initial, _, _ = plan(self.routes, "audit", [ident], [])
            self.assertIn(needed, initial)
        initial, _, _ = plan(self.routes, "research", ["R02"], [])
        self.assertIn("docs/02-research/r02-keyword-discovery.md", initial)

    def test_scope_and_operator_exclusion(self):
        self.assertEqual(plan(self.routes, "out_of_scope", [], []), ([], [], 0))
        for mode, primary, deps in (("audit", ["MAINTAIN"], []),
                                    ("implement", ["T01"], ["MAINTAIN"]),
                                    ("out_of_scope", ["T01"], []),
                                    ("audit", ["T01"], ["T01"]),
                                    ("learn", ["UNKNOWN"], [])):
            with self.subTest(mode=mode, primary=primary):
                with self.assertRaises(ValueError):
                    plan(self.routes, mode, primary, deps)

    def test_budget_excess_is_recorded_not_truncated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for ref in ENTRY:
                p = root / ref
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes((ROOT / ref).read_bytes())
            ref = self.routes["URL_OVERVIEW"][0]
            p = root / ref
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"x" * 100000)
            r = profile(root, [{"id":"synthetic", "mode":"learn", "primary":["URL_OVERVIEW"],"dependencies":[]}])["cases"][0]
            self.assertTrue(r["budget_exceeded"])
            self.assertIn(ref, r["initial_refs"])
            self.assertGreaterEqual(r["initial_bytes"], 100000)

    def test_missing_reference_and_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for refs in (["docs/missing.md"], ["docs/../secret.md"], ["operations/ts07-routing-cases.json"]):
                with self.assertRaises(ValueError):
                    file_bytes(root, refs)


if __name__ == "__main__":
    unittest.main()
