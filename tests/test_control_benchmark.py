import copy
import unittest
from scripts.control_benchmark import schedule, dispatch, blind_packet, finalize, fingerprint

def fixture():
    suite={"version":"fixture","cases":[{"id":x,"prompt":"Question "+x,
           "expected":["criterion"],"disqualifiers":["critical"]} for x in ("A","B","C")]}
    config=dict(model="fictional exact model",runtime="fixture runner",inference_settings="fixed",
        tool_config="none",permission_mode="read-only",skill_commit="a"*40,archive_sha256="b"*64,
        launch_protocol="fresh sessions",review_protocol="independent reviewers",
        suite_kind="public_regression",repeats=2,treatment="complete_toolkit",
        task_context_sha256="c"*64,seed=42,budget="equal",
        rubric_access_policy="rubric inaccessible",candidate_variant="rubric_restricted")
    ctl=schedule(suite,config,["A","B","C"])
    ledger={"control_sha256":fingerprint(ctl),"runs":[dict(
        blind_id=s["blind_id"],status="completed",session_ref="session",environment_ref="environment",
        output_ref="output/"+s["blind_id"],output_sha256="d"*64,trace_ref="trace/"+s["blind_id"],
        trace_sha256="e"*64,failure_reason=None) for s in ctl["slots"]]}
    return suite,ctl,ledger

def grades_for(packet):
    return {"packet_sha256":fingerprint(packet),"records":[{
        "blind_id":r["blind_id"],"reviewer":"fictional grader",
        "output_sha256":r["output_sha256"],"trace_sha256":r["trace_sha256"],
        "expected":[{"criterion":1,"status":"pass","evidence":"synthetic test"}],
        "disqualifiers":[{"criterion":1,"status":"absent","evidence":"synthetic test"}]
        } for r in packet["records"]]}

class ControlTests(unittest.TestCase):
    def test_frozen_balanced_schedule(self):
        suite,c,_=fixture()
        self.assertEqual(c,schedule(suite,c["plan"]["config"],c["cohort_ids"]))
        pairs=[c["slots"][i:i+2] for i in range(0,len(c["slots"]),2)]
        self.assertEqual(len(pairs),6)
        self.assertEqual(sum(p[0]["arm"]=="baseline" for p in pairs),3)
        for a,b in pairs:
            self.assertEqual((a["case_id"],a["repeat"]),(b["case_id"],b["repeat"]))
            self.assertNotEqual(a["arm"],b["arm"])

    def test_dispatch_prompt_only(self):
        _,c,_=fixture()
        self.assertEqual(set(dispatch(c,c["slots"][0]["blind_id"])),{"prompt"})
        with self.assertRaises(ValueError): dispatch(c,"unknown")

    def test_requires_reviewed_config(self):
        s,c,_=fixture()
        cfg=copy.deepcopy(c["plan"]["config"])
        for key,value in (("model","REPLACE me"),("archive_sha256","fake"),("seed",True),
                          ("candidate_variant","unmodified")):
            with self.subTest(key=key):
                altered=cfg|{key:value}
                with self.assertRaises(ValueError): schedule(s,altered,c["cohort_ids"])

    def test_blind_packet_no_structural_arm_leak(self):
        s,c,l=fixture()
        p=blind_packet(s,c,l)
        self.assertEqual([r["blind_id"] for r in p["records"]],c["presentation_order"])
        for row in p["records"]:
            self.assertFalse({"arm","repeat","session_ref","environment_ref","case_id"}&row.keys())

    def test_complete_synthetic_scoring_never_certifies(self):
        s,c,l=fixture()
        r=finalize(s,c,l,grades_for(blind_packet(s,c,l)))
        self.assertEqual(r["matched_pairs"],6)
        self.assertTrue(r["complete"])
        self.assertFalse(r["release_certified"])
        self.assertFalse(r["independent_review_verified"])

    def test_failed_and_ungraded_slots_visible(self):
        s,c,l=fixture()
        l["runs"][0].update(status="timeout",failure_reason="synthetic timeout")
        p=blind_packet(s,c,l)
        g=grades_for(p);g["records"].pop()
        r=finalize(s,c,l,g)
        self.assertFalse(r["complete"])
        self.assertFalse(r["skill_internal_case_gate"])
        self.assertEqual(r["completed_ungraded"],1)
        self.assertEqual(sum(a["timeout"] for a in r["execution_counts"].values()),1)

    def test_ledger_not_allowed_to_omit_failures(self):
        s,c,l=fixture();l["runs"].pop()
        with self.assertRaises(ValueError): blind_packet(s,c,l)

    def test_tampered_grade_artifacts_rejected(self):
        s,c,l=fixture()
        g=grades_for(blind_packet(s,c,l))
        g["records"][0]["output_sha256"]="0"*64
        with self.assertRaises(ValueError): finalize(s,c,l,g)

    def test_control_and_ledger_binding(self):
        s,c,l=fixture();c["slots"][0]["arm"]="other"
        with self.assertRaises(ValueError): blind_packet(s,c,l)
        s,c,l=fixture();l["control_sha256"]="0"*64
        with self.assertRaises(ValueError): blind_packet(s,c,l)

    def test_uncompleted_grade_rejected(self):
        s,c,l=fixture()
        l["runs"][0].update(status="not_started",failure_reason="not launched")
        g=grades_for(blind_packet(s,c,l))
        g["records"][0]["blind_id"]=l["runs"][0]["blind_id"]
        with self.assertRaises(ValueError): finalize(s,c,l,g)
