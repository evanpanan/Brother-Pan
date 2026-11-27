#!/usr/bin/env python3
"""Find the subtitle window containing a line or inspect what was on screen at a drop-off."""
import argparse
import re
import unicodedata
from bisect import bisect_right
from dataclasses import dataclass
from pathlib import Path

from caption_rules import clean_caption


@dataclass(frozen=True)
class Cue:
    start: int
    end: int
    text: str


def milliseconds(timestamp):
    match = re.fullmatch(r'(\d+):([0-5]\d):([0-5]\d)[,.](\d{3})', timestamp)
    if not match:
        raise ValueError(f'时间码有误 {timestamp}')
    hours, minutes, seconds, millis = map(int, match.groups())
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis


def load_srt(path):
    cues = []
    for block in re.split(r'\n\s*\n', path.read_text(encoding='utf-8-sig').strip()):
        lines = block.splitlines()
        if lines and lines[0].strip().isdigit():
            lines.pop(0)
        if len(lines) < 2 or '-->' not in lines[0]:
            raise ValueError('需要带起止时间与字幕的 SRT')
        left, right = lines[0].split('-->', 1)
        start, end = milliseconds(left.strip()), milliseconds(right.strip())
        if start >= end or (cues and start < cues[-1].start):
            raise ValueError(f'时间码倒序 {lines[0]}')
        cues.append(Cue(start, end, ' '.join(lines[1:]).strip()))
    return cues


def search_text(text):
    cleaned = clean_caption(unicodedata.normalize('NFKC', text)).casefold()
    return ''.join(cleaned.split()).replace('？', '')


def find_line(cues, phrase):
    needle = search_text(phrase)
    if not needle:
        raise ValueError('查找词至少应有一个字或数字')
    offsets, pieces = [], []
    length = 0
    for cue in cues:
        offsets.append(length)
        piece = search_text(cue.text)
        pieces.append(piece)
        length += len(piece)
    full = ''.join(pieces)
    for match in re.finditer(re.escape(needle), full):
        first = bisect_right(offsets, match.start()) - 1
        last = bisect_right(offsets, match.end() - 1) - 1
        yield cues[first:last + 1]


def at_time(cues, moment):
    return [cue for cue in cues if cue.start <= moment < cue.end]


def display(cues):
    start, end = cues[0].start / 1000, max(cue.end for cue in cues) / 1000
    return f'{start:.3f}–{end:.3f} 秒  ' + ' / '.join(cue.text for cue in cues)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('srt', type=Path)
    parser.add_argument('--line', action='append', default=[], help='要定位的台词 可跨字幕 可重复指定')
    parser.add_argument('--at', type=float, action='append', default=[], help='在成片第几秒查看当时字幕')
    args = parser.parse_args()
    if not args.line and not args.at:
        parser.error('请给出 --line 或 --at')
    try:
        cues = load_srt(args.srt)
        for phrase in args.line:
            hits = list(find_line(cues, phrase))
            print(f'「{phrase}」')
            print('\n'.join(display(hit) for hit in hits) or '未找到')
        for seconds in args.at:
            if not 0 <= seconds < float('inf'):
                raise ValueError('--at 需要非负有限秒数')
            hits = at_time(cues, round(seconds * 1000))
            print(f'{seconds:g} 秒', display(hits) if hits else '该时刻无字幕')
    except (ValueError, OSError) as error:
        parser.exit(2, f'{error}\n')


if __name__ == '__main__':
    main()
