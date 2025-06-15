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
            r'\b0\d{9,12}\b',  # Format Indonesia, hanya angka, mulai dari 0
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
        return re.findall(self.emailPattern, text)

    def extractPhone(self, text):
        """
        Mengekstrak nomor telepon dari teks (semua format, hasil mentah)
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar nomor telepon yang ditemukan
        """
        phones = []
        for pattern in self.phonePatterns:
            phones.extend(re.findall(pattern, text))
        return phones

    def extractPhones(self, text, digit_length=12):
        """
        Mengekstrak nomor telepon dari teks, hasil hanya digit dan panjang sesuai database
        """
        phones = []
        for pattern in self.phonePatterns:
            phones.extend(re.findall(pattern, text))
        # Bersihkan: hanya digit
        clean_phones = [re.sub(r'\D', '', phone) for phone in phones]
        # Filter panjang sesuai kebutuhan (default 12 digit)
        clean_phones = [phone for phone in clean_phones if len(phone) == digit_length]
        return clean_phones

    def extractSummary(self, text):
        """
        Mengekstrak ringkasan/tujuan dari CV (contoh sederhana: ambil paragraf pertama)
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            str: Teks ringkasan atau string kosong
            
        TODO:
        - Cari bagian summary/objective/profile
        - Ekstrak paragraf yang relevan
        - Bersihkan hasil ekstraksi
        """
        paragraphs = [p.strip() for p in text.split('\n') if len(p.strip()) > 30]
        return paragraphs[0] if paragraphs else ""

    def extractSkills(self, text):
        """
        Mengekstrak keterampilan dari CV (contoh: cari baris dengan kata 'Skill' lalu split koma)
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar keterampilan yang ditemukan
            
        TODO:
        - Cari bagian skills/competencies
        - Ekstrak keterampilan satu per satu
        - Tangani berbagai format (poin, dipisahkan koma, dll)
        """
        skills = []
        for line in text.split('\n'):
            if 'skill' in line.lower():
                # Ambil setelah ':' jika ada
                if ':' in line:
                    skill_line = line.split(':', 1)[1]
                else:
                    skill_line = line
                skills = [s.strip() for s in re.split(r',|;', skill_line) if s.strip()]
                break
        return skills

    def extractExperience(self, text):
        """
        Mengekstrak pengalaman kerja dari CV (contoh sederhana: cari baris dengan 'Experience' dan ambil 3 baris setelahnya)
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar dict dengan informasi pekerjaan
            
        TODO:
        - Cari bagian pengalaman kerja/riwayat pekerjaan
        - Ekstrak jabatan, perusahaan, tanggal
        - Parsing deskripsi pekerjaan
        """
        experiences = []
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if 'experience' in line.lower():
                for j in range(1, 4):
                    if i + j < len(lines):
                        exp_line = lines[i + j].strip()
                        if exp_line:
                            experiences.append({'desc': exp_line})
                break
        return experiences

    def extractEducation(self, text):
        """
        Mengekstrak pendidikan dari CV (contoh sederhana: cari baris dengan 'Education' dan ambil 2 baris setelahnya)
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar dict dengan informasi pendidikan
            
        TODO:
        - Cari bagian pendidikan
        - Ekstrak gelar, institusi, tanggal kelulusan
        - Tangani berbagai format entri pendidikan
        """
        educations = []
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if 'education' in line.lower():
                for j in range(1, 3):
                    if i + j < len(lines):
                        edu_line = lines[i + j].strip()
                        if edu_line:
                            educations.append({'desc': edu_line})
                break
        return educations

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
        return {
            'emails': self.extractEmail(text),
            'phones': self.extractPhones(text),
            'summary': self.extractSummary(text),
            'skills': self.extractSkills(text),
            'experience': self.extractExperience(text),
            'education': self.extractEducation(text),
        }

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

# =====================
# Contoh format hasil ekstraksi:
#
# {
#   'emails': ['john.doe@email.com'],
#   'phones': ['081234567891'],
#   'summary': 'Professional with 5+ years experience...',
#   'skills': ['Python', 'SQL', 'Machine Learning'],
#   'experience': [
#       {'desc': 'Software Engineer at ABC Corp (2020-2023)'},
#       {'desc': 'Intern at XYZ (2019-2020)'
#   ],
#   'education': [
#       {'desc': 'S1 Informatika ITB 2016-2020'},
#       {'desc': 'SMA 1 Ciceeng 2013-2016'}
#   ]
# }
# =====================


# # from regexExtractor import RegexExtractor

# # Contoh teks CV sederhana untuk pengujian
# sample_text = '''
# Nama: John Doe
# Email: john.doe@email.com
# Phone: 081234567891, +62 812-3456-7890

# Summary:
# Professional with 5+ years experience in software engineering.

# Skills: Python, SQL, Machine Learning, Communication

# Experience:
# Software Engineer at ABC Corp (2020-2023)
# Intern at XYZ (2019-2020)

# Education:
# S1 Informatika ITB 2016-2020
# SMA 1 Bandung 2013-2016
# '''

# def main():
#     print("=== RegexExtractor Test ===\n")
#     extractor = RegexExtractor()

#     print("--- Testing extractEmail ---")
#     print(extractor.extractEmail(sample_text))

#     print("\n--- Testing extractPhones (hanya digit, 12 digit) ---")
#     print(extractor.extractPhones(sample_text, digit_length=12))

#     print("\n--- Testing extractPhone (semua format mentah) ---")
#     print(extractor.extractPhone(sample_text))

#     print("\n--- Testing extractSummary ---")
#     print(extractor.extractSummary(sample_text))

#     print("\n--- Testing extractSkills ---")
#     print(extractor.extractSkills(sample_text))

#     print("\n--- Testing extractExperience ---")
#     print(extractor.extractExperience(sample_text))

#     print("\n--- Testing extractEducation ---")
#     print(extractor.extractEducation(sample_text))

#     print("\n--- Testing extractAllInformation ---")
#     from pprint import pprint
#     pprint(extractor.extractAllInformation(sample_text))

#     print("\n=== Test Selesai ===\n")

# if __name__ == "__main__":
#     main()
# # 