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

    def test_phoneme_guesser_default(self):
        p = PocketsphinxHotWordPlugin("go forward", {})
        self.assertIsInstance(p.phonemes, str)
        self.assertFalse(p.found_wake_word(b"\x00" * 32000))


if __name__ == "__main__":
    unittest.main()
