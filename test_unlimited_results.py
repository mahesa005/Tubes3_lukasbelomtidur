#!/usr/bin/env python3
"""
Test untuk memastikan limit hasil pencarian sudah diperbaiki
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.ATSService import ATSService

def test_unlimited_results():
    """Test pencarian dengan batas tinggi"""
    print("=== Testing Unlimited Results ===")
    
    ats_service = ATSService()
    
    # Test dengan topMatches rendah (5)
    print("\n1. Test dengan topMatches = 5")
    result1 = ats_service.searchCVs(["Python"], "KMP", 5)
    results1 = result1.get('results', [])
    metadata1 = result1.get('metadata', {})
    
    print(f"   Hasil dikembalikan: {len(results1)}")
    print(f"   Total yang match: {metadata1.get('total_matches_found', 0)}")
    print(f"   Total dikembalikan: {metadata1.get('total_returned', 0)}")
    
    # Test dengan topMatches tinggi (9999) 
    print("\n2. Test dengan topMatches = 9999 (semua)")
    result2 = ats_service.searchCVs(["Python"], "KMP", 9999)
    results2 = result2.get('results', [])
    metadata2 = result2.get('metadata', {})
    
    print(f"   Hasil dikembalikan: {len(results2)}")
    print(f"   Total yang match: {metadata2.get('total_matches_found', 0)}")
    print(f"   Total dikembalikan: {metadata2.get('total_returned', 0)}")
    
    # Verifikasi
    total_found = metadata2.get('total_matches_found', 0)
    total_returned = metadata2.get('total_returned', 0)
    
    if total_found == total_returned and len(results2) >= len(results1):
        print("\n✅ BERHASIL: Aplikasi mengembalikan semua hasil ketika topMatches >= 9999")
    else:
        print("\n❌ GAGAL: Masih ada pembatasan hasil")
    
    print(f"\nPerbandingan:")
    print(f"  Dengan limit 5: {len(results1)} hasil")
    print(f"  Dengan limit 9999: {len(results2)} hasil")

if __name__ == "__main__":
    test_unlimited_results()
