#!/usr/bin/env python3
"""Generate reviewed metadata drafts and inspect a narrow local JSON-LD profile."""
import argparse
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

METHOD = 'T08-v1'
KEYS = ('title','description','canonical','og:title','og:description','og:type','og:url','og:image')
CONTEXTS = ('https://schema.org','https://schema.org/')


def text(v):
    return isinstance(v,str) and bool(v.strip())


def url(v):
    if not text(v) or any(c.isspace() or ord(c)<32 or ord(c)==127 for c in v) or any(c in v for c in ('#','\\')) or re.search(r'%(?![0-9a-fA-F]{2})',v):
        return False
    try:
        p=urlsplit(v)
        return p.scheme in ('https','http') and bool(p.hostname) and p.port!=0 and p.username is None and p.password is None
    except ValueError:
        return False


def iso_day(v):
    if not isinstance(v,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',v):
        raise ValueError('local article profile requires ISO calendar dates')
    return date.fromisoformat(v)


def unique_object(pairs):
    out={}
    for k,v in pairs:
        if k in out:
            raise ValueError('duplicate JSON key')
        out[k]=v
    return out


def reject_constant(v):
    raise ValueError('non-finite JSON constant')


def loads(s):
    obj=json.loads(s,object_pairs_hook=unique_object,parse_constant=reject_constant)
    json.dumps(obj,allow_nan=False)
    return obj


def safe_script_json(obj):
    # JSON text for an HTML script data block; NOT attribute/HTML text escaping.
    return (json.dumps(obj,ensure_ascii=False,allow_nan=False,separators=(',',':'))
            .replace('<',r'\u003c').replace('>',r'\u003e').replace('&',r'\u0026')
            .replace('\u2028',r'\u2028').replace('\u2029',r'\u2029'))


def draft(plan):
    if type(plan['reviewed']) is not bool or not plan['reviewed'] or not text(plan['facts_ref']):
        raise ValueError('reviewed public facts and reference required')
    for k in ('title','description','share_title','share_description','locale'):
        if not text(plan[k]):
            raise ValueError('reviewed nonempty '+k+' required')
    if not url(plan['canonical']) or not url(plan['share_image']):
        raise ValueError('reviewed absolute canonical and share image required')
    article=plan['article']
    node=None
    if article is not None:
        if article['type'] not in ('Article','BlogPosting') or article['author_type'] not in ('Person','Organization'):
            raise ValueError('unsupported local article profile')
        for k in ('headline','author_name','facts_ref'):
            if not text(article[k]):
                raise ValueError('reviewed article '+k+' required')
        if not url(article['image']):
            raise ValueError('reviewed article image required')
        published=iso_day(article['date_published'])
        modified=article['date_modified']
        if modified is not None and iso_day(modified)<published:
            raise ValueError('modified date precedes publication')
        node={'@context':'https://schema.org','@type':article['type'],
              '@id':plan['canonical']+'#article','mainEntityOfPage':plan['canonical'],
              'headline':article['headline'],'image':article['image'],
              'datePublished':article['date_published'],
              'author':{'@type':article['author_type'],'name':article['author_name']},
              'inLanguage':plan['locale']}
        if modified is not None:
            node['dateModified']=modified
    metadata={'title':plan['title'],'description':plan['description'],'canonical':plan['canonical'],
              'og:title':plan['share_title'],'og:description':plan['share_description'],
              'og:type':'article' if node is not None else 'website',
              'og:url':plan['canonical'],'og:image':plan['share_image']}
    return {'facts_ref':plan['facts_ref'],'article_facts_ref':article['facts_ref'] if node else None,
            'metadata':metadata,'jsonld':node,'jsonld_script_text':safe_script_json(node) if node else None}


def inspect_blocks(blocks, expected, complete):
    findings,deferred=[],[]
    nodes=[]
    uncovered=False
    for i,block in enumerate(blocks):
        try:
            value=loads(block)
        except (ValueError,TypeError,RecursionError):
            findings.append({'code':'jsonld_json_parse_error_review','block':i})
            uncovered=True
            continue
        # Only recognize direct nodes and one simple @graph under an explicit
        # Schema.org context. Do not expand aliases, merge nodes or resolve IRIs.
        if isinstance(value,dict) and value.get('@context') in CONTEXTS:
            if '@graph' in value:
                if not isinstance(value['@graph'],list) or set(value)-{'@context','@graph'}:
                    uncovered=True
                    continue
                items=value['@graph']
            else:
                items=[value]
            for n in items:
                if (not isinstance(n,dict) or (n is not value and '@context' in n)
                    or '@graph' in n or '@reverse' in n or '@included' in n):
                    uncovered=True
                    continue
                nodes.append(n)
                # Nested entities may include the target under another property.
                if any(isinstance(v,(dict,list)) for k,v in n.items()
                       if k not in ('@type','author','image','mainEntityOfPage')):
                    uncovered=True
        else:
            uncovered=True
    if uncovered:
        deferred.append('unhandled_or_invalid_jsonld_scope')
    if expected is None:
        deferred.append('no_reviewed_article_profile')
        return findings,deferred
    candidates=[n for n in nodes if n.get('@id')==expected['@id']]
    if len(candidates)>1:
        findings.append({'code':'repeated_article_id_review'})
        deferred.append('node_merge_not_assessed')
    elif len(candidates)==1:
        n=candidates[0]
        for k,v in expected.items():
            if k in ('@context','@id'):
                continue
            if k not in n:
                if complete and not uncovered:
                    findings.append({'code':'planned_article_property_not_observed_review','property':k})
                else:
                    deferred.append('article_property_incomplete:'+k)
            elif n[k]!=v:
                findings.append({'code':'article_literal_differs_from_reviewed_draft','property':k})
        if set(n)-set(expected):
            deferred.append('additional_article_properties_require_semantic_review')
    elif complete and not uncovered:
        findings.append({'code':'planned_article_id_not_observed_in_recognized_scope_review'})
    else:
        deferred.append('article_presence_not_established')
    return findings,deferred


def audit(data):
    json.dumps(data,allow_nan=False)
    if data['schema_version']!='1' or not text(data['scope']):
        raise ValueError('invalid local QA envelope')
    rows=data['pages']
    if not isinstance(rows,list) or not 1<=len(rows)<=500:
        raise ValueError('expected 1–500 reviewed page plans')
    seen,results,labels=set(),[],{}
    for r in rows:
        ident=r['id']
        if not text(ident) or ident in seen or not text(r['expected_context']):
            raise ValueError('unique page ID and reviewed context required')
        seen.add(ident)
        plan=r['plan']
        proposal=draft(plan)
        label=(plan['locale'],plan['title'])
        labels.setdefault(label,[]).append((ident,plan['canonical']))
        reports={}
        for name in ('source','rendered'):
            c=r[name]
            state=c['status']
            if state not in ('complete','partial','failed','not_collected') or not text(c['context_id']):
                raise ValueError('invalid capture status/context')
            ref=c['evidence_ref']
            if state=='not_collected':
                if ref is not None:
                    raise ValueError('uncollected capture must not assert evidence')
            elif not text(ref):
                raise ValueError('attempted capture requires evidence reference')
            meta=c['metadata']
            if not isinstance(meta,dict) or set(meta)!=set(KEYS):
                raise ValueError('capture requires exactly the documented metadata groups')
            for k,v in meta.items():
                if v is not None and (not isinstance(v,list) or len(v)>100 or not all(isinstance(s,str) for s in v)):
                    raise ValueError('metadata group must be string array or null')
            blocks=c['jsonld_blocks']
            if blocks is not None and (not isinstance(blocks,list) or len(blocks)>50 or
               any(not isinstance(b,str) or len(b)>250000 for b in blocks)):
                raise ValueError('expected bounded JSON-LD text blocks or null')
            if state in ('failed','not_collected') and (blocks is not None or any(v is not None for v in meta.values())):
                raise ValueError('failed/uncollected capture cannot assert values')
            findings,deferred=[],[]
            if state!='complete':
                deferred.append('capture_incomplete')
            if c['context_id']!=r['expected_context']:
                deferred.append('capture_context_mismatch')
            elif state in ('complete','partial'):
                for k,expected in proposal['metadata'].items():
                    v=meta[k]
                    if v is None:
                        deferred.append('metadata_unavailable:'+k)
                    elif not v:
                        if state=='complete':
                            findings.append({'code':'planned_metadata_not_observed_review','field':k})
                        else:
                            deferred.append('metadata_absence_unverified:'+k)
                    else:
                        # Multiple OG images and other repeated properties may be legitimate.
                        if len(v)>1:
                            findings.append({'code':'repeated_metadata_review','field':k})
                        if expected not in v or any(x!=expected for x in v):
                            findings.append({'code':'observed_metadata_differs_from_plan_review','field':k})
                if blocks is None:
                    deferred.append('jsonld_collection_unavailable')
                else:
                    f,d=inspect_blocks(blocks,proposal['jsonld'],state=='complete')
                    findings.extend(f)
                    deferred.extend(d)
            reports[name]={'status':state,'evidence_ref':ref,'review_findings':findings,'deferred_checks':deferred}
        results.append({'id':ident,'draft':proposal,'captures':reports,'plan_review_findings':[]})
    by_id={r['id']:r for r in results}
    for group in labels.values():
        if len({u for _,u in group})>1:
            for ident,_ in group:
                by_id[ident]['plan_review_findings'].append('same_locale_title_reuse_review')
    return {'method':METHOD,'scope':data['scope'],'pages':results,'review_required':True,
            'limits':'Reviewed draft values and supplied capture strings only. No HTML parsing, JSON-LD expansion, remote context resolution, Schema.org or rich-result validation, truth or visible parity verification, rendering, language detection, publication, index or ranking proof. Literal differences require human review.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    try:
        data=loads(args.input.read_text(encoding='utf-8'))
        report=audit(data)
        with args.output.open('x',encoding='utf-8') as out:
            json.dump(report,out,ensure_ascii=False,allow_nan=False,indent=2)
            out.write('\n')
    except (OSError,ValueError,KeyError,TypeError,AttributeError,RecursionError) as exc:
        print('Metadata review failed:',exc)
        return 1
    print('Reviewed metadata drafts and supplied observations; manual review required.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
