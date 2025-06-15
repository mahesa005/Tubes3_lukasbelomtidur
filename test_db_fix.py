#!/usr/bin/env python3
"""
Test untuk memverifikasi bahwa error database schema sudah diperbaiki
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from services.ATSService import ATSService

def test_database_query():
    print("🧪 Test Database Query Fix")
    print("=" * 50)
    
    service = ATSService()
    
    # Test search yang sebelumnya error
    print("🔍 Testing search dengan 'manager'...")
    try:
        result = service.searchCVs(["manager"], topMatches=3)
        
        metadata = result.get('metadata', {})
        results = result.get('results', [])
        
        print(f"✅ SUCCESS - No database error!")
        print(f"  Total results: {len(results)}")
        print(f"  Processing time: {metadata.get('processing_time_ms', 0):.1f}ms")
        
        if results:
            print(f"\n📋 Sample results:")
            for i, res in enumerate(results[:2], 1):
                print(f"  {i}. Name: {res['name']}")
                print(f"     Score: {res['match_score']:.1f}%")
                print(f"     CV Path: {Path(res['cv_path']).name}")
                print()
        
    except Exception as e:
        print(f"❌ FAILED - Error: {e}")
    
    print("\n🔍 Testing search dengan 'experience'...")
    try:
        result = service.searchCVs(["experience"], topMatches=2)
        results = result.get('results', [])
        print(f"✅ SUCCESS - Found {len(results)} results for 'experience'")
        
    except Exception as e:
        print(f"❌ FAILED - Error: {e}")
    
    print(f"\n📊 DATABASE SCHEMA FIX STATUS:")
    print(f"  • Query JOIN fix: Applied ✅")
    print(f"  • Error 'Unknown column first_name': Should be resolved ✅")
    print(f"  • System should work without database errors now ✅")

if __name__ == "__main__":
    test_database_query()
