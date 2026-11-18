import json
import unittest
from scripts.audit_metadata import audit, draft, safe_script_json, loads, KEYS


def plan(**kw):
    p=dict(reviewed=True,facts_ref='fixture:public-facts',title='راهنمای انتخاب صندلی',
           description='راهنمای بررسی ابعاد و تناسب صندلی.',
           share_title='راهنمای صندلی',share_description='بررسی ابعاد و تناسب',
           locale='fa',canonical='https://example.org/fa/راهنما/',
           share_image='https://example.org/img/chair.jpg',
           article=dict(type='BlogPosting',headline='راهنمای انتخاب صندلی',
                        author_type='Organization',author_name='Example',
                        image='https://example.org/img/chair.jpg',date_published='2026-11-17',
                        date_modified=None,facts_ref='fixture:article'))
    p.update(kw)
    return p


def capture(p,**kw):
    d=draft(p)
    c=dict(status='complete',context_id='fixture:context',evidence_ref='fixture:capture',
           metadata={k:[v] for k,v in d['metadata'].items()},
           jsonld_blocks=[d['jsonld_script_text']] if d['jsonld'] else [])
    c.update(kw)
    return c


def row(ident='guide',p=None,**kw):
    p=plan() if p is None else p
    r=dict(id=ident,expected_context='fixture:context',plan=p,
           source=capture(p),rendered=capture(p))
    r.update(kw)
    return r


def envelope(*rows):
    return dict(schema_version='1',scope='synthetic',pages=list(rows))


class MetadataTests(unittest.TestCase):
    def result(self,r=None):
        return audit(envelope(row() if r is None else r))['pages'][0]

    def test_reviewed_draft_and_exact_capture(self):
        d=audit(envelope(row()))
        self.assertTrue(d['review_required'])
        r=d['pages'][0]
        self.assertEqual(r['draft']['jsonld']['inLanguage'],'fa')
        self.assertEqual(r['captures']['source']['review_findings'],[])
        self.assertEqual(r['captures']['rendered']['deferred_checks'],[])

    def test_script_breakout_escaped(self):
        value={'headline':'</ScRiPt><script>alert(1)</script>&\u2028'}
        s=safe_script_json(value)
        self.assertNotIn('<',s)
        self.assertNotIn('&',s)
        self.assertEqual(json.loads(s),value)

    def test_no_unreviewed_generation(self):
        for p in (plan(reviewed=False),plan(reviewed=1),plan(facts_ref='')):
            with self.assertRaises(ValueError): draft(p)

    def test_article_dates_and_urls(self):
        p=plan()
        p['article']['date_modified']='2026-11-16'
        with self.assertRaises(ValueError): draft(p)
        with self.assertRaises(ValueError): draft(plan(canonical='https://user@example.org/'))
        with self.assertRaises(ValueError): draft(plan(share_image='javascript:alert(1)'))

    def test_website_without_article(self):
        r=self.result(row(p=plan(article=None)))
        self.assertIsNone(r['draft']['jsonld'])
        self.assertIn('no_reviewed_article_profile',r['captures']['source']['deferred_checks'])

    def test_complete_missing_vs_partial(self):
        for state in ('complete','partial'):
            r=row()
            r['source']['status']=state
            r['source']['metadata']['title']=[]
            report=self.result(r)['captures']['source']
            self.assertEqual(any(f.get('field')=='title' for f in report['review_findings']),state=='complete')

    def test_context_mismatch_defers(self):
        r=row()
        r['rendered']['context_id']='another-locale'
        r['rendered']['metadata']['title']=['different']
        report=self.result(r)['captures']['rendered']
        self.assertEqual(report['review_findings'],[])
        self.assertIn('capture_context_mismatch',report['deferred_checks'])

    def test_failed_and_uncollected(self):
        r=row()
        r['rendered'].update(status='not_collected',evidence_ref=None,
                             metadata={k:None for k in KEYS},jsonld_blocks=None)
        self.assertEqual(self.result(r)['captures']['rendered']['review_findings'],[])
        r['rendered']['metadata']['title']=[]
        with self.assertRaises(ValueError): self.result(r)

    def test_literal_metadata_conflict(self):
        r=row()
        r['source']['metadata']['canonical']=[r['plan']['canonical'],'https://example.org/']
        flags=self.result(r)['captures']['source']['review_findings']
        self.assertIn({'code':'repeated_metadata_review','field':'canonical'},flags)
        self.assertIn({'code':'observed_metadata_differs_from_plan_review','field':'canonical'},flags)

    def test_malformed_json_and_duplicate_keys(self):
        for block in ('{','{"@type":"A","@type":"B"}','{"rating":NaN}','{"rating":1e999}'):
            r=row()
            r['source']['jsonld_blocks']=[block]
            report=self.result(r)['captures']['source']
            self.assertIn({'code':'jsonld_json_parse_error_review','block':0},report['review_findings'])
            self.assertIn('article_presence_not_established',report['deferred_checks'])

    def test_unknown_context_no_absence(self):
        r=row()
        r['source']['jsonld_blocks']=['{"@context":"https://example.org/context","@id":"x"}']
        report=self.result(r)['captures']['source']
        self.assertEqual(report['review_findings'],[])
        self.assertIn('unhandled_or_invalid_jsonld_scope',report['deferred_checks'])

    def test_article_mismatch(self):
        r=row()
        n=draft(r['plan'])['jsonld']
        n['headline']='Another article'
        n['aggregateRating']={'ratingValue':5}
        r['source']['jsonld_blocks']=[json.dumps(n)]
        report=self.result(r)['captures']['source']
        self.assertIn({'code':'article_literal_differs_from_reviewed_draft','property':'headline'},report['review_findings'])
        self.assertIn('additional_article_properties_require_semantic_review',report['deferred_checks'])

    def test_graph_and_repeated_id(self):
        r=row()
        n=draft(r['plan'])['jsonld'];n.pop('@context')
        r['source']['jsonld_blocks']=[json.dumps({'@context':'https://schema.org','@graph':[n,n]})]
        report=self.result(r)['captures']['source']
        self.assertIn({'code':'repeated_article_id_review'},report['review_findings'])
        self.assertIn('node_merge_not_assessed',report['deferred_checks'])

    def test_same_locale_duplicate_title_candidates(self):
        a=row()
        b=row('second',plan(canonical='https://example.org/fa/second/'))
        for r in audit(envelope(a,b))['pages']:
            self.assertIn('same_locale_title_reuse_review',r['plan_review_findings'])

    def test_duplicate_ids_and_nonfinite_inputs(self):
        with self.assertRaises(ValueError): audit(envelope(row(),row()))
        with self.assertRaises(ValueError): loads('{"a":1,"a":2}')
        data=envelope(row());data['extra']=float('inf')
        with self.assertRaises(ValueError): audit(data)
