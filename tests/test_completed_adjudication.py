"""Synthetic completed-run reviewer/adjudication integrity regression tests."""
import copy
import unittest

from scripts.control_benchmark import schedule, blind_packet, fingerprint
from scripts.prepare_trial import initial_ledger
from scripts.review_completed_adjudication import assess


class CompletedAdjudicationTests(unittest.TestCase):
    def setUp(self):
        self.suite = {"version":"synthetic", "cases":[
            {"id":"A", "prompt":"Fictional task", "expected":["do well"],
             "disqualifiers":["bad access"]}]}
        cfg = dict(model="fictional model", runtime="fictional CLI",
                   inference_settings="fixed", tool_config="none",
                   permission_mode="read-only", skill_commit="a"*40,
                   archive_sha256="b"*64, launch_protocol="synthetic",
                   review_protocol="synthetic", suite_kind="public_regression",
                   repeats=1, treatment="complete_toolkit",
                   task_context_sha256="c"*64, seed=7, budget="matched",
                   rubric_access_policy="restricted",
                   candidate_variant="rubric_restricted")
        self.control = schedule(self.suite,cfg,["A"])
        self.ledger = initial_ledger(self.control)
        for row in self.ledger["runs"]:
            ident = row["blind_id"]
            row.update(status="completed",session_ref="s-"+ident,
                       environment_ref="fictional",output_ref=ident+"/output.txt",
                       output_sha256="d"*64,trace_ref=ident+"/trace.txt",
                       trace_sha256="e"*64,failure_reason=None)
        self.packet = blind_packet(self.suite,self.control,self.ledger)
        self.first = self.grade("first reviewer")
        self.second = self.grade("second reviewer")
        self.final = self.grade("final reviewer")

    def grade(self, who):
        return {"packet_sha256":fingerprint(self.packet), "records":[
            {"blind_id":r["blind_id"],"reviewer":who,
             "output_sha256":r["output_sha256"],
             "trace_sha256":r["trace_sha256"],
             "expected":[{"criterion":1,"status":"pass","evidence":"synthetic"}],
             "disqualifiers":[{"criterion":1,"status":"absent","evidence":"synthetic"}]}
            for r in self.packet["records"]]}

    def resolution(self, ident, kind, criterion, selected):
        return {"packet_sha256":fingerprint(self.packet),
                "first_sha256":fingerprint(self.first),
                "second_sha256":fingerprint(self.second),
                "adjudicated_sha256":fingerprint(self.final),
                "records":[{"blind_id":ident,"kind":kind,"criterion":criterion,
                            "selected_status":selected,"adjudicator":"third reviewer",
                            "rationale":"Fictional explicitly recorded criterion review"}]}

    def test_agreement_still_requires_human_review(self):
        r=assess(self.packet,self.first,self.second,self.final)
        self.assertEqual(r["status"],"ready_for_independent_review")
        self.assertEqual(r["criteria_compared"],4)
        self.assertEqual(r["resolved_disagreements"],0)
        self.assertEqual(r["first_sha256"],fingerprint(self.first))
        self.assertFalse(r["reviewer_independence_verified"])
        self.assertFalse(r["release_approved"])

    def test_unresolved_expected_disagreement_holds(self):
        self.second["records"][0]["expected"][0]["status"]="fail"
        r=assess(self.packet,self.first,self.second,self.final)
        self.assertEqual(r["status"],"hold_missing_or_unresolved_review")
        self.assertIn("disagreements_unresolved",r["hold_reasons"])
        self.assertEqual(len(r["unresolved_disagreements"]),1)

    def test_explicit_resolution_binds_originals_and_final(self):
        self.second["records"][0]["expected"][0]["status"]="fail"
        ident=self.first["records"][0]["blind_id"]
        resolution=self.resolution(ident,"expected",1,"pass")
        r=assess(self.packet,self.first,self.second,self.final,resolution)
        self.assertEqual(r["resolved_disagreements"],1)
        self.assertEqual(r["status"],"ready_for_independent_review")
        self.assertEqual(r["resolutions_sha256"],fingerprint(resolution))
        self.assertFalse(r["adjudicator_independence_verified"])

    def test_original_critical_signal_survives_favorable_adjudication(self):
        self.second["records"][0]["disqualifiers"][0]["status"]="observed"
        ident=self.second["records"][0]["blind_id"]
        resolution=self.resolution(ident,"disqualifiers",1,"absent")
        r=assess(self.packet,self.first,self.second,self.final,resolution)
        self.assertEqual(r["status"],"escalate_to_owner")
        self.assertEqual(len(r["original_observed_disqualifier_signals"]),1)
        self.assertFalse(r["safety_certified"])

    def test_consensus_cannot_be_silently_overridden(self):
        self.final["records"][0]["expected"][0]["status"]="fail"
        with self.assertRaisesRegex(ValueError,"changes reviewer consensus"):
            assess(self.packet,self.first,self.second,self.final)

    def test_missing_reviewer_or_final_coverage_holds(self):
        self.second["records"].pop()
        r=assess(self.packet,self.first,self.second,self.final)
        self.assertIn("original_reviewer_coverage_incomplete",r["hold_reasons"])
        self.assertIn("adjudicated_slots_without_two_reviewers",r["hold_reasons"])
        self.second=self.grade("second reviewer")
        self.final["records"].pop()
        r=assess(self.packet,self.first,self.second,self.final)
        self.assertIn("adjudicated_grades_incomplete",r["hold_reasons"])

    def test_unknown_original_status_cannot_be_erased(self):
        self.first["records"][0]["expected"][0]["status"]="not_observable"
        self.second["records"][0]["expected"][0]["status"]="not_observable"
        self.final["records"][0]["expected"][0]["status"]="not_observable"
        r=assess(self.packet,self.first,self.second,self.final)
        self.assertEqual(r["status"],"hold_missing_or_unresolved_review")
        self.assertIn("original_review_unobservable",r["hold_reasons"])

    def test_tampered_grade_or_review_identity_rejected(self):
        bad=copy.deepcopy(self.first)
        bad["records"][0]["output_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"artifact mismatch"):
            assess(self.packet,bad,self.second,self.final)
        bad=copy.deepcopy(self.second)
        bad["records"][0]["reviewer"]="first reviewer"
        with self.assertRaisesRegex(ValueError,"same reviewer identifier"):
            assess(self.packet,self.first,bad,self.final)

    def test_resolution_drift_and_unrelated_resolution_rejected(self):
        self.second["records"][0]["expected"][0]["status"]="fail"
        ident=self.first["records"][0]["blind_id"]
        resolution=self.resolution(ident,"expected",1,"pass")
        resolution["second_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"source mismatch"):
            assess(self.packet,self.first,self.second,self.final,resolution)
        resolution=self.resolution(ident,"disqualifiers",1,"absent")
        with self.assertRaisesRegex(ValueError,"not a unique graded disagreement"):
            assess(self.packet,self.first,self.second,self.final,resolution)
        resolution=self.resolution(ident,"expected",1,"fail")
        with self.assertRaisesRegex(ValueError,"differs from adjudicated"):
            assess(self.packet,self.first,self.second,self.final,resolution)

    def test_resolution_requires_separate_label_and_no_duplicates(self):
        self.second["records"][0]["expected"][0]["status"]="fail"
        ident=self.first["records"][0]["blind_id"]
        resolution=self.resolution(ident,"expected",1,"pass")
        resolution["records"][0]["adjudicator"]="first reviewer"
        with self.assertRaisesRegex(ValueError,"adjudicator label"):
            assess(self.packet,self.first,self.second,self.final,resolution)
        resolution=self.resolution(ident,"expected",1,"pass")
        resolution["records"].append(copy.deepcopy(resolution["records"][0]))
        with self.assertRaisesRegex(ValueError,"unique graded disagreement"):
            assess(self.packet,self.first,self.second,self.final,resolution)


if __name__=="__main__":
    unittest.main()
