"""Fictional data tests for the private evidence intake; no model sessions."""
import copy
import tempfile
import unittest
from pathlib import Path
from scripts.review_activation_evidence import review
from scripts.verify_package import digest


class ActivationEvidenceTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.pair={"kind":"local_pilot_pair_integrity",
                   "stage_bytes_matched_to_source_archive":True,
                   "control_sha256":"c"*64,"candidate_commit_declared":"a"*40,
                   "archive_sha256":"b"*64,"runtime_kind":"cursor"}
        self.record={"control_sha256":"c"*64,"candidate_commit":"a"*40,
                     "archive_sha256":"b"*64,"runtime_kind":"cursor",
                     "operator":"fictional local operator",
                     "authorization_ref":"fictional approval reference",
                     "probes":{}}
        for arm in ("baseline","skill"):
            self.record["probes"][arm]={
                "runtime_version":"Cursor fictional version",
                "model":"fictional model", "settings_ref":"matching synthetic settings",
                "session_ref":"fictional-session-"+arm,"trace_ref":None,
                "trace_sha256":None,
                "discovery":"absent" if arm=="baseline" else "present",
                "entrypoint_read":"absent" if arm=="baseline" else "present",
                "routed_reference_read":"absent" if arm=="baseline" else "present",
                "unrelated_activation":"absent",
                "read_isolation":"verified_by_operator",
                "tool_permissions":"verified_by_operator",
                "observation_ref":"fictional observation "+arm}

    def add_traces(self):
        for arm in ("baseline","skill"):
            p=self.root/arm
            p.mkdir()
            raw=("fictional trace for "+arm).encode()
            (p/"probe.txt").write_bytes(raw)
            self.record["probes"][arm]["trace_ref"]=arm+"/probe.txt"
            self.record["probes"][arm]["trace_sha256"]=digest(raw)

    def test_nominal_claims_require_independent_review(self):
        self.add_traces()
        r=review(self.pair,self.record,self.root)
        self.assertEqual(r["status"],"ready_for_independent_review")
        self.assertFalse(r["actual_activation_certified"])
        self.assertFalse(r["trace_semantics_verified"])
        self.assertFalse(r["read_isolation_certified"])
        self.assertFalse(r["paid_pilot_authorized"])
        self.assertFalse(r["release_approved"])

    def test_missing_traces_and_unknown_holds(self):
        self.record["probes"]["skill"]["routed_reference_read"]="unknown"
        self.record["probes"]["baseline"]["read_isolation"]="unknown"
        r=review(self.pair,self.record,self.root)
        self.assertEqual(r["status"],"hold_missing_or_unobservable")
        self.assertIn("baseline:trace_unavailable",r["missing_or_unobservable"])

    def test_baseline_contamination_or_permission_failure_escalates(self):
        self.add_traces()
        self.record["probes"]["baseline"]["discovery"]="present"
        self.record["probes"]["skill"]["tool_permissions"]="failed"
        r=review(self.pair,self.record,self.root)
        self.assertEqual(r["status"],"escalate_to_owner")
        self.assertIn("baseline:discovery_unexpected",r["critical_declaration_conflicts"])

    def test_changed_or_wrong_trace_rejected(self):
        self.add_traces()
        (self.root/"skill/probe.txt").write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError,"trace missing, changed"):
            review(self.pair,self.record,self.root)
        self.record["probes"]["skill"]["trace_ref"]="../unknown"
        with self.assertRaisesRegex(ValueError,"nonfixed"):
            review(self.pair,self.record,self.root)

    def test_candidate_mismatch_and_model_divergence(self):
        self.add_traces()
        self.record["control_sha256"]="d"*64
        with self.assertRaisesRegex(ValueError,"candidate binding mismatch"):
            review(self.pair,self.record,self.root)
        self.record["control_sha256"]="c"*64
        self.record["probes"]["skill"]["model"]="another fictional model"
        r=review(self.pair,self.record,self.root)
        self.assertIn("pair:model_mismatch",r["critical_declaration_conflicts"])

    def test_duplicate_session_or_extra_field_rejected(self):
        self.add_traces()
        self.record["probes"]["skill"]["session_ref"]=self.record["probes"]["baseline"]["session_ref"]
        with self.assertRaisesRegex(ValueError,"session reused"):
            review(self.pair,self.record,self.root)
        self.record["probes"]["skill"]["session_ref"]="new fictional session"
        x=copy.deepcopy(self.record)
        x["probes"]["baseline"]["surprise"]="not allowed"
        with self.assertRaisesRegex(ValueError,"unexpected probe fields"):
            review(self.pair,x,self.root)


if __name__=="__main__":
    unittest.main()
