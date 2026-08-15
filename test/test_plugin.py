"""Live detection tests against CMU's reference recording (goforward.raw,
16kHz 16-bit mono, a human saying "go forward ten meters")."""
import unittest
from os.path import dirname, join

from ovos_ww_plugin_pocketsphinx import PocketsphinxHotWordPlugin

AUDIO = join(dirname(__file__), "goforward.raw")


class TestDetection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(AUDIO, "rb") as f:
            cls.frames = f.read()

    def test_detects_spoken_keyphrase(self):
        p = PocketsphinxHotWordPlugin(
            "go forward", {"phonemes": "G OW . F AO R W ER D"})
        self.assertTrue(p.found_wake_word(self.frames))

    def test_rejects_other_keyphrase(self):
        p = PocketsphinxHotWordPlugin(
            "hey mycroft", {"phonemes": "HH EY . M AY K R AO F T"})
        self.assertFalse(p.found_wake_word(self.frames))

    def test_dictionary_default_no_phonemes_config(self):
        # "go" and "forward" are in the bundled cmudict, so no phonemes
        # config is needed and detection still works on the reference audio
        p = PocketsphinxHotWordPlugin("go forward", {})
        self.assertIsNone(p.phonemes)
        self.assertTrue(p.found_wake_word(self.frames))
        self.assertFalse(p.found_wake_word(b"\x00" * 32000))

    def test_out_of_dictionary_word_requires_phonemes(self):
        with self.assertRaises(ValueError):
            PocketsphinxHotWordPlugin("hey zorblefax", {})

    def test_builtin_hey_mycroft_needs_no_config(self):
        p = PocketsphinxHotWordPlugin("hey mycroft", {})
        self.assertEqual(p.phonemes, "HH EY . M AY K R AO F T")
        self.assertFalse(p.found_wake_word(self.frames))

    def test_missing_words_helper(self):
        from pocketsphinx import get_model_path
        from os.path import join
        d = join(get_model_path(), "en-us", "cmudict-en-us.dict")
        self.assertEqual(
            PocketsphinxHotWordPlugin.missing_words(d, "go forward"), [])
        self.assertEqual(
            PocketsphinxHotWordPlugin.missing_words(d, "hey mycroft"),
            ["mycroft"])


if __name__ == "__main__":
    unittest.main()
