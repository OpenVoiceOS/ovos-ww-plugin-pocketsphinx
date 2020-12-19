import re


def msec_to_sec(msecs):
    """Convert milliseconds to seconds.

    Arguments:
        msecs: milliseconds

    Returns:
        int: input converted from milliseconds to seconds
    """
    return msecs / 1000


def clean_word(word, replacement=" "):
    clean = re.sub('[^a-zA-Z0-9 \n\.]', replacement, word)
    return clean


def guess_phonemes(word):
    word = clean_word(word).lower()
    basic_pronunciations = {'a': ['AE'], 'b': ['B'], 'c': ['K'],
                            'd': ['D'],
                            'e': ['EH'], 'f': ['F'], 'g': ['G'],
                            'h': ['HH'],
                            'i': ['IH'],
                            'j': ['JH'], 'k': ['K'], 'l': ['L'],
                            'm': ['M'],
                            'n': ['N'], 'o': ['OW'], 'p': ['P'],
                            'qu': ['K', 'W'], 'r': ['R'],
                            's': ['S'], 't': ['T'], 'u': ['AH'],
                            'v': ['V'],
                            'w': ['W'], 'x': ['K', 'S'], 'y': ['Y'],
                            'z': ['Z'], 'ch': ['CH'],
                            'sh': ['SH'], 'th': ['TH'], 'dg': ['JH'],
                            'dge': ['JH'], 'psy': ['S', 'AY'],
                            'oi': ['OY'],
                            'ee': ['IY'],
                            'ao': ['AW'], 'ck': ['K'], 'tt': ['T'],
                            'nn': ['N'], 'ai': ['EY'], 'eu': ['Y', 'UW'],
                            'ue': ['UW'],
                            'ie': ['IY'], 'ei': ['IY'], 'ea': ['IY'],
                            'ght': ['T'], 'ph': ['F'], 'gn': ['N'],
                            'kn': ['N'], 'wh': ['W'],
                            'wr': ['R'], 'gg': ['G'], 'ff': ['F'],
                            'oo': ['UW'], 'ua': ['W', 'AO'], 'ng': ['NG'],
                            'bb': ['B'],
                            'tch': ['CH'], 'rr': ['R'], 'dd': ['D'],
                            'cc': ['K', 'S'], 'oe': ['OW'],
                            'igh': ['AY'], 'eigh': ['EY']}
    phones = []

    progress = len(word) - 1
    while progress >= 0:
        if word[0:3] in basic_pronunciations.keys():
            for phone in basic_pronunciations[word[0:3]]:
                phones.append(phone)
            word = word[3:]
            progress -= 3
        elif word[0:2] in basic_pronunciations.keys():
            for phone in basic_pronunciations[word[0:2]]:
                phones.append(phone)
            word = word[2:]
            progress -= 2
        elif word[0] in basic_pronunciations.keys():
            for phone in basic_pronunciations[word[0]]:
                phones.append(phone)
            word = word[1:]
            progress -= 1
        else:
            return None
    return phones


def get_phonemes(word):
    word = clean_word(word).lower()
    phonemes = None
    if " " in word:
        total_phonemes = []
        names = word.split(" ")
        for word in names:
            phon = get_phonemes(word)
            if phon is None:
                return None
            total_phonemes.extend(phon)
            total_phonemes.append(" . ")
        if total_phonemes[-1] == " . ":
            total_phonemes = total_phonemes[:-1]
        phonemes = "".join(total_phonemes)
    else:
        guess = guess_phonemes(word)
        if guess is not None:
            phonemes = " ".join(guess)

    return phonemes
