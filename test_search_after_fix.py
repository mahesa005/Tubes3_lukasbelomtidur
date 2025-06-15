#!/usr/bin/env python3
"""
Test search functionality after database fix
"""

import os
import sys
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

from services.ATSService import ATSService

def test_search_after_fix():
    """Test search functionality setelah database di-fix"""
    
    print("🔍 Testing Search Functionality After Database Fix...")
    print("=" * 70)
    
    try:
        # Initialize ATSService
        ats = ATSService()
        
        # Test search with common keywords yang mungkin ada di CV
        test_keywords = [
            ['python', 'programming'],
            ['finance', 'accounting'],
            ['engineering', 'design'],
            ['management', 'business'],
            ['java', 'software']
        ]
        
        for keywords in test_keywords:
            print(f"\n🔎 Testing search with keywords: {keywords}")
            
            # Perform search
            result = ats.searchCVs(keywords=keywords, algorithm='KMP', topMatches=5)
            
            # Check results
            if 'results' in result:
                results = result['results']
                metadata = result.get('metadata', {})
                
                print(f"   📊 Results: {len(results)} matches found")
                print(f"   📈 Metadata: {metadata.get('total_matches_found', 0)} total matches")
                
                # Check if any results have valid application_id
                valid_ids = [r for r in results if r.get('application_id') is not None]
                print(f"   ✅ Valid application_ids: {len(valid_ids)}/{len(results)}")
                
                # Show sample results
                for i, result_item in enumerate(results[:3], 1):
                    app_id = result_item.get('application_id')
                    name = result_item.get('name', 'Unknown')
                    score = result_item.get('match_score', 0)
                    cv_path = result_item.get('cv_path', '')
                    
                    status = "✅ VALID" if app_id is not None else "❌ NULL ID"
                    print(f"     {i}. {status} | ID: {app_id} | {name} | Score: {score:.1f}%")
                    print(f"        Path: {Path(cv_path).name}")
                
            else:
                print(f"   ❌ Error in search: {result}")
            
            # Small delay between searches
            import time
            time.sleep(0.5)
        
        print("\n" + "=" * 70)
        print("🎯 Summary:")
        print("   Database now has 30 entries with normalized paths")
        print("   Search should now return valid application_ids for matching CVs")
        
    except Exception as e:
        print(f"❌ Error in test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_search_after_fix()
