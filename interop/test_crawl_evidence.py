"""Execute the accepted fixtures, plus independent consumer regression cases.

Provide WBS_FIXTURE_ROOT as a trusted checkout of the pinned producer commit.
Do not copy producer files into this repository or fetch anything in tests.
"""
import copy
import json
import os
from pathlib import Path
import unittest

from interop.exchange_profile import profile, preflight
from interop.validate_crawl_evidence import (
    BoundaryError, digest, load_pin, load_validator, read_local, validate, receipt,
)


class CompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(os.environ["WBS_FIXTURE_ROOT"])
        cls.pin=load_pin()
        cls.schema=read_local(cls.root/cls.pin["contract"]["schema_path"])
        cls.validator=load_validator(cls.schema,cls.pin)

    def raw(self,name):
        return read_local(self.root/"packages/evidence-contract/fixtures/valid"/name)

    def check(self,data,status="invalid"):
        raw=json.dumps(data,ensure_ascii=False).encode()
        result,_=validate(raw,self.validator)
        self.assertEqual(result["status"],status,result)
        return result

    def test_all_authoritative_fixtures(self):
        self.assertEqual(len(self.pin["fixtures"]),20)
        expected_counts={"valid":0,"invalid":0}
        for item in self.pin["fixtures"]:
            with self.subTest(fixture=item["path"]):
                raw=read_local(self.root/item["path"])
                self.assertEqual(digest(raw),item["sha256"])
                result,doc=validate(raw,self.validator)
                self.assertEqual(result["status"],item["expected"],result)
                expected_counts[result["status"]]+=1
                if doc is not None:
                    self.assertEqual(doc,json.loads(raw))
        self.assertEqual(expected_counts,{"valid":9,"invalid":11})

    def test_preservation(self):
        for name in ("persian-utf8.json","redirect-repeated-headers.json","partial-crawl.json",
                     "rendering-not-collected.json","observed-absent-metadata.json","cross-page-diagnostic.json"):
            raw=self.raw(name)
            result,doc=validate(raw,self.validator)
            self.assertEqual(result["status"],"valid",result)
            self.assertEqual(doc,json.loads(raw))
            report=receipt(raw,self.validator,self.pin)
            self.assertEqual(report["input_sha256"],digest(raw))
            self.assertFalse(report["actual_exchange_verified"])
            self.assertFalse(report["authorization_verified"])

    def test_duplicate_members_and_malformed_json(self):
        for raw in (b'{"a":1,"a":2}',b'{"x":{"a":1,"\\u0061":2}}',b'{"x":NaN}',b'{"\\q":1}',b'\xff'):
            result,_=validate(raw,self.validator)
            self.assertEqual(result["status"],"invalid",result)

    def test_unsupported_version(self):
        d=json.loads(self.raw("complete-page.json"))
        d["contract"]["version"]="0.1.1"
        self.check(d)

    def test_wrong_schema_hash(self):
        with self.assertRaises(BoundaryError):
            load_validator(self.schema+b"\n",self.pin)

    def test_sensitive_metadata_canonical(self):
        d=json.loads(self.raw("complete-page.json"))
        d["pages"][0]["observations"]["metadata"]["value"]["canonical_urls"]=["https://example.com/?%74oken=synthetic-secret"]
        r=self.check(d)
        self.assertNotIn("synthetic-secret",json.dumps(r))
        self.assertTrue(any(i["code"]=="semantic.unsafe_url" for i in r["issues"]))

    def test_scope_mismatch(self):
        d=json.loads(self.raw("cross-page-diagnostic.json"))
        diag=d["diagnostics"]["value"][0]
        diag["evidence_scope"]="subject_page"
        diag["related_page_ids"]=[]
        self.check(d)

    def test_pointer_conflicts_and_unknown_reason(self):
        base=json.loads(self.raw("complete-page.json"))
        for pointers in (["/missing"],["/canonical_urls/01"],["/title","/title"],["/canonical_urls","/canonical_urls/0"]):
            d=copy.deepcopy(base)
            o=d["pages"][0]["observations"]["metadata"]
            o["field_overrides"]=[{"path":p,"provenance":o["provenance"]} for p in pointers]
            self.check(d)
        d=copy.deepcopy(base)
        d["pages"][0]["observations"]["rendering"]["reasons"]=["unrecognized_reason"]
        self.check(d)

    def test_duplicate_transaction_ids(self):
        d=json.loads(self.raw("redirect-repeated-headers.json"))
        txs=d["pages"][0]["observations"]["http"]["value"]["transactions"]
        txs[1]["id"]=txs[0]["id"]
        self.check(d)

    def test_consumer_guard_is_not_contract_rejection(self):
        raw=b'{"n":9007199254740992}'
        result,_=validate(raw,self.validator)
        self.assertEqual(result["status"],"blocked")
        result,_=validate(b'{"s":"\\ud800"}',self.validator)
        self.assertEqual(result["status"],"blocked")

    def test_exchange_profile_all_valid_fixtures(self):
        for item in self.pin["fixtures"]:
            if item["expected"]=="valid":
                raw=read_local(self.root/item["path"])
                r=preflight(raw,self.validator)
                self.assertEqual(r["disposition"],"candidate_for_joint_review",r)
                self.assertEqual(r["profile_agreement"],"pending_producer_review")
                self.assertFalse(r["actual_exchange_verified"])

    def test_exchange_profile_five_known_differences(self):
        base=json.loads(self.raw("complete-page.json"))
        cases=[]
        d=copy.deepcopy(base)
        d["run"]["started_at"]="2026-11-18T10:00:00.000900Z"
        d["run"]["finished_at"]="2026-11-18T10:00:00.000100Z"
        cases.append((d,"timestamp_precision_exceeds_milliseconds"))
        d=copy.deepcopy(base)
        d["run"]["limits"]["max_pages"]=9007199254740993
        cases.append((d,"numeric_range"))
        d=copy.deepcopy(base)
        d["pages"][0]["observations"]["metadata"]["value"]["title"]=chr(0xd800)
        cases.append((d,"unpaired_unicode_surrogate"))
        d=copy.deepcopy(base)
        d["pages"][0]["observations"]["http"]["value"]["transactions"][-1]["headers"].append(
            {"name":"location","values":["https://example.com\\path"]})
        cases.append((d,"ambiguous_url_representation"))
        d=copy.deepcopy(base)
        d["run"]["finished_at"]="2026-12-31T23:59:60Z"
        cases.append((d,"leap_second"))
        for doc,reason in cases:
            raw=json.dumps(doc,ensure_ascii=True).encode()
            r=preflight(raw,self.validator)
            self.assertEqual(r["disposition"],"hold",r)
            self.assertIn(reason,r["profile"]["reasons"])
            self.assertEqual(r["consumer_validation"],validate(raw,self.validator)[0]["status"])

    def test_profile_is_not_canonical_validation(self):
        raw=self.raw("complete-page.json")
        altered=json.loads(raw)
        altered["run"]["limits"]["max_pages"]=10.0
        raw=json.dumps(altered).encode()
        self.assertEqual(validate(raw,self.validator)[0]["status"],"valid")
        r=preflight(raw,self.validator)
        self.assertEqual(r["disposition"],"hold")
        self.assertIn("non_integer_number_spelling",r["profile"]["reasons"])
        self.assertEqual(profile(b'{"x":1,"x":2}')["status"],"not_assessed")
        self.assertEqual(preflight(b'{}',self.validator)["disposition"],"hold")


if __name__=="__main__":
    unittest.main()
