#!/usr/bin/env python3
"""Check local workrole links, GitHub downloads, redirects, and migration targets.

Resolves repository-owned URLs against this checkout, including URL escaping.
Does not make network requests: new main-branch paths do not exist online until publish.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
TEXT = {'.md', '.html', '.txt', '.py', '.sh', '.yml', '.json'}
URL = re.compile(r'https?://[^\s<>"\'`]+')
LIQUID = re.compile(r'''["']([^"']+)["']\s*\|\s*(?:relative_url|absolute_url)''')
MARKDOWN = re.compile(r'\]\((\.[^\s)]+)\)')
DATA_URL = re.compile(r'''["']url["']\s*:\s*["']([^"']+)["']''')
HTML = re.compile(r'''(?:href|src)=["']([^"']+)["']''')


def exists(path):
    target = ROOT / path.lstrip('/')
    if target.is_file():
        return True
    if target.is_dir():
        return (target / 'index.md').is_file() or (target / 'index.html').is_file()
    if target.suffix == '.html':
        return target.with_suffix('.md').is_file()
    if not target.suffix:
        return target.with_suffix('.md').is_file() or target.with_suffix('.html').is_file()
    return False


def check():
    errors = []
    checked = 0
    for file in sorted(ROOT.rglob('*')):
        if not file.is_file() or file.suffix not in TEXT or '.git' in file.parts:
            continue
        rel = file.relative_to(ROOT)
        if rel.parts[0] in {'scripts', 'docs', '_legacy_workrole_redirects'}:
            continue
        try:
            text = file.read_text()
        except UnicodeDecodeError:
            continue
        # Historical paths belong only in the migration map and redirect declarations.
        if re.search(r'\b(?:classes|workroles)/', text):
            errors.append(f'{rel}: obsolete workrole path')
        references = [(m[1], 'root') for m in LIQUID.finditer(text)]
        references += [(m[1], 'relative') for m in MARKDOWN.finditer(text)]
        references += [(m[1], 'html') for m in HTML.finditer(text) if '{{' not in m[1]]
        references += [(m[1], 'root') for m in DATA_URL.finditer(text)]
        references += [(m[0], 'url') for m in URL.finditer(text)]
        for raw, kind in references:
            raw = raw.replace(r'\(', '(').replace(r'\)', ')').rstrip('.,;')
            while raw.endswith(')') and raw.count(')') > raw.count('('):
                raw = raw[:-1]
            path = None
            if raw.startswith(('http:', 'https:')):
                parsed = urlsplit(raw)
                parts = unquote(parsed.path).split('/')
                if parsed.netloc == 'raw.githubusercontent.com' and parts[1:3] == ['jboyce1', 'ppsCTF']:
                    if parts[3] != 'main':
                        errors.append(f'{rel}: download pinned to old revision: {raw}')
                    path = '/'.join(parts[4:])
                elif parsed.netloc == 'github.com' and parts[1:4] == ['jboyce1', 'ppsCTF', 'raw']:
                    path = '/'.join(parts[5:])
                elif parsed.netloc == 'jboyce1.github.io' and parsed.path.startswith('/ppsCTF/'):
                    path = unquote(parsed.path[len('/ppsCTF/'):])
            elif raw.startswith(('#', 'mailto:', 'javascript:', 'data:')):
                continue
            elif kind == 'root' or raw.startswith('/'):
                path = unquote(raw.split('#')[0].split('?')[0]).lstrip('/')
            elif kind in {'relative', 'html'}:
                path = str(rel.parent / unquote(raw.split('#')[0].split('?')[0]))
            # Audit owned workrole links plus shared navigation/assets. Unrelated event sites are out of scope.
            if path is None or not (path.startswith('workrole/') or rel.parts[0] in {'workrole', '_layouts'}):
                continue
            checked += 1
            if not exists(path):
                line = text[:text.find(raw)].count('\n') + 1 if raw in text else '?'
                errors.append(f'{rel}:{line}: missing {path}')
    mapping = json.loads((ROOT / 'docs/workrole-paths.json').read_text())
    for old, new in mapping.items():
        if not (ROOT / new).is_file():
            errors.append(f'Migration target missing: {old} -> {new}')
    redirects = ROOT / '_legacy_workrole_redirects'
    if '_legacy_workrole_redirects' not in (ROOT / '_config.yml').read_text():
        errors.append('Jekyll config does not include legacy redirects')
    for file in redirects.glob('*.html'):
        text = file.read_text()
        destination = re.search(r'^redirect_to: (.+)$', text, re.M)
        if not destination or not exists(destination[1]):
            errors.append(f'{file.name}: invalid redirect destination')
    for obsolete in ['classes', 'workroles']:
        if (ROOT / obsolete).exists():
            errors.append(f'Obsolete directory still exists: {obsolete}')
    for error in sorted(set(errors)):
        print(error)
    print(f'Checked {checked} link references, {len(mapping)} migration paths, and {len(list(redirects.glob("*.html")))} redirects.')
    return bool(errors)


if __name__ == '__main__':
    sys.exit(check())
