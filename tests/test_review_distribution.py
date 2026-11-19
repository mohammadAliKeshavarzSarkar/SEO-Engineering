import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_skill import build, LIBRARY_DIRS
from scripts.review_distribution import scan, scan_bytes, blank_review, review_status, safe_path


class ReviewDistributionTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        def put(name,text):
            p=self.root/name
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(text,encoding="utf-8")
        for d in LIBRARY_DIRS: put(d+"/demo.md","Fictional example")
        put("skills/seo-engineering/SKILL.md","---\nname: seo-engineering\ndescription: Synthetic skill\n---\n")
        put("skills/seo-engineering/references/router.md","router")
        put("skills/seo-engineering/references/execution-contract.md","contract")
        for name in ("audit_html.py","check_docs.py","cluster_keywords.py","audit_topic_graph.py",
                     "prioritize_opportunities.py","audit_locale_manifest.py","validate_research.py",
                     "inspect_architecture.py","audit_rendering.py","audit_spa_build.py","audit_next_delivery.py",
                     "audit_crawl_evidence.py","audit_index_evidence.py","audit_migration.py","audit_metadata.py",
                     "audit_performance.py","audit_technical.py","review_release_gates.py","review_incident.py","README.md"):
            put("scripts/"+name,"demo")
        put("private-looking-not-packaged.txt","https://example.invalid/?token="+"fictional-test-value")
        put("docs/sample.md","Contact fictional@example.invalid")
        self.archive=self.root/"candidate.zip"
        build(self.root,self.archive)

    def report(self):
        return scan(self.root,self.archive,"a"*40,["docs/sample.md","private-looking-not-packaged.txt"])

    def test_distinct_archive_and_tracked_scope(self):
        r=self.report()
        self.assertGreater(r["summary"]["archive"]["files"],0)
        self.assertEqual(r["summary"]["tracked"]["files"],2)
        self.assertEqual(r["summary"]["tracked"]["signals"],2)
        self.assertFalse(r["privacy_approved"])
        self.assertFalse(r["release_approved"])
        self.assertNotIn("fictional-test-value",json.dumps(r))
        self.assertNotIn("fictional@example.invalid",json.dumps(r))

    def test_secret_shapes_no_values(self):
        raw=("https://u:synthetic@example.invalid\n"+"gh"+"p_"+"A"*36+"\n"+
             "-----BEGIN "+"PRIVATE KEY-----\n"+"api_key = 'fictional-test-value'").encode()
        state,s=scan_bytes(raw)
        self.assertEqual(state,"scanned")
        self.assertEqual({x["rule"] for x in s},{"url_userinfo","token_shape","private_key_marker","credential_assignment","email_shape"})

    def test_non_utf8_and_nul_explicit(self):
        self.assertEqual(scan_bytes(b"\xff")[0],"non_utf8")
        self.assertEqual(scan_bytes(b"a\0b")[0],"binary_or_nul")

    def test_blank_record_is_incomplete(self):
        r=self.report();v=blank_review(r);s=review_status(r,v)
        self.assertFalse(s["review_record_complete"])
        self.assertEqual(s["unreviewed_files"],len(r["files"]))

    def test_complete_attestation_not_approval(self):
        r=self.report();v=blank_review(r)
        v.update(reviewer="fictional reviewer",authorization_ref="fictional approval reference")
        for row,source in zip(v["files"],r["files"]):
            row.update(state="reviewed_with_findings" if source["signals"] else "reviewed_no_issue",evidence="synthetic test")
        for row in v["findings"]:
            row.update(disposition="synthetic_or_public_reference",evidence="synthetic test")
        result=review_status(r,v)
        self.assertTrue(result["review_record_complete"])
        self.assertFalse(result["privacy_approved"])
        self.assertFalse(result["release_approved"])

    def test_missing_duplicate_stale_review_rejected(self):
        r=self.report()
        for mode in ("missing","duplicate","stale"):
            v=blank_review(r)
            if mode=="missing": v["files"].pop()
            elif mode=="duplicate": v["findings"].append(copy.deepcopy(v["findings"][0]))
            else: v["report_sha256"]="0"*64
            with self.assertRaises(ValueError): review_status(r,v)

    def test_unreviewed_finding_cannot_disappear(self):
        r=self.report();v=blank_review(r)
        v["findings"][0].update(disposition="requires_correction",evidence="synthetic blocker")
        s=review_status(r,v)
        self.assertGreater(s["unresolved_or_correction_signals"],0)
        self.assertFalse(s["review_record_complete"])

    def test_path_traversal_and_symlink(self):
        with self.assertRaises(ValueError): safe_path(self.root,"../outside")
        (self.root/"alias").symlink_to(self.root/"docs")
        with self.assertRaises(ValueError): safe_path(self.root,"alias/sample.md")

    def test_source_changed_rejects_archive(self):
        (self.root/"docs/sample.md").write_text("different")
        with self.assertRaises(ValueError): self.report()
