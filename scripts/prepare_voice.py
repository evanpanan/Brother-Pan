#!/usr/bin/env python3
"""Create cached dual Mandarin narration and aligned clean captions in an episode."""
import argparse
import asyncio
import hashlib
import json
import math
import re
import subprocess
import unicodedata
from pathlib import Path
from caption_rules import clean_caption


def normalized(text):
    return ''.join(c.lower() for c in unicodedata.normalize('NFKC', text) if c.isalnum())


def voice_key(text, voice, rate, pitch):
    return hashlib.sha256(json.dumps([text, voice, rate, pitch], ensure_ascii=False).encode()).hexdigest()[:20]


def pages(words, source, limit=13):
    words = [dict(w) for w in words]
    source = unicodedata.normalize('NFKC', source)
    positions = [i for i, ch in enumerate(source) if ch.isalnum()]
    matched = ''.join(normalized(w['text']) for w in words) == normalized(source)
    cursor, count, group, result = 0, 0, [], []
    for i, word in enumerate(words):
        if matched:
            size = len(normalized(word['text']))
            if size:
                first = positions[cursor]
                cursor += size
                end = positions[cursor] if cursor < len(positions) else len(source)
                word['text'] = source[first:end]
        group.append(word)
        count += len(clean_caption(word['text']))
        if re.search(r'[,，。.!！？?;；:：]', word['text']) or count >= limit or i == len(words) - 1:
            text = clean_caption(''.join(w['text'] for w in group))
            if text:
                result.append(dict(text=text, startMs=group[0]['startMs'], endMs=group[-1]['endMs']))
            group, count = [], 0
    return result


def stamp(ms):
    h, left = divmod(round(ms), 3600000)
    m, left = divmod(left, 60000)
    s, ms = divmod(left, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'


async def produce(project):
    import edge_tts
    project = Path(project).resolve()
    config = json.loads((project / 'brand.json').read_text())
    rows = json.loads((project / 'script.json').read_text())
    if not isinstance(rows, list) or not rows:
        raise ValueError('script.json must be a nonempty scene array')
    if any(r.get('speaker') not in {'M', 'F'} or not r.get('text', '').strip() for r in rows):
        raise ValueError('Each scene needs text and speaker M/F')
    cache = project / 'voice-cache'
    cache.mkdir(exist_ok=True)
    sem = asyncio.Semaphore(3)
    locks = {}

    async def one(index, row):
        choice = config['voices']['male' if row['speaker'] == 'M' else 'female']
        text = row.get('ttsText', row['text'])
        rate = row.get('rate', config['voices']['hook_rate'] if row.get('kind') == 'hook' else choice['rate'])
        key = voice_key(text, choice['id'], rate, choice['pitch'])
        mp3, meta = cache / f'{key}.mp3', cache / f'{key}.json'
        if mp3.exists() and meta.exists() and mp3.stat().st_size:
            return mp3, json.loads(meta.read_text())
        async with locks.setdefault(key, asyncio.Lock()):
            if mp3.exists() and meta.exists() and mp3.stat().st_size:
                return mp3, json.loads(meta.read_text())
            async with sem:
                for attempt in range(2):
                    temp = mp3.with_suffix('.part')
                    timings = []
                    try:
                        with temp.open('wb') as out:
                            async for chunk in edge_tts.Communicate(text, choice['id'], rate=rate, pitch=choice['pitch'], boundary='WordBoundary').stream():
                                if chunk['type'] == 'audio':
                                    out.write(chunk['data'])
                                elif chunk['type'] == 'WordBoundary':
                                    timings.append(dict(text=chunk['text'], startMs=chunk['offset'] / 10000, endMs=(chunk['offset'] + chunk['duration']) / 10000))
                        if not timings or not temp.stat().st_size:
                            raise RuntimeError('Voice service returned no audio/timing')
                        temp.replace(mp3)
                        meta.write_text(json.dumps(timings, ensure_ascii=False))
                        print(f'Voice {index + 1}/{len(rows)}', flush=True)
                        return mp3, timings
                    except Exception:
                        temp.unlink(missing_ok=True)
                        if attempt:
                            raise
    generated = await asyncio.gather(*(one(i, r) for i, r in enumerate(rows)))
    episode = json.loads((project / 'src/episode.json').read_text())
    fps, cursor, scenes, listing, srt = episode.get('fps', 30), 0, [], [], []
    for i, (row, (mp3, words)) in enumerate(zip(rows, generated)):
        duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(mp3)]))
        frames = math.ceil((duration + .14) * fps)
        wav = cache / f'part-{i:03}.wav'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(mp3), '-af', f'apad=whole_dur={frames/fps}', '-t', str(frames/fps), '-ar', '48000', '-ac', '1', str(wav)], check=True)
        listing.append(f"file 'part-{i:03}.wav'")
        caps = pages(words, row.get('ttsText', row['text']), config['captions']['max_chars'])
        for cap in caps:
            srt.append(f"{len(srt)+1}\n{stamp(cursor/fps*1000+cap['startMs'])} --> {stamp(cursor/fps*1000+cap['endMs'])}\n{cap['text']}\n")
        scenes.append(dict(row, sceneId=row.get('sceneId', f'scene-{i:03}'), start=cursor, frames=frames, caps=caps))
        cursor += frames
    concat = cache / 'concat.txt'
    concat.write_text('\n'.join(listing) + '\n')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', str(project / 'public/narration.wav')], check=True)
    episode.update(scenes=scenes, audio='narration.wav', sound='narration-generated')
    (project / 'src/episode.json').write_text(json.dumps(episode, ensure_ascii=False, indent=2) + '\n')
    (project / 'outputs').mkdir(exist_ok=True)
    (project / 'outputs/captions.srt').write_text('\n'.join(srt))
    print(f'{cursor} frames / {cursor/fps:.2f} seconds')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    args = parser.parse_args()
    asyncio.run(produce(args.project))
