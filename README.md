## Description
This adds a plugin for pocketsphinx, this is the fallback mycroft wake word 
engine and is supported out of the box by core, however I have some issues 
with the official implementation that I try to solve with this

- does not require setting phonemes, this plugin will [guess them automatically](https://github.com/OpenJarbas/phoneme_guesser)
- allow setting your own acoustic model, mycroft-core only bundles the english model
  - to change language you need to modify mycroft-core
  - core wont take PRs for new language models
  - by default this package uses english model from speech_recognition package, which is a requirement of mycroft-core 
  - mycroft-core bundles it's own model which is unnecessary
- allow overriding recording of wake words time, this is derived from number of phonemes and sometimes inadequate
  
The "plugins" are pip install-able modules that provide new engines for mycroft

more info in the [docs](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/plugins)

## Install

`pip install ovos-ww-plugin-pocketsphinx`

Configure your wake word in mycroft.conf

```json
 "listener": {
      "wake_word": "andromeda"
 },
 "hotwords": {
    "andromeda": {
        "module": "ovos-ww-plugin-pocketsphinx",
        "threshold": 1e-45
    }
  }
 
```

Advanced configuration

You can get acoustic models from [sourceforge](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/)

NOTE: it might be useful to use an acoustic model from a language that is
not your own and set phonemes manually, eg, spanish model works just fine
for portuguese

```json
 "listener": {
      "wake_word": "dinossauro"
 },
 "hotwords": {
    "dinossauro": {
        "module": "ovos-ww-plugin-pocketsphinx",
        "threshold": 1e-20,
        "phonemes": "d i n o s a u r o",
        "hmm": "/path/to/sourceforge/es-es/hmm/",
        "expected_duration": 2
    }
  }
 
```

- `threshold` defaults to 1e-30, there is no good default value and this is
  arbitrary, to increase the sensitivity, reduce the threshold. The
  threshold is usually given in scientific notation.
- `hmm` path to your own [acoustic model](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/)
  - you might need to change `lang` if using your own model
  - you might need to set `phonemes` manually if using un[supported languages](https://github.com/OpenJarbas/phoneme_guesser/tree/master/phoneme_guesser/res)
- `lang` override language, by default the global lang set in mycroft.conf is used
  - this value is used to [guess phonemes](https://github.com/OpenJarbas/phoneme_guesser)
  - if `lang` is not english, you need to set `hmm` because no model will be loaded
  - if `phonemes` is not set and `lang` is unsupported, an exception will be raised
- `phonemes` the phonemes corresponding to the wake word. If your wake word 
  phrase is more than one word, remember to include a period (.) between 
  words. 
  - this plugin uses the [phoneme_guesser](https://github.com/OpenJarbas/phoneme_guesser) package to set phonemes
  - most of the time you only need to set the phonemes to improve accuracy, especially for out of vocabulary words (not present in [the .dict files](https://github.com/OpenJarbas/phoneme_guesser/tree/master/phoneme_guesser/res))
  - the number of words in keyword (split by " ") must match the number of words in phonemes (split by ".")
  - lookup phonemes by inspecting [the .dict files](https://github.com/OpenJarbas/phoneme_guesser/tree/master/phoneme_guesser/res) for similar words
  - phonemes depend on [acoustic model](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/) used, there are several [Notational Systems](https://en.wikipedia.org/wiki/Phonetic_transcription#Notational_systems)

- `expected_duration` defaults to 3 seconds (max value), this is the time 
  used for [saving wake word samples](https://github.com/MycroftAI/mycroft-core/blob/4c84f66e15a361d9f3d650def1ba97fa80506456/mycroft/configuration/mycroft.conf#L160)