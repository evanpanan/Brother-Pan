#!/usr/bin/env python3
"""Create a portable isolated episode from the reusable library."""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def create(out, asset_ids=(), root=ROOT):
    out = Path(out).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError('Output must be new or empty; existing episode is not overwritten')
    shutil.copytree(root / 'assets/starter', out, dirs_exist_ok=True)
    shutil.copytree(root / 'library', out / 'src/library')
    (out / 'public').mkdir(exist_ok=True)
    for name in ['host-poses.png', 'front-poses.png']:
        shutil.copy2(root / 'assets/characters' / name, out / 'public' / name)
    shutil.copy2(root / 'assets/fonts/head.woff', out / 'public/head.woff')
    shutil.copy2(root / 'assets/fonts/OFL-NotoSansSC.txt', out / 'public/OFL-NotoSansSC.txt')
    registry = json.loads((root / 'assets/registry.json').read_text())['assets']
    index = {r['id']: r for r in registry}
    manifest = []
    for asset_id in asset_ids:
        row = index[asset_id]
        if row['kind'] not in {'background', 'illustration', 'reference'}:
            raise ValueError('Optional copy accepts image assets; code is already copied')
        target = out / 'public' / Path(row['path']).name
        if target.exists():
            raise ValueError('Asset filename collision')
        shutil.copy2(root / row['path'], target)
        manifest.append(dict(id=asset_id, path='public/' + target.name, kind=row['kind'], sha256=row['sha256'], origin=row['origin']))
    (out / 'asset-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    (out / 'brand.json').write_text((root / 'config/brand.json').read_text())
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--assets', nargs='*', default=[])
    args = parser.parse_args()
    print(create(args.out, args.assets))
