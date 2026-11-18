import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("review_release_gates", ROOT / "scripts/review_release_gates.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples/deployment-regression/sample.json").read_text())

    def test_optional_gap(self):
        report = module.review(self.data)
        self.assertEqual(report["disposition"], "review_optional")
        self.assertFalse(report["deployment_authorized"])

    def test_all_pass(self):
        self.data["gates"].pop()
        self.assertEqual(module.review(self.data)["disposition"], "ready_for_owner_review")

    def test_required_missing(self):
        self.data["gates"][0]["evidence"] = None
        self.assertEqual(module.review(self.data)["blockers"], ["public-delivery"])

    def test_required_fail_or_incomplete(self):
        for state in ("fail", "incomplete"):
            self.data["gates"][0]["evidence"]["outcome"] = state
            self.assertEqual(module.review(self.data)["disposition"], "hold")

    def test_changed_subject(self):
        for key in self.data["subject"]:
            with self.subTest(key=key):
                data = copy.deepcopy(self.data)
                data["subject"][key] = "production" if key == "stage" else "different"
                report = module.review(data)
                self.assertEqual(report["gates"][0]["state"], "stale")
                self.assertEqual(report["disposition"], "hold")

    def test_exposure_current_and_stale(self):
        for ref_subject in (self.data["subject"], {**self.data["subject"], "artifact": "older"}):
            self.data["exposure"] = {"subject": ref_subject, "ref": "synthetic-exposure"}
            self.assertEqual(module.review(self.data)["disposition"], "escalate")

    def test_duplicate_ids(self):
        self.data["gates"].append(self.data["gates"][0])
        with self.assertRaises(ValueError):
            module.review(self.data)

    def test_required_bool(self):
        self.data["gates"][0]["required"] = 1
        with self.assertRaises(ValueError):
            module.review(self.data)

    def test_no_required(self):
        for gate in self.data["gates"]:
            gate["required"] = False
        with self.assertRaises(ValueError):
            module.review(self.data)

    def test_unknown_outcome(self):
        self.data["gates"][0]["evidence"]["outcome"] = "assumed"
        with self.assertRaises(ValueError):
            module.review(self.data)

    def test_unknown_fields(self):
        self.data["arbitrary_command"] = "not permitted"
        with self.assertRaises(ValueError):
            module.review(self.data)

    def test_cli_invalid_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dst = Path(tmp) / "input.json", Path(tmp) / "output.json"
            cmd = [sys.executable, str(ROOT / "scripts/review_release_gates.py"), "--input", str(src), "--output", str(dst)]
            for invalid in ('{"a":1,"a":2}', '{"number":NaN}'):
                src.write_text(invalid)
                self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)
                self.assertFalse(dst.exists())
            src.write_text(json.dumps(self.data))
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            original = dst.read_bytes()
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)
            self.assertEqual(dst.read_bytes(), original)
