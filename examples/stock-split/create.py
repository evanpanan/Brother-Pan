#!/usr/bin/env python3
"""Scaffold the one-for-two stock split rehearsal with an editable silent timeline."""
import argparse
from array import array
import json
import math
import random
import shutil
import sys
import wave
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parent
ROOT = EXAMPLE.parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from caption_rules import clean_caption
from new_episode import create


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_paper_sound(path):
    """A quiet, deterministic paper tear, generated locally from filtered noise."""
    rng = random.Random(29)
    rate, seconds = 48000, .27
    samples = array('h')
    coarse = fine = 0.
    for i in range(round(rate * seconds)):
        t = i / rate
        noise = rng.uniform(-1., 1.)
        coarse += .07 * (noise - coarse)
        fine += .40 * (noise - fine)
        envelope = min(t / .015, 1.) * (1. - t / seconds) ** 1.6
        fibers = .30 + .70 * abs(math.sin(90 * t + 180 * t * t)) ** .55
        samples.append(round(11500 * envelope * fibers * (fine - coarse)))
    if sys.byteorder != 'little':
        samples.byteswap()
    with wave.open(str(path), 'wb') as output:
        output.setparams((1, 2, rate, 0, 'NONE', 'not compressed'))
        output.writeframes(samples.tobytes())


def scaffold(out):
    create(out)
    write_paper_sound(out / 'public/paper-tear.wav')
    shutil.copy2(EXAMPLE / 'Film.tsx', out / 'src/Film.tsx')
    turns = json.loads((EXAMPLE / 'turns.json').read_text(encoding='utf-8'))
    script, scenes = [], []
    fps, cursor = 30, 0
    for turn in turns:
        phrases = turn['phrases']
        row = dict(sceneId=turn['sceneId'], speaker=turn['speaker'], kind=turn['sceneId'],
                   text=''.join(text for text, _ in phrases))
        caps = []
        elapsed = 0.17
        for text, seconds in phrases:
            caps.append(dict(text=clean_caption(text), startMs=round(elapsed * 1000),
                             endMs=round((elapsed + seconds - 0.12) * 1000)))
            elapsed += seconds
        frames = round((elapsed + 0.35) * fps)
        script.append(row)
        scenes.append(dict(row, caps=caps, start=cursor, frames=frames))
        cursor += frames
    save(out / 'script.json', script)
    save(out / 'src/scene-kinds.json', [s['kind'] for s in scenes])
    save(out / 'src/episode.json', dict(title='股票一拆二', fps=fps, sound='silent-demo', scenes=scenes))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    scaffold(parser.parse_args().out.resolve())
