#!/usr/bin/env python3
"""Extract actual frame samples for inspection (Pillow required)."""
import argparse
import json
import subprocess
from pathlib import Path


def create(video, timeline, out):
    from PIL import Image, ImageDraw
    data = json.loads(Path(timeline).read_text())
    fps = data.get('fps', 30)
    shots = data['scenes']
    out.mkdir(parents=True, exist_ok=True)
    canvas = Image.new('RGB', (810, 500 * len(shots)), '#deded5')
    draw = ImageDraw.Draw(canvas)
    for i, shot in enumerate(shots):
        for col, fraction in enumerate([.05, .5, .95]):
            t = (shot['start'] + max(0, shot['frames'] - 1) * fraction) / fps
            path = out / f'{i:03}-{col}.png'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.4f}', '-i', str(video), '-frames:v', '1', str(path)], check=True)
            im = Image.open(path)
            im.thumbnail((270, 480))
            canvas.paste(im, (col * 270, i * 500))
            draw.text((col * 270 + 5, i * 500 + 480), f'{shot["sceneId"]} {t:.2f}s', fill='black')
    target = out / 'contact.jpg'
    canvas.save(target)
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', type=Path, required=True)
    parser.add_argument('--timeline', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    print(create(args.video, args.timeline, args.out))
