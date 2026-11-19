#!/usr/bin/env python3
"""Clean displayed captions; preserve timing, questions and numeric meaning."""
import argparse
import json
import re
import unicodedata
from pathlib import Path


def digit(ch):
    return bool(ch) and ch in '0123456789０１２３４５６７８９'


def letter(ch):
    return bool(ch) and ch.isascii() and ch.isalpha()


def clean_caption(text):
    out = []
    for i, ch in enumerate(text):
        a = text[i - 1] if i else ''
        b = text[i + 1] if i + 1 < len(text) else ''
        if ch in '?？':
            out.append('？')
        elif ch in '%％/':
            out.append(ch)
        elif ((ch in '.．:：' and digit(a) and digit(b)) or (ch == '.' and letter(a) and letter(b))):
            out.append({'．': '.', '：': ':'}.get(ch, ch))
        elif ch in '-−' and digit(b):
            out.append(ch)
        elif ch in '–—~～' and (digit(a) or (bool(a) and a in '%％')) and digit(b):
            out.append('至')
        elif ch in "-'’" and letter(a) and letter(b):
            out.append(ch)
        elif not unicodedata.category(ch).startswith('P'):
            out.append(ch)
    return re.sub(r'\s+', ' ', ''.join(out)).strip()


def clean_srt(text):
    blocks = re.split(r'\n\s*\n', text.replace('\r\n', '\n').strip())
    result = []
    for block in blocks:
        lines = block.splitlines()
        time_index = next((i for i, line in enumerate(lines) if '-->' in line), None)
        if time_index is None:
            raise ValueError('SRT block has no timing line')
        caption = '\n'.join(filter(None, (clean_caption(x) for x in lines[time_index + 1:])))
        if caption:
            result.append(f'{len(result) + 1}\n{lines[time_index]}\n{caption}')
    return '\n\n'.join(result) + ('\n' if result else '')


def clean_timeline(obj):
    """Only caption fields; narration text must remain unchanged."""
    scenes = obj.get('scenes', []) if isinstance(obj, dict) else obj
    for scene in scenes:
        for cap in scene.get('caps', []):
            cap['text'] = clean_caption(cap['text'])
    return obj


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = args.input.read_text(encoding='utf-8')
    result = json.dumps(clean_timeline(json.loads(raw)), ensure_ascii=False, indent=2) + '\n' if args.input.suffix == '.json' else clean_srt(raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding='utf-8')
