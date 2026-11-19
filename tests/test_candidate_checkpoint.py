import copy
import unittest
from pathlib import Path

from scripts.check_candidate_checkpoint import validate, REQUIRED, OPTIONAL
from scripts.score_benchmark import load

ROOT=Path(__file__).resolve().parents[1]


class CandidateCheckpointTests(unittest.TestCase):
    def setUp(self):
        self.record=load(ROOT/"operations/ts05-candidate-checkpoint.json")

    def test_actual_checkpoint_held(self):
        r=validate(self.record)
        self.assertEqual(r["mandatory_gate_count"],16)
        self.assertEqual(r["recorded_passes"],5)
        self.assertEqual(len(r["open_mandatory_gates"]),11)
        self.assertEqual(r["separate_optional_gates"],[{"id":"websitebotscroll_exchange","state":"not_run"}])
        self.assertFalse(r["release_approved"])
        self.assertFalse(r["evidence_authenticity_verified"])

    def test_required_gates_cannot_disappear(self):
        for mode in ("missing","duplicate","downgrade"):
            with self.subTest(mode=mode):
                r=copy.deepcopy(self.record)
                if mode=="missing": r["gates"].pop(0)
                elif mode=="duplicate": r["gates"].append(r["gates"][0])
                else: r["gates"][0]["required"]=False
                with self.assertRaises(ValueError): validate(r)

    def test_invalid_candidate_rejected(self):
        for field,value in (("source_commit","main"),("archive_sha256","0"),("version","0.3.0"),
                            ("scope","with_provider")):
            with self.subTest(field=field):
                r=copy.deepcopy(self.record)
                r["candidate"][field]=value
                with self.assertRaises(ValueError): validate(r)

    def test_claimed_pass_without_reference(self):
        self.record["gates"][0]["evidence_refs"]=[]
        with self.assertRaises(ValueError): validate(self.record)

    def test_approval_cannot_be_inferred(self):
        for g in self.record["gates"]:
            g["state"]="observed_pass"
            g["evidence_refs"]=["synthetic test; not independent evidence"]
        r=validate(self.record)
        self.assertEqual(r["recorded_passes"],16)
        self.assertFalse(r["release_approved"])
        self.assertEqual(r["release_decision"],"hold")
        self.record["release_decision"]="approve"
        with self.assertRaises(ValueError): validate(self.record)

    def test_no_true_approval_flag(self):
        self.record["release_approved"]=True
        with self.assertRaises(ValueError): validate(self.record)
