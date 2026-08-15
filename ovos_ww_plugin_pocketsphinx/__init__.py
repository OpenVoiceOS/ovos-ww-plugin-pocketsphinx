# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import tempfile
from os.path import join

from ovos_plugin_manager.templates.hotwords import HotWordEngine, msec_to_sec
from ovos_utils.log import LOG
from pocketsphinx import Decoder, get_model_path


#: Pronunciations for key phrases whose words are not in the bundled
#: dictionary, so the stock OVOS wake words work with no configuration.
BUILTIN_PHONEMES = {
    "hey mycroft": "HH EY . M AY K R AO F T",
}


class PocketsphinxHotWordPlugin(HotWordEngine):
    """Wake word engine using PocketSphinx.

    PocketSphinx is very general purpose but has a somewhat high error rate.
    The key advantage is to be able to specify the wake word with phonemes.
    """

    def __init__(self, key_phrase="hey mycroft", config=None, lang="en-us"):
        super().__init__(key_phrase, config)
        self.lang = self.config.get("lang", lang).lower()

        self.hmm = self.config.get("hmm")
        if not self.hmm and self.lang.startswith("en"):
            self.hmm = self.get_default_english_model()
        elif not self.hmm:
            raise ValueError("No pocketsphinx hmm model provided")
        # TODO threshold is a bitch to automate, maybe raise exception ?
        self.threshold = self.config.get("threshold", 1e-30)

        # pronunciation: an explicit "phonemes" config builds a dedicated
        # dictionary for the key phrase; otherwise the words are looked up in
        # a real pronunciation dictionary ("dict" config, defaulting to the
        # cmudict bundled with the English model) - a word missing there
        # needs "phonemes" in config, there is no grapheme guessing
        self.phonemes = self.config.get("phonemes") or \
                        BUILTIN_PHONEMES.get(self.key_phrase)
        if self.phonemes:
            dict_name = self.create_dict(self.key_phrase, self.phonemes)
        else:
            dict_name = self.config.get("dict")
            if not dict_name and self.lang.startswith("en"):
                dict_name = join(get_model_path(), "en-us",
                                 "cmudict-en-us.dict")
            if not dict_name:
                raise ValueError(
                    "No pronunciation available: provide 'phonemes' or a "
                    "'dict' file in the hotword config")
            missing = self.missing_words(dict_name, self.key_phrase)
            if missing:
                raise ValueError(
                    f"words {missing} not in pronunciation dictionary "
                    f"{dict_name}; provide 'phonemes' in the hotword config")
        num_phonemes = (len(self.phonemes.split(" ")) if self.phonemes
                        else len(self.key_phrase.replace(" ", "")))
        phoneme_duration = msec_to_sec(
            self.config.get('phoneme_duration', 120))
        self.expected_duration = self.config.get("expected_duration") or \
                                 num_phonemes * phoneme_duration

        self.sample_rate = self.config.get("sample_rate") or 16000
        self.decoder = Decoder(hmm=self.hmm,
                               dict=dict_name,
                               keyphrase=self.key_phrase,
                               kws_threshold=float(self.threshold),
                               samprate=float(self.sample_rate),
                               nfft=2048,
                               logfn=os.devnull)
        self._in_utt = False

    @staticmethod
    def missing_words(dict_path, key_phrase):
        """Key-phrase words absent from a sphinx pronunciation dictionary."""
        words = set(key_phrase.lower().split())
        try:
            with open(dict_path, encoding="utf-8") as f:
                for line in f:
                    entry = line.split(" ", 1)[0].split("(", 1)[0].strip()
                    words.discard(entry.lower())
                    if not words:
                        break
        except OSError as e:
            LOG.error(f"could not read pronunciation dictionary: {e}")
        return sorted(words)

    @staticmethod
    def create_dict(key_phrase, phonemes):
        (fd, file_name) = tempfile.mkstemp()
        words = key_phrase.split()
        phoneme_groups = phonemes.split('.')
        with os.fdopen(fd, 'w') as f:
            for word, phoneme in zip(words, phoneme_groups):
                f.write(word + ' ' + phoneme.strip() + '\n')
        return file_name

    @staticmethod
    def get_default_english_model():
        # the bundled model ships as model/en-us/en-us (acoustic model dir
        # nested under a folder that also carries the dictionary and LMs)
        return join(get_model_path(), "en-us", "en-us")

    def update(self, chunk: bytes):
        """Stream a chunk into an open keyword-spotting utterance."""
        if not self._in_utt:
            self.decoder.start_utt()
            self._in_utt = True
        self.decoder.process_raw(chunk, False, False)

    def found_wake_word(self, frame_data=None) -> bool:
        """Streaming query when called with no arguments (the audio has been
        fed through ``update``); one-shot decode of a complete buffer when a
        legacy caller passes ``frame_data``."""
        if frame_data is not None:
            self.reset()
            self.decoder.start_utt()
            self.decoder.process_raw(frame_data, False, False)
            self.decoder.end_utt()
            hyp = self.decoder.hyp()
            return bool(hyp and self.key_phrase in hyp.hypstr.lower())
        if not self._in_utt:
            return False
        hyp = self.decoder.hyp()
        if hyp and self.key_phrase in hyp.hypstr.lower():
            self.reset()
            return True
        return False

    def reset(self):
        if self._in_utt:
            self.decoder.end_utt()
            self._in_utt = False

    def shutdown(self):
        self.reset()
