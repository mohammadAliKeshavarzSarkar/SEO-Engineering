#!/usr/bin/env python3
"""Verify a portable ZIP against a trusted source checkout; never install it."""
import argparse
import hashlib
import json
import re
import stat
import sys
import zlib
from pathlib import Path
from zipfile import BadZipFile, ZipFile
if __package__:
    from .build_skill import collect, ROOT
else:
    from build_skill import collect, ROOT

PREFIX = 'seo-engineering/'
REQUIRED = {PREFIX + 'SKILL.md', PREFIX + 'references/router.md',
            PREFIX + 'references/execution-contract.md'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify(root, archive):
    expected = collect(root)
    if not REQUIRED <= expected.keys():
        raise ValueError('missing required skill entrypoints')
    records = []
    with ZipFile(archive) as bundle:
        infos = bundle.infolist()
        names = [i.filename for i in infos]
        if len(names) != len(set(names)) or len(names) != len({n.casefold() for n in names}):
            raise ValueError('duplicate or case-colliding package paths')
        if set(names) != set(expected):
            raise ValueError('archive membership differs from approved source selection')
        if sum(n.rsplit('/', 1)[-1].casefold() == 'skill.md' for n in names) != 1:
            raise ValueError('expected exactly one skill entrypoint')
        for info in sorted(infos, key=lambda x: x.filename):
            name = info.filename
            if (not name.startswith(PREFIX) or '\\' in name or
                    any(p in ('', '.', '..') for p in name.split('/')) or
                    not stat.S_ISREG(info.external_attr >> 16) or info.flag_bits & 1):
                raise ValueError(f'unsafe archive member: {name}')
            source = expected[name].read_bytes()
            if info.file_size != len(source):
                raise ValueError(f'size mismatch: {name}')
            data = bundle.read(info)
            if data != source:
                raise ValueError(f'content mismatch: {name}')
            records.append({'path':name, 'bytes':len(data), 'sha256':digest(data)})
        entry = bundle.read(PREFIX + 'SKILL.md').decode('utf-8')
        # Check this project's simple scalar frontmatter contract, not arbitrary YAML.
        head = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n', entry, re.S)
        if not head or not re.search(r'^name: seo-engineering\s*$', head[1], re.M):
            raise ValueError('invalid skill name or frontmatter')
        descriptions = re.findall(r'^description: ([^\r\n]+)$', head[1], re.M)
        if len(descriptions) != 1 or not 1 <= len(descriptions[0].strip()) <= 1024:
            raise ValueError('invalid skill description')
    return {'schema_version':'1', 'scope':'archive_vs_trusted_checkout',
            'archive_sha256':digest(Path(archive).read_bytes()),
            'archive_bytes':Path(archive).stat().st_size, 'file_count':len(records),
            'uncompressed_bytes':sum(r['bytes'] for r in records),
            'python':sys.version.split()[0], 'zlib':zlib.ZLIB_RUNTIME_VERSION,
            'files':records, 'privacy_review':'required', 'runtime_activation':'not_tested'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True, type=Path)
    parser.add_argument('--report', required=True, type=Path, help='New JSON receipt path')
    args = parser.parse_args()
    try:
        report = verify(ROOT, args.archive)
        with args.report.open('x', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            f.write('\n')
    except (OSError, ValueError, BadZipFile, RuntimeError, NotImplementedError) as exc:
        print(f'Package verification failed: {exc}')
        return 1
    print(f"Verified {report['file_count']} source-matched files; SHA-256 {report['archive_sha256']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
