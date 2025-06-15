#!/usr/bin/env python3

import sys
import os
sys.path.append('.')

from src.database.connection import DatabaseConnection

def debug_exact_path_match():
    print("=== Testing Exact Path Match ===")
    
    # Get a sample file path like ATSService would generate
    sample_absolute = r"C:\Users\MSI\Desktop\tubes3stima\Tubes3_lukasbelomtidur\Tubes3_lukasbelomtidur\src\archive\data\data\ADVOCATE\26071861.pdf"
    
    print(f"Sample absolute path: {sample_absolute}")
      # Convert like ATSService does
    try:
        relative_path = os.path.relpath(sample_absolute)
        # Fixed conversion: normalize to forward slashes first, then to double backslashes
        db_format = relative_path.replace('\\', '/').replace('/', '\\\\')
        print(f"Converted to DB format: {repr(db_format)}")
    except Exception as e:
        print(f"Conversion failed: {e}")
        return
    
    # Check if this exact path exists in database
    db = DatabaseConnection()
    if db.connect():
        cursor = db.connection.cursor()
        
        # Check for exact match
        cursor.execute("SELECT cv_path, first_name, last_name, application_id FROM ApplicationDetail ad JOIN ApplicantProfile ap ON ad.applicant_id = ap.applicant_id WHERE ad.cv_path = %s", (db_format,))
        exact_match = cursor.fetchone()
        
        if exact_match:
            print(f"✅ EXACT MATCH FOUND: {exact_match}")
        else:
            print("❌ No exact match found")
            
            # Let's see what similar paths exist
            cursor.execute("SELECT cv_path FROM ApplicationDetail WHERE cv_path LIKE %s LIMIT 5", (f"%{26071861}%",))
            similar = cursor.fetchall()
            print("Similar paths in DB:")
            for (path,) in similar:
                print(f"  {repr(path)}")
        
        cursor.close()
        db.disconnect()
    else:
        print("Failed to connect to database")

if __name__ == "__main__":
    debug_exact_path_match()
