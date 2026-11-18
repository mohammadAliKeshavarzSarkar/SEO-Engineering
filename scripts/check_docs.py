#!/usr/bin/env python3
"""Check relative Markdown targets and explicit skill routing resources offline."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
RESOURCE = re.compile(r'\b(?:docs|templates|decision-engine|workflows|implementation-patterns|evaluations|scripts)/[\w./-]+\.(?:md|py|csv|json)\b')
LINK = re.compile(r'\]\(([^)\s]+)\)')
SKIP = {'.git', 'private', '__pycache__', 'node_modules', 'dist'}


def audit(root):
    root = Path(root).resolve()
    if root.name == 'library' and root.parent.name == 'references':
        skill = root.parent.parent
        boundary = skill
        files = list(root.rglob('*.md')) + [skill / 'SKILL.md']
        files += [p for p in (skill / 'references').glob('*.md')]
    else:
        skill = root / 'skills/seo-engineering'
        boundary = root
        files = list(root.rglob('*.md'))
    errors = []
    count = 0
    required = [skill / 'SKILL.md', skill / 'references/router.md',
                skill / 'references/execution-contract.md']
    for p in required:
        if not p.is_file() or not p.resolve().is_relative_to(boundary):
            errors.append(f'missing or unsafe skill resource: {p.name}')
    for file in sorted(set(files)):
        if not file.is_file() or SKIP.intersection(file.relative_to(boundary).parts):
            continue
        count += 1
        if not file.resolve().is_relative_to(boundary):
            errors.append(f'unsafe Markdown file: {file.relative_to(boundary)}')
            continue
        content = re.sub(r'```[^\n]*\n.*?```', '', file.read_text(encoding='utf-8'), flags=re.S)
        for match in LINK.finditer(content):
            url = urlsplit(match.group(1))
            if url.scheme or url.netloc or not url.path:
                continue
            target = (file.parent / unquote(url.path)).resolve()
            if not target.is_relative_to(boundary) or not target.exists():
                errors.append(f'{file.relative_to(boundary)}: {match.group(1)}')
    refs = set()
    for file in required:
        if file.is_file() and file.resolve().is_relative_to(boundary):
            refs.update(RESOURCE.findall(file.read_text(encoding='utf-8')))
    for ref in sorted(refs):
        path = (root / ref).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append(f'skill routing: {ref}')
    return count, len(refs), errors


def main():
    try:
        count, refs, errors = audit(ROOT)
    except (OSError, ValueError) as exc:
        print(f'Check failed: {exc}')
        return 1
    for error in errors:
        print('BROKEN:', error)
    print(f'{count} Markdown files; {refs} skill resource paths; {len(errors)} findings.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
