#!/usr/bin/env python3

import sys
import os
sys.path.append('.')

from src.services.ATSService import ATSService

def test_application_id_fix():
    print("=== Testing Application ID Fix ===")
    
    # Initialize service
    ats = ATSService()
    
    # Test search with a simple keyword
    results = ats.searchCVs(['python'], 'KMP', 3)
    
    print(f"Found {len(results['results'])} results:")
    print()
    
    for i, result in enumerate(results['results'], 1):
        app_id = result.get('application_id')
        name = result.get('name', 'Unknown')
        cv_path = result.get('cv_path', 'Unknown')
        
        print(f"{i}. Name: {name}")
        print(f"   Application ID: {app_id}")
        print(f"   CV Path: {cv_path}")
        print(f"   Status: {'✅ SUCCESS' if app_id is not None else '❌ FAILED'}")
        print()
    
    # Count successful lookups
    successful = sum(1 for r in results['results'] if r.get('application_id') is not None)
    print(f"Summary: {successful}/{len(results['results'])} results have application_id")

if __name__ == "__main__":
    test_application_id_fix()
