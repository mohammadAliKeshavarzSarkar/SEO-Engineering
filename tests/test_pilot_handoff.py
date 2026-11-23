"""Actually exercise local file-byte verification and conservative handoff review."""
import copy
import tempfile
import unittest
from pathlib import Path

from scripts.check_pilot_handoff import review
from scripts.control_benchmark import schedule, blind_packet, fingerprint
from scripts.prepare_trial import initial_ledger
from scripts.verify_package import digest


class HandoffTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.suite={"version":"fixture","cases":[{"id":"A","prompt":"Fictional task",
                       "expected":["document facts"],"disqualifiers":["exposure"]}]}
        cfg=dict(model="fictional model",runtime="fictional CLI",
                 inference_settings="none",tool_config="none",permission_mode="read-only",
                 skill_commit="a"*40,archive_sha256="b"*64,
                 launch_protocol="fictional",review_protocol="fictional",
                 suite_kind="public_regression",repeats=1,treatment="complete_toolkit",
                 task_context_sha256="c"*64,seed=7,budget="matched",
                 rubric_access_policy="restricted",candidate_variant="rubric_restricted")
        self.control=schedule(self.suite,cfg,["A"])
        self.ledger=initial_ledger(self.control)
        self.artifacts=self.root/"artifacts"
        self.artifacts.mkdir()
        self.activation={"kind":"unscored_activation_evidence_intake",
                         "candidate_commit":"a"*40,
                         "archive_sha256":"b"*64,
                         "control_sha256":fingerprint(self.control),
                         "status":"ready_for_independent_review",
                         "actual_activation_certified":False,
                         "read_isolation_certified":False,
                         "paid_pilot_authorized":False,"release_approved":False}

    def complete(self,which=(0,1)):
        for i in which:
            row=self.ledger["runs"][i]
            ident=row["blind_id"]
            folder=self.artifacts/ident
            folder.mkdir()
            raw=("fictional output "+ident).encode()
            trace=("fictional trace "+ident).encode()
            (folder/"output.txt").write_bytes(raw)
            (folder/"trace.txt").write_bytes(trace)
            row.update(status="completed",session_ref="session-"+ident,
                       environment_ref="env-"+ident,
                       output_ref=ident+"/output.txt",output_sha256=digest(raw),
                       trace_ref=ident+"/trace.txt",trace_sha256=digest(trace),
                       failure_reason=None)

    def grades(self,critical=False):
        packet=blind_packet(self.suite,self.control,self.ledger)
        return {"packet_sha256":fingerprint(packet),"records":[{
            "blind_id":r["blind_id"],"reviewer":"fictional reviewer",
            "output_sha256":r["output_sha256"],"trace_sha256":r["trace_sha256"],
            "expected":[{"criterion":1,"status":"pass","evidence":"fixture"}],
            "disqualifiers":[{"criterion":1,"status":"observed" if critical else "absent",
                             "evidence":"fixture"}]
            } for r in packet["records"]]}

    def test_not_started_is_hold_without_artifacts(self):
        r=review(self.suite,self.control,self.ledger,self.artifacts)
        self.assertEqual(r["disposition"],"hold_evidence_and_owner_review")
        self.assertEqual(r["execution_counts"]["not_started"],2)
        self.assertIn("not_started_slots",r["hold_reasons"])
        self.assertFalse(r["pilot_approved"])

    def test_complete_favorable_synthetic_grade_never_approves(self):
        self.complete()
        r=review(self.suite,self.control,self.ledger,self.artifacts,self.grades(),
                 activation_intake=self.activation)
        self.assertEqual(r["execution_counts"]["completed"],2)
        self.assertEqual(r["verified_submitted_artifacts"],4)
        self.assertTrue(r["completed_grade_report"]["skill_internal_case_gate"])
        self.assertIn("activation_not_independently_verified",r["hold_reasons"])
        self.assertFalse(r["model_execution_independently_verified"])
        self.assertFalse(r["pilot_approved"])
        self.assertFalse(r["release_approved"])

    def test_incomplete_disqualifier_escalates_even_with_good_completed_grade(self):
        self.complete((0,))
        missing=self.ledger["runs"][1]
        missing["status"]="timeout"
        missing["failure_reason"]="synthetic timeout"
        grade=self.grades()
        from scripts.review_incomplete_trials import packet as incomplete_packet
        p=incomplete_packet(self.suite,self.control,self.ledger,self.artifacts)
        reviews={"packet_sha256":fingerprint(p),"records":[{
            "blind_id":r["blind_id"],"reviewer":"fictional safety reviewer",
            "output_sha256":r["output_sha256"],"trace_sha256":r["trace_sha256"],
            "disqualifiers":[{"criterion":1,"status":"not_observable",
                             "evidence":"no trace"}]} for r in p["records"]]}
        r=review(self.suite,self.control,self.ledger,self.artifacts,grade,reviews)
        self.assertIn("incomplete_or_failed_slots",r["hold_reasons"])
        self.assertIn("incomplete_disqualifier_unobservable",r["hold_reasons"])
        self.assertFalse(r["completed_grade_report"]["complete"])
        # Add actual fictional partial artifact to support an observed finding.
        folder=self.artifacts/missing["blind_id"]
        folder.mkdir()
        raw=b"fictional partial output"
        (folder/"output.txt").write_bytes(raw)
        missing.update(output_ref=missing["blind_id"]+"/output.txt",
                       output_sha256=digest(raw))
        p=incomplete_packet(self.suite,self.control,self.ledger,self.artifacts)
        reviews["packet_sha256"]=fingerprint(p)
        reviews["records"][0]["output_sha256"]=digest(raw)
        reviews["records"][0]["disqualifiers"][0].update(
            status="observed",evidence="fictional local partial evidence")
        r=review(self.suite,self.control,self.ledger,self.artifacts,grade,reviews)
        self.assertEqual(r["disposition"],"escalate_to_owner")
        self.assertIn("incomplete_disqualifier_observed",r["escalation_reasons"])

    def test_incomplete_review_missing_stays_visible(self):
        self.complete((0,))
        row=self.ledger["runs"][1]
        row.update(status="error",failure_reason="fictional error")
        r=review(self.suite,self.control,self.ledger,self.artifacts,self.grades())
        self.assertIn("incomplete_safety_review_missing",r["hold_reasons"])
        self.assertFalse(r["pilot_approved"])

    def test_tampered_artifact_or_grade_rejected(self):
        self.complete()
        grade=self.grades()
        (self.artifacts/self.ledger["runs"][0]["output_ref"]).write_bytes(b"other")
        with self.assertRaisesRegex(ValueError,"artifact missing, empty or changed"):
            review(self.suite,self.control,self.ledger,self.artifacts,grade)
        orig=self.ledger["runs"][0]
        (self.artifacts/orig["output_ref"]).write_bytes(
            ("fictional output "+orig["blind_id"]).encode())
        grade["packet_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"grades/packet mismatch"):
            review(self.suite,self.control,self.ledger,self.artifacts,grade)

    def test_activation_mismatched_or_falsely_certified_rejected(self):
        self.complete()
        activation=copy.deepcopy(self.activation)
        activation["archive_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"activation record does not match"):
            review(self.suite,self.control,self.ledger,self.artifacts,self.grades(),
                   activation_intake=activation)
        activation=copy.deepcopy(self.activation)
        activation["release_approved"]=True
        with self.assertRaisesRegex(ValueError,"claims certification"):
            review(self.suite,self.control,self.ledger,self.artifacts,self.grades(),
                   activation_intake=activation)

    def test_skill_critical_grade_escalates(self):
        self.complete()
        packet=blind_packet(self.suite,self.control,self.ledger)
        grades=self.grades()
        skill=next(s["blind_id"] for s in self.control["slots"] if s["arm"]=="skill")
        g=next(r for r in grades["records"] if r["blind_id"]==skill)
        g["disqualifiers"][0]["status"]="observed"
        r=review(self.suite,self.control,self.ledger,self.artifacts,grades)
        self.assertEqual(r["disposition"],"escalate_to_owner")
        self.assertIn("skill_critical_failure_observed",r["escalation_reasons"])


if __name__=="__main__":
    unittest.main()
