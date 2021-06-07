#!/usr/bin/env python3
from setuptools import setup


PLUGIN_ENTRY_POINT = \
    'ovos_ww_pocketsphinx=ovos_wake_word_plugin_pocketsphinx:PocketsphinxHotWordPlugin'
setup(
    name='ovos-wake-word-plugin-pocketsphinx',
    version='0.3.2',
    description='A wake word plugin for OpenVoiceOS',
    url='https://github.com/OpenVoiceOS/ovos-wakeword-plugin-pocketsphinx',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=['ovos_wake_word_plugin_pocketsphinx'],
    install_requires=["pocketsphinx", "phoneme_guesser",
                      "ovos-plugin-manager>=0.0.1a3"],
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mycroft plugin wake word',
    entry_points={'mycroft.plugin.wake_word': PLUGIN_ENTRY_POINT}
)
