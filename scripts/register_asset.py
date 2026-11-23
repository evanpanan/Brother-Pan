#!/usr/bin/env python3
"""Register an owned/licensed reusable asset; refuse duplicate bytes and outside paths."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def register(path, asset_id, kind, tags, origin, description='', root=ROOT):
    root = root.resolve()
    path = (root / path).resolve()
    rel = path.relative_to(root).as_posix()
    if not rel.startswith(('assets/', 'library/')) or not path.is_file():
        raise ValueError('Only existing assets/ or library/ files may be registered')
    if path.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.svg', '.tsx', '.ts', '.json', '.woff', '.ttf', '.webp'}:
        raise ValueError('Unsupported reusable asset format')
    registry = root / 'assets/registry.json'
    data = json.loads(registry.read_text())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if any(x['id'] == asset_id for x in data['assets']):
        raise ValueError('Asset id already exists; update its record explicitly')
    same = next((x for x in data['assets'] if x['sha256'] == digest), None)
    if same:
        raise ValueError(f'Duplicate bytes: reuse {same["id"]}')
    data['assets'].append(dict(id=asset_id, path=rel, kind=kind, tags=tags, origin=origin, description=description, sha256=digest))
    registry.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return asset_id


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    parser.add_argument('--id', required=True)
    parser.add_argument('--kind', required=True)
    parser.add_argument('--tags', default='')
    parser.add_argument('--origin', required=True, choices=['original-generated', 'original-code', 'brand-reference', 'licensed-font'])
    parser.add_argument('--description', default='')
    args = parser.parse_args()
    print(register(args.path, args.id, args.kind, args.tags.split(','), args.origin, args.description))
