from options import N, LETTERS

def count_letter_pos(words):
    """How many words are used by every letter/position combo."""

    counts = [{
        c: 0 for c in LETTERS
    } for i in xrange(N)]

    for word in words:
        for i, c in enumerate(word):
            counts[i][c] += 1

    return counts


def words_by_usefulness(words):
    """Copies and sorts words by how many possible words can cross it."""

    counts = build_letter_freq(words)

    trans = []

    for word in words:
        usefulness = 1.0
        for i, c in enumerate(word):
            usefulness /= counts[c]

        trans.append((usefulness, word))

    return [w for _, w in sorted(trans)]


def build_prefix_cache(words):

    cache = {}
    for i in xrange(N + 1):
        for word in words:
            prefix = word[:i]
            cache.setdefault(prefix, []).append(word)

    return cache

def build_letter_freq(words):
    counts = { c: 0.0 for c in LETTERS }
    for word in words:
        for c in word:
            counts[c] += 1

    return counts
