#!/usr/bin/env python3
"""
Quick test untuk melihat debug logging dan memperbaiki application_id issue
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

def test_with_debug_logging():
    """Test dengan debug logging enabled"""
    
    print("🔍 TEST WITH DEBUG LOGGING")
    print("=" * 50)
    
    try:
        # Enable debug logging
        import logging
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
        
        from src.services.ATSService import ATSService
        
        # Search dengan keyword yang simple
        ats_service = ATSService()
        result = ats_service.searchCVs(["fitness"], "KMP", 2)  # Only 2 results untuk debug
        
        if result and 'results' in result:
            results = result['results']
            print(f"\nSearch returned {len(results)} results:")
            
            for i, res in enumerate(results):
                app_id = res.get('application_id')
                name = res.get('name')
                cv_path = res.get('cv_path')
                
                print(f"\n{i+1}. Name: {name}")
                print(f"   application_id: {app_id}")
                print(f"   cv_path: {cv_path}")
                
                if app_id is not None:
                    print(f"   ✅ SUCCESS: This result has application_id!")
                else:
                    print(f"   ❌ FAILED: application_id is None")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_with_debug_logging()
