import copy
import tempfile
import unittest
from pathlib import Path

from scripts.control_benchmark import schedule, fingerprint, blind_packet
from scripts.prepare_trial import initial_ledger
from scripts.review_incomplete_trials import packet, assess
from scripts.verify_package import digest


class IncompleteTrialTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.suite = {"version":"fixture", "cases":[{"id":"A", "prompt":"Task",
                      "expected":["good"], "disqualifiers":["bad"]}]}
        cfg = dict(model="fictional model", runtime="fixture runtime",
                   inference_settings="fixed", tool_config="matched", permission_mode="read-only",
                   skill_commit="a"*40, archive_sha256="b"*64, launch_protocol="fresh sessions",
                   review_protocol="blind reviewers", suite_kind="public_regression", repeats=1,
                   treatment="complete_toolkit", task_context_sha256="c"*64, seed=12,
                   budget="equal", rubric_access_policy="restricted", candidate_variant="rubric_restricted")
        self.control = schedule(self.suite, cfg, ["A"])
        self.ledger = initial_ledger(self.control)
        self.row = self.ledger["runs"][0]

    def partial(self, kind="trace"):
        self.row.update(status="timeout", session_ref="test-session",
                        environment_ref="fixture", failure_reason="fixture timeout")
        ident = self.row["blind_id"]
        p = self.root / ident
        p.mkdir(exist_ok=True)
        raw = b"synthetic evidence"
        (p / (kind + ".txt")).write_bytes(raw)
        self.row[kind+"_ref"] = ident + "/" + kind + ".txt"
        self.row[kind+"_sha256"] = digest(raw)

    def get(self):
        return packet(self.suite, self.control, self.ledger, self.root)

    def review(self, p, status="observed"):
        return {"packet_sha256":fingerprint(p), "records":[
                {"blind_id":r["blind_id"], "reviewer":"fixture reviewer",
                 "output_sha256":r["output_sha256"], "trace_sha256":r["trace_sha256"],
                 "disqualifiers":[{"criterion":1, "status":status, "evidence":"fictional rationale"}]}
                for r in p["records"]]}

    def test_trace_only_timeout_preserved_outside_scoring(self):
        self.partial()
        p = self.get()
        self.assertEqual(len(p["records"]), 1)
        self.assertEqual(p["not_started_slots"], 1)
        self.assertIsNone(p["records"][0]["output_ref"])
        self.assertEqual(blind_packet(self.suite,self.control,self.ledger)["records"], [])
        self.assertFalse({"arm","session_ref","failure_reason"} & p["records"][0].keys())
        r = assess(p, self.review(p))
        self.assertTrue(r["escalation_required"])
        self.assertEqual(r["action"], "hold_review")
        self.assertFalse(r["release_certified"])

    def test_no_signal_is_not_clearance(self):
        self.partial("output")
        p = self.get()
        r = assess(p, self.review(p, "no_signal_in_available_evidence"))
        self.assertFalse(r["safety_certified"])
        self.assertEqual(r["action"], "hold_review")
        self.assertEqual(r["no_signal_in_available_evidence_criteria"], 1)

    def test_missing_review_and_no_artifact(self):
        self.row.update(status="error", failure_reason="fixture error")
        p = self.get()
        r = assess(p, {"packet_sha256":fingerprint(p), "records":[]})
        self.assertEqual(r["missing_review_slots"], [self.row["blind_id"]])
        with self.assertRaisesRegex(ValueError, "no artifact"):
            assess(p, self.review(p))
        r = assess(p, self.review(p, "not_observable"))
        self.assertEqual(r["not_observable_criteria"], 1)

    def test_tamper_and_stale_packet(self):
        self.partial()
        p = self.get()
        grades = self.review(p)
        (self.root / self.row["trace_ref"]).write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "changed"):
            self.get()
        (self.root / self.row["trace_ref"]).write_bytes(b"synthetic evidence")
        self.row["status"] = "incomplete"
        with self.assertRaisesRegex(ValueError, "packet mismatch"):
            assess(self.get(), grades)

    def test_duplicate_invalid_review_and_not_started_reference(self):
        self.partial()
        p = self.get()
        grades = self.review(p)
        altered = copy.deepcopy(grades)
        altered["records"].append(altered["records"][0])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            assess(p, altered)
        grades["records"][0]["trace_sha256"] = "a"*64
        with self.assertRaisesRegex(ValueError, "artifact mismatch"):
            assess(p, grades)
        self.row["status"] = "not_started"
        with self.assertRaisesRegex(ValueError, "not-started"):
            self.get()

    def test_all_not_started_no_pass(self):
        p = self.get()
        r = assess(p, self.review(p))
        self.assertEqual(r["not_started_slots"], 2)
        self.assertEqual(r["action"], "hold_review")
        self.assertFalse(r["actual_execution_verified"])


if __name__ == "__main__":
    unittest.main()
