"""
Utilitas logging untuk aplikasi ATS
Tujuan: Konfigurasi logging terpusat
"""

import logging
import os
from datetime import datetime
from config import LOG_LEVEL, LOG_FILE

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
    logger = logging.getLogger("ATSLogger")
    logger.setLevel(LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler
    if LOG_FILE:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.propagate = False
    return logger

def getLogger(name):
    """
    Mendapatkan logger untuk modul tertentu
    
    Argumen:
        name (str): Nama logger (biasanya __name__)
        
    Mengembalikan:
        logging.Logger: Instance logger
    """
    pass