# Pre-release quirks

Behavior changes since the last stable release, newest first. This file is
reset at each stable release.

## 0.2.1a1

- The `phoneme_guesser` dependency is gone (ancient and unmaintained). With
  no `phonemes` config, key-phrase words are now validated against a real
  pronunciation dictionary — the `dict` config path, defaulting to the
  cmudict bundled with the English model — instead of grapheme guessing.
  A key phrase with a word missing from the dictionary raises `ValueError`
  at load, telling the user to set `phonemes`. "hey mycroft" carries a
  built-in pronunciation and keeps working with no configuration.

## 0.2.0a1

- Ported to pocketsphinx 5: the ancient `pocketsphinx~=0.1` SWIG bindings do
  not build on current Python; the plugin now uses the maintained
  `pocketsphinx>=5.0.0` wheel/sdist (verified on Python 3.12, 3.13 and 3.14)
  and its bundled en-US acoustic model. The `SpeechRecognition` dependency is
  gone — it was only used to borrow that model.
- Packaging is pyproject-only (setup.py and requirements/ removed); the
  entry point id is unchanged.
- Constructor follows the current ovos-plugin-manager `HotWordEngine`
  template (`key_phrase, config`); `lang` is still accepted as a kwarg and
  can also be set in the plugin config.
