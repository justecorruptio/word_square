import re

from options import N
from logic import State


def load_words():
    fh = open('twl2018.txt', 'r')

    words = []
    for line in fh:
        word = line.strip().upper()
        if len(word) != N:
            continue

        if re.search(r'[QZXJKYFWV]', word):
            continue

        words.append(word)

    words.sort()

    return words


ALL_WORDS = load_words()

state = State(ALL_WORDS)

found = state.fill()
print found
print state
