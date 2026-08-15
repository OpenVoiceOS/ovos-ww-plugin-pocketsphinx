import unittest

from phoneme_guesser import get_phonemes


class TestPhonemes(unittest.TestCase):
    def test_guess_phonemes(self):
        self.assertEqual(get_phonemes("hey mycroft", "en-us"),
                         "HH EH Y . M Y K R OW F T")
