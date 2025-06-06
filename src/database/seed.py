# ===== src/database/seed.py =====
"""
Script utama untuk membuat tabel dan melakukan seeding data ke database ATS.
Menggabungkan:
  1. DatabaseConnection.createTables() – memastikan tabel dibuat.
  2. Seeding data (dari Resume.csv & sampel dummy).
"""

import csv
import os
import logging
import random
from pathlib import Path

from .connection import DatabaseConnection
from config import RESUME_CSV_PATH, DATA_DIR


class DataSeeder:
    """
    Kelas untuk melakukan seeding data ke database.
    """

    def __init__(self):
        self.db = DatabaseConnection()
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            h = logging.StreamHandler()
            fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            h.setFormatter(fmt)
            self.logger.addHandler(h)
            self.logger.setLevel(logging.INFO)

    def clearAllData(self):
        """
        Truncate tabel ApplicantProfile & ApplicationDetail.
        """
        if not self.db.connect():
            self.logger.error("clearAllData: Gagal koneksi.")
            return

        try:
            self.db.execute("SET FOREIGN_KEY_CHECKS=0;")
            self.db.execute("TRUNCATE TABLE ApplicationDetail;")
            self.db.execute("TRUNCATE TABLE ApplicantProfile;")
            self.db.execute("SET FOREIGN_KEY_CHECKS=1;")
            self.logger.info("clearAllData: Semua tabel ditruncate.")
        except Exception as e:
            self.logger.error(f"clearAllData: {e}")
        finally:
            self.db.disconnect()

    def seedFromCSV(self):
        """
        Membaca Resume.csv dan insert ke ApplicantProfile:
          (name, email, phone, resume_path)

        Karena CSV hanya punya kolom ID, Resume_str, Resume_html, Category,
        kita gunakan ID sebagai 'name', email & phone dibiarkan NULL,
        dan resume_path dari file PDF di DATA_DIR/<Category>/<ID>.pdf.
        """
        if not self.db.connect():
            self.logger.error("seedFromCSV: Gagal koneksi.")
            return

        if not RESUME_CSV_PATH.exists():
            self.logger.error(f"seedFromCSV: Resume.csv tidak ditemukan di {RESUME_CSV_PATH}")
            self.db.disconnect()
            return

        inserted = 0
        with open(RESUME_CSV_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                external_id_raw = row.get("ID", "").strip()
                category       = row.get("Category", "").strip()

                if not external_id_raw or not category:
                    self.logger.warning(f"seedFromCSV: Data kurang lengkap, skip → {row}")
                    continue

                # Nama file PDF: "<ID>.pdf"
                pdf_path = Path(DATA_DIR) / category / f"{external_id_raw}.pdf"
                if not pdf_path.exists():
                    self.logger.warning(f"seedFromCSV: PDF tidak ditemukan → {pdf_path}")
                    continue

                # Karena tabel ApplicantProfile punya kolom (name, email, phone, resume_path)
                insert_query = """
                    INSERT INTO ApplicantProfile (name, email, phone, resume_path)
                    VALUES (%s, %s, %s, %s)
                """
                params = (
                    external_id_raw,  # menyimpan ID sebagai 'name'
                    None,             # email tidak tersedia di CSV
                    None,             # phone tidak tersedia
                    str(pdf_path)
                )

                if self.db.execute(insert_query, params):
                    inserted += 1
                    self.logger.info(f"seedFromCSV: Inserted ID={external_id_raw}")
                else:
                    self.logger.error(f"seedFromCSV: Gagal insert ID={external_id_raw}")

        self.logger.info(f"seedFromCSV: Total baris di‐insert → {inserted}")
        self.db.disconnect()

    def generateSampleApplicants(self, count=10):
        """
        Membuat data dummy untuk ApplicantProfile (name/email/phone/resume_path).
        """
        if not self.db.connect():
            self.logger.error("generateSampleApplicants: Gagal koneksi.")
            return

        inserted = 0
        for i in range(1, count + 1):
            name        = f"SampleUser{i}"
            email       = f"user{i}@example.com"
            phone       = f"0812{random.randint(10000000, 99999999)}"
            resume_path = None

            insert_query = """
                INSERT INTO ApplicantProfile (name, email, phone, resume_path)
                VALUES (%s, %s, %s, %s)
            """
            params = (name, email, phone, resume_path)

            if self.db.execute(insert_query, params):
                inserted += 1
            else:
                self.logger.error(f"generateSampleApplicants: Gagal insert dummy {name}")

        self.logger.info(f"generateSampleApplicants: Total dummy di‐insert → {inserted}")
        self.db.disconnect()

    def linkCVFiles(self):
        """
        (Opsional) Jika ada baris yang resume_path= NULL, cari PDF berdasar nama file.
        Karena kita sudah meng‐insert dari CSV, biasanya resume_path sudah terisi.
        Namun jika ada yang kosong (misal dummy), Anda bisa skip atau implementasi sendiri.
        """
        # Dalam skema ini, kita tidak melakukan update lagi.
        self.logger.info("linkCVFiles: Tidak ada aksi karena resume_path sudah di-handle.")

    def seedTestData(self):
        """
        1. clearAllData()
        2. seedFromCSV() jika ada Resume.csv
        3. generateSampleApplicants() untuk tambahan dummy
        4. linkCVFiles() (tidak wajib)
        """
        self.logger.info("seedTestData: Mulai seeding.")
        self.clearAllData()

        if RESUME_CSV_PATH.exists():
            self.seedFromCSV()
        else:
            self.logger.warning("seedTestData: Resume.csv tidak ditemukan, skip seedFromCSV().")

        self.generateSampleApplicants(count=10)
        # linkCVFiles tidak melakukan apapun di contoh ini
        self.logger.info("seedTestData: Selesai seeding.")

def main():
    """
    1. Buat tabel lewat DatabaseConnection.createTables()
    2. Jalankan DataSeeder.seedTestData()
    """
    # Setup logger
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        h = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        h.setFormatter(fmt)
        logger.addHandler(h)
        logger.setLevel(logging.INFO)

    # 1. Create/update tabel
    db = DatabaseConnection()
    logger.info("main: Memulai pembuatan/memperbarui tabel.")
    if db.connect():
        db.createTables()
        db.disconnect()
        logger.info("main: Tabel berhasil dibuat/diupdate.")
    else:
        logger.error("main: Gagal koneksi ke database.")
        return

    # 2. Seeding data
    logger.info("main: Mulai seeding data.")
    seeder = DataSeeder()
    seeder.seedTestData()
    logger.info("main: Proses seeding selesai.")

if __name__ == "__main__":
    main()
