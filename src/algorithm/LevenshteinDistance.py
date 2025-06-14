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
        
# def main():
#     print("=== Levenshtein Distance Module Test Suite ===\n")
    
#     ld_calculator = LevenshteinDistance()
    
#     # --- Test calculate() ---
#     print("--- Testing calculate() (Levenshtein Distance) ---")
#     test_cases_calculate = [
#         ("kitten", "sitting", 3),
#         ("saturday", "sunday", 3),
#         ("flaw", "lawn", 2),
#         ("hello", "hello", 0),
#         ("apple", "aple", 1),
#         ("book", "back", 2),
#         ("", "abc", 3),
#         ("xyz", "", 3),
#         ("", "", 0),
#         ("a", "b", 1),
#         ("abc", "axbyc", 2),
#         ("algorithm", "altruistic", 6)
#     ]

#     for s1, s2, expected_dist in test_cases_calculate:
#         actual_dist = ld_calculator.calculate(s1, s2)
#         status = "PASSED" if actual_dist == expected_dist else f"FAILED (Expected: {expected_dist}, Got: {actual_dist})"
#         print(f"'{s1}' vs '{s2}' -> Distance: {actual_dist} ({status})")
    
#     # --- Test similarity() ---
#     print("\n--- Testing similarity() (Similarity Ratio 0.0-1.0) ---")
#     test_cases_similarity = [
#         ("kitten", "sitting", 0.5714),
#         ("saturday", "sunday", 0.6250),
#         ("apple", "aple", 0.8000),
#         ("hello", "hello", 1.0000),
#         ("", "abc", 0.0000),
#         ("abc", "", 0.0000),
#         ("", "", 1.0000),
#         ("python", "pyhon", 0.8333)
#     ]

#     for s1, s2, expected_sim in test_cases_similarity:
#         actual_sim = ld_calculator.similarity(s1, s2)
#         status = "PASSED" if abs(actual_sim - expected_sim) < 0.0001 else f"FAILED (Expected: {expected_sim:.4f}, Got: {actual_sim:.4f})"
#         print(f"'{s1}' vs '{s2}' -> Similarity Ratio: {actual_sim:.4f} ({status})")

#     # --- Test findBestMatches() ---
#     print("\n--- Testing findBestMatches() ---")
#     target_word_1 = "programing" # typo dari programming
#     candidate_words_1 = ["programming", "programer", "java", "coding", "python", "software", ""] # Tambahkan string kosong untuk uji kasus
    
#     print(f"\nTarget: '{target_word_1}'")
#     print(f"Candidates: {candidate_words_1}")

#     print("\nBest Matches (threshold=0.7, maxResults=10):")
#     best_matches_1 = ld_calculator.findBestMatches(target_word_1, candidate_words_1)
#     if best_matches_1:
#         for match, score in best_matches_1:
#             print(f"   - '{match}': {score:.2f}") # Changed % to empty string, as it's already a percentage
#     else:
#         print("   No matches found above the threshold.")

#     print("\nBest Matches (threshold=0.8, maxResults=2):")
#     best_matches_2 = ld_calculator.findBestMatches(target_word_1, candidate_words_1, threshold=0.8, maxResults=2)
#     if best_matches_2:
#         for match, score in best_matches_2:
#             print(f"   - '{match}': {score:.2f}")
#     else:
#         print("   No matches found above the threshold.")

#     target_word_2 = "designer"
#     candidate_words_2 = ["design", "desainer", "graphic designer", "desire", "drawing"]
#     print(f"\nTarget: '{target_word_2}'")
#     print(f"Candidates: {candidate_words_2}")
    
#     print("\nBest Matches (threshold=0.6, maxResults=5):")
#     best_matches_3 = ld_calculator.findBestMatches(target_word_2, candidate_words_2, threshold=0.6, maxResults=5)
#     if best_matches_3:
#         for match, score in best_matches_3:
#             print(f"   - '{match}': {score:.2f}")
#     else:
#         print("   No matches found above the threshold.")

