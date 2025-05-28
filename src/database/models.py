"""
Model Database untuk Sistem ATS
Tujuan: Mendefinisikan skema database dan model ORM
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class ApplicantProfile:
    """
    Model untuk tabel ApplicantProfile
    
    TODO:
    - Definisikan semua field yang dibutuhkan
    - Tambahkan metode validasi
    - Implementasi enkripsi/dekripsi untuk data sensitif (bonus)
    """
    
    applicant_id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def validate(self):
        """
        Validasi data profil pelamar
        
        Returns:
            bool: True jika valid, False jika tidak
            
        TODO:
        - Validasi format email
        - Validasi nomor telepon
        - Cek field yang wajib diisi
        """
        pass
    
    def toDict(self):
        """Konversi model ke dictionary"""
        pass

@dataclass  
class ApplicationDetail:
    """
    Model untuk tabel ApplicationDetail
    
    TODO:
    - Definisikan relasi dengan ApplicantProfile
    - Tambahkan field status pemrosesan CV
    - Sertakan informasi hasil ekstraksi CV
    """
    
    application_id: Optional[int] = None
    applicant_id: int = 0
    position_applied: str = ""
    cv_path: str = ""
    cv_text: str = ""
    extracted_summary: str = ""
    extracted_skills: str = ""
    extracted_experience: str = ""
    extracted_education: str = ""
    application_date: Optional[datetime] = None
    status: str = "pending"  # pending, processed, reviewed
    
    def validate(self):
        """Validasi data ApplicationDetail"""
        pass
    
    def toDict(self):
        """Konversi model ke dictionary"""
        pass

class DatabaseSchema:
    """
    Skema database
    
    TODO:
    - Definisikan perintah CREATE TABLE
    - Tambahkan index untuk performa
    - Definisikan relasi foreign key
    """
    
    CREATE_APPLICANT_PROFILE = """
    CREATE TABLE IF NOT EXISTS ApplicantProfile (
        applicant_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone VARCHAR(20),
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """
    
    CREATE_APPLICATION_DETAIL = """
    CREATE TABLE IF NOT EXISTS ApplicationDetail (
        application_id INT AUTO_INCREMENT PRIMARY KEY,
        applicant_id INT NOT NULL,
        position_applied VARCHAR(200),
        cv_path VARCHAR(500) NOT NULL,
        cv_text LONGTEXT,
        extracted_summary TEXT,
        extracted_skills TEXT,
        extracted_experience TEXT,
        extracted_education TEXT,
        application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status ENUM('pending', 'processed', 'reviewed') DEFAULT 'pending',
        FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id)
    )
    """