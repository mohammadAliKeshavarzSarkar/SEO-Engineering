#!/usr/bin/env python3
"""Build a portable SEO skill ZIP from public, allowlisted repository resources."""
import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent.parent
LIBRARY_DIRS = ('docs', 'templates', 'decision-engine', 'workflows',
                'implementation-patterns', 'evaluations', 'examples')
ALLOWED_SUFFIXES = {'.md', '.csv', '.json', '.html', '.py'}
EXCLUDED = {'private', 'projects', '__pycache__', 'node_modules', 'dist'}


def collect(root):
    root = Path(root).resolve()
    entries = {}

    def include(source, target):
        if source.is_symlink() or not source.is_file() or not source.resolve().is_relative_to(root):
            raise ValueError(f'Unsafe or missing resource: {source}')
        if target in entries:
            raise ValueError(f'Duplicate package path: {target}')
        entries[target] = source

    def folder(relative, target):
        base = root / relative
        if not base.is_dir() or base.is_symlink() or not base.resolve().is_relative_to(root):
            raise ValueError(f'Unsafe or missing resource directory: {relative}')
        for source in sorted(base.rglob('*')):
            parts = source.relative_to(base).parts
            if any(p.startswith('.') or p in EXCLUDED for p in parts):
                continue
            if source.is_symlink():
                raise ValueError(f'Symlink not allowed: {source}')
            if source.is_file() and source.suffix in ALLOWED_SUFFIXES:
                include(source, f'{target}/{source.relative_to(base).as_posix()}')

    include(root / 'skills/seo-engineering/SKILL.md', 'seo-engineering/SKILL.md')
    folder('skills/seo-engineering/references', 'seo-engineering/references')
    for relative in LIBRARY_DIRS:
        folder(relative, f'seo-engineering/references/library/{relative}')
    for relative in ('scripts/audit_html.py', 'scripts/check_docs.py', 'scripts/cluster_keywords.py', 'scripts/audit_topic_graph.py', 'scripts/prioritize_opportunities.py', 'scripts/audit_locale_manifest.py', 'scripts/validate_research.py', 'scripts/inspect_architecture.py', 'scripts/audit_rendering.py', 'scripts/audit_spa_build.py', 'scripts/audit_next_delivery.py', 'scripts/README.md'):
        include(root / relative, f'seo-engineering/references/library/{relative}')
    return entries


def build(root, output):
    entries = collect(root)
    # Read all sources before opening the output; do not overwrite existing archives.
    payload = [(name, path.read_bytes()) for name, path in sorted(entries.items())]
    with ZipFile(output, 'x', compression=ZIP_DEFLATED) as archive:
        for name, data in payload:
            # Fixed timestamps and permissions; reproducible within a pinned Python/zlib runtime.
            info = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compress_type=ZIP_DEFLATED, compresslevel=9)
    return len(entries)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path, help='New ZIP file; parent must exist')
    args = parser.parse_args()
    try:
        count = build(ROOT, args.out)
    except (OSError, ValueError) as exc:
        print(f'Build failed: {exc}')
        return 1
    print(f'{count} resources packaged in {args.out}. Review contents before distribution.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
