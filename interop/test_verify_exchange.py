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
        from interop.validate_crawl_evidence import parse
        def manifest_only(raw):
            if raw==self.raw or raw==self.raw+b" ":
                raise AssertionError("must not parse evidence")
            return parse(raw)
        with patch("interop.verify_exchange.parse",side_effect=manifest_only), patch("interop.verify_exchange.validate",side_effect=AssertionError("must not validate")):
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

    def test_producer_8e3ca8f_contract_string_holds(self):
        # The real producer's exchange-manifest.ts at 8e3ca8f emits this string;
        # our accepted 17-key layout requires an object, not a second format.
        self.m["contract"]="seo-crawl-evidence/0.1.0"
        r=self.check()
        self.assertEqual(r["disposition"],"hold")
        self.assertIn("manifest.contract_mismatch",r["issues"])
        self.assertFalse(r["byte_length_verified"])
        self.assertFalse(r["manifest_binding_verified"])
        self.assertEqual(r["consumer_validation"],"not_run")

    def test_observation_definition_version_does_not_change_contract_pin(self):
        self.m["contract"]={"name":"seo-crawl-evidence","version":"1.1.0"}
        r=self.check()
        self.assertEqual(r["disposition"],"hold")
        self.assertIn("manifest.contract_mismatch",r["issues"])
        # Observation definition 1.1.0 is separate from evidence schema 0.1.0.

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

    def test_bom_and_invalid_utf8_with_correct_checksum(self):
        for raw,code in ((b"\xef\xbb\xbf"+self.raw,"evidence.utf8_bom_forbidden"),
                         (b"\xff"+self.raw,"evidence.invalid_utf8")):
            self.m.update(evidence_sha256=digest(raw),evidence_bytes=len(raw))
            r=self.check(raw)
            self.assertTrue(r["checksum_verified"])
            self.assertFalse(r["evidence_json_parsed"])
            self.assertIn(code,r["issues"])
            self.assertEqual(r["consumer_validation"],"not_run")

    def test_length_before_checksum_and_exact_bytes(self):
        self.m["evidence_bytes"]=0
        r=self.check()
        self.assertFalse(r["byte_length_verified"])
        self.assertFalse(r["checksum_verified"])
        self.m["evidence_bytes"]=len(self.raw)
        r=self.check(self.raw+b"\n")
        self.assertFalse(r["byte_length_verified"])
        altered=bytes([self.raw[0]])+self.raw[1:-1]+b" "
        r=self.check(altered)
        self.assertTrue(r["byte_length_verified"])
        self.assertFalse(r["checksum_verified"])
        self.assertFalse(r["evidence_json_parsed"])

    def test_invalid_declaration_never_candidate(self):
        for v in ("PASS",True,{},None):
            self.m["producer_validation"]=v
            r=self.check()
            self.assertIn("manifest.invalid_producer_declaration",r["issues"])
            self.assertEqual(r["disposition"],"hold")

    def test_binding_precedes_canonical_validation(self):
        self.m["run_id"]="different"
        with patch("interop.verify_exchange.validate",side_effect=AssertionError("wrong stage")):
            r=self.check()
        self.assertTrue(r["evidence_json_parsed"])
        self.assertFalse(r["manifest_binding_verified"])
        self.assertEqual(r["consumer_validation"],"not_run")

    def test_unvalidated_shape_and_type_exact_equality(self):
        from interop.verify_exchange import same_json
        self.assertFalse(same_json({"count":True},{"count":1}))
        self.assertFalse(same_json([1,2],[2,1]))
        self.rebind({"run":[],"producer":None})
        r=self.check()
        self.assertTrue(r["evidence_json_parsed"])
        self.assertFalse(r["manifest_binding_verified"])

    def test_negative_zero_held_without_rewrite(self):
        # Insert -0 into an existing integer field without introducing an extra member.
        import re
        raw=re.sub(rb'("max_pages"\s*:\s*)[0-9]+',rb'\g<1>-0',self.raw,count=1)
        self.assertNotEqual(raw,self.raw)
        self.m.update(evidence_sha256=digest(raw),evidence_bytes=len(raw))
        r=self.check(raw)
        self.assertTrue(r["checksum_verified"])
        self.assertTrue(r["manifest_binding_verified"])
        self.assertIn("negative_zero_spelling",r["consumer_preflight"]["reasons"])
        self.assertEqual(r["disposition"],"hold")


if __name__=="__main__":
    unittest.main()
