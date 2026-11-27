#!/usr/bin/env python3
"""Create cached dual Mandarin narration and aligned clean captions in an episode."""
import argparse
import asyncio
import hashlib
import json
import math
import os
import re
import subprocess
import unicodedata
import tempfile
from contextlib import contextmanager
from pathlib import Path
from local_narration import LocalNarrator
from caption_rules import clean_caption


def normalized(text):
    return ''.join(c.lower() for c in unicodedata.normalize('NFKC', text) if c.isalnum())


def voice_key(text, voice, rate, pitch):
    return hashlib.sha256(json.dumps([text, voice, rate, pitch], ensure_ascii=False).encode()).hexdigest()[:20]


def pronunciation_text(text, config):
    for original, spoken in config.get('pronunciation', {}).get('same_length_substitutions', {}).items():
        if not original or len(normalized(original)) != len(normalized(spoken)):
            raise ValueError('Pronunciation substitutions must preserve normalized character count')
        text = text.replace(original, spoken)
    return text


def pages(words, source, limit=13, spoken_source=None):
    words = [dict(w) for w in words]
    positions = [i for i, ch in enumerate(source) if ch.isalnum()]
    alignment = normalized(spoken_source if spoken_source is not None else source)
    matched = (''.join(normalized(w['text']) for w in words) == alignment
               and len(positions) == len(alignment))
    cursor, end, count, group, result = 0, 0, 0, [], []
    if matched:
        words = [w for w in words if normalized(w['text'])]
    for i, word in enumerate(words):
        if matched:
            first = end
            cursor += len(normalized(word['text']))
            end = positions[cursor] if cursor < len(positions) else len(source)
            if cursor < len(positions):
                while end > first + 1 and source[end-1] in '$¥￥€£+-−':
                    end -= 1
            word['text'] = source[first:end]
        group.append(word)
        count += len(clean_caption(word['text']))
        next_char = words[i+1]['text'][:1] if i+1 < len(words) else ''
        numeric_join = bool(next_char.isdigit() and re.search(r'\d[.,:]?$', word['text']))
        phrase_end = re.search(r'[,，。.!！？?;；:：]\s*$', word['text']) or count >= limit
        if (phrase_end and not numeric_join) or i == len(words) - 1:
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


def manual_caps(cues, source, duration):
    result, last = [], 0.0
    for cue in cues:
        start, end = float(cue['startMs']), float(cue['endMs'])
        if not last <= start < end <= duration:
            raise ValueError('captionCues 必须在当轮音频内且不能重叠')
        result.append(dict(text=clean_caption(cue['text']), startMs=start, endMs=end))
        last = end
    joined = ''.join(c['text'] for c in result).replace(' ', '')
    if not result or joined != clean_caption(source).replace(' ', ''):
        raise ValueError('captionCues 必须覆盖整轮显示文稿')
    return result


def voice_choice(row, config):
    choice = config['voices']['male' if row['speaker'] == 'M' else 'female']
    provider = choice.get('provider', 'edge-tts')
    if provider not in {'kokoro', 'edge-tts'}:
        raise ValueError(f"不支持的配音服务 {provider}（{choice['id']}）")
    return provider, choice


async def edge_take(text, choice, rate, mp3, meta):
    import edge_tts
    for attempt in range(2):
        try:
            words = []
            with mp3.open('wb') as out:
                client = edge_tts.Communicate(text, choice['id'], rate=rate,
                                              pitch=choice['pitch'], boundary='WordBoundary')
                async for chunk in client.stream():
                    if chunk['type'] == 'audio':
                        out.write(chunk['data'])
                    elif chunk['type'] == 'WordBoundary':
                        words.append(dict(text=chunk['text'], startMs=chunk['offset'] / 10000,
                                          endMs=(chunk['offset'] + chunk['duration']) / 10000))
            if not mp3.stat().st_size or not words:
                raise RuntimeError('Edge 服务未返回声音或时间码')
            meta.write_text(json.dumps(words, ensure_ascii=False))
            return
        except Exception as exc:
            if attempt:
                raise RuntimeError(f"无法生成 Edge 声线 {choice['id']}。检查网络或使用已授权的 audioFile。") from exc
            await asyncio.sleep(1)


