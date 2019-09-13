import re
import os
import signal
import sys
import time

from options import N, CONSONANTS, VOWELS, PARALLEL
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
children = []

parent_pid = os.getpid()

os.setpgrp()

for i in xrange(PARALLEL):
    pid = os.fork()
    if pid:
        children.append(pid)
    else:
        state = State(ALL_WORDS, i)
        found = state.fill()
        print found
        print state
        os.killpg(parent_pid, signal.SIGTERM)

while True:
    time.sleep(1)
