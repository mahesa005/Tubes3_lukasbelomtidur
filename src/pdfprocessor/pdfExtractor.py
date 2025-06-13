# ===== src/pdfProcessor/pdfExtractor.py =====
"""
Modul Ekstraksi Teks PDF
Tujuan: Ekstraksi teks dari file PDF CV
"""

import pypdf
from pathlib import Path
import logging
import os

class PDFExtractor:
    """
    Kelas untuk ekstraksi teks dari file PDF
    
    TODO:
    - Implementasi ekstraksi menggunakan PyPDF2
    - Implementasi ekstraksi menggunakan pdfplumber
    - Menangani berbagai format PDF
    - Optimasi untuk performa
    """
    
    def __init__(self):
        """Inisialisasi PDF extractor"""
        self.logger = logging.getLogger(__name__)
    
    def extractWithPyPDF2(self, pdfPath):
        """
        Ekstraksi teks menggunakan PyPDF2
        
        Argumen:
            pdfPath (str): Path ke file PDF
            
        Mengembalikan:
            str: Teks yang diekstrak
            
        TODO:
        - Buka file PDF
        - Ekstrak teks dari semua halaman
        - Menangani PDF terenkripsi
        - Membersihkan teks hasil ekstraksi
        """
        pass
    
    def extractWithPdfplumber(self, pdfPath):
        """
        Ekstraksi teks menggunakan pdfplumber (lebih akurat)
        
        Argumen:
            pdfPath (str): Path ke file PDF
            
        Mengembalikan:
            str: Teks yang diekstrak
            
        TODO:
        - Gunakan pdfplumber untuk ekstraksi
        - Menangani ekstraksi tabel
        - Menjaga format yang penting
        """
        pass
    
    def extractText(self, pdfPath, method='pdfplumber'):
        """
        Ekstraksi teks dengan metode yang dipilih
        
        Argumen:
            pdfPath (str): Path ke file PDF
            method (str): Metode ekstraksi ('pypdf2' atau 'pdfplumber')
            
        Mengembalikan:
            str: Teks yang diekstrak
            
        TODO:
        - Pilih metode ekstraksi
        - Fallback ke metode lain jika gagal
        - Penanganan error
        - Pembersihan teks
        """
        pass
    
    def cleanText(self, text):
        """
        Membersihkan teks hasil ekstraksi
        
        Argumen:
            text (str): Teks mentah dari PDF
            
        Mengembalikan:
            str: Teks yang sudah dibersihkan
            
        TODO:
        - Menghapus spasi berlebih
        - Memperbaiki pemisah baris
        - Menghapus karakter khusus yang tidak perlu
        - Normalisasi encoding
        """
        pass
    
    def extractMetadata(self, pdfPath):
        """
        Ekstraksi metadata dari PDF
        
        Argumen:
            pdfPath (str): Path ke file PDF
            
        Mengembalikan:
            dict: Metadata PDF
            
        TODO:
        - Ekstrak author, judul, tanggal pembuatan
        - Ekstrak jumlah halaman
        - Informasi ukuran file
        """
        pass

    # Versi mahesa
    def PDFextract(self, pdfPath):
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
        except pypdf.errors.PdfReadError: # Error class juga disesuaikan
            print(f"Error: Gagal membaca file PDF {pdfPath}. Mungkin terenkripsi atau rusak.")
            return ""
        except Exception as e:
            print(f"Terjadi error tak terduga saat memproses {pdfPath}: {e}")
            return ""
        return full_text.strip()




# Tester
def main():
        """Main function untuk debugging dan testing"""
        print("=== PDF Extractor Debug Mode ===\n")
        
        # Inisialisasi extractor
        extractor = PDFExtractor()
        
        output = extractor.PDFextract(r"C:\Users\Mahesa\OneDrive\ITB\Coding\College\Academic\IF\Smt-4\Strategi Algoritma\Tubes\Tubes 3\Tubes3_lukasbelomtidur\src\archive\data\data\ACCOUNTANT\10554236.pdf")

        print(output)
if __name__ == "__main__":
        main()



