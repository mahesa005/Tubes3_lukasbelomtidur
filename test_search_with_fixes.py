#!/usr/bin/env python3
"""
Test the search functionality after fixing table names and path conversion
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.ATSService import ATSService
from src.utils.Logger import setupLogger

def test_search_functionality():
    """Test search with fixes for table names and path conversion"""
    logger = setupLogger()
    
    try:
        # Initialize ATS Service
        ats_service = ATSService()
        
        # Test search with a common keyword
        keywords = ["python"]
        algorithm = "KMP"
        top_matches = 3
        
        print(f"🔍 Testing search for keywords: {keywords}")
        print(f"   Algorithm: {algorithm}")
        print(f"   Top matches: {top_matches}")
        print("-" * 50)
        
        # Perform search
        results = ats_service.searchCVs(keywords, algorithm, top_matches)
        
        if 'results' in results:
            search_results = results['results']
            metadata = results.get('metadata', {})
            
            print(f"📊 Search Results:")
            print(f"   Total files processed: {metadata.get('total_processed', 'N/A')}")
            print(f"   Total matches found: {metadata.get('total_matches_found', 'N/A')}")
            print(f"   Results returned: {len(search_results)}")
            print(f"   Processing time: {metadata.get('processing_time_ms', 'N/A'):.2f}ms")
            print()
            
            # Check results for application_id values
            valid_ids = 0
            for i, result in enumerate(search_results, 1):
                app_id = result.get('application_id')
                name = result.get('name', 'Unknown')
                score = result.get('match_score', 0)
                cv_path = result.get('cv_path', '')
                
                print(f"   Result {i}:")
                print(f"     Name: {name}")
                print(f"     Application ID: {app_id}")
                print(f"     Match Score: {score:.1f}%")
                print(f"     CV Path: {cv_path}")
                print()
                
                if app_id is not None:
                    valid_ids += 1
            
            print(f"✅ Results with valid application_id: {valid_ids}/{len(search_results)}")
            
            if valid_ids > 0:
                print("🎉 SUCCESS: Search now returns valid application_id values!")
            else:
                print("❌ ISSUE: All application_id values are still None")
                
        else:
            print(f"❌ Search failed: {results}")
            
    except Exception as e:
        print(f"❌ Error during search test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_search_functionality()
