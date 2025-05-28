"""
Utilitas logging untuk aplikasi ATS
Tujuan: Konfigurasi logging terpusat
"""

import logging
import os
from datetime import datetime
from Tubes3_plscukup.config import LOG_LEVEL, LOG_FILE

def setupLogger():
    """
    Menyiapkan logger aplikasi
    
    Mengembalikan:
        logging.Logger: Instance logger yang sudah dikonfigurasi
        
    TODO:
    - Membuat direktori log jika belum ada
    - Mengkonfigurasi handler file dan konsol
    - Mengatur format log
    - Mengatur level log
    """
    pass

def getLogger(name):
    """
    Mendapatkan logger untuk modul tertentu
    
    Argumen:
        name (str): Nama logger (biasanya __name__)
        
    Mengembalikan:
        logging.Logger: Instance logger
    """
    pass