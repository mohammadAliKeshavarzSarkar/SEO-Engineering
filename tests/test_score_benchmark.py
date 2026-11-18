import unittest
from scripts.score_benchmark import prepare, score, fingerprint


def fixture():
    suite = {'version':'synthetic','cases':[{'id':'X','prompt':'Invented prompt',
             'expected':['one','two','three','four','five'],'disqualifiers':['bad']}]}
    config = dict(model='fixture',runtime='fixture',tool_config='none',permission_mode='read-only',
                  skill_commit='fixture',launch_protocol='fixture',review_protocol='fixture',
                  suite_kind='public_regression',repeats=1)
    plan = prepare(suite,config)
    def row(arm, expected='pass', disq='absent'):
        return dict(case_id='X',repeat=1,arm=arm,output_ref='synthetic',trace_ref='synthetic',reviewer='synthetic',
                    expected=[dict(criterion=i,status=expected,evidence='synthetic') for i in range(1,6)],
                    disqualifiers=[dict(criterion=1,status=disq,evidence='synthetic')])
    grades = dict(plan_sha256=fingerprint(plan),runs=[row('baseline','fail'),row('skill')])
    return suite,plan,grades


class BenchmarkTests(unittest.TestCase):
    def test_prompt_only(self):
        _,plan,_ = fixture()
        self.assertEqual(set(plan['tasks'][0]),{'case_id','repeat','prompt'})

    def test_matched_delta(self):
        report = score(*fixture())
        self.assertEqual(report['matched_delta_percentage_points'],100)
        self.assertTrue(report['skill_internal_case_gate'])
        self.assertFalse(report['release_certified'])

    def test_missing_pair(self):
        suite,plan,grades = fixture()
        grades['runs'].pop()
        report = score(suite,plan,grades)
        self.assertIsNone(report['matched_delta_percentage_points'])
        self.assertFalse(report['complete'])
        self.assertFalse(report['skill_internal_case_gate'])

    def test_critical_overrides(self):
        suite,plan,grades = fixture()
        grades['runs'][1]['disqualifiers'][0]['status'] = 'observed'
        report = score(suite,plan,grades)
        self.assertFalse(report['skill_internal_case_gate'])
        self.assertEqual(report['arms']['skill']['critical_failures_all_graded'],1)

    def test_unobservable(self):
        suite,plan,grades = fixture()
        grades['runs'][1]['expected'][0]['status'] = 'not_observable'
        report = score(suite,plan,grades)
        self.assertFalse(report['skill_internal_case_gate'])
        self.assertEqual(report['arms']['skill']['matched_rate'],0.8)

    def test_duplicate_run(self):
        suite,plan,grades = fixture()
        grades['runs'].append(grades['runs'][0])
        with self.assertRaises(ValueError): score(suite,plan,grades)

    def test_frozen_plan(self):
        suite,plan,grades = fixture()
        suite['cases'][0]['expected'][0] = 'changed'
        with self.assertRaises(ValueError): score(suite,plan,grades)

    def test_missing_criterion(self):
        suite,plan,grades = fixture()
        grades['runs'][1]['expected'].pop()
        with self.assertRaises(ValueError): score(suite,plan,grades)
