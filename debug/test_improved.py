#!/usr/bin/env python3
"""
Test improved search with case-insensitive pattern matching
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_improved_search():
    """Test pencarian dengan pattern matching yang sudah diperbaiki"""
    
    print("=== Testing Improved Case-Insensitive Search ===")
    
    try:
        from src.services.ATSService import ATSService
        service = ATSService()
        
        # Test keywords yang umum ditemukan dalam CV
        test_cases = [
            {'keywords': ['Python'], 'expected': 'Should find python/Python/PYTHON'},
            {'keywords': ['Java'], 'expected': 'Should find java/Java/JAVA'},
            {'keywords': ['Manager'], 'expected': 'Should find manager/Manager'},
            {'keywords': ['Programming'], 'expected': 'Should find programming/Programming'},
            {'keywords': ['Python', 'Java'], 'expected': 'Should find files with both'},
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- Test Case {i}: {test_case['keywords']} ---")
            print(f"Expected: {test_case['expected']}")
            
            start_time = time.time()
            result = service.searchCVs(
                test_case['keywords'], 
                algorithm='KMP', 
                topMatches=5
            )
            end_time = time.time()
            
            print(f"⏱️  Search time: {(end_time - start_time):.2f} seconds")
            print(f"📊 Results found: {len(result['results'])}")
            
            metadata = result.get('metadata', {})
            print(f"🔍 Files processed: {metadata.get('total_processed', 'N/A')}")
            print(f"📁 Total files available: {metadata.get('total_files_available', 'N/A')}")
            print(f"🚀 Early termination: {metadata.get('early_termination', 'N/A')}")
            
            if result['results']:
                print("✅ Found matches:")
                for j, res in enumerate(result['results'][:3], 1):
                    print(f"   {j}. {res['name']} - Score: {res['match_score']:.1f}%")
                    print(f"      Keywords: {res['keywords']}")
            else:
                print("❌ No matches found")
        
        # Test cache statistics
        cache_stats = service.get_cache_stats()
        print(f"\n📋 Cache Statistics:")
        print(f"   Cache size: {cache_stats['cache_size']} files")
        print(f"   Cache file exists: {cache_stats['cache_file_exists']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_improved_search()
