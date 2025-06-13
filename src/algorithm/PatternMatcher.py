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


    def fuzzyMatch(self, text, keywords, threshold=0.7) -> dict:
        """
        Melakukan pencocokan pola fuzzy menggunakan jarak Levenshtein
        
        Argumen:
            text (str): Teks yang akan dicari
            keywords (list): Daftar kata kunci yang akan dicari
            threshold (float): Ambang batas kemiripan minimum
            
        Mengembalikan:
            dict: Hasil yang berisi kecocokan fuzzy dan info waktu eksekusi
            
        TODO:
        - Tokenisasi teks menjadi kata-kata
        - Temukan kecocokan fuzzy untuk setiap kata kunci
        - Filter berdasarkan ambang batas kemiripan
        - Ukur waktu eksekusi
        """
        start = time.time()
        result = {}
        tokens = text.split() #ini maksudnya displit, misal "lukas raja" jadi ["lukas", "raja"]
        for keyword in keywords: 
            fuzzyResults = [] # buat list buat nyimpen hasil fuzzy tiap keyword
            for idx, token in enumerate(tokens): # maksuddari enumerate itu buat dapetin indexnya juga
                maxLen = max(len(token), len(keyword)) # bakal cari yang panjangnya maksimal dari keyword ama hasil split tadi
                if maxLen == 0: # kalo misalkan panjangnya 0, yaudah gaada yang bisa dibandingin
                    similarity = 1.0

                # WARNING: INI PAKE LEVENSHTEIN DISTANCE
                else: # kalo ga 0, pake Levenshtein (HARUSNYA DISINI MANGGIL DARI LevenshteinDistance.py)
                    dist = self.levenshtein.distance(token, keyword) #ini cari jaraknya berdasarkan total subtitusi, hapus, insert
                    similarity = 1 - dist / maxLen # rumusnya ini, harusnya di LevenshteinDistance.py ada fungsi similarity yang bisa dipake
                    # jadi ntar ..... 
                    # manggilnya sim = self.levenshtein.similarity(token, keyword)
                if similarity >= threshold: # ini jadi sim >= threshold 
                    fuzzyResults.append({'token': token, 'index': idx, 'similarity': similarity}) # similarity => sim ; 
                # WARNING: INI PAKE LEVENSHTEIN DISTANCE

            result[keyword] = fuzzyResults
        end = time.time() - start
        return {
            'matches': result,
            'threshold': threshold,
            'endtime': end + "ms"  # waktu eksekusi dalam milisekon
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