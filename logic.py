import time
from options import N
from stats import words_by_usefulness, build_prefix_cache, build_letter_freq


class State(object):

    def __init__(self, words):
        self.rows = []
        self.cols = []
        self.used = set()

        self.step = 0
        self.percent = 0

        self.sorted_words = words_by_usefulness(words)
        self.prefix_cache = build_prefix_cache(self.sorted_words)
        self.letter_freq = build_letter_freq(self.sorted_words)

        self.good_list_cache = {}

    def __str__(self):
        mat = [['.'] * N for i in xrange(N)]
        for i, row in enumerate(self.rows):
            for j, c in enumerate(row):
                mat[i][j] = c

        for j, col in enumerate(self.cols):
            for i, c in enumerate(col):
                mat[i][j] = c

        ret = ''
        for row in mat:
            for c in row:
                ret += c + ' '
            ret += '\n'

        return ret

    def _build_good_list(self, rows, cols):
        depth = len(rows)
        prefix = ''.join(col[depth] for col in cols)

        cacheable = depth < 4

        if cacheable:
            cache_key = ':'.join(rows) + '|' + prefix
            if cache_key in self.good_list_cache:
                return self.good_list_cache[cache_key]

        possible = self.prefix_cache[prefix]

        R = xrange(len(prefix), N)
        col_pref_cache = [None] * N

        good_list = []
        for word in possible:
            for i in R:
                if col_pref_cache[i] is None:
                    col_pref_cache[i] = ''.join(row[i] for row in rows)
                col_pref = col_pref_cache[i] + word[i]
                if col_pref not in self.prefix_cache:
                    break
            else:
                good_list.append(word)

        if cacheable:
            self.good_list_cache[cache_key] = good_list

        return good_list

    def _recur(self, rows, cols):
        if len(rows) == len(cols) == N:
            return True

        good_list = self._build_good_list(rows, cols)

        for i, word in enumerate(good_list):
            if word in self.used:
                continue

            rows.append(word)
            self.used.add(word)
            self.step += 1
            if not cols:
                self.percent = 1. * i / len(good_list)
            if (self.step & 0xFFFF) == 0:
                print '\033[2J\033[H'
                print "ELAPSED: %.0fs" % (time.time() - self.start_time,)
                print "PERCENT: %0.2f%%" % (self.percent * 100.0,)
                print self
            if self._recur(cols, rows):
                return True
            rows.pop()
            self.used.remove(word)
            if not self.used:
                self.good_list_cache = {}
        return False

    def fill(self):
        self.start_time = time.time()
        return self._recur(self.rows, self.cols)
