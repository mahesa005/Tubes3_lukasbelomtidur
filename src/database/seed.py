import csv
import os
import logging
import random
from pathlib import Path
from faker import Faker
from config import DATABASE_CONFIG

from .connection import DatabaseConnection
from config import RESUME_CSV_PATH, DATA_DIR


class DataSeeder:
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

    def generateSampleApplicants(self, count=10):

        # 1) buka koneksi ke database
        if not self.db.connect():
            self.logger.error("generateSampleApplicants: Gagal koneksi.")
            return

        fake = Faker()
        base_data_dir = Path(DATA_DIR)

        role_dirs = [d for d in base_data_dir.iterdir() if d.is_dir()]
        if not role_dirs:
            self.logger.error(f"generateSampleApplicants: Tidak ada subfolder di {base_data_dir}")
            self.db.disconnect()
            return

        for _ in range(count):
            # dummy si AP
            first_name = fake.first_name()
            last_name  = fake.last_name()
            dob = fake.date_of_birth(minimum_age=18, maximum_age=60)
            address    = fake.address().replace("\n", ", ")
            phone      = f"0812{random.randint(10_000_000, 99_999_999)}"

            # insert ke AP
            insert_profile = """
                INSERT INTO ApplicantProfile
                  (first_name, last_name, date_of_birth, address, phone_number)
                VALUES (%s, %s, %s,%s, %s)
            """
            params_profile = (first_name, last_name, dob, address, phone)

            if not self.db.execute(insert_profile, params_profile):
                self.logger.error("generateSampleApplicants: Gagal insert dummy applicant ke ApplicantProfile")
                continue  # lanjutkan ke kandidat berikutnya

            # ambil applicant_id yang baru aja di‐insert
            new_applicant_id = self.db.cursor.lastrowid
            self.logger.info(
                f"generateSampleApplicants: Inserted ApplicantProfile → "
                f"id={new_applicant_id}, name={first_name} {last_name}, phone={phone}"
            )

            # pilih 1 folder dari folder data
            chosen_role_dir = random.choice(role_dirs)
            application_role = chosen_role_dir.name

            # milih pdf dari folder itu
            pdf_files = list(chosen_role_dir.glob("*.pdf"))
            if not pdf_files:
                self.logger.warning(
                    f"generateSampleApplicants: Folder '{application_role}' kosong (tidak ada PDF), "
                    f"skipping ApplicationDetail untuk applicant_id={new_applicant_id}"
                )
                continue

            chosen_pdf = random.choice(pdf_files)
            cv_path = str(chosen_pdf)

            # insert ke AD
            insert_detail = """
                INSERT INTO ApplicationDetail
                  (applicant_id, application_role, cv_path)
                VALUES (%s, %s, %s)
            """
            params_detail = (new_applicant_id, application_role, cv_path)

            if self.db.execute(insert_detail, params_detail):
                self.logger.info(
                    f"generateSampleApplicants: Inserted ApplicationDetail → "
                    f"applicant_id={new_applicant_id}, role='{application_role}', cv='{cv_path}'"
                )
            else:
                self.logger.error(
                    f"generateSampleApplicants: Gagal insert ApplicationDetail untuk applicant_id={new_applicant_id}"
                )

        # trus tutup
        self.db.disconnect()

    def seedTestData(self):
        self.logger.info("seedTestData: Mulai seeding.")
        self.clearAllData()
        self.generateSampleApplicants(20)
        self.logger.info("seedTestData: Selesai seeding.")

def main():
    db_name = DATABASE_CONFIG['database']
    db = DatabaseConnection()

    if not db.dropDatabase(db_name):
        return

    if not db.createDatabase(db_name):
        return

    if not db.connect():
        return
    if not db.useDatabase(db_name):
        return

    db.createTables()

    seeder = DataSeeder()
    seeder.db = db

    seeder.clearAllData()
    seeder.generateSampleApplicants(30)

    db.disconnect()

if __name__ == "__main__":
    main()