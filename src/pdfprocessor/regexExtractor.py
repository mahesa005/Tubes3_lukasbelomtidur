# ===== src/pdfProcessor/regexExtractor.py =====
"""
Ekstraksi Informasi Berbasis Regex dari CV
Tujuan: Mengekstrak informasi spesifik dari teks CV menggunakan regex
"""

import re
from datetime import datetime
import logging

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

    def removeAllNewLine(self, text):
        """
        Menghilangkan seluruh newline dari string
        """
        newLinePattern = r'\n' 
        cleanString = re.sub(newLinePattern, '', text)

        return cleanString