#!/usr/bin/env python3
"""Verify a portable ZIP against a trusted source checkout; never install it."""
import argparse
import hashlib
import json
import os
import re
import unicodedata
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


def portable_paths(names):
    """Reject ambiguous paths, including directory-prefix collisions."""
    seen = {}
    files = set(names)
    reserved = {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"} | {
        f"{kind}{number}" for kind in ("COM", "LPT") for number in "123456789¹²³"}
    for name in names:
        parts = name.split("/")
        for i, part in enumerate(parts):
            if (not part or part in (".", "..") or part.endswith((" ", "."))
                    or any(c in '<>:"|?*\\\\' or ord(c) < 32 for c in part)
                    or part.split(".", 1)[0].upper() in reserved):
                raise ValueError("nonportable archive path")
            prefix = "/".join(parts[:i+1])
            folded = unicodedata.normalize("NFC", prefix).casefold()
            if folded in seen and seen[folded] != prefix:
                raise ValueError("case-colliding or normalization-colliding archive paths")
            seen[folded] = prefix
            if i < len(parts)-1 and prefix in files:
                raise ValueError("file/directory archive collision")


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
        portable_paths(names)
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
        if not head or re.findall(r'^name: ([^\r\n]+)
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


def verify_installed(installation, verified_receipt):
    """Compare a fresh installed directory to a receipt from verify() in this run.

    The directory and its parent are trusted local paths, not hostile mutable
    filesystems. Never execute content as part of the comparison.
    """
    root = Path(installation)
    if root.name != "seo-engineering" or root.is_symlink() or not root.is_dir():
        raise ValueError("expected real seo-engineering installation directory")
    records = {r["path"][len(PREFIX):]: r for r in verified_receipt["files"]}
    expected_dirs = {str(parent).replace(os.sep, "/") for name in records
                     for parent in Path(name).parents if str(parent) != "."}
    observed, dirs = set(), set()
    for folder, dirnames, filenames in os.walk(root, followlinks=False,
                                                onerror=lambda e: (_ for _ in ()).throw(e)):
        folder = Path(folder)
        for name in dirnames:
            path = folder / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink() or not stat.S_ISDIR(path.lstat().st_mode):
                raise ValueError("unsafe installation directory")
            if rel not in expected_dirs:
                raise ValueError("unexpected installation directory")
            dirs.add(rel)
        for name in filenames:
            path = folder / name
            rel = path.relative_to(root).as_posix()
            status = path.lstat()
            if not stat.S_ISREG(status.st_mode):
                raise ValueError("unsafe installation file")
            if rel not in records:
                raise ValueError("unexpected installation file")
            record = records[rel]
            if status.st_size != record["bytes"] or digest(path.read_bytes()) != record["sha256"]:
                raise ValueError("installed content mismatch")
            observed.add(rel)
    if observed != records.keys() or dirs != expected_dirs:
        raise ValueError("installation membership mismatch")
    return {"status": "source_matched", "file_count": len(observed),
            "archive_sha256": verified_receipt["archive_sha256"],
            "runtime_activation": "not_tested", "privacy_review": "required"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True, type=Path)
    parser.add_argument('--report', required=True, type=Path, help='New JSON receipt path')
    parser.add_argument('--installed', type=Path, help='Optional fresh installed seo-engineering directory')
    args = parser.parse_args()
    try:
        report = verify(ROOT, args.archive)
        if args.installed is not None:
            report['installation'] = verify_installed(args.installed, report)
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
, head[1], re.M) != ['seo-engineering']:
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
