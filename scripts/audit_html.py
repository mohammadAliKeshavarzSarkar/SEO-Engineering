#!/usr/bin/env python3
"""Local initial-HTML smoke test; not HTTP, rendering, or index inspection."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


def absolute_url(value):
    if not isinstance(value, str) or not value or any(c.isspace() for c in value) or '#' in value:
        return False
    try:
        parts = urlsplit(value)
        _ = parts.port
        return parts.scheme in ('http', 'https') and bool(parts.hostname) and not (
            parts.username is not None or parts.password is not None)
    except ValueError:
        return False


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.titles, self.descriptions, self.canonicals, self.robots, self.h1s = [], [], [], [], []
        self.capture = None
        self.parts = []
        self.in_head = False
        self.inert = []
        self.misplaced = []

    def handle_starttag(self, tag, attrs):
        if tag in ('template', 'svg', 'math', 'noscript'):
            self.inert.append(tag)
        if self.inert:
            return
        if tag == 'head':
            self.in_head = True
        if tag == 'body':
            self.in_head = False
        attrs = dict(attrs)
        if (tag == 'title' and self.in_head) or (tag == 'h1' and not self.in_head):
            self.capture, self.parts = tag, []
        if tag == 'link' and 'canonical' in (attrs.get('rel') or '').lower().split():
            if self.in_head:
                self.canonicals.append((attrs.get('href') or '').strip())
            else:
                self.misplaced.append('canonical')
        if tag == 'meta':
            name = (attrs.get('name') or '').lower()
            if name == 'description':
                if self.in_head:
                    self.descriptions.append((attrs.get('content') or '').strip())
                else:
                    self.misplaced.append('description')
            if name in ('robots', 'googlebot', 'bingbot'):
                self.robots.extend((attrs.get('content') or '').lower().replace(',', ' ').split())

    def handle_data(self, data):
        if self.capture and not self.inert:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if self.inert:
            if tag == self.inert[-1]:
                self.inert.pop()
            return
        if tag == 'head':
            self.in_head = False
        if tag == self.capture:
            target = self.titles if tag == 'title' else self.h1s
            target.append(''.join(self.parts).strip())
            self.capture, self.parts = None, []


def audit(routes, root):
    errors = []
    titles = {}
    descriptions = {}
    seen_urls = set()
    root = Path(root).resolve()
    if not isinstance(routes, list):
        raise ValueError('manifest must be an array')
    if not routes:
        return ['Manifest contains no routes']
    for route in routes:
        url, file = route['url'], route['file']
        if not absolute_url(url) or not isinstance(file, str) or not file.strip():
            raise ValueError('route requires absolute HTTP(S) URL and nonempty file path')
        if type(route.get('indexable', True)) is not bool:
            raise ValueError('indexable must be a JSON boolean')
        if url in seen_urls:
            errors.append(f'{url}: duplicate manifest URL')
        seen_urls.add(url)
        if route.get('indexable', True) is False:
            continue  # this tool does not validate nonindexable routes or HTTP status
        p = (root / file).resolve()
        if not p.is_relative_to(root):
            errors.append(f'{url}: file escapes root')
            continue
        if not p.is_file():
            errors.append(f'{url}: missing HTML {file}')
            continue
        page = Page()
        page.feed(p.read_text(encoding='utf-8'))
        page.close()
        for label, values in [('title', page.titles), ('description', page.descriptions), ('canonical', page.canonicals), ('h1', page.h1s)]:
            if len(values) != 1 or not values[0]:
                errors.append(f'{url}: expected exactly one nonempty {label}')
        for label in sorted(set(page.misplaced)):
            errors.append(f'{url}: {label} outside explicit head')
        expected = route.get('canonical', url)
        if not absolute_url(expected):
            errors.append(f'{url}: manifest expected canonical not an absolute HTTP(S) URL')
        if page.canonicals != [expected]:
            errors.append(f'{url}: canonical mismatch (expected {expected})')
        if 'noindex' in page.robots or 'none' in page.robots:
            errors.append(f'{url}: unexpected noindex/none in robots meta')
        for label, values, previous in [('title', page.titles, titles), ('description', page.descriptions, descriptions)]:
            if len(values) == 1 and values[0]:
                value = values[0]
                if value in previous:
                    errors.append(f'{url}: duplicate {label} with {previous[value]}')
                else:
                    previous[value] = url
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--manifest', required=True, type=Path)
    ap.add_argument('--root', required=True, type=Path)
    args = ap.parse_args()
    try:
        routes = json.loads(args.manifest.read_text(encoding='utf-8'))
        errors = audit(routes, args.root)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as ex:
        print(f'Invalid manifest or input: {ex}')
        return 2
    for item in errors:
        print('FAIL:', item)
    print(f'{len(routes)} manifest entries; {len(errors)} findings. Nonindexable entries skipped. Local explicit-head HTML project-policy checks only.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
