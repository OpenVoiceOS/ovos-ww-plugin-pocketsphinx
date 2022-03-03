# write your first unittest!
import unittest
from ovos_ww_plugin_pocketsphinx import PocketsphinxHotWordPlugin


class TestPhonemes(unittest.TestCase):
    def test_guess_phonemes(self):
        self.assertEqual(PocketsphinxHotWordPlugin.get_phonemes("hey mycroft"),
                         ['HH', 'EH', 'Y', '.', 'M', 'Y', 'K', 'R', 'OW', 'F', 'T'])
        self.assertEqual(PocketsphinxHotWordPlugin.get_phonemes("hey neon"),
                         ['HH', 'EH', 'Y', '.', 'N', 'EH', 'OW', 'N'])
        self.assertEqual(PocketsphinxHotWordPlugin.get_phonemes("hey siri"),
                         ['HH', 'EH', 'Y', '.',  'S', 'IH', 'R', 'IH'])
        self.assertEqual(PocketsphinxHotWordPlugin.get_phonemes("hey firefox"),
                         ['HH', 'EH', 'Y', '.', 'F', 'IH', 'R', 'EH', 'F', 'OW', 'K', 'S'])
        self.assertEqual(PocketsphinxHotWordPlugin.get_phonemes("ok google"),
                         ['OW', 'K', '.', 'G', 'UW', 'G', 'L', 'EH'])
        self.assertEqual(PocketsphinxHotWordPlugin.get_phonemes("alexa"),
                         ['AE', 'L', 'EH', 'K', 'S', 'AE'])

