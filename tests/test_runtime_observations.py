"""Synthetic runtime-capture intake checks. Never invokes Cursor or Codex."""
import copy
import tempfile
import unittest
from pathlib import Path

from scripts.control_benchmark import schedule, fingerprint
from scripts.prepare_trial import initial_ledger
from scripts.review_runtime_observations import review, PROMPT_PREFIX
from scripts.verify_package import digest


class RuntimeObservationTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.artifacts=self.root/"artifacts"
        self.captures=self.root/"captures"
        self.artifacts.mkdir()
        self.captures.mkdir()
        self.suite={"version":"fictional","cases":[{"id":"A","prompt":"Fictional task",
                    "expected":["answer"],"disqualifiers":["exposure"]}]}
        config=dict(model="fictional-model",runtime="cursor CLI fixture",
                    inference_settings="matched setting",tool_config="none",
                    permission_mode="read-only",skill_commit="a"*40,
                    archive_sha256="b"*64,launch_protocol="fictional",
                    review_protocol="fictional",suite_kind="public_regression",
                    repeats=1,treatment="complete_toolkit",task_context_sha256="c"*64,
                    seed=7,budget="matched",rubric_access_policy="restricted",
                    candidate_variant="rubric_restricted")
        self.control=schedule(self.suite,config,["A"])
        self.ledger=initial_ledger(self.control)
        self.report={"schema_version":"1","record_kind":"private_runtime_capture_declarations",
                     "control_sha256":fingerprint(self.control),
                     "source_commit":"a"*40,"archive_sha256":"b"*64,
                     "runtime_kind":"cursor","runs":[]}

    def completed(self, indices=(0,1)):
        for i in indices:
            slot=self.control["slots"][i]
            row=self.ledger["runs"][i]
            ident=slot["blind_id"]
            artifacts=self.artifacts/ident
            artifacts.mkdir(exist_ok=True)
            hashes={}
            for kind in ("output","trace"):
                raw=("fictional "+kind+" "+ident).encode()
                (artifacts/(kind+".txt")).write_bytes(raw)
                hashes[kind]=digest(raw)
            row.update(status="completed",session_ref="session-"+ident,
                       environment_ref="env-"+ident,
                       output_ref=ident+"/output.txt",output_sha256=hashes["output"],
                       trace_ref=ident+"/trace.txt",trace_sha256=hashes["trace"],
                       failure_reason=None)
            self.add_record(i,terminal="success",code=0)

    def add_record(self,i,terminal="success",code=0):
        slot=self.control["slots"][i]
        row=self.ledger["runs"][i]
        ident=slot["blind_id"]
        folder=self.captures/ident
        folder.mkdir(exist_ok=True)
        raw=("fictional sanitized CLI events for "+ident).encode()
        (folder/"events.txt").write_bytes(raw)
        cfg=self.control["plan"]["config"]
        self.report["runs"].append({
            "blind_id":ident,"status":row["status"],
            "session_ref":row["session_ref"],"environment_ref":row["environment_ref"],
            "runtime_version":"fictional Cursor 0.0.1",
            "model":cfg["model"],"inference_settings":cfg["inference_settings"],
            "permission_mode":cfg["permission_mode"],
            "prompt_sha256":digest((PROMPT_PREFIX+slot["prompt"]+"\n").encode()),
            "terminal_event":terminal,"exit_code":code,"elapsed_ms":42,
            "read_isolation":"verified_by_operator",
            "skill_activation":"absent" if slot["arm"]=="baseline" else "observed",
            "output_sha256":row["output_sha256"],"trace_sha256":row["trace_sha256"],
            "capture_ref":ident+"/events.txt","capture_sha256":digest(raw)})

    def check(self):
        return review(self.suite,self.control,self.ledger,self.artifacts,
                      self.report,self.captures)

    def test_valid_pair_is_only_ready_for_human_review(self):
        self.completed()
        out=self.check()
        self.assertEqual(out["status"],"ready_for_independent_review")
        self.assertEqual(len(out["verified_declared_capture_files"]),2)
        self.assertEqual(out["missing_capture_slots"],[])
        self.assertFalse(out["actual_model_execution_independently_verified"])
        self.assertFalse(out["release_approved"])

    def test_missing_started_slot_is_a_hold(self):
        self.completed((0,))
        slot=self.ledger["runs"][1]
        slot.update(status="error",failure_reason="synthetic runtime error")
        out=self.check()
        self.assertEqual(out["status"],"hold_missing_or_unobservable")
        self.assertEqual(out["missing_capture_slots"],[slot["blind_id"]])

    def test_capture_file_tampering_rejected(self):
        self.completed()
        ident=self.report["runs"][0]["blind_id"]
        (self.captures/ident/"events.txt").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError,"capture missing, empty or changed"):
            self.check()

    def test_orphan_and_symlink_capture_rejected(self):
        self.completed()
        (self.captures/"surprise.txt").write_bytes(b"not declared")
        with self.assertRaisesRegex(ValueError,"undeclared capture directory"):
            self.check()
        (self.captures/"surprise.txt").unlink()
        ident=self.report["runs"][0]["blind_id"]
        (self.captures/ident/"secret-link.txt").symlink_to(self.captures/ident/"events.txt")
        with self.assertRaisesRegex(ValueError,"unexpected runtime capture file"):
            self.check()

    def test_mismatched_prompt_or_settings_rejected(self):
        self.completed()
        self.report["runs"][0]["prompt_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"prompt digest mismatch"):
            self.check()
        self.report["runs"][0]["prompt_sha256"]=digest(
            (PROMPT_PREFIX+self.control["slots"][0]["prompt"]+"\n").encode())
        self.report["runs"][0]["model"]="different-model"
        with self.assertRaisesRegex(ValueError,"frozen settings mismatch"):
            self.check()

    def test_bad_ledger_status_and_terminal_event_rejected(self):
        self.completed()
        self.report["runs"][0]["terminal_event"]="failure"
        with self.assertRaisesRegex(ValueError,"lacks successful terminal"):
            self.check()
        self.report["runs"][0]["terminal_event"]="success"
        self.report["runs"][0]["session_ref"]="wrong session"
        with self.assertRaisesRegex(ValueError,"status or session binding"):
            self.check()

    def test_permissions_failure_escalates(self):
        self.completed()
        self.report["runs"][1]["read_isolation"]="failed"
        out=self.check()
        self.assertEqual(out["status"],"escalate_to_owner")
        self.assertTrue(out["critical_operator_declaration_conflicts"])

    def test_activation_failure_escalates(self):
        self.completed()
        self.report["runs"][0]["skill_activation"]="observed" if (
            self.control["slots"][0]["arm"]=="baseline") else "absent"
        self.assertEqual(self.check()["status"],"escalate_to_owner")

    def test_missing_observability_holds(self):
        self.completed()
        self.report["runs"][0]["skill_activation"]="unknown"
        self.assertEqual(self.check()["status"],"hold_missing_or_unobservable")

    def test_out_of_order_capture_declarations_hold(self):
        self.completed()
        self.report["runs"].reverse()
        out=self.check()
        self.assertIn("capture_records_outside_frozen_launch_order",
                      out["missing_or_unobservable"])

    def test_nonstarted_run_cannot_have_capture(self):
        self.completed((0,))
        self.report["runs"][0]["blind_id"]=self.control["slots"][1]["blind_id"]
        with self.assertRaisesRegex(ValueError,"one started slot"):
            self.check()

    def test_timeout_with_partial_trace_is_not_success(self):
        row=self.ledger["runs"][0]
        ident=row["blind_id"]
        folder=self.artifacts/ident
        folder.mkdir()
        raw=b"fictional partial trace"
        (folder/"trace.txt").write_bytes(raw)
        row.update(status="timeout",session_ref="s-"+ident,
                   environment_ref="e-"+ident,
                   failure_reason="synthetic timeout",
                   trace_ref=ident+"/trace.txt",trace_sha256=digest(raw))
        self.add_record(0,terminal="timeout",code=None)
        out=self.check()
        self.assertEqual(out["status"],"ready_for_independent_review")
        self.assertEqual(out["started_slots"],1)


if __name__ == "__main__":
    unittest.main()
