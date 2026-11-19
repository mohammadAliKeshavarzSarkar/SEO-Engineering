"""Synthetic manifest tests only; never evidence of an actual collection run."""
import copy
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from interop.validate_crawl_evidence import digest, load_pin, load_validator, read_local
from interop.exchange_profile import PROFILE_ID
from interop.verify_exchange import verify


class ExchangeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pin=load_pin()
        root=Path(os.environ["WBS_FIXTURE_ROOT"])
        cls.validator=load_validator(read_local(root/cls.pin["contract"]["schema_path"]),cls.pin)
        cls.base=json.loads(read_local(root/"packages/evidence-contract/fixtures/valid/complete-page.json"))

    def setUp(self):
        self.commit="a"*40  # fictional export revision, not actual producer provenance
        self.doc=copy.deepcopy(self.base)
        self.doc["producer"]["version"]=self.commit
        self.raw=json.dumps(self.doc,ensure_ascii=False).encode()
        run=self.doc["run"]
        self.m={"contract":{"name":self.pin["contract"]["name"],"version":"0.1.0"},
                "exchange_profile":PROFILE_ID,"producer_commit":self.commit,
                "contract_source_commit":self.pin["producer_commit"],
                "schema_sha256":self.pin["contract"]["schema_sha256"],
                "evidence_sha256":digest(self.raw),"checksum_algorithm":"SHA-256",
                "evidence_filename":"evidence.json","evidence_bytes":len(self.raw),
                "run_id":run["id"],"authorization_ref":"fictional-test-only",
                "authorized_scope":run["scope"],"started_at":run["started_at"],
                "finished_at":run["finished_at"],"coverage_limitations":run["limitations"],
                "producer_validation":"pass","producer_preflight":"pass"}

    def check(self,raw=None,name="evidence.json"):
        return verify(json.dumps(self.m).encode(),self.raw if raw is None else raw,
                      name,self.validator,self.pin,self.commit)

    def rebind(self,doc):
        self.raw=json.dumps(doc,ensure_ascii=True).encode()
        self.m.update(evidence_sha256=digest(self.raw),evidence_bytes=len(self.raw))

    def test_candidate_is_not_actual_exchange(self):
        r=self.check()
        self.assertEqual(r["disposition"],"candidate_for_joint_review",r)
        self.assertTrue(r["checksum_verified"])
        self.assertTrue(r["manifest_binding_verified"])
        for field in ("authorization_verified","provenance_verified","producer_validation_independently_verified",
                      "actual_exchange_verified","operational_integration_approved"):
            self.assertFalse(r[field])
        self.assertEqual(r["producer_validation"],"declared_pass")
        self.assertEqual(r["consumer_validation"],"valid")

    def test_checksum_checked_before_parsing(self):
        with patch("interop.verify_exchange.validate",side_effect=AssertionError("must not parse")):
            self.assertEqual(self.check(self.raw+b" ")["consumer_validation"],"not_run")
            self.m["evidence_sha256"]="0"*64
            self.assertFalse(self.check()["checksum_verified"])

    def test_manifest_identity_and_unsafe_filename(self):
        for field,value in (("producer_commit","b"*40),("contract_source_commit","b"*40),
                            ("schema_sha256","0"*64),("exchange_profile","unreviewed"),
                            ("evidence_filename","../evidence.json"),("evidence_bytes",True)):
            with self.subTest(field=field):
                original=self.m[field]
                self.m[field]=value
                self.assertEqual(self.check()["disposition"],"hold")
                self.m[field]=original
        self.assertEqual(self.check(name="wrong.json")["disposition"],"hold")

    def test_manifest_binding(self):
        for field,value in (("run_id","wrong"),("authorization_ref"," "),
                            ("authorized_scope",{}),("coverage_limitations",[{}]),
                            ("finished_at","2026-12-01T00:00:00Z")):
            original=self.m[field]
            self.m[field]=value
            r=self.check()
            self.assertTrue(r["checksum_verified"])
            self.assertFalse(r["manifest_binding_verified"])
            self.m[field]=original
        self.doc["producer"]["version"]="0.1.0"
        self.rebind(self.doc)
        self.assertFalse(self.check()["manifest_binding_verified"])

    def test_producer_status_remains_independent(self):
        self.m["producer_preflight"]="fail"
        r=self.check()
        self.assertEqual(r["consumer_validation"],"valid")
        self.assertEqual(r["consumer_preflight"]["status"],"within_profile")
        self.assertEqual(r["disposition"],"hold")

    def test_profile_violation_with_matching_hash(self):
        self.doc["pages"][0]["observations"]["http"]["value"]["transactions"][-1]["headers"].append(
            {"name":"link","values":["</fa>; title="+chr(127)]})
        self.rebind(self.doc)
        r=self.check()
        self.assertTrue(r["checksum_verified"])
        self.assertEqual(r["consumer_preflight"]["status"],"outside_profile")
        self.assertEqual(r["disposition"],"hold")

    def test_manifest_duplicates_and_extra_fields(self):
        bad=b'{"run_id":"a","run_id":"b"}'
        r=verify(bad,self.raw,"evidence.json",self.validator,self.pin,self.commit)
        self.assertEqual(r["consumer_validation"],"not_run")
        self.m["unexpected"]=True
        self.assertFalse(self.check()["checksum_verified"])


if __name__=="__main__":
    unittest.main()
