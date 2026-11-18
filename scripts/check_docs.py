#!/usr/bin/env python3
"""Check relative Markdown link targets (not headings or remote links)."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent


def main():
    errors = []
    count = 0
    for file in sorted(ROOT.rglob('*.md')):
        if any(p in ('.git', 'private', '__pycache__') for p in file.relative_to(ROOT).parts):
            continue
        count += 1
        content = re.sub(r'```[^\n]*\n.*?```', '', file.read_text(encoding='utf-8'), flags=re.S)
        for match in re.finditer(r'\]\(([^)\s]+)\)', content):
            url = urlsplit(match.group(1))
            if url.scheme or url.netloc or not url.path:
                continue
            path = (file.parent / unquote(url.path)).resolve()
            if not path.is_relative_to(ROOT) or not path.exists():
                errors.append(f'{file.relative_to(ROOT)}: {match.group(1)}')
    for error in errors:
        print('BROKEN:', error)
    print(f'{count} Markdown files; {len(errors)} broken relative targets.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
