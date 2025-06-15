"""
Implementasi Algoritma Levenshtein Distance
Tujuan: Menghitung jarak edit antar string untuk pencocokan fuzzy
"""
import re
try:
    # Try relative import first (when used as module)
    from ..pdfprocessor.regexExtractor import RegexExtractor
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    
    from pdfprocessor.regexExtractor import RegexExtractor

class LevenshteinDistance:
    """
    Implementasi Levenshtein Distance untuk pencocokan string fuzzy

    TODO:
    - Implementasikan perhitungan dasar Levenshtein distance
    - Implementasikan versi yang efisien dalam penggunaan memori
    - Tambahkan perhitungan rasio kemiripan
    - Tangani biaya operasi string yang berbeda
    """

    def __init__(self):
        """Inisialisasi kalkulator Levenshtein"""
        pass
    

    def calculate(self, str1, str2):
        """
        Hitung jarak Levenshtein antara dua string

        Argumen:
            str1 (str): String pertama
            str2 (str): String kedua

        Mengembalikan:
            int: Jarak Levenshtein
        """
        m = len(str1)
        n = len(str2)

        # create DP table
        dp = [[0] * (n + 1) for _ in range(m + 1)] 
        
        # fill all base problems
        for j in range(0, n + 1): # fill columns
            dp[0][j] = j
            
        for i in range(0, m + 1): # fill rows
            dp[i][0] = i
        
        # fill dp table to get final distance using lev dist algo
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i-1] == str2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i-1][j-1], # replace
                        dp[i][j-1], # insert
                        dp[i-1][j] # delete
                    )
        return dp[m][n] # return distance


    def similarity(self, str1, str2):
        """
        Hitung rasio kemiripan antara dua string

        Argumen:
            str1 (str): String pertama
            str2 (str): String kedua

        Mengembalikan:
            float: Rasio kemiripan (0.0 sampai 1.0)
        """
        if not str1 and not str2:
            return 1.0
            
        max_len = max(len(str1), len(str2))
        if max_len == 0: 
            return 1.0 
        
        LD = self.calculate(str1, str2)

        sim_ratio = 1- LD/max_len
        
        return sim_ratio


    def findBestMatches(self, target, candidates, threshold=0.7, maxResults=10):
        """
        Temukan string yang paling cocok dari kandidat

        Argumen:
            target (str): String target yang akan dicocokkan
            candidates (list): Daftar string kandidat
            threshold (float): Ambang minimum kemiripan
            maxResults (int): Jumlah maksimum hasil yang dikembalikan

        Mengembalikan:
            list: Daftar tuple (kandidat, skor_kemiripan)
        """
        results = []
        for candidate in candidates:
            sim_ratio = self.similarity(target, candidate)
            if sim_ratio >= threshold:
                result = (candidate, sim_ratio)
                results.append(result)
        # sort results
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:maxResults]
    

    def search(self, text, keyword, threshold=0.7, caseSensitive=True) -> list:
        if not caseSensitive:
            text = text.lower()  # lower text if not case sensitive
            keyword = keyword.lower()

        regex = RegexExtractor()
        processed_text = regex.seperatePunctuations(text) # seperate punctuations
        words = processed_text.split() # split words in string

        result = self.findBestMatches(keyword, words, threshold)
        return result
    
    
    def searchMultiple(self, text, keywords, threshold=0.7, caseSensitive=True) -> dict:
        results = {}
        for keyword in keywords:
            results[keyword] = self.search(text, keyword, threshold, caseSensitive)
        return results
    

    def count_every_word_occurrence(self, text, keywords, threshold=0.7, caseSensitive=True) -> dict:
        """
        Menghitung setiap kemunculan fuzzy dari kata kunci dalam teks.

        Argumen:
            text (str): Teks input yang akan dicari.
            keywords (list): Daftar kata kunci yang akan dihitung.
            threshold (float): Ambang minimum kemiripan untuk dipertimbangkan sebagai kecocokan.
            caseSensitive (bool): Jika True, pencocokan akan peka huruf besar/kecil.

        Mengembalikan:
            dict: Sebuah kamus di mana kunci adalah kata kunci dan nilai adalah 
                  jumlah kemunculan fuzzy dalam teks.
        """
        occurrence_counts = {keyword: 0 for keyword in keywords}
        
        regex = RegexExtractor()
        # Preprocess the text once
        processed_text = regex.seperatePunctuations(text)
        words = processed_text.split()

        # Adjust keywords and words if not case sensitive
        if not caseSensitive:
            keywords_lower = [k.lower() for k in keywords]
            words_lower = [w.lower() for w in words]
        else:
            keywords_lower = keywords # Use original keywords for comparison
            words_lower = words      # Use original words for comparison


        for i, text_word_original in enumerate(words):
            text_word = words_lower[i] # Use lowercased word for comparison if not case sensitive
            
            for j, keyword_original in enumerate(keywords):
                keyword = keywords_lower[j] # Use lowercased keyword for comparison if not case sensitive

                sim_ratio = self.similarity(keyword, text_word)
                if sim_ratio >= threshold:
                    occurrence_counts[keyword_original] += 1
        
        for keyword in keywords:
            if occurrence_counts[keyword] == 0:
                occurrence_counts.pop(keyword)  # Remove keywords with no occurrences
        return occurrence_counts
        