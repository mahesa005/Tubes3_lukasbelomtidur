#!/usr/bin/env python3
"""
Check the actual table structure
"""

import sys
import os
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

from database.connection import DatabaseConnection

def check_table_structure():
    """Check the actual structure of the tables"""
    
    try:
        # Initialize database connection
        db = DatabaseConnection()
        if not db.connect():
            print("❌ Failed to connect to database")
            return
            
        # Check structure of applicantprofile table
        print("🔍 Structure of applicantprofile table:")
        db.execute("DESCRIBE applicantprofile")
        columns = db.cursor.fetchall()
        for column in columns:
            print(f"   {column}")
        
        print("\n🔍 Structure of applicationdetail table:")
        db.execute("DESCRIBE applicationdetail")
        columns = db.cursor.fetchall()
        for column in columns:
            print(f"   {column}")
        
        # Check sample data from both tables
        print("\n📊 Sample data from applicantprofile:")
        db.execute("SELECT * FROM applicantprofile LIMIT 3")
        profile_data = db.cursor.fetchall()
        for row in profile_data:
            print(f"   {row}")
        
        print("\n📊 Sample data from applicationdetail:")
        db.execute("SELECT * FROM applicationdetail LIMIT 3")
        detail_data = db.cursor.fetchall()
        for row in detail_data:
            print(f"   {row}")
        
        db.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_table_structure()
