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
            
        TODO:
        - Implementasikan pencocokan eksak menggunakan algoritma yang dipilih
        - Ukur waktu eksekusi
        - Hitung jumlah kemunculan untuk setiap kata kunci
        - Kembalikan hasil yang komprehensif
        """
        start = time.time() # waktu jalan
        result = {} # dict 
        if algorithm.upper() == 'KMP': #kalo milih kmp.upper = KMP
            matches = self.kmp.searchMultiple(text, keywords)
        elif algorithm.upper() == 'BM': # kalo milih BM.upper = BM
            matches = self.boyerMoore.searchMultiple(text, keywords)
        # elif algorithm.upper() == 'AC' ; 
        #     matches = self.ac.SearchMultiple(text, keywords)  --- ntar kalo implement 
        else: 
            raise ValueError("Algoritma tidak dikenali. Pilih 'KMP' atau 'BM' (atau 'AC').") # kek throw kalo di java
        for keyword in keywords:
            result[keyword] = {
                'positions': matches.get(keyword, []),  # ngambil posisi pattern yang ketemu (index pertamanya pattern ditext)
                'count': len(matches.get(keyword, [])) # nyimpen jumlah kemunculanny 
            }
        end = time.time() - start 
        return { # nested dict
            'matches': result, # hasilnya dalam dict 
            'algorithm': algorithm,
            'endtime': end + "ms" # pake milisekon
        }


    def fuzzyMatch(self, text, keywords, threshold=0.7, caseSensitive=True) -> dict:
        """
        Melakukan pencocokan pola fuzzy menggunakan jarak Levenshtein
        
        Argumen:
            text (str): Teks yang akan dicari
            keywords (list): Daftar kata kunci yang akan dicari
            threshold (float): Ambang batas kemiripan minimum
            caseSensitive (bool): Jika True, pencocokan akan peka huruf besar/kecil.
            
        Mengembalikan:
            dict: Hasil yang berisi kecocokan fuzzy (keyword: count) dan info waktu eksekusi
        """
        start = time.perf_counter()
        
        matches_counts = self.levenshtein.count_every_word_occurrence(
            text, keywords, threshold=threshold, caseSensitive=caseSensitive
        )
        
        end = time.perf_counter()
        execution_time_ms = (end - start) * 1000 

        return {
            'matches': matches_counts, 
            'threshold': threshold,
            'caseSensitive': caseSensitive,
            'execution_time_ms': f"{execution_time_ms:.2f}ms"
        }

    def hybridMatch(self, text, keywords, algorithm='KMP', fuzzyThreshold=0.7) -> dict:
        """
        Melakukan pencocokan hibrida (eksak + fuzzy untuk kata kunci yang tidak cocok)
        
        Argumen:
            text (str): Teks yang akan dicari
            keywords (list): Daftar kata kunci yang akan dicari
            algorithm (str): Algoritma untuk pencocokan eksak
            fuzzyThreshold (float): Ambang batas untuk pencocokan fuzzy
            
        Mengembalikan:
            dict: Hasil gabungan dari pencocokan eksak dan fuzzy
            
        TODO:
        - Lakukan pencocokan eksak terlebih dahulu
        - Untuk kata kunci yang tidak ditemukan secara eksak, lakukan pencocokan fuzzy
        - Gabungkan dan kembalikan hasilnya
        """
        # nah ini mau gmn... mau ceritanya, 
        # 1. cari exact match dulu, baru abis itu cari fuzzy match kalo gaada (status quo)
        # 2. atau cari 2 2 nya sekalan 
        exact = self.exactMatch(text, keywords, algorithm) 
        notFound = [k for k, v in exact['matches'].items() if v['count'] == 0] # ini kalo buat nyari keyword yang gaada di hasil exact match
        fuzzy = self.fuzzyMatch(text, notFound, fuzzyThreshold) if notFound else {'matches': {}}
        return {
            'exact': exact,
            'fuzzy': fuzzy
        }