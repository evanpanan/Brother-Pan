#!/usr/bin/env python3
"""Check portable paths, metadata, owned asset integrity and local Markdown links."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', '__pycache__', '.venv', 'outputs', 'rendered', '.generated', 'voice-cache'}


def check(root=ROOT):
    errors = []
    data = json.loads((root / 'assets/registry.json').read_text())
    ids, paths, digests = set(), set(), {}
    for row in data['assets']:
        if row['id'] in ids or row['path'] in paths:
            errors.append('duplicate asset id/path')
        ids.add(row['id'])
        paths.add(row['path'])
        path = (root / row['path']).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            errors.append(f'missing/outside asset: {row["id"]}')
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != row['sha256']:
            errors.append(f'asset changed without updating registry: {row["id"]}')
        if digest in digests:
            errors.append(f'duplicate asset bytes: {row["id"]} / {digests[digest]}')
        digests[digest] = row['id']
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if any(part in SKIP for part in rel.parts) or not path.is_file():
            continue
        if path.is_symlink():
            errors.append(f'symlink is not portable: {rel}')
        if path.stat().st_size > 10 * 1024 * 1024:
            errors.append(f'oversized non-library file: {rel}')
        if path.suffix not in {'.md', '.json', '.py', '.ts', '.tsx', '.yaml', '.yml', '.txt', '.cjs'}:
            continue
        text = path.read_text(encoding='utf-8')
        if re.search(r'/(?:Users|home)/[^\s/]+/', text) or re.search(r'/private/(?:var|tmp)/', text):
            errors.append(f'machine-specific path: {rel}')
        if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', text) or re.search(r'\bsk-[A-Za-z0-9]{32,}\b', text):
            errors.append(f'possible credential material: {rel}')
        if path.suffix == '.md':
            for link in re.findall(r'\]\(([^)]+)\)', text):
                target = link.strip('<>').split('#')[0]
                if not target or '://' in target or target.startswith(('mailto:', '#')):
                    continue
                if not (path.parent / target).exists():
                    errors.append(f'broken local Markdown link in {rel}: {target}')
    return dict(ok=not errors, errors=errors, assets=len(ids))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    result = check(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['ok'] else 1)
