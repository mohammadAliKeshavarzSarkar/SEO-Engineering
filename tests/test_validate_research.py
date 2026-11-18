import unittest
from scripts.validate_research import validate


def fixture():
    return {'schema_version':'1', 'scope':'fictional', 'evidence':[
        dict(id='e1',kind='observed',value=0,source_ref='fixture',scope='sample',
             limitations='synthetic',collected_date='2026-11-18'),
        dict(id='e2',kind='unknown',value=None,source_ref='unavailable',scope='sample',
             limitations='no data',collected_date='2026-11-18')], 'decisions':[
        dict(id='d1',status='reviewed',reviewer='fictional reviewer',evidence_ids=['e1'],
             rationale='sample only',next_check='repeat'),
        dict(id='d2',status='provisional',evidence_ids=['e2'],rationale='unknown',next_check='collect')]}


class ResearchTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate(fixture())['provisional'], ['d2'])

    def test_unknown_zero(self):
        data = fixture()
        data['evidence'][1]['value'] = 0
        with self.assertRaises(ValueError): validate(data)

    def test_dangling_reference(self):
        data = fixture()
        data['decisions'][0]['evidence_ids'] = ['missing']
        with self.assertRaises(ValueError): validate(data)

    def test_duplicate(self):
        data = fixture()
        data['evidence'].append(data['evidence'][0])
        with self.assertRaises(ValueError): validate(data)

    def test_unknown_not_reviewed_evidence(self):
        data = fixture()
        data['decisions'][0]['evidence_ids'] = ['e2']
        with self.assertRaises(ValueError): validate(data)

    def test_bad_date(self):
        data = fixture()
        data['evidence'][0]['collected_date'] = '2026-02-30'
        with self.assertRaises(ValueError): validate(data)

    def test_missing_reviewer(self):
        data = fixture()
        data['decisions'][0].pop('reviewer')
        with self.assertRaises(ValueError): validate(data)
