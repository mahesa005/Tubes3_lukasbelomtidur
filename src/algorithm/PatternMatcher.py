"""
Pattern Matcher - Antarmuka utama untuk semua algoritma pencocokan pola
Tujuan: Antarmuka terpadu untuk operasi pencocokan pola
"""

from .BoyerMoore import BoyerMoore
from .KnuthMorrisPratt import KnuthMorrisPratt
from .LevenshteinDistance import LevenshteinDistance
import time

class PatternMatcher:
    """
    Antarmuka pencocokan pola terpadu
    """
    def __init__(self):
        """Inisialisasi pattern matcher dengan algoritma KMP, BM, dan Lev dist"""
        self.boyerMoore  = BoyerMoore()
        self.kmp         = KnuthMorrisPratt()
        self.levenshtein = LevenshteinDistance()

    def exactMatch(self, text, keywords, algorithm='KMP') -> dict:
        """
        Melakukan pencocokan pola secara eksak menggunakan KMP atau BM
        """
        start = time.time()
        algo = algorithm.upper()
        if algo == 'KMP':
            matches = self.kmp.searchMultiple(text, keywords)
        elif algo == 'BM':
            matches = self.boyerMoore.searchMultiple(text, keywords)
        else:
            raise ValueError("Algoritma tidak dikenali. Pilih 'KMP' atau 'BM'.")

        result = {
            kw: {
                'positions': matches.get(kw, []),
                'count': len(matches.get(kw, []))
            }
            for kw in keywords
        }
        duration_ms = (time.time() - start) * 1000
        return {
            'matches': result,
            'algorithm': algorithm,
            'execution_time_ms': f"{duration_ms:.2f}ms"
        }

    def fuzzyMatch(self, text, keywords, threshold=0.7, caseSensitive=True) -> dict:
        """
        Melakukan pencocokan pola fuzzy menggunakan Levenshtein Distance
        """
        start = time.perf_counter()
        matches_counts = self.levenshtein.count_every_word_occurrence(
            text, keywords, threshold=threshold, caseSensitive=caseSensitive
        )
        duration_ms = (time.perf_counter() - start) * 1000
        return {
            'matches': matches_counts,
            'threshold': threshold,
            'caseSensitive': caseSensitive,
            'execution_time_ms': f"{duration_ms:.2f}ms"
        }

    def hybridMatch(self, text, keywords, algorithm='KMP', fuzzyThreshold=0.7) -> dict:
        """
        Gabungan exact + fuzzy untuk kata kunci yang tak ditemukan
        """
        exact = self.exactMatch(text, keywords, algorithm)
        not_found = [k for k, v in exact['matches'].items() if v['count'] == 0]
        fuzzy = self.fuzzyMatch(text, not_found, fuzzyThreshold) if not_found else {'matches': {}}
        return {
            'exact': exact,
            'fuzzy': fuzzy
        }

# kontol = hybrdiMatds; {}
# rsultcard.matchers = kontol[matches][1]