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
    
    TODO:
    - Integrasikan semua algoritma pencocokan pola
    - Implementasikan pencocokan eksak dan fuzzy
    - Tambahkan pengukuran performa
    - Tangani beberapa kata kunci
    """
    
    def __init__(self):
        """Inisialisasi pattern matcher dengan semua algoritma"""
        self.boyerMoore = BoyerMoore()
        self.kmp = KnuthMorrisPratt()
        self.levenshtein = LevenshteinDistance()
        # self.ac = AhoCorasick() # ntar kalo implement Aho-Corasick
        
    def exactMatch(self, text, keywords, algorithm='KMP') -> dict:
        """
        Melakukan pencocokan pola secara eksak
        
        Argumen:
            text (str): Teks yang akan dicari
            keywords (list): Daftar kata kunci yang akan dicari
            algorithm (str): Algoritma yang digunakan ('KMP' atau 'BM')
        
        Mengembalikan:
            dict: Hasil yang berisi kecocokan dan info waktu eksekusi
        """
        start = time.perf_counter()
        # Pilih algoritma
        if algorithm.upper() == 'KMP':
            matches = self.kmp.searchMultiple(text, keywords)
        elif algorithm.upper() == 'BM':
            matches = self.boyerMoore.searchMultiple(text, keywords)
        else:
            raise ValueError(
                "Algoritma tidak dikenali. Pilih 'KMP' atau 'BM' (atau 'AC')."
            )
        # Siapkan hasil
        result = {}
        for kw in keywords:
            positions = matches.get(kw, [])
            result[kw] = {
                'positions': positions,
                'count': len(positions)
            }
        # Hitung waktu eksekusi dalam ms
        end = time.perf_counter()
        exec_ms = (end - start) * 1000
        return {
            'matches': result,
            'algorithm': algorithm,
            'execution_time_ms': f"{exec_ms:.2f}ms"
        }

    def fuzzyMatch(self, text, keywords, threshold=0.7, caseSensitive=True) -> dict:
        """
        Melakukan pencocokan pola fuzzy menggunakan jarak Levenshtein
        """
        start = time.perf_counter()
        counts = self.levenshtein.count_every_word_occurrence(
            text, keywords,
            threshold=threshold,
            caseSensitive=caseSensitive
        )
        end = time.perf_counter()
        exec_ms = (end - start) * 1000
        return {
            'matches': counts,
            'threshold': threshold,
            'caseSensitive': caseSensitive,
            'execution_time_ms': f"{exec_ms:.2f}ms"
        }

    def hybridMatch(self, text, keywords, algorithm='KMP', fuzzyThreshold=0.7) -> dict:
        """
        Melakukan pencocokan hibrida (eksak + fuzzy)
        """
        exact = self.exactMatch(text, keywords, algorithm)
        not_found = [k for k, v in exact['matches'].items() if v['count'] == 0]
        fuzzy = ({ 'matches': {} } if not not_found else
                 self.fuzzyMatch(text, not_found, threshold=fuzzyThreshold))
        return {
            'exact': exact,
            'fuzzy': fuzzy
        }
