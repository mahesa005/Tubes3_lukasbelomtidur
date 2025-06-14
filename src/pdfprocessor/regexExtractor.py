# ===== src/pdfProcessor/regexExtractor.py =====
"""
Ekstraksi Informasi Berbasis Regex dari CV
Tujuan: Mengekstrak informasi spesifik dari teks CV menggunakan regex
"""

import re
from datetime import datetime
import logging
import unicodedata

class RegexExtractor:
    """
    Kelas untuk ekstraksi informasi menggunakan regex
    
    TODO:
    - Definisikan pola regex untuk berbagai informasi
    - Ekstrak nama, email, nomor telepon, dll
    - Ekstrak pengalaman kerja, pendidikan, keterampilan
    - Tangani berbagai format CV
    """
    
    def __init__(self):
        """Inisialisasi regex extractor"""
        self.logger = logging.getLogger(__name__)
        self.setupPatterns()
    
    def setupPatterns(self):
        """
        Menyiapkan pola regex untuk berbagai informasi
        
        TODO:
        - Pola email
        - Pola nomor telepon (berbagai format)
        - Pola tanggal
        - Pola pengalaman kerja
        - Pola pendidikan
        - Pola keterampilan
        """
        # Pola email
        self.emailPattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Pola nomor telepon (berbagai format)
        self.phonePatterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # Format US
            r'\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US dengan kode negara
            r'\+\d{1,3}[-.\s]?\d{1,14}',  # Format internasional
        ]
        
        # Pola tanggal
        self.datePatterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',  # MM/DD/YYYY
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',  # YYYY/MM/DD
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b',  # Bulan Tahun
        ]
    
    def extractEmail(self, text):
        """
        Mengekstrak alamat email dari teks
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar alamat email yang ditemukan
        """
        pass
    
    def extractPhone(self, text):
        """
        Mengekstrak nomor telepon dari teks
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar nomor telepon yang ditemukan
        """
        pass
    
    def extractSummary(self, text):
        """
        Mengekstrak ringkasan/tujuan dari CV
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            str: Teks ringkasan atau string kosong
            
        TODO:
        - Cari bagian summary/objective/profile
        - Ekstrak paragraf yang relevan
        - Bersihkan hasil ekstraksi
        """
        pass
    
    def extractSkills(self, text):
        """
        Mengekstrak keterampilan dari CV
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar keterampilan yang ditemukan
            
        TODO:
        - Cari bagian skills/competencies
        - Ekstrak keterampilan satu per satu
        - Tangani berbagai format (poin, dipisahkan koma, dll)
        """
        pass
    
    def extractExperience(self, text):
        """
        Mengekstrak pengalaman kerja dari CV
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar dict dengan informasi pekerjaan
            
        TODO:
        - Cari bagian pengalaman kerja/riwayat pekerjaan
        - Ekstrak jabatan, perusahaan, tanggal
        - Parsing deskripsi pekerjaan
        """
        pass
    
    def extractEducation(self, text):
        """
        Mengekstrak informasi pendidikan dari CV
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar dict dengan informasi pendidikan
            
        TODO:
        - Cari bagian pendidikan
        - Ekstrak gelar, institusi, tanggal kelulusan
        - Tangani berbagai format entri pendidikan
        """
        pass
    
    def extractAllInformation(self, text):
        """
        Mengekstrak semua informasi dari CV
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            dict: Dictionary dengan semua informasi yang diekstrak
            
        TODO:
        - Panggil semua metode ekstraksi
        - Gabungkan hasil dalam format standar
        - Tangani error dari masing-masing ekstraktor
        """
        pass

    def cleanseText(self, text):
        
        # 1. Normalize unicode
        cleaned_text = unicodedata.normalize('NFKC', text)

        # 2. Remove non-visual characters
        cleaned_text = re.sub(r'[\x00-\x1F\x7F]', '', cleaned_text)

        # 3. Remove bullet and other unneccessary symbols
        cleaned_text = re.sub(r'[•▪●◦\uf0b7\u2022\u25cf]', '', cleaned_text)

        # 4. Remove extra whitspace
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

        # 5. Remove extra white space and beginning and end of string
        cleaned_text = cleaned_text.strip()

        # 6. Clean up spacing around punctuation
        cleaned_text = re.sub(r'\s+([,.;:!?])', r'\1', cleaned_text)  # Remove space before punctuation
        
        return cleaned_text
    

    def cleanseTextN(self, text):
        """
        cleanse text but keep the newlines
        """
        # 1. Normalize unicode
        cleaned_text = unicodedata.normalize('NFKC', text)

        # 2. Remove non-visual characters
        cleaned_text = re.sub(r'[\x00-\x09\x0B-\x1F\x7F]', '', cleaned_text)

        # 3. Remove bullet and other unneccessary symbols
        cleaned_text = re.sub(r'[•▪●◦\uf0b7\u2022\u25cf]', '', cleaned_text)

        # 4. Remove extra whitspace
        # 4. Clean multiple spaces/tabs but keep single newlines
        cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)  # Multiple spaces/tabs -> single space
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)  # Multiple newlines -> double newline max

        # 5. Remove extra white space and beginning and end of string
        cleaned_text = cleaned_text.strip()

        # 6. Clean up spacing around punctuation
        cleaned_text = re.sub(r'\s+([,.;:!?])', r'\1', cleaned_text)  # Remove space before punctuation
        
        return cleaned_text
    
    def seperatePunctuations(self, text):
        """
        Memisahkan semua tanda baca dalam teks dengan sebuah spasi.
        Contoh: "Hello,world!" -> "Hello , world !"
                "Test.One" -> "Test . One"
                "Buy 1 get 1." -> "Buy 1 get 1 ."
                "end-to-end" -> "end - to - end" (jika '-' dianggap dipisah)

        Args:
            text (str): String teks yang akan diproses.

        Returns:
            str: String teks dengan tanda baca yang sudah dipisahkan spasi.
        """
        if not text:
            return ""
        # 1. Add whitespace sebelum punctuation
        text = re.sub(r'(\S)([^\w\s])', r'\1 \2', text)

        # 2. Add whitespace setelah punctuation
        text = re.sub(r'([^\w\s])(\S)', r'\1 \2', text)

        # 3. Remove every extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text