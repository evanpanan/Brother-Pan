"""Synthesize a whole Mandarin turn locally and timestamp its written transcript."""
import hashlib
import re
import subprocess
from difflib import SequenceMatcher
from functools import cached_property
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


class LocalNarrator:
    def __init__(self, model, voices, align_model):
        self.files = [Path(p).expanduser() if p else None for p in (model, voices)]
        for path, option in zip(self.files, ('--kokoro-model', '--kokoro-voices')):
            if path is None or not path.is_file():
                raise ValueError(f'请用 {option} 指定已下载的 Kokoro v1.0 文件。见 references/voice-setup.md')
        self.align_model = align_model
        self.model_key = [digest(p) for p in self.files]

    @cached_property
    def kokoro(self):
        from kokoro_onnx import Kokoro
        return Kokoro(*(str(p) for p in self.files))

    @cached_property
    def mandarin(self):
        from misaki.zh import ZHG2P
        return ZHG2P()

    def speak(self, text, choice, speed, out):
        import soundfile
        # v1.0's Chinese frontend passes Latin script through. Phonemize it
        # with the same engine's English frontend before joining the full turn.
        phrases = re.split(r"([A-Za-z]+(?:[ '-][A-Za-z]+)*)", text)
        sounds = [self.kokoro.tokenizer.phonemize(s, 'en-us') if i % 2 else self.mandarin(s)[0]
                  for i, s in enumerate(phrases) if s.strip()]
        samples, rate = self.kokoro.create(' '.join(sounds), voice=choice['id'],
                                           speed=speed, is_phonemes=True)
        soundfile.write(str(out), samples, rate, format='WAV', subtype='PCM_16')

    @cached_property
    def aligner(self):
        from faster_whisper import WhisperModel
        try:
            return WhisperModel(self.align_model, device='cpu', compute_type='int8',
                                cpu_threads=4, local_files_only=True)
        except (OSError, ValueError) as exc:
            raise ValueError('找不到本地字幕对齐模型。请按 references/voice-setup.md 下载，'
                             '或用 --align-model 指向完整目录。') from exc

    def align(self, wav, display):
        import numpy as np
        from faster_whisper.tokenizer import Tokenizer
        model = self.aligner
        tokenizer = Tokenizer(model.hf_tokenizer, model.model.is_multilingual,
                              language='zh', task='transcribe')
        pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(wav),
                                       '-ar', '16000', '-ac', '1', '-f', 'f32le', '-'])
        samples = np.frombuffer(pcm, dtype='<f4')
        return self._align_window(samples, display, tokenizer, 0)

    def _align_window(self, audio, text, tokenizer, offset):
        """Split only alignment windows; never split/re-synthesize the audible turn."""
        from faster_whisper.audio import pad_or_trim
        model = self.aligner
        tokens = tokenizer.encode(text)
        if len(audio) > 29 * 16000 or len(tokens) + 8 > model.max_length:
            mid_char, mid_sample = self._find_split(audio, text)
            return (self._align_window(audio[:mid_sample], text[:mid_char], tokenizer, offset)
                    + self._align_window(audio[mid_sample:], text[mid_char:], tokenizer,
                                         offset + mid_sample / 16))
        mel = model.feature_extractor(audio)
        words = model.find_alignment(tokenizer, [tokens], model.encode(pad_or_trim(mel)),
                                     mel.shape[-1])[0]
        duration = len(audio) / 16
        return [dict(text=w['word'], startMs=offset + min(w['start'] * 1000, duration),
                     endMs=offset + min(w['end'] * 1000, duration)) for w in words]

    def _find_split(self, audio, text):
        """Use a recognized mid-turn phrase to locate the next acoustic window."""
        segments, _ = self.aligner.transcribe(audio, language='zh', word_timestamps=True,
                                              beam_size=3, vad_filter=False)
        transcript, starts = [], []
        for segment in segments:
            for word in segment.words or []:
                chars = [c.casefold() for c in word.word if c.isalnum()]
                for i, c in enumerate(chars):
                    transcript.append(c)
                    starts.append(word.start + (word.end - word.start) * i / len(chars))
        positions = [i for i, c in enumerate(text) if c.isalnum()]
        expected = ''.join(text[i].casefold() for i in positions)
        match = SequenceMatcher(None, expected, ''.join(transcript), autojunk=False)
        middle = len(audio) / 32000
        candidates = []
        for block in match.get_matching_blocks():
            if block.size < 3:
                continue
            for i in range(1, block.size - 1):
                s = starts[block.b + i]
                if middle * .4 < s < middle * 1.6:
                    candidates.append((abs(s - middle), positions[block.a + i], round(s * 16000)))
        if not candidates:
            raise ValueError('长轮次没有找到可靠的语音边界。请试听，并在该轮填写 captionCues。')
        _, char, sample = min(candidates)
        return char, sample
