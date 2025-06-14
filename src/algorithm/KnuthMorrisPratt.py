"""
Implementasi Algoritma Knuth-Morris-Pratt
Tujuan: Pencocokan pola string secara efisien menggunakan algoritma KMP
"""

class KnuthMorrisPratt:
    """
    Implementasi algoritma pencocokan pola KMP
    
    TODO:
    - Implementasi perhitungan fungsi failure
    - Implementasi pencarian utama KMP
    - Menangani pencarian banyak pola
    """
    
    def __init__(self):
        """Inisialisasi pencocok KMP"""
        pass
    
    def computeFailureFunction(self, pattern) -> list:
        """
        Menghitung fungsi failure (array LPS) untuk pola
        
        Argumen:pola
            pattern (str): Pola yang akan dihitung fungsi failurenya
            
        Mengembalikan:
            list: Array fungsi failure
            
        TODO:
        - Implementasi perhitungan LPS (Longest Proper Prefix yang juga Suffix)
        - Menangani kasus khusus untuk  kosong atau satu karakter
        """
        # misalkan LPS = [0, 0, 1, 0, 1, 2, 0] buat pattern yang dicari "ABACABC"

        lps = [0] * len(pattern) #ini inisialisassi arraynya, jadi [0, 0, 0, 0, 0, 0, 0] sepanjang pattern
        length = 0  # panjang prefix yang cocok, inisalisassinya 0
        i = 1  # ini mulai dari index 1 karena index 0 selalu 0 (yadong, kan gaada lagi yang lebih awal)
        while i < len(pattern): # mulai loooping
            if pattern[i] == pattern[length]: # 2 iterator, i buat tiap karakter di pattern
                length += 1 # jadi besar prefix yang cocok bertambah
                lps[i] = length 
                i += 1  
            else: # kalo gasama di suatu titik
                if length != 0: # ini kalo misalkan sebelumnya ada prefix yang cocok, 
                    length = lps[length - 1] #emang ga diiterasi i+1, jadi multiple check ampe antara lengthnya abiss = > 0 atau nemu karakter yang sama dari pattern(length-x)
                else:
                    lps[i] = 0 # kalo ampe akhir gaada yang cocok, yaudah lps[i] = 0
                    i += 1
        return lps

    def search(self, text, pattern, caseSensitive=True) -> list:
        """
        Mencari pola dalam teks menggunakan algoritma KMP
        
        Argumen:
            text (str): Teks yang akan dicari
            pattern (str): Pola yang akan dicari
            caseSensitive (bool): Apakah pencarian sensitif terhadap huruf besar/kecil
            
        Mengembalikan:
            list: Daftar posisi awal di mana pola ditemukan
            
        TODO:
        - Implementasi algoritma pencarian utama KMP
        - Menggunakan fungsi failure untuk menghindari perbandingan yang tidak perlu
        - Menangani sensitivitas huruf besar/kecil
        - Mengembalikan semua posisi kemunculan
        """
        if not caseSensitive: # kalo mau disamain huruf besar kecilnya, lowerin semua
            text = text.lower() 
            pattern = pattern.lower()
        lps = self.computeFailureFunction(pattern) # panggil lpsny
        result = []
        i = 0  # index untuk text
        j = 0  # index untuk pattern
        while i < len(text):
            if pattern[j] == text[i]:
                i += 1 # kalo sama, majuin kkeduanya iterator
                j += 1
            if j == len(pattern): # kalo udah ampe akhir pattern, artinya ketemu 
                result.append(i - j) # append posisi awalnya string
                j = lps[j - 1] # reset j ke posisi sebelumnya yang masih cocok
            elif i < len(text) and pattern[j] != text[i]: # kalo ga sama
                if j != 0: # sama kayak pas hitung lps, kalo sebelumnya ada prefix yang cocok
                    j = lps[j - 1] # j nya bakal multiple check ke sebelumnya
                else:
                    i += 1 
        return result

    def searchMultiple(self, text, patterns, caseSensitive=True) -> dict:
        """
        Mencari beberapa pola dalam teks
        
        Argumen:
            text (str): Teks yang akan dicari
            patterns (list): Daftar pola yang akan dicari
            caseSensitive (bool): Apakah pencarian sensitif terhadap huruf besar/kecil
            
        Mengembalikan:
            dict: Dictionary yang memetakan pola ke posisi kemunculannya
            
        TODO:
        - Implementasi pencarian banyak pola
        - Optimasi untuk banyak pola
        """
        results = {} # dictionary untuk menyimpan hasil
        for pattern in patterns:
            results[pattern] = self.search(text, pattern, caseSensitive)
        return results