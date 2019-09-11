from options import N
from stats import words_by_usefulness, build_prefix_cache


class State(object):

    def __init__(self, words):
        self.rows = []
        self.cols = []
        self.used = set()

        self.step = 0

        self.prefix_cache = build_prefix_cache(words)

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

    def _recur(self, rows, cols):
        #if self.step > 100000:
        #    return True
        if len(rows) == len(cols) == N:
            return True

        depth = len(rows)
        prefix = ''.join(col[depth] for col in cols)
        possible = self.prefix_cache[prefix]

        col_pref_cache = [None] * N
        R = range(len(prefix), N)
        for i in R:
            col_pref_cache[i] = ''.join(row[i] for row in rows)

        good_list = []
        for word in possible:
            if word in self.used:
                continue

            good = True
            usage = 0
            for i in R:
                col_pref = col_pref_cache[i] + word[i]
                if col_pref not in self.prefix_cache:
                    good = False
                    break
                usage += len(self.prefix_cache[col_pref]) * 256 / (i + 1)
            if good:
                good_list.append((usage, word))

        good_list.sort(reverse=True)

        for usage, word in good_list:

            rows.append(word)
            self.used.add(word)
            self.step += 1
            if (self.step & 4095) == 0:
                print self
            if self._recur(cols, rows):
                return True
            rows.pop()
            self.used.remove(word)
        return False

    def fill(self):
        return self._recur(self.rows, self.cols)
