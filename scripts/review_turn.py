#!/usr/bin/env python3
"""Extract one full dialogue turn with both voice handoffs, at the film's original speed."""
import argparse
import json
import math
import os
import subprocess
import tempfile
from pathlib import Path


def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries',
        'stream=codec_type,duration:format=duration', '-of', 'json', str(path),
    ]))


def extract(project, turn_id, source, dest, lead=2.0, tail=2.0, allow_silent=False):
    if not all(math.isfinite(n) and n >= 0 for n in (lead, tail)):
        raise ValueError('lead and tail must be finite nonnegative seconds')
    source, dest = source.resolve(), dest.resolve()
    if source == dest or dest.suffix.lower() != '.mp4':
        raise ValueError('Choose a separate .mp4 output path')
    episode = json.loads((project / 'src/episode.json').read_text(encoding='utf-8'))
    fps = episode['fps']
    matches = [s for s in episode['scenes'] if s['sceneId'] == turn_id]
    if len(matches) != 1:
        raise ValueError(f'Expected exactly one sceneId {turn_id!r}, found {len(matches)}')
    scene = matches[0]
    info = probe(source)
    video = next((s for s in info['streams'] if s['codec_type'] == 'video'), None)
    audio = any(s['codec_type'] == 'audio' for s in info['streams'])
    if video is None or (not audio and not allow_silent):
        raise ValueError('Source needs a picture and sound; only a motion rehearsal may use --allow-silent')
    source_secs = float(video.get('duration') or info['format']['duration'])
    timeline_end = max(s['start'] + s['frames'] for s in episode['scenes'])
    if abs(source_secs - timeline_end / fps) > max(2 / fps, .10):
        raise ValueError('Film length differs from episode.json. Use the timeline that was rendered.')
    begin = max(0, scene['start'] - round(lead * fps)) / fps
    end = min(timeline_end, scene['start'] + scene['frames'] + round(tail * fps)) / fps
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=dest.parent) as folder:
        clip = Path(folder) / 'clip.mp4'
        subprocess.run([
            'ffmpeg', '-v', 'error', '-nostdin', '-ss', f'{begin:.9f}', '-i', str(source),
            '-t', f'{end - begin:.9f}', '-map', '0:v:0', '-map', '0:a:0?',
            '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast',
            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
            '-movflags', '+faststart', str(clip),
        ], check=True)
        os.replace(clip, dest)
    return dict(sceneId=turn_id, start=round(begin, 3), end=round(end, 3),
                original_speed=1, audio=audio, file=str(dest))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--turn', required=True, help='sceneId, as stored in src/episode.json')
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--video', type=Path, help='Default: outputs/video.mp4 under the project')
    parser.add_argument('--lead', type=float, default=2., help='Preceding seconds, default 2')
    parser.add_argument('--tail', type=float, default=2., help='Following seconds, default 2')
    parser.add_argument('--allow-silent', action='store_true', help='Explicitly review picture only')
    args = parser.parse_args()
    try:
        result = extract(args.project, args.turn, args.video or args.project / 'outputs/video.mp4',
                         args.out, args.lead, args.tail, args.allow_silent)
    except ValueError as err:
        parser.exit(2, f'{err}\n')
    print(json.dumps(result, ensure_ascii=False))
