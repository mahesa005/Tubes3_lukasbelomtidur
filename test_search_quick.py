#!/usr/bin/env python3
"""
Quick test to verify search functionality works correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.ATSService import ATSService

def test_search_quick():
    """Quick test of search functionality"""
    
    try:
        # Initialize ATS Service
        ats_service = ATSService()
        
        # Test search
        keywords = ["python"]
        algorithm = "KMP"
        top_matches = 3
        
        print(f"🔍 Testing search for: {keywords}")
        print(f"   Algorithm: {algorithm}")
        print(f"   Top matches: {top_matches}")
        print("-" * 40)
        
        # Perform search
        results = ats_service.searchCVs(keywords, algorithm, top_matches)
        
        if 'results' in results:
            search_results = results['results']
            metadata = results.get('metadata', {})
            
            print(f"📊 Search Metadata:")
            print(f"   Files processed: {metadata.get('total_processed', 'N/A')}")
            print(f"   Matches found: {metadata.get('total_matches_found', 'N/A')}")
            print(f"   Results returned: {len(search_results)}")
            print(f"   Processing time: {metadata.get('processing_time_ms', 'N/A'):.1f}ms")
            print()
            
            print(f"📋 Search Results:")
            for i, result in enumerate(search_results, 1):
                app_id = result.get('application_id')
                name = result.get('name', 'Unknown')
                score = result.get('match_score', 0)
                
                print(f"   {i}. {name} (ID: {app_id}) - Score: {score:.1f}%")
            
            if len(search_results) > 0:
                print(f"\n✅ Search working correctly!")
            else:
                print(f"\n⚠️  No results returned")
                
        else:
            print(f"❌ Search failed: {results}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_search_quick()
