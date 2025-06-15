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
        Melakukan pencocokan pola secara eksak (case-insensitive)
        
        Argumen:
            text (str): Teks yang akan dicari
            keywords (list): Daftar kata kunci yang akan dicari
            algorithm (str): Algoritma yang digunakan ('KMP' atau 'BM')
            
        Mengembalikan:
            dict: Hasil yang berisi kecocokan dan info waktu eksekusi
        """
        start = time.time()
        result = {}
          # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()
        keywords_lower = [keyword.lower() for keyword in keywords]
        
        if algorithm.upper() == 'KMP':
            matches = self.kmp.searchMultiple(text_lower, keywords_lower)
        elif algorithm.upper() == 'BM' or algorithm.upper() == 'BOYER-MOORE':
            matches = self.boyerMoore.searchMultiple(text_lower, keywords_lower)
        else: 
            raise ValueError(f"Algoritma tidak dikenali: '{algorithm}'. Pilih 'KMP', 'BM', atau 'Boyer-Moore'.")
            
        # Map results back to original keywords (preserve original case)
        for i, keyword in enumerate(keywords):
            keyword_lower = keywords_lower[i]
            result[keyword] = {
                'positions': matches.get(keyword_lower, []),
                'count': len(matches.get(keyword_lower, []))
            }
            
        end = time.time() - start 
        return {
            'matches': result,
            'algorithm': algorithm,
            'endtime': f"{end*1000:.2f} ms"
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
                    similarity = 1.0                # WARNING: INI PAKE LEVENSHTEIN DISTANCE
                else: # kalo ga 0, pake Levenshtein (HARUSNYA DISINI MANGGIL DARI LevenshteinDistance.py)
                    similarity = self.levenshtein.similarity(token, keyword)
                if similarity >= threshold: # ini jadi sim >= threshold 
                    fuzzyResults.append({'token': token, 'index': idx, 'similarity': similarity}) # similarity => sim ; 
                # WARNING: INI PAKE LEVENSHTEIN DISTANCE

            result[keyword] = fuzzyResults
        end = time.time() - start
        return {
            'matches': result,
            'threshold': threshold,
            'endtime': f"{end*1000:.2f} ms"  # waktu eksekusi dalam milisekon
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
    
#     # from PatternMatcher import PatternMatcher

# def main():
#     print("=== PatternMatcher Module Test Suite ===\n")
#     matcher = PatternMatcher()
#     text = "Saya adalah seorang Software Engineer berpengalaman di bidang Python dan ReactJS. Pernah mengerjakan project database SQL dan juga memiliki basic di C++."
#     keywords = ["python", "reactjs", "engineer", "sql", "c++", "java"]

#     # --- Test exactMatch (KMP) ---
#     print("--- Testing exactMatch() with KMP ---")
#     result_kmp = matcher.exactMatch(text, keywords, algorithm='KMP')
#     for k, v in result_kmp['matches'].items():
#         print(f"Keyword: '{k}' | Positions: {v['positions']} | Count: {v['count']}")
#     print(f"Algorithm: {result_kmp['algorithm']}, Time: {result_kmp['endtime']}")

#     # --- Test exactMatch (BM) ---
#     print("\n--- Testing exactMatch() with BM ---")
#     result_bm = matcher.exactMatch(text, keywords, algorithm='BM')
#     for k, v in result_bm['matches'].items():
#         print(f"Keyword: '{k}' | Positions: {v['positions']} | Count: {v['count']}")
#     print(f"Algorithm: {result_bm['algorithm']}, Time: {result_bm['endtime']}")

#     # --- Test fuzzyMatch ---
#     print("\n--- Testing fuzzyMatch() ---")
#     typo_keywords = ["pythun", "reactj", "enginer", "sqle", "c++", "java"]
#     result_fuzzy = matcher.fuzzyMatch(text, typo_keywords, threshold=0.7)
#     for k, matches in result_fuzzy['matches'].items():
#         print(f"Keyword: '{k}' | Matches: {matches}")
#     print(f"Threshold: {result_fuzzy['threshold']}, Time: {result_fuzzy['endtime']}")

#     # --- Test hybridMatch ---
#     print("\n--- Testing hybridMatch() ---")
#     result_hybrid = matcher.hybridMatch(text, typo_keywords, algorithm='KMP', fuzzyThreshold=0.7)
#     print("Exact matches:")
#     for k, v in result_hybrid['exact']['matches'].items():
#         print(f"Keyword: '{k}' | Positions: {v['positions']} | Count: {v['count']}")
#     print("Fuzzy matches:")
#     for k, matches in result_hybrid['fuzzy']['matches'].items():
#         print(f"Keyword: '{k}' | Matches: {matches}")
#     print(f"Hybrid test done.\n")

#     print("=== All PatternMatcher Tests Completed ===\n")

# if __name__ == "__main__":
#     main()
# # 