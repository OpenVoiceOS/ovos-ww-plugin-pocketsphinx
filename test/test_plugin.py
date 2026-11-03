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
        # deterministic: with no usable G2P guess, out-of-dictionary raises
        from unittest import mock
        with mock.patch("ovos_ww_plugin_pocketsphinx.guess_phonemes",
                        return_value=None):
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


class TestOptionalG2P(unittest.TestCase):
    """The g2p extra (orthography2ipa + scriptconv) guesses phonemes for
    out-of-dictionary words; unmapped symbols degrade to the explicit-config
    error instead of loading a broken pronunciation."""

    def test_guess_produces_valid_phones(self):
        from ovos_ww_plugin_pocketsphinx import guess_phonemes, \
            dictionary_phoneset
        from pocketsphinx import get_model_path
        from os.path import join
        guessed = guess_phonemes("banana", "en-us")
        self.assertIsInstance(guessed, str)
        inventory = dictionary_phoneset(
            join(get_model_path(), "en-us", "cmudict-en-us.dict"))
        for phone in guessed.split():
            if phone != ".":
                self.assertIn(phone, inventory)

    def test_unmappable_word_returns_none_not_garbage(self):
        from ovos_ww_plugin_pocketsphinx import guess_phonemes
        guessed = guess_phonemes("mycroft", "en-us")
        self.assertTrue(guessed is None or "?" not in guessed)

    def test_guess_takes_the_engine_pronunciation(self):
        # the bundled cmudict is an independent gold for these regular words
        from ovos_ww_plugin_pocketsphinx import guess_phonemes
        from pocketsphinx import get_model_path
        from os.path import join
        gold = {}
        with open(join(get_model_path(), "en-us", "cmudict-en-us.dict"),
                  encoding="utf-8") as f:
            for line in f:
                word, *phones = line.split()
                gold.setdefault(word, " ".join(phones))
        for word in ("cat", "cup", "sit", "stop"):
            self.assertEqual(guess_phonemes(word, "en-us"), gold[word])
        self.assertEqual(guess_phonemes("cup stop", "en-us"),
                         f"{gold['cup']} . {gold['stop']}")


def to_arpa(ipa):
    """ARPAbet for *ipa*, through scriptconv and the plugin's alias table."""
    from scriptconv import ipa_to_arpa
    from ovos_ww_plugin_pocketsphinx import ARPA_ALIASES
    ipa = "".join(ch for ch in ipa if ch not in "\u02c8\u02cc\u02d0.")
    return " ".join(ARPA_ALIASES.get(ph, ph) for ph in ipa_to_arpa(ipa).split())


def lexicon_arpa(word):
    """ARPAbet for the IPA that the packaged en-GB TSV file lists for *word*.

    The IPA comes from the o2i-lexicons data file, not from engine output.
    """
    from o2i_lexicons import DATA_DIR
    for path in sorted((DATA_DIR / "en-GB").glob("*.tsv")):
        for line in path.read_text(encoding="utf-8").splitlines():
            entry, _, ipa = line.partition("\t")
            if entry == word:
                return to_arpa(ipa)
    raise LookupError(f"{word!r} is not in the packaged en-GB lexicon")


class TestPackagedLexicons(unittest.TestCase):
    """The packaged_lexicons key (default on) enables o2i-lexicons for the
    language the guess transcribes. orthography2ipa keeps lexicons
    process-wide, so every test starts and ends with clear_lexicons()."""

    def setUp(self):
        import orthography2ipa
        orthography2ipa.clear_lexicons()

    tearDown = setUp

    def test_guess_uses_the_packaged_lexicon(self):
        from ovos_ww_plugin_pocketsphinx import guess_phonemes
        expected = lexicon_arpa("yacht")
        self.assertEqual(expected, "Y AA T")  # the bundled cmudict entry
        self.assertEqual(guess_phonemes("yacht", "en-us"), expected)

    def test_off_equals_plain_orthography2ipa(self):
        import orthography2ipa
        from ovos_ww_plugin_pocketsphinx import guess_phonemes
        off = guess_phonemes("yacht", "en-us", packaged_lexicons=False)
        self.assertEqual(orthography2ipa.available_lexicon_codes(), [])
        plain = to_arpa(orthography2ipa.G2P("en").transcribe("yacht"))
        self.assertEqual(off, plain)
        self.assertNotEqual(off, lexicon_arpa("yacht"))

    def test_plugin_enables_the_lexicon_by_default(self):
        # "abaci" is not in the bundled cmudict, so the plugin guesses it
        p = PocketsphinxHotWordPlugin("abaci", {})
        self.assertEqual(p.phonemes, lexicon_arpa("abaci"))

    def test_plugin_config_turns_the_lexicon_off(self):
        import orthography2ipa
        p = PocketsphinxHotWordPlugin("abaci", {"packaged_lexicons": False})
        self.assertEqual(orthography2ipa.available_lexicon_codes(), [])
        plain = to_arpa(orthography2ipa.G2P("en").transcribe("abaci"))
        self.assertEqual(p.phonemes, plain)
        self.assertNotEqual(p.phonemes, lexicon_arpa("abaci"))
