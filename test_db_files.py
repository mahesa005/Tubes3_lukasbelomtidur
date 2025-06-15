#!/usr/bin/env python3

import sys
import os
sys.path.append('.')
from src.database.connection import DatabaseConnection
from src.services.ATSService import ATSService

def test_with_database_files():
    print("=== Testing with files that exist in database ===")
    
    # Get some files that actually exist in database
    db = DatabaseConnection()
    if db.connect():
        cursor = db.connection.cursor()
        cursor.execute("SELECT cv_path FROM ApplicationDetail LIMIT 10")
        db_files = [row[0] for row in cursor.fetchall()]
        cursor.close()
        db.disconnect()
        
        print(f"Files in database (sample): {db_files[:5]}")
        print()
        
        # Extract just the filenames for searching
        filenames = [os.path.basename(path).replace('.pdf', '') for path in db_files[:5]]
        print(f"Searching for content in these files: {filenames}")
        print()
        
        # Initialize service and search
        ats = ATSService()
        # Search with common keywords that might be in any CV
        results = ats.searchCVs(['experience', 'work'], 'KMP', 10)
        
        print(f"Found {len(results['results'])} total results")
        
        # Look for results that match our database files
        successful = 0
        for i, result in enumerate(results['results'], 1):
            app_id = result.get('application_id')
            name = result.get('name', 'Unknown')
            cv_path = result.get('cv_path', 'Unknown')
            
            if app_id is not None:
                successful += 1
                print(f"✅ SUCCESS {successful}: {name} (ID: {app_id})")
                print(f"   Path: {os.path.basename(cv_path)}")
                print()
            
            if successful >= 3:  # Show first 3 successful matches
                break
        
        print(f"Summary: {successful} results have application_id out of {len(results['results'])} total")
    else:
        print('Failed to connect to database')

if __name__ == "__main__":
    test_with_database_files()
