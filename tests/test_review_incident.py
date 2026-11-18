import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("review_incident", ROOT / "scripts/review_incident.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class IncidentTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples/technical-incident/sample.json").read_text())

    def finish_checks(self):
        self.data["checks"][1].update(evidence_id="fixed-http", outcome="pass")

    def test_conflicts_and_exclusions(self):
        r = module.review(self.data)
        self.assertEqual(r["hypotheses"][0]["state"], "conflicting")
        self.assertEqual(r["hypotheses"][0]["excluded_ids"], ["old-preview"])
        self.assertEqual(r["hypotheses"][1]["state"], "unresolved")
        self.assertFalse(r["root_cause_confirmed"])

    def test_missing_recovery_check(self):
        r = module.review(self.data)
        self.assertEqual(r["disposition"], "investigate")
        self.assertEqual(r["required_blockers"], ["rendered-directive"])

    def test_recovery_ready_not_closed(self):
        self.finish_checks()
        r = module.review(self.data)
        self.assertEqual(r["disposition"], "technical_recovery_review")
        self.assertFalse(r["incident_closed"])
        self.assertFalse(r["search_recovery_established"])
        self.assertEqual(r["search_follow_up"], "pending")

    def test_exposure_precedence(self):
        self.finish_checks()
        self.data["exposure_ref"] = "restricted-reported-exposure"
        self.assertEqual(module.review(self.data)["disposition"], "escalate")

    def test_old_and_partial_recovery(self):
        for ident in ("initial-noindex", "partial-log"):
            self.data["checks"][1].update(evidence_id=ident, outcome="pass")
            self.assertEqual(module.review(self.data)["checks"][1]["state"], "unmatched_or_partial")

    def test_unknown_ref(self):
        self.data["hypotheses"][0]["assessments"][0]["evidence_id"] = "unknown"
        with self.assertRaises(ValueError):
            module.review(self.data)

    def test_duplicate_assessment(self):
        a = self.data["hypotheses"][0]["assessments"]
        a.append(copy.deepcopy(a[0]))
        with self.assertRaises(ValueError):
            module.review(self.data)

    def test_cross_scope(self):
        self.data["evidence"][0]["subject"]["scope_ref"] = "unrelated"
        with self.assertRaises(ValueError):
            module.review(self.data)

    def test_missing_evidence_cannot_pass(self):
        self.data["checks"][1]["outcome"] = "pass"
        with self.assertRaises(ValueError):
            module.review(self.data)

    def test_no_recovery_subject(self):
        self.data["recovery_subject"] = None
        with self.assertRaises(ValueError):
            module.review(self.data)
        self.data["checks"] = []
        self.assertEqual(module.review(self.data)["disposition"], "investigate")

    def test_optional_gap(self):
        self.data["checks"][1]["required"] = False
        self.assertEqual(module.review(self.data)["disposition"], "review_optional")

    def test_no_required_checks(self):
        for c in self.data["checks"]:
            c["required"] = False
        with self.assertRaises(ValueError):
            module.review(self.data)

    def test_cli_duplicate_and_nonfinite_and_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dst = Path(tmp) / "input.json", Path(tmp) / "output.json"
            cmd = [sys.executable, str(ROOT / "scripts/review_incident.py"), "--input", str(src), "--output", str(dst)]
            for invalid in ('{"a":1,"a":2}', '{"number":NaN}'):
                src.write_text(invalid)
                self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)
                self.assertFalse(dst.exists())
            src.write_text(json.dumps(self.data))
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            original = dst.read_bytes()
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)
            self.assertEqual(dst.read_bytes(), original)
