#!/usr/bin/env python3
"""
Test untuk memastikan total_matches sudah benar di GUI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.ATSService import ATSService

def test_search_metadata():
    """Test metadata yang dikembalikan dari search"""
    print("=== Testing Search Metadata ===")
    
    ats_service = ATSService()
    
    # Test search dengan keywords yang pasti ada
    keywords = ["Python", "Java"]
    result = ats_service.searchCVs(keywords, "BoyerMoore", 10)
    
    print("\n=== Search Result Structure ===")
    print(f"Results count: {len(result.get('results', []))}")
    
    metadata = result.get('metadata', {})
    print(f"\n=== Metadata Keys ===")
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    
    # Check the specific field that was causing issues
    total_matches_found = metadata.get('total_matches_found', 'NOT_FOUND')
    total_matches = metadata.get('total_matches', 'NOT_FOUND')
    
    print(f"\n=== Key Fields ===")
    print(f"total_matches_found: {total_matches_found}")
    print(f"total_matches: {total_matches}")
    
    if total_matches_found != 'NOT_FOUND' and total_matches_found > 0:
        print("✅ total_matches_found is correctly set!")
    else:
        print("❌ total_matches_found is missing or zero")
    
    return result

if __name__ == "__main__":
    test_search_metadata()
