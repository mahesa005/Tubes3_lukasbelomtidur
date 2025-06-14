class BoyerMoore:
    def __init__(self):
        self.bad_char = {}
        self.good_suffix = []

    def preprocessBadCharacter(self, pattern):
        bad = {}
        m = len(pattern)
        for i in range(m):
            bad[pattern[i]] = i  # simpan posisi terakhir kemunculan
        return bad

    def preprocessGoodSuffix(self, pattern):
        m = len(pattern)
        good = [0] * (m + 1)
        border = [0] * (m + 1)
        
        # langkah 1 hitung border dari suffix
        i = m
        j = m + 1
        border[i] = j
        while i > 0:
            while j <= m and pattern[i-1] != pattern[j-1]:
                if good[j] == 0:
                    good[j] = j - i
                j = border[j]
            i -= 1
            j -= 1
            border[i] = j

        # langkah 2 isi good untuk prefix
        j = border[0]
        for i in range(m + 1):
            if good[i] == 0:
                good[i] = j
            if i == j:
                j = border[j]
        return good

    def search(self, text, pattern, caseSensitive=True):
        if not caseSensitive:
            text = text.lower()
            pattern = pattern.lower()
        n = len(text)
        m = len(pattern)
        if m == 0:
            return []
        # pra pemrosesan
        bad = self.preprocessBadCharacter(pattern)
        good = self.preprocessGoodSuffix(pattern)
        # pencarian utama
        occurrences = []
        s = 0
        while s <= n - m:
            j = m - 1
            while j >= 0 and pattern[j] == text[s+j]:
                j -= 1
            if j < 0:
                occurrences.append(s)
                s += good[0]
            else:
                char_shift = j - bad.get(text[s+j], -1)
                suffix_shift = good[j+1]
                s += max(char_shift, suffix_shift)
        return occurrences

    def countOccurrences(self, text, pattern, caseSensitive=True):
        return len(self.search(text, pattern, caseSensitive))

# coba
if __name__ == '__main__':
    bm = BoyerMoore()
    text = "dadasdihawidhalukasbelomtidurhdiwhdia"
    pattern = "lukasbelomtidur"
    print("Matches at:", bm.search(text, pattern))
    print("Count:", bm.countOccurrences(text, pattern))
