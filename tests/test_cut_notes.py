import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from cut_notes import at_time, find_line, load_srt


class CutNotes(unittest.TestCase):
    def test_cross_caption_phrase_and_a_real_pause(self):
        with tempfile.TemporaryDirectory() as tmp:
            srt = Path(tmp) / '字幕.srt'
            srt.write_bytes(('\ufeff1\r\n00:00:00,100 --> 00:00:01,900\r\n开价1.2\r\n'
                             '\r\n2\r\n00:00:02,100 --> 00:00:03,150\r\n亿美元？\r\n'
                             '\r\n3\r\n00:00:03,200 --> 00:00:04,100\r\n开价12美元\r\n').encode())
            cues = load_srt(srt)
        self.assertEqual(list(find_line(cues, '1.2 亿美元')), [cues[:2]])
        self.assertEqual(list(find_line(cues, '开价12')), [[cues[2]]])
        self.assertEqual(list(find_line(cues, '开价')), [[cues[0]], [cues[2]]])
        self.assertEqual(at_time(cues, 1900), [])
        self.assertEqual(at_time(cues, 2100), [cues[1]])
