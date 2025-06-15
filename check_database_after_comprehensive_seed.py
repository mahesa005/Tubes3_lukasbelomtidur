#!/usr/bin/env python3
"""
Check database after comprehensive seeding to see what paths are actually stored
"""

import sys
import os
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

from database.connection import DatabaseConnection

def check_database_content():
    """Check what paths are stored in the database after comprehensive seeding"""
    
    try:
        # Initialize database connection
        db = DatabaseConnection()
        if not db.connect():
            print("❌ Failed to connect to database")
            return
              # Get total count
        db.execute("SELECT COUNT(*) FROM applicantprofile")
        total_count = db.cursor.fetchone()[0]
        print(f"📊 Total entries in database: {total_count}")
        
        # Get first 10 entries to see path format
        db.execute("""
            SELECT ap.application_id, ap.full_name, ad.file_path 
            FROM applicantprofile ap 
            JOIN applicationdetail ad ON ap.application_id = ad.application_id 
            LIMIT 10
        """)
        
        entries = db.cursor.fetchall()
        print(f"\n🔍 Sample database entries:")
        for app_id, name, path in entries:
            print(f"   {app_id} | {name} | {path}")
        
        # Check if there are any paths that match the search patterns
        # The search generates paths like: "C:\Users\MSI\Desktop\tubes3stima\..."
        search_prefix = "C:/Users/MSI/Desktop/tubes3stima/Tubes3_lukasbelomtidur/Tubes3_lukasbelomtidur/src/archive/data/data"
        
        db.execute("""
            SELECT ap.application_id, ad.file_path 
            FROM applicantprofile ap 
            JOIN applicationdetail ad ON ap.application_id = ad.application_id 
            WHERE ad.file_path LIKE %s
            LIMIT 5
        """, (f"{search_prefix}%",))
        
        matching_entries = db.cursor.fetchall()
        print(f"\n🎯 Entries matching search path pattern (starting with {search_prefix}):")
        if matching_entries:
            for app_id, path in matching_entries:
                print(f"   {app_id} | {path}")
        else:
            print("   ❌ No entries found matching the search path pattern")
        
        # Check what the actual path format looks like
        db.execute("""
            SELECT DISTINCT SUBSTR(ad.file_path, 1, 100) as path_prefix
            FROM applicationdetail ad 
            LIMIT 5
        """)
        
        path_prefixes = db.cursor.fetchall()
        print(f"\n📁 Sample path prefixes in database:")
        for prefix, in path_prefixes:
            print(f"   {prefix}...")
        
        db.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database_content()
