#!/usr/bin/env python3
"""Check observable timeline, caption and photo-reuse invariants; not visual quality."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from caption_rules import clean_caption


def audit(project):
    project = Path(project)
    data = json.loads((project / 'src/episode.json').read_text())
    fps = data.get('fps', 30)
    scenes = data['scenes']
    errors, ids, compositions, cursor = [], set(), {}, 0
    kinds_file = project / 'src/scene-kinds.json'
    supported = set(json.loads(kinds_file.read_text())) if kinds_file.exists() else None
    if not isinstance(fps, (int, float)) or fps <= 0:
        return dict(ok=False, errors=['fps must be positive'], frames=0, seconds=0, visual_review='not_performed_by_this_script')
    if not scenes:
        errors.append('episode has no scenes')
    used = {}
    manifest = json.loads((project / 'asset-manifest.json').read_text()) if (project / 'asset-manifest.json').exists() else []
    assets = {r['id']: r for r in manifest}
    source_ids = {s['id'] for s in data.get('sources', [])}
    for index, shot in enumerate(scenes):
        sid = shot.get('sceneId')
        if not sid or sid in ids:
            errors.append(f'scene {index}: missing/duplicate sceneId')
        ids.add(sid)
        if supported is not None and shot.get('kind') not in supported:
            errors.append(f'{sid}: unimplemented scene kind; add a real renderer before export')
        if shot.get('start') != cursor or not isinstance(shot.get('frames'), int) or shot['frames'] <= 0:
            errors.append(f'{sid}: invalid or discontinuous frame interval')
        cursor = shot.get('start', 0) + shot.get('frames', 0)
        if shot.get('speaker') not in {'M', 'F'}:
            errors.append(f'{sid}: speaker must be M or F')
        composition = shot.get('compositionId', sid)
        if composition in compositions:
            prior = compositions[composition]
            if prior != index - 1 or not shot.get('continuityGroup') or shot.get('continuityGroup') != scenes[prior].get('continuityGroup'):
                errors.append(f'{sid}: repeated full composition outside a continuous shot')
        compositions[composition] = index
        last = -1
        for cap in shot.get('caps', []):
            if cap['startMs'] < last or cap['endMs'] <= cap['startMs'] or cap['endMs'] > shot['frames'] / fps * 1000 + 20:
                errors.append(f'{sid}: invalid caption timing')
            last = cap['endMs']
            if cap['text'] != clean_caption(cap['text']):
                errors.append(f'{sid}: display punctuation remains')
            if len(cap['text']) > 30:
                errors.append(f'{sid}: caption needs shorter paging/line fitting')
        if 'voicedMs' in shot:
            intervals = shot['voicedMs']
            previous_end = 0
            duration_ms = shot['frames'] * 1000 / fps
            if not isinstance(intervals, list):
                errors.append(f'{sid}: voicedMs must be a list of intervals')
            else:
                for interval in intervals:
                    if (not isinstance(interval, list) or len(interval) != 2
                            or not all(isinstance(n, (float, int)) and math.isfinite(n) for n in interval)
                            or not previous_end <= interval[0] < interval[1] <= duration_ms + .001):
                        errors.append(f'{sid}: mouth activity falls outside its speaking turn or overlaps')
                        break
                    previous_end = interval[1]
        if shot.get('factual') and (not shot.get('sourceIds') or not set(shot['sourceIds']) <= source_ids):
            errors.append(f'{sid}: factual claim lacks known source ids')
        for aid in shot.get('assets', []):
            row = assets.get(aid)
            if row is None:
                errors.append(f'{sid}: unregistered asset {aid}')
                continue
            path = (project / row['path']).resolve()
            if not path.is_relative_to(project.resolve()) or not path.is_file():
                errors.append(f'{sid}: missing/outside asset {aid}')
                continue
            if row['kind'] in {'photo', 'video', 'evidence'}:
                key = row.get('sourceAssetId') or hashlib.sha256(path.read_bytes()).hexdigest()
                used.setdefault(key, []).append(index)
    for indexes in used.values():
        unique = sorted(set(indexes))
        if unique and unique != list(range(unique[0], unique[-1] + 1)):
            errors.append('same photo/video has multiple separated intervals')
    return dict(ok=not errors, errors=errors, frames=cursor, seconds=cursor / fps, visual_review='not_performed_by_this_script')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    args = parser.parse_args()
    result = audit(args.project)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['ok'] else 1)
