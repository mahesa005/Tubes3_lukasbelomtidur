# ===== src/database/seedData.py =====
"""
Seeding Data untuk Database ATS
Tujuan: Mengisi database dengan data sampel untuk pengujian dan pengembangan
"""

import csv
import os
from pathlib import Path
from .connection import DatabaseConnection
from .models import ApplicantProfile, ApplicationDetail
from config import RESUME_CSV_PATH, DATA_DIR
import logging

class DataSeeder:
    """
    Kelas untuk melakukan seeding data ke database
    
    TODO:
    - Memuat data dari Resume.csv
    - Membuat profil pelamar
    - Menghubungkan file CV dengan record database
    - Menangani bulk insert untuk performa
    """
    
    def __init__(self):
        """Inisialisasi data seeder"""
        self.db = DatabaseConnection()
        self.logger = logging.getLogger(__name__)
    
    def seedFromCSV(self):
        """
        Seeding data dari file Resume.csv
        
        TODO:
        - Membaca file Resume.csv
        - Mem-parsing data CV
        - Membuat profil pelamar
        - Memasukkan ke database
        - Menghubungkan dengan file PDF yang sesuai
        """
        pass
    
    def generateSampleApplicants(self, count=50):
        """
        Membuat data pelamar sampel
        
        Args:
            count (int): Jumlah sampel yang akan dibuat
            
        TODO:
        - Membuat data pelamar yang realistis
        - Nama, email, dan nomor telepon yang beragam
        - Alamat acak
        """
        pass
    
    def linkCVFiles(self):
        """
        Menghubungkan file CV dengan record database
        
        TODO:
        - Memindai direktori data untuk file PDF
        - Mencocokkan dengan record di database
        - Memperbarui cv_path di ApplicationDetail
        """
        pass
    
    def clearAllData(self):
        """
        Menghapus semua data dari database (untuk memulai dari awal)
        
        TODO:
        - Mengosongkan semua tabel
        - Mereset auto increment
        - Menangani foreign key constraints
        """
        pass
    
    def seedTestData(self):
        """
        Seeding data untuk pengujian
        
        TODO:
        - Membuat dataset minimal untuk pengujian
        - Menyertakan edge case
        - Memastikan konsistensi data
        """
        pass
