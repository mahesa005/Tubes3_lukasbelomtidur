# ===== src/pdfProcessor/pdfExtractor.py =====
"""
Modul Ekstraksi Teks PDF
Tujuan: Ekstraksi teks dari file PDF CV
"""

import pypdf
from .regexExtractor import RegexExtractor
import logging
import os
from pathlib import Path

class PDFExtractor:
    """
    Kelas untuk ekstraksi teks dari file PDF
    """
    
    def __init__(self):
        """Inisialisasi PDF extractor"""
        self.logger = logging.getLogger(__name__)
    
    
    def cleanText(self, text):
        """
        Membersihkan teks hasil ekstraksi
        
        Argumen:
            text (str): Teks mentah dari PDF
            
        Mengembalikan:
            str: Teks yang sudah dibersihkan
        """
        regex = RegexExtractor()    
        full_text = regex.cleanseTextN(text)
        return full_text

    # Versi mahesa
    def PDFtoText(self, pdfPath):
        """
        Extract pdf text into string (still include newlines)
        """
        try:
            if not os.path.exists(pdfPath):
                print(f"Error: File PDF tidak ditemukan pada: {pdfPath}")

            full_text = ""
            with open(pdfPath, 'rb') as file:
                # Create object reader
                reader = pypdf.PdfReader(file)
                # Extract pages
                pageTotal = len(reader.pages)

                for page_num in range(pageTotal):
                    page = reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        cleaned_text = page_text.strip()
                        full_text += cleaned_text + "\n"
        except pypdf.errors.PdfReadError:
            print(f"Error: Gagal membaca file PDF {pdfPath}. Mungkin terenkripsi atau rusak.")
            return ""
        except Exception as e:
            print(f"Terjadi error tak terduga saat memproses {pdfPath}: {e}")
            return ""
        return full_text.strip()
    

    def PDFExtractForMatch(self, pdfPath):
        """
        Extract pdf text into string (remove newline) for summary
        """
        regex = RegexExtractor()
        # result string with all newline removed
        result = regex.cleanseText(self.PDFtoText(pdfPath))
        return result



# def main():
#     print("=== PDF Extractor Test ===\n")

#     # Inisialisasi extractor
#     extractor = PDFExtractor()
#     regex_cleaner = RegexExtractor() # Mungkin tidak perlu inisialisasi di sini jika sudah di PDFExtractor
    
#     # Path ke file PDF yang akan diuji
#     # Pastikan ini benar-benar sesuai dengan lokasi file Anda
#     # Menggunakan Path dari pathlib untuk penanganan path yang lebih robust
#     pdf_file_path = Path("C:/Users/Mahesa/OneDrive/ITB/Coding/College/Academic/IF/Smt-4/Strategi Algoritma/Tubes/Tubes 3/Tubes3_lukasbelomtidur/src/archive/data/data/ACCOUNTANT/10554236.pdf")

#     # --- Test PDFtoText (ekstraksi mentah dengan newline antar halaman) ---
#     print("--- Testing PDFtoText ---")
#     extracted_raw_text = extractor.PDFtoText(str(pdf_file_path)) # Pastikan pass string path
#     if extracted_raw_text:
#         print("\n[SUCCESS] Teks mentah (dengan newline) berhasil diekstrak:")
#         print("--------------------------------------------------")
#         print(extracted_raw_text[:500]) # Tampilkan 500 karakter pertama
#         print("...")
#         print(f"Total karakter: {len(extracted_raw_text)}")
#         print("--------------------------------------------------")
#     else:
#         print("[FAILED] Gagal mengekstrak teks menggunakan PDFtoText.")

#     # --- Test cleanText (membersihkan teks menggunakan RegexExtractor.cleanseTextN) ---
#     print("\n--- Testing cleanText (via RegexExtractor.cleanseTextN) ---")
#     if extracted_raw_text:
#         cleaned_text_n = extractor.cleanText(extracted_raw_text)
#         print("\n[SUCCESS] Teks dibersihkan (dengan newline antar halaman) menggunakan cleanText:")
#         print("--------------------------------------------------")
#         print(cleaned_text_n[:500]) # Tampilkan 500 karakter pertama
#         print("...")
#         print(f"Total karakter setelah cleanText: {len(cleaned_text_n)}")
#         print("--------------------------------------------------")
#     else:
#         print("[SKIP] cleanText test skipped because PDFtoText failed.")

#     # --- Test PDFExtractForMatch (ekstraksi teks tanpa newline untuk matching) ---
#     print("\n--- Testing PDFExtractForMatch (via RegexExtractor.cleanseText) ---")
#     extracted_text_for_match = extractor.PDFExtractForMatch(str(pdf_file_path)) # Pastikan pass string path
#     if extracted_text_for_match:
#         print("\n[SUCCESS] Teks diekstrak dan diratakan (tanpa newline) untuk matching:")
#         print("--------------------------------------------------")
#         print(extracted_text_for_match[:500]) # Tampilkan 500 karakter pertama
#         print("...")
#         print(f"Total karakter setelah PDFExtractForMatch: {len(extracted_text_for_match)}")
#         print(f"Apakah ada newline di 500 karakter pertama? {'\\n' in extracted_text_for_match[:500]}")
#         print("--------------------------------------------------")
#     else:
#         print("[FAILED] Gagal mengekstrak teks menggunakan PDFExtractForMatch.")

#     print("\n=== Test Selesai ===\n")

# if __name__ == "__main__":
#     main()
