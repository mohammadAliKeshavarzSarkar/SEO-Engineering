#!/usr/bin/env python3
"""Check an explicit local route/build artifact plan; no build or network execution."""
import argparse
import json
import stat
from pathlib import Path
from urllib.parse import urlsplit

METHOD = 'T03-v1'
PURPOSES = {'acquisition', 'public_utility', 'protected', 'missing', 'redirect'}
DELIVERY = {'prerendered', 'spa_shell', 'runtime', 'none', 'error_document'}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def absolute_url(value):
    if not nonempty(value) or any(c.isspace() or ord(c) < 32 for c in value) or '#' in value or '\\' in value:
        return False
    try:
        parts = urlsplit(value)
        _ = parts.port
        return (parts.scheme in ('http', 'https') and bool(parts.hostname)
                and parts.username is None and parts.password is None)
    except ValueError:
        return False


def relative_file(value):
    if not nonempty(value) or any(c in value for c in ('\\', ':')) or any(ord(c) < 32 for c in value):
        raise ValueError('expected portable relative artifact path')
    parts = value.split('/')
    if any(not p or p in ('.', '..') or p.startswith('.') or p != p.strip() for p in parts):
        raise ValueError('unsafe artifact path component')
    return parts


def check_file(root, value):
    parts = relative_file(value)
    current = root
    for i, part in enumerate(parts):
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            return 'missing'
        if stat.S_ISLNK(mode):
            raise ValueError('symlink in artifact path')
        if i < len(parts) - 1 and not stat.S_ISDIR(mode):
            return 'missing'
        if i == len(parts) - 1 and not stat.S_ISREG(mode):
            return 'not_regular'
    return 'present' if current.stat().st_size > 0 else 'empty'


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def audit(plan, root):
    json.dumps(plan, allow_nan=False)
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('artifact root must be a directory')
    if plan['schema_version'] != '1' or not nonempty(plan['scope']):
        raise ValueError('invalid build plan schema or scope')
    routes = plan['routes']
    if not isinstance(routes, list) or not 1 <= len(routes) <= 2000:
        raise ValueError('expected 1–2000 route records')
    seen_ids, seen_urls, html_owners = set(), set(), {}
    results = []
    for row in routes:
        ident, url = row['id'], row['url']
        if not nonempty(ident) or ident in seen_ids or not absolute_url(url) or url in seen_urls:
            raise ValueError('unique route ID and absolute URL required')
        seen_ids.add(ident)
        seen_urls.add(url)
        purpose, delivery = row['purpose'], row['delivery']
        if purpose not in PURPOSES or delivery not in DELIVERY:
            raise ValueError('invalid purpose or delivery plan')
        if type(row['sitemap_expected']) is not bool:
            raise ValueError('sitemap_expected must be boolean')
        canonical = row['canonical_expected']
        if canonical is not None and not absolute_url(canonical):
            raise ValueError('canonical_expected must be absolute URL or null')
        html = row['html_file']
        if delivery in ('prerendered', 'spa_shell', 'error_document'):
            if not isinstance(html, str) or not html.lower().endswith(('.html', '.htm')):
                raise ValueError('HTML artifact required for this delivery plan')
            relative_file(html)
            html_owners.setdefault(html.casefold(), []).append((ident, html, delivery))
        elif html is not None:
            raise ValueError('runtime/none must not assert a local document path')
        files = row['required_files']
        if not isinstance(files, list) or len(files) > 100 or not all(isinstance(p,str) for p in files):
            raise ValueError('expected at most 100 required artifact paths')
        if len({p.casefold() for p in files}) != len(files):
            raise ValueError('duplicate/case-colliding required file')
        if html is not None and html.casefold() in {p.casefold() for p in files}:
            raise ValueError('document path already listed separately')
        flags, deferred = [], ['deployed_routing_headers_and_status_not_checked',
                               'content_metadata_and_resource_resolution_not_checked']
        if row['sitemap_expected'] and purpose != 'acquisition':
            flags.append('non_acquisition_route_in_sitemap_plan')
        if row['sitemap_expected'] and canonical is None:
            deferred.append('sitemap_canonical_expectation_unknown')
        elif row['sitemap_expected'] and canonical != url:
            flags.append('sitemap_non_self_canonical_plan_review')
        if purpose == 'protected' and delivery == 'prerendered':
            flags.append('protected_route_prerender_plan_review')
        if purpose == 'acquisition' and delivery in ('none','error_document'):
            flags.append('acquisition_document_plan_review')
        if purpose == 'missing' and delivery == 'spa_shell':
            flags.append('missing_route_fallback_status_review')
        if purpose == 'redirect' and delivery in ('prerendered','spa_shell','error_document'):
            flags.append('redirect_document_plan_review')
        checks = []
        for path in ([html] if html is not None else []) + files:
            state = check_file(root, path)
            checks.append({'path':path,'state':state})
            if state != 'present':
                flags.append('required_artifact_' + state)
        if delivery == 'runtime':
            deferred.append('runtime_document_not_assessed')
        if delivery == 'spa_shell':
            deferred.append('route_specific_initial_html_not_assessed')
        results.append({'id':ident,'url':url,'purpose':purpose,'delivery':delivery,
                        'artifact_checks':checks,'review_findings':sorted(set(flags)),
                        'deferred_checks':deferred})
    by_id = {r['id']:r for r in results}
    for owners in html_owners.values():
        if len(owners) > 1:
            spelled = {o[1] for o in owners}
            kinds = {o[2] for o in owners}
            # One shared SPA shell or one shared error document can be deliberate.
            if len(spelled) > 1 or kinds not in ({'spa_shell'}, {'error_document'}):
                for ident, _, _ in owners:
                    by_id[ident]['review_findings'].append('document_path_collision_review')
    return {'method':METHOD,'scope':plan['scope'],'routes':results,'review_required':True,
            'limits':'Explicit local artifact plan and regular-file existence/size only; not generated route discovery, actual sitemap, metadata/content, asset linkage, server behavior, authorization, index or ranking proof. No build executed.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        plan = json.loads(args.input.read_text(encoding='utf-8'), object_pairs_hook=unique_object)
        result = audit(plan, args.root)
        with args.output.open('x', encoding='utf-8') as stream:
            json.dump(result, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write('\n')
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print('SPA artifact QA failed:', exc)
        return 1
    print('Local artifact plan inspected; review findings and deferred checks.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
