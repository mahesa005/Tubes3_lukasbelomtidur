#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from services.ATSService import ATSService

def test_python_search():
    """Test searching for Python keyword"""
    print("Testing Python keyword search...")
    
    service = ATSService()
    
    # Test with Python keyword
    keywords = ["Python"]
    print(f"Searching for keywords: {keywords}")    
    result = service.searchCVs(keywords)
    
    print(f"Found {len(result.get('results', []))} results for 'Python'")
    
    if result.get('results'):
        print("\nFirst few results:")
        for i, res in enumerate(result['results'][:3]):
            print(f"{i+1}. {res.filename}")
            print(f"   Score: {res.match_score}")
            print(f"   Matches: {res.matches}")
            print()
    else:
        print("No results found for 'Python'")
        
        # Let's test if files are being processed at all
        print("\nTesting with a common word like 'experience':")
        test_result = service.searchCVs(["experience"])
        print(f"Found {len(test_result.get('results', []))} results for 'experience'")
        
        if test_result.get('results'):
            print("Files are being processed, issue seems to be with 'Python' keyword specifically")
        else:
            print("No files are being processed at all - there's a bigger issue")

if __name__ == "__main__":
    test_python_search()
