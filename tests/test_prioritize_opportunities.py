import unittest
from scripts.prioritize_opportunities import prioritize


def item(ident, **changes):
    r = dict(id=ident, severity='P2', status='pending', fit='eligible', risk='low',
             confidence='high', impact=4, effort_days=[2,4], depends_on=[])
    r.update(changes)
    return r


class PriorityTests(unittest.TestCase):
    def rows(self, *records):
        return {r['id']:r for r in prioritize(list(records))['rows']}

    def test_incident_override(self):
        rows = prioritize([item('growth', effort_days=[.25,.25]), item('urgent', severity='P0',
                          risk='unknown', confidence='unknown', impact=None, depends_on=['growth'])])['rows']
        self.assertEqual(rows[0]['lane'], 'incident')
        self.assertIsNone(rows[0]['score'])
        self.assertEqual(rows[0]['unmet_dependencies'], ['growth'])

    def test_repair_without_estimates(self):
        self.assertEqual(self.rows(item('a', severity='P1', impact=None))['a']['lane'], 'repair')

    def test_excluded_and_unknown(self):
        r = self.rows(item('a', fit='excluded'), item('b', confidence='low'), item('c', effort_days=None))
        self.assertEqual([r[i]['lane'] for i in 'abc'], ['excluded','investigate','investigate'])
        self.assertTrue(all(x['score'] is None for x in r.values()))

    def test_risk_gate(self):
        self.assertEqual(self.rows(item('a', risk='high'))['a']['lane'], 'review')

    def test_dependencies(self):
        self.assertEqual(self.rows(item('a'), item('b', depends_on=['a']))['b']['lane'], 'blocked')
        self.assertEqual(self.rows(item('a', status='verified'), item('b', depends_on=['a']))['b']['lane'], 'growth')

    def test_range_and_order(self):
        rows = prioritize([item('a', confidence='medium'), item('b')])['rows']
        self.assertEqual([r['id'] for r in rows], ['b','a'])
        self.assertEqual(rows[0]['score'], {'low':1.0,'high':2.0,'mid':4/3})
        self.assertTrue(rows[0]['authorization_required'])

    def test_cycles_and_missing_dependency(self):
        for records in ([item('a', depends_on=['b'])], [item('a', depends_on=['b']),item('b', depends_on=['a'])]):
            with self.assertRaises(ValueError): prioritize(records)

    def test_numeric_and_identity_validation(self):
        for records in ([item('a', effort_days=[0,1])], [item('a', effort_days=[1,float('nan')])],
                        [item('a', impact=True)], [item('a'),item('a')], [item('a', severity='P0', fit='excluded')]):
            with self.assertRaises(ValueError): prioritize(records)

    def test_inconsistent_verified_status(self):
        for records in ([item('a'), item('b', status='verified', depends_on=['a'])],
                        [item('a', status='verified', fit='excluded')]):
            with self.assertRaises(ValueError): prioritize(records)
