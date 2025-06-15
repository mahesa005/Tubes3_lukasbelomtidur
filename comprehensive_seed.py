#!/usr/bin/env python3
"""
Comprehensive database seeding with ALL CV files
"""

import os
import sys
from pathlib import Path
import random

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

from database.connection import DatabaseConnection
from faker import Faker

def comprehensive_seed():
    """Seed database dengan SEMUA file CV yang ada"""
    
    print("🚀 Starting Comprehensive Database Seeding...")
    print("=" * 60)
    
    # Connect to database
    db = DatabaseConnection()
    if not db.connect():
        print("❌ Failed to connect to database")
        return
    
    try:
        # Clear existing data
        print("🧹 Clearing existing database data...")
        db.execute("SET FOREIGN_KEY_CHECKS=0;")
        db.execute("TRUNCATE TABLE ApplicationDetail;")
        db.execute("TRUNCATE TABLE ApplicantProfile;")
        db.execute("SET FOREIGN_KEY_CHECKS=1;")
        print("✅ Database cleared")
        
        # Find all CV files
        data_dir = current_dir / 'src' / 'archive' / 'data' / 'data'
        print(f"📁 Scanning directory: {data_dir}")
        
        all_cv_files = []
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith('.pdf'):
                    full_path = Path(root) / file
                    # Get relative path from project root
                    try:
                        rel_path = full_path.relative_to(current_dir)
                        all_cv_files.append({
                            'full_path': full_path,
                            'rel_path': str(rel_path).replace('\\', '/'),  # Normalize to forward slashes
                            'role': Path(root).name,
                            'filename': file
                        })
                    except ValueError:
                        # Skip files outside project directory
                        continue
        
        print(f"📊 Found {len(all_cv_files)} CV files")
        
        if len(all_cv_files) == 0:
            print("❌ No CV files found!")
            return
        
        # Initialize faker for generating dummy applicant data
        fake = Faker()
        
        # Process files in batches
        batch_size = 100
        total_processed = 0
        
        for i in range(0, len(all_cv_files), batch_size):
            batch = all_cv_files[i:i + batch_size]
            print(f"📦 Processing batch {i//batch_size + 1} ({len(batch)} files)...")
            
            for cv_file in batch:
                # Generate dummy applicant data
                first_name = fake.first_name()
                last_name = fake.last_name()
                dob = fake.date_of_birth(minimum_age=22, maximum_age=65)
                address = fake.address().replace("\n", ", ")
                phone = f"0812{random.randint(10_000_000, 99_999_999)}"
                
                # Insert applicant profile
                insert_profile = """
                    INSERT INTO ApplicantProfile
                    (first_name, last_name, date_of_birth, address, phone_number)
                    VALUES (%s, %s, %s, %s, %s)
                """
                params_profile = (first_name, last_name, dob, address, phone)
                
                if db.execute(insert_profile, params_profile):
                    applicant_id = db.cursor.lastrowid
                    
                    # Insert application detail
                    insert_detail = """
                        INSERT INTO ApplicationDetail
                        (applicant_id, application_role, cv_path)
                        VALUES (%s, %s, %s)
                    """
                    params_detail = (applicant_id, cv_file['role'], cv_file['rel_path'])
                    
                    if db.execute(insert_detail, params_detail):
                        total_processed += 1
                    else:
                        print(f"❌ Failed to insert ApplicationDetail for {cv_file['filename']}")
                else:
                    print(f"❌ Failed to insert ApplicantProfile for {cv_file['filename']}")
            
            # Progress update
            print(f"   ✅ Batch complete. Total processed: {total_processed}")
        
        print("\n" + "=" * 60)
        print(f"🎉 Comprehensive seeding completed!")
        print(f"   📊 Total files processed: {total_processed}")
        print(f"   📈 Database entries created: {total_processed}")
        
        # Verify results
        cursor = db.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM ApplicantProfile")
        profile_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM ApplicationDetail")
        detail_count = cursor.fetchone()[0]
        cursor.close()
        
        print(f"   ✅ ApplicantProfile records: {profile_count}")
        print(f"   ✅ ApplicationDetail records: {detail_count}")
        
        if total_processed == len(all_cv_files):
            print("🎯 SUCCESS: All CV files have been added to database!")
        else:
            print(f"⚠️  WARNING: {len(all_cv_files) - total_processed} files were not processed")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.disconnect()

if __name__ == "__main__":
    comprehensive_seed()
