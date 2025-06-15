#!/usr/bin/env python3
"""
Check the actual column names in the applicantprofile table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.connection import DatabaseConnection

def check_applicantprofile_columns():
    """Check what columns exist in applicantprofile table"""
    
    try:
        db = DatabaseConnection()
        db.connect()
        cursor = db.connection.cursor()
        
        # Show table structure
        cursor.execute("DESCRIBE applicantprofile")
        columns = cursor.fetchall()
        
        print("📋 Columns in applicantprofile table:")
        for column in columns:
            field, type_, null, key, default, extra = column
            print(f"   {field} | {type_} | {null} | {key}")
        
        # Also check a sample record
        cursor.execute("SELECT * FROM applicantprofile LIMIT 1")
        sample = cursor.fetchone()
        
        if sample:
            print(f"\n📄 Sample record:")
            cursor.execute("SHOW COLUMNS FROM applicantprofile")
            column_names = [desc[0] for desc in cursor.fetchall()]
            
            for i, value in enumerate(sample):
                print(f"   {column_names[i]}: {value}")
        
        db.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_applicantprofile_columns()
