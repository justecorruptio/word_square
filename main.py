import re

from options import N, CONSONANTS, VOWELS
from logic import State


def load_words():
    fh = open('twl2018.txt', 'r')

    words = []
    for line in fh:
        word = line.strip().upper()
        if len(word) != N:
            continue

        '''
        #f re.search(r'[QZXJKYFWV]', word):
        if re.search(r'[QZXJ]', word):
            continue

        if not re.match(r"""
            ^{C}{V}{C} |
            ^{V}{C}{V}
        """.format(
            C='[' + CONSONANTS + ']',
            V='[' + VOWELS + ']',
        ), word, re.X):
            continue
        '''

        words.append(word)

    words.sort()

    return words


ALL_WORDS = load_words()

state = State(ALL_WORDS)

found = state.fill()
print found
print state
