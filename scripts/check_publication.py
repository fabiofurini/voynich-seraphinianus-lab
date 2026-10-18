"""Pre-publication checks. Run before every push:

    python scripts/check_publication.py

Checks: Python syntax, JSON validity, unique HTML ids and working local links on
every page of the website (English and Italian), working relative links in every Markdown file, and the
absence of private data or third-party material that must not be redistributed.
"""
from pathlib import Path
import ast
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN_TEXT = ['voynich_mail_attachments', '@gmail.com', '@lix.polytechnique.fr',
                  'ANGjdJ', 'base64_url_content', 'browserAuth']
# Third-party inputs that fetch_data.py downloads locally; they must never be committed.
FORBIDDEN_FILES = ['CS_OCR_TRANSLITERATION.txt', 'voynich_ZL3b.txt', 'crib_latin.txt', 'crib_italian.txt']
errors = []


def tracked_files():
    """Files under version control (falls back to the whole tree outside a git checkout)."""
    try:
        out = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        return [ROOT / line for line in out.splitlines() if (ROOT / line).is_file()]
    except (OSError, subprocess.CalledProcessError):
        return [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and '.venv' not in p.parts]


def is_external(target):
    return target.startswith(('https:', 'http:', 'data:', 'mailto:'))


# 1. Code and data parse
for p in ROOT.rglob('*.py'):
    if '.venv' in p.parts:
        continue
    try:
        ast.parse(p.read_text(), filename=str(p))
    except SyntaxError as e:
        errors.append(f'Python syntax: {p.relative_to(ROOT)}: {e}')
for p in ROOT.rglob('*.json'):
    try:
        json.loads(p.read_text())
    except ValueError as e:
        errors.append(f'Invalid JSON: {p.relative_to(ROOT)}: {e}')

# 2. Website pages: unique ids, local links and anchors resolve
for page in sorted((ROOT / 'docs').rglob('*.html')):
    html = page.read_text()
    name = page.relative_to(ROOT / 'docs')
    ids = re.findall(r'\bid="([^"]+)"', html)
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        errors.append(f'{name}: duplicate ids {sorted(dupes)}')
    for target in re.findall(r'(?:href|src)="([^"]+)"', html):
        if is_external(target):
            continue
        path, _, anchor = target.partition('#')
        if path and not (page.parent / path).exists():
            errors.append(f'{name}: missing file {target}')
        elif anchor:
            dest = (page.parent / path).read_text() if path else html
            if f'id="{anchor}"' not in dest:
                errors.append(f'{page.name}: missing anchor {target}')

# 3. Markdown: relative links resolve
for md in ROOT.rglob('*.md'):
    if '.git' in md.parts or '.venv' in md.parts:
        continue
    for target in re.findall(r'\]\(([^)\s]+)\)', md.read_text()):
        if is_external(target) or target.startswith('#'):
            continue
        path = target.split('#')[0]
        if path and not (md.parent / path).exists():
            errors.append(f'{md.relative_to(ROOT)}: broken link {target}')

# 4. Private data and non-redistributable sources
for p in tracked_files():
    if p.name in FORBIDDEN_FILES:
        errors.append(f'Third-party source must not be committed: {p.relative_to(ROOT)}')
    if p.name == 'check_publication.py' or p.suffix not in {'.py', '.md', '.json', '.html', '.js', '.yml', '.txt', '.cff'}:
        continue
    text = p.read_text(errors='ignore')
    for f in FORBIDDEN_TEXT:
        if f in text:
            errors.append(f'Private data pattern {f!r} in {p.relative_to(ROOT)}')

if errors:
    print('Publication checks FAILED:')
    for e in errors:
        print('  -', e)
    sys.exit(1)
print('Publication checks passed: syntax, JSON, website links and ids, Markdown links, private-data exclusions.')
