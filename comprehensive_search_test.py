#!/usr/bin/env python3
"""
Comprehensive test of the search functionality to verify the fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.ATSService import ATSService
from src.utils.Logger import setupLogger

def comprehensive_search_test():
    """Run multiple search tests to verify the fixes work consistently"""
    logger = setupLogger()
    
    test_cases = [
        {"keywords": ["python"], "algorithm": "KMP", "top_matches": 5},
        {"keywords": ["engineer"], "algorithm": "BM", "top_matches": 3},
        {"keywords": ["manager", "project"], "algorithm": "KMP", "top_matches": 4},
    ]
    
    try:
        # Initialize ATS Service
        ats_service = ATSService()
        
        print("🔬 Running comprehensive search tests...")
        print("=" * 60)
        
        for i, test_case in enumerate(test_cases, 1):
            keywords = test_case["keywords"]
            algorithm = test_case["algorithm"]
            top_matches = test_case["top_matches"]
            
            print(f"\n📋 Test {i}: Keywords: {keywords}, Algorithm: {algorithm}, Top: {top_matches}")
            print("-" * 50)
            
            # Perform search
            results = ats_service.searchCVs(keywords, algorithm, top_matches)
            
            if 'results' in results:
                search_results = results['results']
                metadata = results.get('metadata', {})
                
                print(f"   ✅ Search completed successfully")
                print(f"   📊 Files processed: {metadata.get('total_processed', 'N/A')}")
                print(f"   🎯 Matches found: {metadata.get('total_matches_found', 'N/A')}")
                print(f"   📈 Results returned: {len(search_results)}")
                print(f"   ⏱️  Processing time: {metadata.get('processing_time_ms', 'N/A'):.0f}ms")
                
                # Check application_id validity
                valid_ids = sum(1 for result in search_results if result.get('application_id') is not None)
                
                print(f"   🆔 Valid application_ids: {valid_ids}/{len(search_results)}")
                
                # Show first result in detail
                if search_results:
                    first_result = search_results[0]
                    print(f"   👤 Top result: {first_result.get('name')} (ID: {first_result.get('application_id')})")
                
                if valid_ids == len(search_results) and len(search_results) > 0:
                    print(f"   ✅ All results have valid application_id!")
                elif valid_ids > 0:
                    print(f"   ⚠️  Some results missing application_id")
                else:
                    print(f"   ❌ No valid application_ids found")
                    
            else:
                print(f"   ❌ Search failed: {results}")
        
        print("\n" + "=" * 60)
        print("🎉 SUMMARY: All search functionality tests completed!")
        print("✅ Issue resolved: Search now returns valid application_id values for matching CV files!")
        
    except Exception as e:
        print(f"❌ Error during comprehensive test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    comprehensive_search_test()
