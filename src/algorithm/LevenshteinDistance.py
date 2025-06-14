"""
Implementasi Algoritma Levenshtein Distance
Tujuan: Menghitung jarak edit antar string untuk pencocokan fuzzy
"""

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

        TODO:
        - Implementasikan solusi dynamic programming
        - Tangani kasus khusus (string kosong)
        - Optimalkan kompleksitas memori
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

        TODO:
        - Hitung kemiripan untuk semua kandidat
        - Filter berdasarkan ambang batas
        - Urutkan berdasarkan skor kemiripan
        - Kembalikan hasil teratas
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

def main():
    print("=== Levenshtein Distance Module Test Suite ===\n")
    
    ld_calculator = LevenshteinDistance()
    
    # --- Test calculate() ---
    print("--- Testing calculate() (Levenshtein Distance) ---")
    test_cases_calculate = [
        ("kitten", "sitting", 3),
        ("saturday", "sunday", 3),
        ("flaw", "lawn", 2),
        ("hello", "hello", 0),
        ("apple", "aple", 1),
        ("book", "back", 2),
        ("", "abc", 3),
        ("xyz", "", 3),
        ("", "", 0),
        ("a", "b", 1),
        ("abc", "axbyc", 2),
        ("algorithm", "altruistic", 6)
    ]

    for s1, s2, expected_dist in test_cases_calculate:
        actual_dist = ld_calculator.calculate(s1, s2)
        status = "PASSED" if actual_dist == expected_dist else f"FAILED (Expected: {expected_dist}, Got: {actual_dist})"
        print(f"'{s1}' vs '{s2}' -> Distance: {actual_dist} ({status})")
    
    # --- Test similarity() ---
    print("\n--- Testing similarity() (Similarity Ratio 0.0-1.0) ---")
    test_cases_similarity = [
        ("kitten", "sitting", 0.5714),  # Jarak 3, max_len 7 -> (1 - 3/7) = 0.5714
        ("saturday", "sunday", 0.6250), # Jarak 3, max_len 8 -> (1 - 3/8) = 0.625
        ("apple", "aple", 0.8000),      # Jarak 1, max_len 5 -> (1 - 1/5) = 0.8
        ("hello", "hello", 1.0000),     # Jarak 0, max_len 5 -> (1 - 0/5) = 1.0
        ("", "abc", 0.0000),            # Jarak 3, max_len 3 -> (1 - 3/3) = 0.0
        ("abc", "", 0.0000),            # Jarak 3, max_len 3 -> (1 - 3/3) = 0.0
        ("", "", 1.0000),               # Jarak 0, max_len 0 -> (penanganan khusus) 1.0
        ("python", "pyhon", 0.8333)     # Jarak 1, max_len 6 -> (1 - 1/6) = 0.8333
    ]

    for s1, s2, expected_sim in test_cases_similarity:
        actual_sim = ld_calculator.similarity(s1, s2)
        # Menggunakan abs() dan toleransi kecil untuk membandingkan float
        status = "PASSED" if abs(actual_sim - expected_sim) < 0.0001 else f"FAILED (Expected: {expected_sim:.4f}, Got: {actual_sim:.4f})"
        print(f"'{s1}' vs '{s2}' -> Similarity Ratio: {actual_sim:.4f} ({status})")

    # --- Test findBestMatches() ---
    print("\n--- Testing findBestMatches() ---")
    target_word_1 = "programing" # typo dari programming
    candidate_words_1 = ["programming", "programer", "java", "coding", "python", "software"]
    
    print(f"\nTarget: '{target_word_1}'")
    print(f"Candidates: {candidate_words_1}")

    # Test dengan threshold default (0.7) dan maxResults default (10)
    print("\nBest Matches (threshold=0.7, maxResults=10):")
    best_matches_1 = ld_calculator.findBestMatches(target_word_1, candidate_words_1)
    if best_matches_1:
        for match, score in best_matches_1:
            print(f"  - '{match}': {score:.2f}%")
    else:
        print("  No matches found above the threshold.")

    # Test dengan threshold yang lebih ketat (misal 0.8) dan maxResults lebih kecil
    print("\nBest Matches (threshold=0.8, maxResults=2):")
    best_matches_2 = ld_calculator.findBestMatches(target_word_1, candidate_words_1, threshold=0.8, maxResults=2)
    if best_matches_2:
        for match, score in best_matches_2:
            print(f"  - '{match}': {score:.2f}%")
    else:
        print("  No matches found above the threshold.")

    # Test dengan target dan kandidat yang berbeda
    target_word_2 = "designer"
    candidate_words_2 = ["design", "desainer", "graphic designer", "desire", "drawing"]
    print(f"\nTarget: '{target_word_2}'")
    print(f"Candidates: {candidate_words_2}")
    
    print("\nBest Matches (threshold=0.6, maxResults=5):")
    best_matches_3 = ld_calculator.findBestMatches(target_word_2, candidate_words_2, threshold=0.6, maxResults=5)
    if best_matches_3:
        for match, score in best_matches_3:
            print(f"  - '{match}': {score:.2f}%")
    else:
        print("  No matches found above the threshold.")

if __name__ == "__main__":
    main()