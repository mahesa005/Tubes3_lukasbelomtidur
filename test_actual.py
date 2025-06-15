#!/usr/bin/env python3
"""
Test with actual ATSService - demonstrate the new approach
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_actual_implementation():
    """Test to see the improvement in action"""
    
    print("=== Testing Improved CV Search ===")
    
    # Test with different numbers of results requested
    test_cases = [
        {'keywords': ['Python'], 'top_matches': 3},
        {'keywords': ['Manager'], 'top_matches': 5},
        {'keywords': ['Java', 'Python'], 'top_matches': 2},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Keywords: {test_case['keywords']}")
        print(f"Top matches requested: {test_case['top_matches']}")
        
        try:
            from src.services.ATSService import ATSService
            service = ATSService()
            
            start_time = time.time()
            result = service.searchCVs(
                test_case['keywords'], 
                algorithm='KMP', 
                topMatches=test_case['top_matches']
            )
            end_time = time.time()
            
            print(f"⏱️  Search time: {(end_time - start_time):.2f} seconds")
            print(f"📊 Results found: {len(result['results'])}")
            
            metadata = result.get('metadata', {})
            print(f"📁 Total files available: {metadata.get('total_files_available', 'N/A')}")
            print(f"🔍 Files processed: {metadata.get('total_processed', 'N/A')}")
            print(f"🚀 Early termination: {metadata.get('early_termination', 'N/A')}")
            
            if result['results']:
                print("🎯 Sample result:")
                sample = result['results'][0]
                print(f"   {sample['name']} - Score: {sample['match_score']:.1f}%")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Using simulation instead...")
            
            # Simulate the improved approach
            total_files = 2484
            batch_size = 50
            target = test_case['top_matches']
            
            files_processed = 0
            matches_found = 0
            
            start_sim = time.time()
            
            for batch_num in range(0, total_files, batch_size):
                if matches_found >= target:
                    break
                    
                # Simulate batch processing time
                time.sleep(0.05)  # 50ms per batch
                
                batch_matches = min(2, target - matches_found)  # Find some matches
                matches_found += batch_matches
                files_processed += min(batch_size, total_files - batch_num)
            
            end_sim = time.time()
            
            print(f"⏱️  Simulated time: {(end_sim - start_sim):.2f} seconds")
            print(f"📊 Simulated results: {matches_found}")
            print(f"📁 Total files available: {total_files}")
            print(f"🔍 Files processed: {files_processed}")
            print(f"🚀 Early termination: {files_processed < total_files}")
            print(f"💪 Efficiency: {((total_files - files_processed) / total_files * 100):.1f}% files saved")

if __name__ == "__main__":
    test_actual_implementation()
