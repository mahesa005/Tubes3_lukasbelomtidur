#!/usr/bin/env python3
"""
Debug script untuk mengecek mengapa application_id bernilai None
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

def debug_application_id():
    """Debug mengapa application_id None"""
    
    print("🔍 DEBUG: APPLICATION_ID IS NONE")
    print("=" * 50)
    
    try:
        from src.services.ATSService import ATSService
        
        # Test search results
        print("1. Testing ATSService.searchCVs...")
        ats_service = ATSService()
        
        # Coba search dengan keyword sederhana
        result = ats_service.searchCVs("python", "KMP", 5)
        
        print(f"Search result type: {type(result)}")
        print(f"Search result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
        
        if result and 'results' in result:
            results = result['results']
            print(f"Number of results: {len(results)}")
            
            for i, res in enumerate(results[:3]):  # Check first 3 results
                print(f"\nResult {i+1}:")
                print(f"  Type: {type(res)}")
                if isinstance(res, dict):
                    print(f"  Keys: {list(res.keys())}")
                    print(f"  application_id: {res.get('application_id')}")
                    print(f"  name: {res.get('name')}")
                    print(f"  cv_path: {res.get('cv_path')}")
                else:
                    print(f"  Content: {res}")
        else:
            print("❌ No results or results key missing")
        
        # Test database query langsung
        print("\n2. Testing direct database query...")
        from src.database.connection import DatabaseConnection
        
        db = DatabaseConnection()
        if db.connect():
            query = "SELECT application_id, cv_path FROM ApplicationDetail LIMIT 5"
            db_results = db.fetchAll(query)
            
            print(f"Database results: {len(db_results) if db_results else 0}")
            for i, row in enumerate(db_results[:3] if db_results else []):
                print(f"  Row {i+1}: application_id={row[0]}, cv_path={row[1]}")
            
            db.disconnect()
        else:
            print("❌ Database connection failed")
            
    except Exception as e:
        print(f"❌ Error in debug: {e}")
        import traceback
        traceback.print_exc()

def check_ats_service_search():
    """Check ATSService search method in detail"""
    
    print("\n3. Checking ATSService.searchCVs method...")
    
    try:
        # Read the searchCVs method
        import inspect
        from src.services.ATSService import ATSService
        
        ats_service = ATSService()
        
        # Get source code
        search_method = getattr(ats_service, 'searchCVs')
        print("✅ Found searchCVs method")
        
        # Test with debug
        print("\n🧪 Testing searchCVs with detailed logging...")
        
        # Temporarily monkey patch untuk debug
        original_search = ats_service.searchCVs
        
        def debug_search(keywords, algorithm, top_matches):
            print(f"🔄 searchCVs called with: keywords={keywords}, algorithm={algorithm}, top_matches={top_matches}")
            result = original_search(keywords, algorithm, top_matches)
            print(f"🔄 searchCVs returned: {type(result)}")
            if isinstance(result, dict) and 'results' in result:
                print(f"🔄 Results count: {len(result['results'])}")
                for i, res in enumerate(result['results'][:2]):
                    print(f"🔄 Result {i}: {res}")
            return result
        
        ats_service.searchCVs = debug_search
        
        # Test search
        test_result = ats_service.searchCVs("java", "KMP", 3)
        
        if test_result and 'results' in test_result:
            first_result = test_result['results'][0] if test_result['results'] else None
            if first_result:
                print(f"\n✅ First result analysis:")
                print(f"   Type: {type(first_result)}")
                print(f"   Has application_id: {'application_id' in first_result}")
                print(f"   application_id value: {first_result.get('application_id')}")
                print(f"   All keys: {list(first_result.keys())}")
        
    except Exception as e:
        print(f"❌ Error checking ATSService: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_application_id()
    check_ats_service_search()
