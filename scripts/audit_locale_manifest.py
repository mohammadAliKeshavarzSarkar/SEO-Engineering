#!/usr/bin/env python3
"""Check a supplied locale manifest against a strict project contract, offline."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

TAG = re.compile(r"^[a-z]{2}(?:-[A-Za-z]{4})?(?:-[A-Za-z]{2})?$", re.I)


def absolute(url):
    if not isinstance(url, str) or any(c.isspace() for c in url):
        return False
    try:
        p = urlsplit(url)
        return p.scheme in ('http', 'https') and bool(p.hostname) and not (
            p.username or p.password or p.fragment)
    except ValueError:
        return False


def audit(data):
    tags = data['allowed_tags']
    pages = data['pages']
    if not isinstance(tags, list) or not tags or any(
        not isinstance(t, str) or not TAG.fullmatch(t) for t in tags
    ) or len(set(t.lower() for t in tags)) != len(tags):
        raise ValueError('expected unique project-approved language tags')
    allowed = {t.lower() for t in tags} | {'x-default'}
    if not isinstance(pages, list) or not pages:
        raise ValueError('expected nonempty pages array')
    registry = {}
    for page in pages:
        url = page['url']
        if not absolute(url) or url in registry:
            raise ValueError('expected unique absolute page URLs')
        if not isinstance(page['group'], str) or not page['group'].strip():
            raise ValueError('expected nonempty group ID')
        if not isinstance(page['locale'], str) or page['locale'].lower() not in allowed:
            raise ValueError('locale must be project-approved')
        if type(page['status']) is not int or type(page['index_intent']) is not bool:
            raise ValueError('invalid status or index intent')
        if not absolute(page['canonical']):
            raise ValueError('expected absolute canonical')
        if not isinstance(page['alternates'], list):
            raise ValueError('expected alternate array')
        registry[url] = page
    findings = []
    groups = {}
    for url, page in registry.items():
        group = groups.setdefault(page['group'], {})
        locale = page['locale'].lower()
        if locale in group:
            findings.append([url, 'duplicate_locale_in_group'])
        group[locale] = url
    for url, page in registry.items():
        expected = groups[page['group']]
        actual = {}
        for alt in page['alternates']:
            tag, target = alt['tag'], alt['url']
            if not isinstance(tag, str) or tag.lower() not in allowed or not absolute(target):
                findings.append([url, 'invalid_alternate'])
                continue
            tag = tag.lower()
            if tag in actual:
                findings.append([url, 'duplicate_alternate_tag'])
            actual[tag] = target
            if target not in registry:
                findings.append([url, 'target_not_in_manifest'])
            elif registry[target]['group'] != page['group']:
                findings.append([url, 'target_wrong_group'])
        if len(expected) > 1 or actual:
            if actual.get(page['locale'].lower()) != url:
                findings.append([url, 'missing_or_wrong_self'])
            if actual != expected:
                findings.append([url, 'alternate_set_differs_from_group'])
        if page['status'] != 200 or not page['index_intent']:
            findings.append([url, 'representative_not_expected_eligible'])
        if page['canonical'] != url:
            findings.append([url, 'non_self_canonical_review'])
    return {'scope':'supplied_manifest_only', 'review_required':True,
            'findings':[{'url':u,'reason':r} for u,r in sorted(set(tuple(x) for x in findings))]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    try:
        report = audit(json.loads(args.input.read_text(encoding='utf-8')))
        with args.output.open('x', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            f.write('\n')
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(f'Validation failed: {exc}')
        return 2
    print(f"{len(report['findings'])} manifest findings; live checks not performed.")
    return 1 if report['findings'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
