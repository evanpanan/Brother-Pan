#!/usr/bin/env python3
"""Check streams and complete decoding, without claiming visual/audio review."""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path


def verify(path, allow_silent=False, width=1080, height=1920, fps=30):
    info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
    videos = [s for s in info['streams'] if s['codec_type'] == 'video']
    audio = [s for s in info['streams'] if s['codec_type'] == 'audio']
    errors = []
    if not videos:
        errors.append('No video stream')
    else:
        if (videos[0]['width'], videos[0]['height']) != (width, height):
            errors.append('Dimensions differ from the requested format')
        try:
            actual_fps = float(Fraction(videos[0]['avg_frame_rate']))
            if abs(actual_fps - fps) > .01:
                errors.append('Frame rate differs from requested fps')
        except (KeyError, ValueError, ZeroDivisionError):
            errors.append('Video has no usable frame rate')
    if not audio and not allow_silent:
        errors.append('No audio stream; only intentional silent demos may use --allow-silent')
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'null', '-'], check=True, capture_output=True)
    return dict(ok=not errors, errors=errors, duration=float(info['format']['duration']), complete_decode=True, has_audio=bool(audio), realtime_review='not_performed_by_this_script')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--allow-silent', action='store_true')
    parser.add_argument('--width', type=int, default=1080)
    parser.add_argument('--height', type=int, default=1920)
    parser.add_argument('--fps', type=float, default=30)
    args = parser.parse_args()
    result = verify(args.video, args.allow_silent, args.width, args.height, args.fps)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['ok'] else 1)
