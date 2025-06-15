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
from src.pdfprocessor.regexExtractor import RegexExtractor

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