def activity(wav):
    # Derive sound intervals from the recorded signal, independent of subtitle pages.
    import wave
    from array import array
    import sys
    with wave.open(str(wav)) as source:
        assert source.getsampwidth() == 2 and source.getnchannels() == 1
        hop = source.getframerate() // 50
        samples = array('h', source.readframes(source.getnframes()))
        if sys.byteorder != 'little':
            samples.byteswap()
    active = []
    for i in range(0, len(samples), hop):
        frame = samples[i:i+hop]
        if sum(x*x for x in frame) > len(frame) * 180**2:
            begin, end = i * 20 / hop, min(i+hop, len(samples)) * 20 / hop
            if active and begin - active[-1][1] <= 40:
                active[-1][1] = end
            else:
                active.append([begin, end])
    if not active:
        raise ValueError('该轮配音只检测到静音')
    return active, len(samples) * 20 / hop


def reaction_gap(row, following):
    if 'gapAfterMs' in row:
        gap = float(row['gapAfterMs'])
        if not math.isfinite(gap) or gap < 0:
            raise ValueError('gapAfterMs 必须是非负毫秒数')
        return gap
    if following and following['speaker'] != row['speaker']:
        return 750 if row['text'].rstrip().endswith(('？', '?')) else 580
    return 320


@contextmanager
def project_lock(path):
    # One writer per episode; the OS releases the lock even if synthesis crashes.
    with path.open('a+b') as lock:
        try:
            if os.name == 'nt':
                import msvcrt
                if not lock.tell():
                    lock.write(b'0')
                    lock.flush()
                lock.seek(0)
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise RuntimeError('已有配音任务正在写入同一期工程，请等它完成后再运行。') from exc
        yield


async def produce(project, model=None, voices=None, align_model='small'):
    project = Path(project).resolve()
    cache = project / 'voice-cache'
    cache.mkdir(exist_ok=True)
    with project_lock(cache/'writer.lock'):
        await build(project, cache, model, voices, align_model)


