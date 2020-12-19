## Description
This adds a plugin for pocketsphinx, this is the fallback mycroft wake word 
engine and is supported out of the box by core, however I have some issues 
with the official implementation that I try to solve with this

- does not require setting phonemes, this plugin will guess them automatically (for english only)
- allow setting your own HMM model, mycroft-core only bundles the english model
  - to change language you need to modify core
  - core wont take PRs for new language models
  - by default this package uses english model from speech_recognition package, which is a requirement of mycroft-core 
  - core bundles it's own model which is unnecessary
- allow overriding recording of wake words time, this is derived from phonemes and sometimes inadequate
  
The "plugins" are pip install-able modules that provide new engines for mycroft

more info in the [docs](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/plugins)

## Install

`mycroft-pip install jarbas-wake-word-plugin-pocketsphinx`

Configure your wake word in mycroft.conf

```json
 "listener": {
      "wake_word": "andromeda"
 },
 "hotwords": {
    "andromeda": {
        "module": "jarbas_pocketsphinx_ww_plug",
        "threshold": 1e-45
    }
  }
 
```

Advanced configuration

You can get acoustic models from [sourceforge](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/)

```json
 "listener": {
      "wake_word": "dinosaur"
 },
 "hotwords": {
    "dinosaur": {
        "module": "jarbas_pocketsphinx_ww_plug",
        "threshold": 1e-20,
        "phonemes": "d i n o s a u r i o",
        "hmm": "/path/to/sourceforge/es-es/hmm/",
        "expected_duration": 2
    }
  }
 
```


- `hmm` if you want to use your own acoustic model, usually to account for 
  phonemes from other languages, expects full path to hmm folder
- `threshold` defaults to 1e-30, there is no good default value and this is 
  arbitrary, To increase the sensitivity, reduce the Threshold. The 
  Threshold is usually given in scientific notation.
- `phonemes` The phonemes corresponding to the Wake Word. If your Wake Word 
  phrase is more than one word, remember to include a period (.) between 
  words. NOTE: the number of words in keyword (split by " ") must match the 
  number of words in phonemes (split by ".")
- `expected_duration` defaults to 3 seconds (max value), this is the time 
  used for [saving wake word samples](https://github.com/MycroftAI/mycroft-core/blob/4c84f66e15a361d9f3d650def1ba97fa80506456/mycroft/configuration/mycroft.conf#L160)