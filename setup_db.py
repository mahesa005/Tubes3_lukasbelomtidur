#!/usr/bin/env python3
"""
Setup Database untuk ATS CV Matcher
Script untuk membuat database dan tabel yang diperlukan
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.connection import DatabaseConnection
from src.database.seed import DataSeeder
from config import DATABASE_CONFIG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Setup database dan tabel"""
    try:
        # Buat database connection instance
        db = DatabaseConnection()
        
        # Drop database lama jika ada (optional)
        db_name = DATABASE_CONFIG['database']
        logger.info(f"Setting up database: {db_name}")
        
        # Buat database baru
        if not db.createDatabase(db_name):
            logger.error("Gagal membuat database")
            return False
        
        # Connect ke database
        if not db.connect():
            logger.error("Gagal koneksi ke database")
            return False
        
        # Gunakan database
        if not db.useDatabase(db_name):
            logger.error("Gagal menggunakan database")
            return False
        
        # Buat tabel
        logger.info("Membuat tabel...")
        db.createTables()
        
        # Seed data sample (optional)
        logger.info("Seeding sample data...")
        seeder = DataSeeder()
        seeder.db = db
        seeder.generateSampleApplicants(30)
        
        db.disconnect()
        logger.info("Database setup berhasil!")
        return True
        
    except Exception as e:
        logger.error(f"Error setup database: {e}")
        return False

if __name__ == "__main__":
    success = setup_database()
    if success:
        print("✅ Database setup berhasil!")
        print("Database siap digunakan.")
    else:
        print("❌ Database setup gagal!")
        print("Periksa konfigurasi database di config.py")
