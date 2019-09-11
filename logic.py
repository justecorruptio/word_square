from options import N
from stats import words_by_usefulness, build_prefix_cache, build_letter_freq


class State(object):

    def __init__(self, words):
        self.rows = []
        self.cols = []
        self.used = set()

        self.step = 0

        self.prefix_cache = build_prefix_cache(words)
        self.letter_freq = build_letter_freq(words)

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

        cacheable = depth < 3

        if cacheable:
            cache_key = ':'.join(rows) + '|' + prefix
            if cache_key in self.good_list_cache:
                return self.good_list_cache[cache_key]

        possible = self.prefix_cache[prefix]

        col_pref_cache = [None] * N
        R = range(len(prefix), N)
        for i in R:
            col_pref_cache[i] = ''.join(row[i] for row in rows)

        good_list = []
        for word in possible:
            good = True
            usage = 1
            for i in R:
                col_pref = col_pref_cache[i] + word[i]
                if col_pref not in self.prefix_cache:
                    good = False
                    break
                #usage += len(self.prefix_cache[col_pref]) * 256 / (i + 1)
                usage /= self.letter_freq[word[i]]
            if good:
                good_list.append((usage, word))

        good_list.sort(reverse=False)
        if cacheable:
            self.good_list_cache[cache_key] = good_list

        return good_list

    def _recur(self, rows, cols):
        #if self.step > 100000:
        #    return True
        if len(rows) == len(cols) == N:
            return True

        good_list = self._build_good_list(rows, cols)

        for usage, word in good_list:
            if word in self.used:
                continue

            rows.append(word)
            self.used.add(word)
            self.step += 1
            if (self.step & 0xFFFF) == 0:
                print self
            if self._recur(cols, rows):
                return True
            rows.pop()
            self.used.remove(word)
        return False

    def fill(self):
        return self._recur(self.rows, self.cols)
