import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from caption_rules import clean_caption, clean_srt, clean_timeline
from prepare_voice import pages, voice_key, pronunciation_text, require_edge_voices
from new_episode import create
from audit_episode import audit
from register_asset import register


class Captions(unittest.TestCase):
    def test_numeric_and_language_semantics(self):
        for raw, wanted in json.loads((ROOT / 'tests/caption_cases.json').read_text()):
            with self.subTest(raw=raw):
                self.assertEqual(clean_caption(raw), wanted)

    def test_srt_timings_preserved(self):
        text='1\n00:00:01,200 --> 00:00:03,400\n车价29,990美元，月费呢？\n'
        cleaned=clean_srt(text)
        self.assertIn('00:00:01,200 --> 00:00:03,400', cleaned)
        self.assertIn('车价29990美元月费呢？', cleaned)

    def test_narration_not_cleaned(self):
        data={'scenes':[{'text':'等等，真的吗？','caps':[{'text':'等等，真的吗？'}]}]}
        clean_timeline(data)
        self.assertEqual(data['scenes'][0]['text'], '等等，真的吗？')
        self.assertEqual(data['scenes'][0]['caps'][0]['text'], '等等真的吗？')

    def test_real_word_timing_and_question(self):
        result=pages([{'text':'真的','startMs':100,'endMs':400},{'text':'吗','startMs':400,'endMs':700}], '真的吗？')
        self.assertEqual(result,[{'text':'真的吗？','startMs':100,'endMs':700}])

    def test_pronunciation_keeps_written_caption_and_word_times(self):
        config={'pronunciation':{'same_length_substitutions':{'行情':'航情'}}}
        self.assertEqual(pronunciation_text('今天的行情。', config), '今天的航情。')
        for words in [
            [{'text':'航情','startMs':100,'endMs':500}],
            [{'text':'航','startMs':100,'endMs':300},{'text':'情','startMs':300,'endMs':500}],
        ]:
            self.assertEqual(pages(words, '行情。', spoken_source='航情。'),
                             [{'text':'行情','startMs':100,'endMs':500}])
        with self.assertRaises(ValueError):
            pronunciation_text('行情', {'pronunciation':{'same_length_substitutions':{'行情':'háng qíng'}}})

    def test_kokoro_is_not_sent_to_edge_or_silently_substituted(self):
        config={'voices':{'male':{'provider':'kokoro','id':'zm_yunxi'}}}
        with self.assertRaisesRegex(RuntimeError, 'zm_yunxi'):
            require_edge_voices([{'speaker':'M'}],config)
        require_edge_voices([{'speaker':'M'}], {'voices':{'male':{'id':'legacy-edge'}}})

    def test_voice_cache_invalidates_configuration(self):
        keys={voice_key('同一句话',v,r,p) for v,r,p in [('male','+8%','+0Hz'),('female','+8%','+0Hz'),('male','+5%','+0Hz'),('male','+8%','+2Hz')]}
        self.assertEqual(len(keys),4)


class PortableEpisode(unittest.TestCase):
    def test_new_project_and_no_overwrite(self):
        with tempfile.TemporaryDirectory(prefix='brother pan ') as temp:
            out=Path(temp)/'中文 episode'
            create(out)
            self.assertTrue((out/'public/front-poses.png').is_file())
            self.assertTrue((out/'src/library/vector/chips.tsx').is_file())
            self.assertTrue((out/'package-lock.json').is_file())
            self.assertTrue(audit(out)['ok'])
            with self.assertRaises(ValueError):
                create(out)

    def test_detect_separated_photo_even_under_different_id(self):
        with tempfile.TemporaryDirectory() as temp:
            out=create(Path(temp)/'episode')
            (out/'public/photo-a.png').write_bytes(b'same-photo')
            (out/'public/photo-b.png').write_bytes(b'same-photo')
            (out/'asset-manifest.json').write_text(json.dumps([{'id':'a','path':'public/photo-a.png','kind':'photo'},{'id':'b','path':'public/photo-b.png','kind':'photo'}]))
            path=out/'src/episode.json';data=json.loads(path.read_text())
            data['scenes'][0]['assets']=['a'];data['scenes'][2]['assets']=['b']
            path.write_text(json.dumps(data))
            self.assertIn('same photo/video has multiple separated intervals',audit(out)['errors'])

    def test_discontinuous_time_and_unverified_claim(self):
        with tempfile.TemporaryDirectory() as temp:
            out=create(Path(temp)/'episode');path=out/'src/episode.json';data=json.loads(path.read_text())
            data['scenes'][1]['start']+=1;data['scenes'][2]['factual']=True
            path.write_text(json.dumps(data));errors=audit(out)['errors']
            self.assertTrue(any('discontinuous' in s for s in errors))
            self.assertTrue(any('source' in s for s in errors))

    def test_unknown_scene_is_not_a_successful_default_duo(self):
        with tempfile.TemporaryDirectory() as temp:
            out=create(Path(temp)/'episode');path=out/'src/episode.json';data=json.loads(path.read_text())
            data['scenes'][2]['kind']='new-mechanism-not-implemented'
            path.write_text(json.dumps(data))
            self.assertTrue(any('unimplemented' in s for s in audit(out)['errors']))

    def test_empty_episode_and_bad_fps_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            out=create(Path(temp)/'episode');path=out/'src/episode.json';data=json.loads(path.read_text())
            data['scenes']=[];path.write_text(json.dumps(data))
            self.assertFalse(audit(out)['ok'])
            data['fps']=0;path.write_text(json.dumps(data))
            self.assertFalse(audit(out)['ok'])

    def test_asset_deduplication(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'assets').mkdir();(root/'assets/registry.json').write_text('{"assets":[]}')
            (root/'assets/a.png').write_bytes(b'illustration');(root/'assets/b.png').write_bytes(b'illustration')
            register(Path('assets/a.png'),'a','illustration',[],'original-generated',root=root)
            with self.assertRaises(ValueError):
                register(Path('assets/b.png'),'b','illustration',[],'original-generated',root=root)


if __name__=='__main__':
    unittest.main()
