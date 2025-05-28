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
    
    def computeFailureFunction(self, pattern):
        """
        Menghitung fungsi failure (array LPS) untuk pola
        
        Argumen:
            pattern (str): Pola yang akan dihitung fungsi failurenya
            
        Mengembalikan:
            list: Array fungsi failure
            
        TODO:
        - Implementasi perhitungan LPS (Longest Proper Prefix yang juga Suffix)
        - Menangani kasus khusus untuk pola kosong atau satu karakter
        """
        pass
    
    def search(self, text, pattern, caseSensitive=True):
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
        pass
    
    def searchMultiple(self, text, patterns, caseSensitive=True):
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
        pass