async def build(project, cache, model, voices, align_model):
    narration = project / 'public/narration.wav'
    config = json.loads((project / 'brand.json').read_text())
    rows = json.loads((project / 'script.json').read_text())
    if not isinstance(rows, list) or not rows:
        raise ValueError('script.json must be a nonempty scene array')
    if any(r.get('speaker') not in {'M', 'F'} or not r.get('text', '').strip() for r in rows):
        raise ValueError('Each scene needs text and speaker M/F')
    episode = json.loads((project / 'src/episode.json').read_text())
    fps = episode.get('fps', 30)
    cursor, scenes, listing, srt = 0, [], [], []
    local = None
    with tempfile.TemporaryDirectory(dir=cache) as temp:
        stage = Path(temp)
        for i, row in enumerate(rows):
            provider, choice = voice_choice(row, config)
            display = row['text']
            text = pronunciation_text(row.get('ttsText', display), config)
            timings = None
            if row.get('audioFile'):
                take = (project / row['audioFile']).resolve()
                if take == narration.resolve():
                    raise ValueError('public/narration.wav 是合成输出。请先复制原始录音到 recordings/ 再作为 audioFile 使用。')
                if not take.is_relative_to(project) or not take.is_file():
                    raise ValueError('audioFile 必须是本期工程中的录音')
                if 'captionCues' not in row:
                    raise ValueError('导入录音请同时提供已核对的 captionCues')
            elif provider == 'kokoro':
                if local is None:
                    local = LocalNarrator(model, voices, align_model)
                speed = float(row.get('speed', choice['speed']))
                key = voice_key(text, choice['id'], speed, ['kokoro-v1', local.model_key])
                take = cache / f'{key}.wav'
                if not take.is_file():
                    local.speak(text, choice, speed, stage/'new.wav')
                    (stage/'new.wav').replace(take)
                if 'captionCues' not in row:
                    align_key = voice_key(key, display, str(align_model), 'acoustic-align-v1')
                    meta = cache / f'{align_key}.json'
                    if not meta.exists():
                        timings = local.align(take, display)
                        (stage/'new.json').write_text(json.dumps(timings, ensure_ascii=False))
                        (stage/'new.json').replace(meta)
                    else:
                        timings = json.loads(meta.read_text())
            else:
                rate = row.get('rate', config['voices']['hook_rate'] if row.get('kind') == 'hook' else choice['rate'])
                key = voice_key(text, choice['id'], rate, choice['pitch'])
                take, meta = cache / f'{key}.mp3', cache / f'{key}.json'
                if not (take.exists() and take.stat().st_size and meta.exists()):
                    await edge_take(text, choice, rate, stage/'new.mp3', stage/'new.json')
                    (stage/'new.mp3').replace(take)
                    (stage/'new.json').replace(meta)
                timings = json.loads(meta.read_text())

            raw = stage/'turn.wav'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(take), '-ar', '48000',
                            '-ac', '1', '-c:a', 'pcm_s16le', str(raw)], check=True)
            voiced, duration_ms = activity(raw)
            if 'captionCues' in row:
                caps = manual_caps(row['captionCues'], display, duration_ms)
            else:
                spoken = display if provider == 'kokoro' else text
                if len(normalized(spoken)) != len(normalized(display)):
                    raise ValueError('变长 Edge 读音覆盖请提供 captionCues，保留正确的屏显原文')
                caps = pages(timings, display, config['captions']['max_chars'], spoken_source=spoken)
                try:
                    caps = manual_caps(caps, display, duration_ms)
                except ValueError as exc:
                    raise ValueError(f"第 {i+1} 轮自动时间码或文字不完整。"
                                     "请试听该轮并填写 captionCues 后重试。") from exc
            gap = reaction_gap(row, rows[i+1] if i+1 < len(rows) else None)
            # gapAfterMs is the audible reaction gap. Keep natural decay and
            # account for silence the synthesizer already put at the end.
            frames = math.ceil(max(duration_ms, voiced[-1][1] + gap) * fps / 1000)
            part = stage / f'part-{i:04d}.wav'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', 'apad',
                            '-t', str(frames/fps), str(part)], check=True)
            listing.append(f"file '{part.name}'")
            for cap in caps:
                srt.append(f"{len(srt)+1}\n{stamp(cursor/fps*1000+cap['startMs'])} --> {stamp(cursor/fps*1000+cap['endMs'])}\n{cap['text']}\n")
            scenes.append(dict(row, sceneId=row.get('sceneId', f'scene-{i:03}'), start=cursor,
                               frames=frames, caps=caps, voicedMs=voiced))
            cursor += frames
            print(f'Voice {i+1}/{len(rows)}', flush=True)
        listing_path = stage/'concat.txt'
        listing_path.write_text('\n'.join(listing) + '\n')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i',
                        str(listing_path), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar',
                        '48000', str(stage/'narration.wav')], check=True)
        episode.update(scenes=scenes, audio='narration.wav', sound='narration-generated')
        (stage/'episode.json').write_text(json.dumps(episode, ensure_ascii=False, indent=2) + '\n')
        (stage/'captions.srt').write_text('\n'.join(srt))
        (project/'outputs').mkdir(exist_ok=True)
        (stage/'narration.wav').replace(narration)
        (stage/'captions.srt').replace(project/'outputs/captions.srt')
        (stage/'episode.json').replace(project/'src/episode.json')
    print(f'{cursor} frames / {cursor/fps:.2f} seconds')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--kokoro-model', default=os.environ.get('KOKORO_MODEL'))
    parser.add_argument('--kokoro-voices', default=os.environ.get('KOKORO_VOICES'))
    parser.add_argument('--align-model', default=os.environ.get('WHISPER_ALIGN_MODEL', 'small'))
    args = parser.parse_args()
    asyncio.run(produce(args.project, args.kokoro_model, args.kokoro_voices, args.align_model))
