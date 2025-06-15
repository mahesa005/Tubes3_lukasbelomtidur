#!/usr/bin/env python3
"""
Check what names are actually in the database vs seeding.sql
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.connection import DatabaseConnection

def check_database_names():
    """Check what names are in the database"""
    
    try:
        db = DatabaseConnection()
        db.connect()
        cursor = db.connection.cursor()
        
        # Get all names from database
        cursor.execute("""
            SELECT ap.first_name, ap.last_name, ad.cv_path, ap.applicant_id
            FROM applicantprofile ap
            JOIN applicationdetail ad ON ad.application_id = ap.applicant_id
            ORDER BY ap.first_name, ap.last_name
        """)
        
        results = cursor.fetchall()
        
        print(f"📋 Names in database ({len(results)} total):")
        print("-" * 60)
        
        james_found = []
        for first_name, last_name, cv_path, applicant_id in results:
            full_name = f"{first_name} {last_name}"
            print(f"   {applicant_id:3d} | {full_name:25s} | {cv_path}")
            
            # Check for James specifically
            if first_name.lower() == "james":
                james_found.append((full_name, cv_path))
        
        print(f"\n🔍 James entries found: {len(james_found)}")
        for name, path in james_found:
            print(f"   {name} -> {path}")
        
        # Check for Jones specifically
        cursor.execute("""
            SELECT ap.first_name, ap.last_name, ad.cv_path
            FROM applicantprofile ap
            JOIN applicationdetail ad ON ad.application_id = ap.applicant_id
            WHERE ap.last_name LIKE '%Jones%'
        """)
        
        jones_results = cursor.fetchall()
        print(f"\n🔍 Jones entries found: {len(jones_results)}")
        for first_name, last_name, cv_path in jones_results:
            print(f"   {first_name} {last_name} -> {cv_path}")
        
        db.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database_names()
