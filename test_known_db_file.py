#!/usr/bin/env python3

import sys
import os
sys.path.append('.')
from src.services.ATSService import ATSService

def test_known_db_file():
    print("=== Testing with known database file names ===")
    
    # These are the file names we know exist in the database from earlier check
    known_db_files = [
        "54259150.pdf",  # FITNESS 
        "11676151.pdf",  # AGRICULTURE
        "26410763.pdf",  # ARTS
        "29990140.pdf",  # CHEF  
        "99714410.pdf"   # CONSULTANT
    ]
    
    print(f"Known database files: {known_db_files}")
    
    # Initialize service and search using something likely to be in these files
    ats = ATSService()
    
    # Try to search for a very common term that should be in most CVs
    results = ats.searchCVs(['the'], 'KMP', 20)  # Increase limit to catch more
    
    print(f"Found {len(results['results'])} total results")
    print()
    
    # Look specifically for files that match our known database files  
    matches_found = []
    for result in results['results']:
        cv_path = result.get('cv_path', '')
        filename = os.path.basename(cv_path)
        
        if filename in known_db_files:
            matches_found.append(result)
            
    print(f"Matches with known DB files: {len(matches_found)}")
    for match in matches_found:
        app_id = match.get('application_id')
        name = match.get('name', 'Unknown')
        filename = os.path.basename(match.get('cv_path', ''))
        
        print(f"✅ Found DB file: {filename}")
        print(f"   Name: {name}")
        print(f"   Application ID: {app_id}")
        print(f"   Status: {'SUCCESS' if app_id is not None else 'FAILED'}")
        print()

if __name__ == "__main__":
    test_known_db_file()
