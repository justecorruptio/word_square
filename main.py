import re
import os
import signal
import sys
import time

from multiprocessing import Lock

from options import N, CONSONANTS, VOWELS, PARALLEL
from logic import State


def load_words():
    #fh = open('twl2018.txt', 'r')
    fh = open('nwl2020.txt', 'r')
    #fh = open('sowpods.txt', 'r')
    #fh = open('scowl69.txt', 'r')
    #fh = open('gngram69.txt', 'r')
    #fh = open('test.txt', 'r')

    words = []
    for line in fh:
        word = line.strip().upper()
        if len(word) != N:
            continue

        '''
        if re.search(r'[QZXJKYFWV]', word):
        #if re.search(r'[QZXJ]', word):
            continue
        '''

        '''
        if not re.match(r"""
            ^{C}{V}{C}{V}{C}{V}{C}{V} |
            ^{V}{C}{V}{C}{V}{C}{V}{C}
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

print_lock = Lock()

for i in xrange(PARALLEL):
    pid = os.fork()
    if pid:
        children.append(pid)
    else:
        state = State(ALL_WORDS, i, print_lock=print_lock)
        found = state.fill()
        if found:
            print found
            print state
            os.killpg(parent_pid, signal.SIGTERM)
        else:
            os.kill(parent_pid, signal.SIGUSR1)
            sys.exit()

children_reported = 0
def signal_handler(signum, frame):
    global children_reported
    children_reported += 1
    if children_reported == PARALLEL:
        print "NO SOLUTION!"
        sys.exit()

signal.signal(signal.SIGUSR1, signal_handler)

while True:
    time.sleep(1)
