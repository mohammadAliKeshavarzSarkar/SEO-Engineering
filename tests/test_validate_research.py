import unittest
import json
import subprocess
import sys
import tempfile
from pathlib import Path
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

    def test_nonfinite_evidence(self):
        for value in (float('nan'), float('inf'), {'nested': [float('-inf')]}):
            data = fixture()
            data['evidence'][0]['value'] = value
            with self.assertRaises(ValueError): validate(data)

    def test_canonical_calendar_date(self):
        for value in ('20261118', '2026-W47-3'):
            data = fixture()
            data['evidence'][0]['collected_date'] = value
            with self.assertRaises(ValueError): validate(data)

    def test_duplicate_json_key_cli(self):
        raw = json.dumps(fixture()).replace('"schema_version": "1"',
                                           '"schema_version": "0", "schema_version": "1"')
        self.assert_invalid_cli(raw)

    def test_nonfinite_cli(self):
        data = fixture()
        data['evidence'][0]['value'] = float('inf')
        self.assert_invalid_cli(json.dumps(data))

    def assert_invalid_cli(self, raw):
        script = Path(__file__).resolve().parents[1] / 'scripts/validate_research.py'
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / 'input.json', Path(tmp) / 'report.json'
            source.write_text(raw, encoding='utf-8')
            result = subprocess.run([sys.executable, str(script), '--input', str(source),
                                     '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(output.exists())
