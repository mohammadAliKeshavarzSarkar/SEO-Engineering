import unittest
from scripts.audit_topic_graph import audit


def fixture():
    return {'pages': [dict(id=i, state=s, index_intent=x, priority=y) for i,s,x,y in [
        ('home','public',True,True),('hub','public',True,True),('guide','public',True,True),
        ('orphan','public',True,True),('island','public',True,True),('island2','public',True,False),
        ('private','private',False,False),('planned','planned',True,True)]],
        'entries':['home'], 'links':[{'from':a,'to':b,'kind':k} for a,b,k in [
        ('home','hub','crawlable'),('hub','guide','crawlable'),('hub','guide','crawlable'),
        ('guide','hub','crawlable'),('home','orphan','interaction_only'),
        ('island','island2','crawlable'),('island2','island','crawlable'),
        ('home','planned','proposed'),('private','orphan','crawlable')]]}


class GraphTests(unittest.TestCase):
    def rows(self, data):
        return {p['id']:p for p in audit(data)['pages']}

    def test_depth_and_unique_inbound(self):
        rows = self.rows(fixture())
        self.assertEqual(rows['guide']['depth'], 2)
        self.assertEqual(rows['guide']['unique_inbound_sources'], 1)
        self.assertIsNone(rows['orphan']['depth'])
        self.assertTrue(rows['orphan']['index_intent_no_inbound'])

    def test_disconnected_cycle(self):
        row = self.rows(fixture())['island']
        self.assertEqual(row['unique_inbound_sources'], 1)
        self.assertTrue(row['priority_unreachable'])
        self.assertFalse(row['index_intent_no_inbound'])

    def test_private_planned_exclusion(self):
        rows = self.rows(fixture())
        self.assertNotIn('private', rows)
        self.assertNotIn('planned', rows)
        self.assertFalse(rows['home']['index_intent_no_inbound'])

    def test_self_link_not_inbound(self):
        data = fixture()
        data['links'].append(dict(**{'from':'orphan','to':'orphan','kind':'crawlable'}))
        self.assertTrue(self.rows(data)['orphan']['index_intent_no_inbound'])

    def test_observed_planned_link_warning(self):
        data = fixture()
        data['links'].append({'from':'home','to':'planned','kind':'crawlable'})
        self.assertEqual(len(audit(data)['issues']), 1)

    def test_bad_reference(self):
        data = fixture()
        data['links'].append({'from':'home','to':'missing','kind':'crawlable'})
        with self.assertRaises(ValueError):
            audit(data)

    def test_duplicate_id(self):
        data = fixture()
        data['pages'].append(data['pages'][0])
        with self.assertRaises(ValueError):
            audit(data)

    def test_private_entry(self):
        data = fixture()
        data['entries'] = ['private']
        with self.assertRaises(ValueError):
            audit(data)