#     # --- Test search() ---
#     print("\n--- Testing search() ---")
#     sample_cv_text = "Saya adalah seorang Software Engineer berpengalaman di bidang Python dan ReactJS. Pernah mengerjakan project database SQL dan juga memiliki basic di C++. "
    
#     print(f"\nSample CV Text: '{sample_cv_text}'")

#     print("\nSearch for 'pytton' (case-insensitive, threshold 0.7):")
#     results_pytton = ld_calculator.search(sample_cv_text, "pytton", threshold=0.7, caseSensitive=False)
#     if results_pytton:
#         for word, score in results_pytton:
#             print(f"   Found: '{word}' (Score: {score:.2f})")
#     else:
#         print("   No fuzzy matches found.")

#     print("\nSearch for 'ReactJS' (case-sensitive, threshold 0.8):")
#     results_reactjs = ld_calculator.search(sample_cv_text, "ReactJS", threshold=0.8, caseSensitive=True)
#     if results_reactjs:
#         for word, score in results_reactjs:
#             print(f"   Found: '{word}' (Score: {score:.2f})")
#     else:
#         print("   No fuzzy matches found.")

#     print("\nSearch for 'Engineer' (case-insensitive, threshold 0.9):")
#     results_engineer = ld_calculator.search(sample_cv_text, "Engineer", threshold=0.9, caseSensitive=False)
#     if results_engineer:
#         for word, score in results_engineer:
#             print(f"   Found: '{word}' (Score: {score:.2f})")
#     else:
#         print("   No fuzzy matches found.")

#     # --- Test searchMultiple() ---
#     print("\n--- Testing searchMultiple() ---")
#     keywords_to_search = ["pythun", "reactj", "sqle", "c++", "engineer"]
#     print(f"\nKeywords to search: {keywords_to_search}")

#     multiple_results = ld_calculator.searchMultiple(sample_cv_text, keywords_to_search, threshold=0.7, caseSensitive=False)
    
#     for keyword, matches in multiple_results.items():
#         print(f"\nResults for '{keyword}':")
#         if matches:
#             for word, score in matches:
#                 print(f"   - Found: '{word}' (Score: {score:.2f})")
#         else:
#             print("   No fuzzy matches found for this keyword.")
    
#     # --- Test count_every_word_occurrence() ---
#     print("\n--- Testing count_every_word_occurrence() ---")
#     sample_text_for_count = "Python programmer, a python enthusiast, and also codes in Cpp. I love python!"
#     keywords_for_count = ["Python", "programmer", "cpp", "java"]

#     print(f"\nSample Text: '{sample_text_for_count}'")
#     print(f"Keywords to count: {keywords_for_count}")

#     counts_case_sensitive = ld_calculator.count_every_word_occurrence(
#         sample_text_for_count, keywords_for_count, threshold=0.8, caseSensitive=True
#     )
#     print("\nCounts (Case Sensitive, Threshold 0.8):")
#     for keyword, count in counts_case_sensitive.items():
#         print(f"  '{keyword}': {count} occurrences")

#     counts_case_insensitive = ld_calculator.count_every_word_occurrence(
#         sample_text_for_count, keywords_for_count, threshold=0.8, caseSensitive=False
#     )
#     print("\nCounts (Case Insensitive, Threshold 0.8):")
#     for keyword, count in counts_case_insensitive.items():
#         print(f"  '{keyword}': {count} occurrences")

#     # Another example for count_every_word_occurrence
#     sample_text_2 = "software development, developer, develop, developing, develop"
#     keywords_2 = ["develop", "software"]
#     counts_2 = ld_calculator.count_every_word_occurrence(
#         sample_text_2, keywords_2, threshold=0.7, caseSensitive=False
#     )
#     print(f"\nSample Text 2: '{sample_text_2}'")
#     print(f"Keywords to count 2: {keywords_2}")
#     print("\nCounts (Case Insensitive, Threshold 0.7):")
#     for keyword, count in counts_2.items():
#         print(f"  '{keyword}': {count} occurrences")


#     print("\n=== All Tests Completed ===\n")

# if __name__ == "__main__":
#     main()