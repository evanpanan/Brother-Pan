import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_episode import audit
from new_episode import create


class Handoff(unittest.TestCase):
    def test_voice_tail_cannot_open_the_mouth_in_the_next_turn(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = create(Path(tmp) / 'film')
            path = project / 'src/episode.json'
            timeline = json.loads(path.read_text())
            turn = timeline['scenes'][0]
            end = turn['frames'] * 1000 / timeline['fps']
            for spans, valid in (([[100, 250], [300, end]], True),
                                 ([[100, 250], [249, 300]], False),
                                 ([[100, end + 20]], False)):
                with self.subTest(spans=spans):
                    turn['voicedMs'] = spans
                    path.write_text(json.dumps(timeline))
                    self.assertEqual(audit(project)['ok'], valid)
