import unittest
from scripts.cluster_keywords import normalize, jaccard, cluster


def record(ident, paths, **changes):
    item = dict(id=ident, query='office chair ' + ident, market='CA', language='en',
                device='mobile', engine='example', surface='web', batch='S1',
                intent='transact', complete=True, urls=['https://example.org/' + x for x in paths])
    item.update(changes)
    return item


class ClusterTests(unittest.TestCase):
    def test_persian_matching_and_raw(self):
        raw = '  ضربان‌سنج  كاربردي ۱۲ '
        self.assertEqual(normalize(raw, 'fa-IR'), 'ضربان سنج کاربردی 12')
        self.assertEqual(cluster([record('a', [], query=raw, language='fa')])['queries'][0]['raw_query'], raw)

    def test_preserve_meaning(self):
        self.assertNotEqual(normalize('chair without arms'), normalize('chair with arms'))
        self.assertNotEqual(normalize('2 kg'), normalize('20 kg'))
        self.assertNotEqual(normalize('C++'), normalize('C'))
        self.assertNotEqual(normalize('ك', 'ar'), normalize('ک', 'ar'))
        self.assertEqual(normalize('Cafe\u0301'), normalize('Café'))

    def test_overlap(self):
        self.assertEqual(jaccard({'a', 'b'}, {'b', 'c'}), 1/3)
        self.assertIsNone(jaccard(set(), set()))

    def test_eligible(self):
        result = cluster([record('a', '12345'), record('b', '12346')])
        self.assertEqual(result['candidate_groups'], [['a', 'b']])
        self.assertEqual(result['pairs'][0]['shared_urls'], 4)

    def test_scope_and_intent_gates(self):
        for change in ({'market':'US'}, {'device':'unknown'}, {'batch':'S2'}, {'intent':'learn'}, {'intent':'mixed'}, {'complete':False}):
            result = cluster([record('a', '12345'), record('b', '12345', **change)])
            self.assertEqual(result['candidate_groups'], [['a'], ['b']])
            self.assertIsNone(result['pairs'][0]['jaccard'])

    def test_no_serp_no_merge(self):
        result = cluster([record('a', [], query='same'), record('b', [], query='same')])
        self.assertTrue(result['pairs'][0]['normalized_equal'])
        self.assertEqual(result['candidate_groups'], [['a'], ['b']])

    def test_chain_not_transitive(self):
        a, b, c = record('a', '12345'), record('b', '12345678'), record('c', '45678')
        result = cluster([c, b, a])
        self.assertEqual(result['candidate_groups'], [['a', 'b'], ['c']])
        self.assertEqual(result, cluster([a, b, c]))

    def test_duplicate_urls_do_not_inflate(self):
        result = cluster([record('a', '11111'), record('b', '11111')])
        self.assertIsNone(result['pairs'][0]['jaccard'])

    def test_bad_input(self):
        for records in ([], [record('a', '12345'), record('a', '12345')], [record('a', [], urls=['file:///etc/passwd'])]):
            with self.assertRaises(ValueError):
                cluster(records)
        with self.assertRaises(ValueError):
            cluster([record('a', '12345')], float('nan'))
