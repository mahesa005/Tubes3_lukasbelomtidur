#!/usr/bin/env python3
"""
Enhanced seeding script to populate the database with ALL available CV files in the data directory.
This script will create applicant profiles for every PDF file found in the data directory.
"""

import sys
import os
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.connection import DatabaseConnection
from src.database.seed import DataSeeder
from faker import Faker
from config import DATA_DIR, DATABASE_CONFIG
import logging
import random

class ComprehensiveSeeder(DataSeeder):
    def __init__(self):
        super().__init__()
        self.fake = Faker()
        
    def seedAllCVFiles(self):
        """Seed the database with ALL CV files found in the data directory"""
        self.logger.info("Starting comprehensive seeding of all CV files...")
        
        if not self.db.connect():
            self.logger.error("Failed to connect to database")
            return False
        
        try:
            # Clear existing data
            self.clearAllData()
            
            # Get all PDF files from the data directory
            base_data_dir = Path(DATA_DIR)
            self.logger.info(f"Scanning directory: {base_data_dir}")
            
            if not base_data_dir.exists():
                self.logger.error(f"Data directory does not exist: {base_data_dir}")
                return False
            
            # Find all role directories
            role_dirs = [d for d in base_data_dir.iterdir() if d.is_dir()]
            if not role_dirs:
                self.logger.error(f"No role directories found in {base_data_dir}")
                return False
            
            total_files = 0
            total_inserted = 0
            
            # Process each role directory
            for role_dir in role_dirs:
                role_name = role_dir.name
                self.logger.info(f"Processing role: {role_name}")
                
                # Find all PDF files in this role directory
                pdf_files = list(role_dir.glob("*.pdf"))
                self.logger.info(f"Found {len(pdf_files)} PDF files in {role_name}")
                
                for pdf_file in pdf_files:
                    total_files += 1
                    
                    if self._insertCVFile(pdf_file, role_name):
                        total_inserted += 1
                    
                    # Log progress every 100 files
                    if total_files % 100 == 0:
                        self.logger.info(f"Processed {total_files} files, inserted {total_inserted}")
            
            self.logger.info(f"Seeding complete! Processed {total_files} files, successfully inserted {total_inserted}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during comprehensive seeding: {e}")
            return False
        finally:
            self.db.disconnect()
    
    def _insertCVFile(self, pdf_file, role_name):
        """Insert a single CV file into the database with a generated applicant profile"""
        try:
            # Generate fake applicant data
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            dob = self.fake.date_of_birth(minimum_age=18, maximum_age=60)
            address = self.fake.address().replace("\n", ", ")
            phone = f"0812{random.randint(10_000_000, 99_999_999)}"
            
            # Insert applicant profile
            insert_profile = """
                INSERT INTO ApplicantProfile
                  (first_name, last_name, date_of_birth, address, phone_number)
                VALUES (%s, %s, %s, %s, %s)
            """
            params_profile = (first_name, last_name, dob, address, phone)
            
            if not self.db.execute(insert_profile, params_profile):
                self.logger.error(f"Failed to insert applicant profile for {pdf_file.name}")
                return False
            
            # Get the new applicant ID
            new_applicant_id = self.db.cursor.lastrowid
            
            # Calculate the CV path relative to project root (using forward slashes)
            project_root = Path(__file__).resolve().parent
            try:
                cv_path = str(pdf_file.relative_to(project_root)).replace('\\', '/')
            except ValueError:
                # If pdf_file is not relative to project_root, use absolute path conversion
                cv_path = str(pdf_file).replace('\\', '/')
                # Try to make it relative to project root manually
                if str(project_root) in cv_path:
                    cv_path = cv_path.replace(str(project_root).replace('\\', '/') + '/', '')
            
            # Insert application detail
            insert_detail = """
                INSERT INTO ApplicationDetail
                  (applicant_id, application_role, cv_path)
                VALUES (%s, %s, %s)
            """
            params_detail = (new_applicant_id, role_name, cv_path)
            
            if self.db.execute(insert_detail, params_detail):
                self.logger.debug(f"Inserted: {first_name} {last_name} -> {role_name} -> {cv_path}")
                return True
            else:
                self.logger.error(f"Failed to insert application detail for {pdf_file.name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error inserting CV file {pdf_file}: {e}")
            return False

def main():
    """Main function to run comprehensive seeding"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    logger.info("Starting comprehensive database seeding...")
    
    # Verify database configuration
    logger.info(f"Database config: {DATABASE_CONFIG}")
    logger.info(f"Data directory: {DATA_DIR}")
    
    # Create the comprehensive seeder
    seeder = ComprehensiveSeeder()
    
    # Run the seeding
    success = seeder.seedAllCVFiles()
    
    if success:
        logger.info("✅ Comprehensive seeding completed successfully!")
        
        # Quick verification - count entries in database
        db = DatabaseConnection()
        if db.connect():
            try:
                result = db.fetchAll("SELECT COUNT(*) as count FROM ApplicationDetail")
                if result:
                    count = result[0]['count']
                    logger.info(f"Database now contains {count} CV entries")
            except Exception as e:
                logger.error(f"Error verifying database count: {e}")
            finally:
                db.disconnect()
    else:
        logger.error("❌ Comprehensive seeding failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
