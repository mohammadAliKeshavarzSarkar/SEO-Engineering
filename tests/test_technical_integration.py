"""Synthetic reviewed handoffs; never an automatic provider mapping."""
import copy
import json
import unittest
from pathlib import Path

from scripts.audit_technical import audit
from scripts.review_release_gates import review as release_review
from scripts.review_incident import review as incident_review

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT/'examples'/name).read_text(encoding='utf-8'))

def adverse_audit():
    return audit(load('technical-audit/adverse.json'),ROOT/'examples/spa-build/artifacts')

class TechnicalIntegrationTests(unittest.TestCase):
    def test_failed_audit_and_rejected_grouping_do_not_hide_security_signal(self):
        r=adverse_audit()
        self.assertEqual(r['grouping_status'],'rejected')
        self.assertEqual(r['coverage']['module_counts']['failed'],1)
        by_id={s['id']:s for s in r['signals']}
        escalations=[by_id[i] for i in r['coverage']['escalation_candidate_ids']]
        self.assertTrue(any(s['code']=='suspected_private_content_exposure_escalate' for s in escalations))
        self.assertIsNone(r['triage'])

    def test_reviewed_exposure_handoff_escalates_both_following_workflows(self):
        r=adverse_audit()
        signal=r['coverage']['escalation_candidate_ids'][0]
        # Simulated owner review: native suspicion alone is not confirmed exposure.
        # Fictional reviewer independently confirms it for the corresponding fixture subjects.
        ref='synthetic-independent-confirmation:'+signal
        release=load('deployment-regression/sample.json')
        release['exposure']={'subject':release['subject'],'ref':ref}
        release['gates'][0]['evidence']=None
        result=release_review(release)
        self.assertEqual(result['disposition'],'escalate')
        self.assertIn('public-delivery',result['blockers'])
        self.assertFalse(result['deployment_authorized'])
        incident=load('technical-incident/sample.json')
        incident['exposure_ref']=ref
        out=incident_review(incident)
        self.assertEqual(out['disposition'],'escalate')
        self.assertFalse(out['incident_closed'])
        self.assertFalse(out['search_recovery_established'])

    def test_stage_scope_and_policy_change_cannot_reuse_gate_pass(self):
        base=load('deployment-regression/sample.json')
        for field,new in (('stage','production'),('scope_ref','different-tenant-scope'),
                          ('profile','new-profile'),('config_ref','new-config')):
            data=copy.deepcopy(base)
            data['subject'][field]=new
            result=release_review(data)
            self.assertEqual(result['disposition'],'hold')
            self.assertIn('private-access',result['blockers'])
        data=copy.deepcopy(base)
        data['policy_ref']='new-policy'
        self.assertEqual(release_review(data)['disposition'],'hold')

    def test_processed_diagnostic_is_not_assertion_specific_recovery(self):
        audit_report=adverse_audit()
        self.assertGreater(audit_report['coverage']['module_counts']['processed'],0)
        release=load('deployment-regression/sample.json')
        release['gates'][0]['evidence']=None
        self.assertEqual(release_review(release)['disposition'],'hold')
        incident=load('technical-incident/sample.json')
        # A report reference is insufficient without separate reviewed rendered verification.
        incident['checks'][1].update(evidence_id='fixed-http',outcome='pass')
        r=incident_review(incident)
        self.assertEqual(r['checks'][1]['state'],'unmatched_assertion')
        self.assertEqual(r['disposition'],'investigate')
        self.assertFalse(r['root_cause_confirmed'])

    def test_malformed_review_envelopes_and_unicode_identifiers(self):
        for fn,fixture,field in (
            (release_review,'deployment-regression/sample.json','release_id'),
            (incident_review,'technical-incident/sample.json','incident_id')):
            for invalid in (None,[],{},True):
                with self.assertRaises(ValueError):
                    fn(invalid)
            for invalid in (None,True,[],{},' ',chr(0xd800)):
                data=load(fixture);data[field]=invalid
                with self.assertRaises(ValueError):
                    fn(data)

    def test_partial_and_wrong_subject_are_not_recovery(self):
        data=load('technical-incident/sample.json')
        data['evidence'][-1]['quality']='partial'
        r=incident_review(data)
        self.assertIn('http-header',r['required_blockers'])
        self.assertEqual(r['disposition'],'investigate')
        data=load('technical-incident/sample.json')
        data['recovery_subject']['config_ref']='new-config'
        self.assertIn('http-header',incident_review(data)['required_blockers'])
