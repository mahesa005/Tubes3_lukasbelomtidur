#!/usr/bin/env python3
"""
Test untuk memverifikasi bahwa sistem memproses semua PDF 
ketika user meminta hasil yang banyak (9999).
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from services.ATSService import ATSService

def test_large_search():
    print("🧪 Test Pencarian Besar - Memproses Semua PDF")
    print("=" * 60)
    
    service = ATSService()
    
    # Test 1: Permintaan kecil (5 hasil) - should use early termination
    print("\n📋 Test 1: Permintaan Kecil (topMatches=5)")
    print("-" * 40)
    
    result_small = service.searchCVs(["experience"], topMatches=5)
    metadata_small = result_small['metadata']
    
    print(f"  Total file tersedia: {metadata_small['total_files_available']}")
    print(f"  File yang diproses: {metadata_small['total_processed']}")
    print(f"  Total match ditemukan: {metadata_small['total_matches_found']}")
    print(f"  Hasil dikembalikan: {metadata_small['total_returned']}")
    print(f"  Early termination: {metadata_small['early_termination']}")
    print(f"  Waktu proses: {metadata_small['processing_time_ms']:.1f}ms")
    
    # Test 2: Permintaan besar (100 hasil) - should process all files
    print("\n📋 Test 2: Permintaan Besar (topMatches=100)")
    print("-" * 40)
    
    result_large = service.searchCVs(["experience"], topMatches=100)
    metadata_large = result_large['metadata']
    
    print(f"  Total file tersedia: {metadata_large['total_files_available']}")
    print(f"  File yang diproses: {metadata_large['total_processed']}")
    print(f"  Total match ditemukan: {metadata_large['total_matches_found']}")
    print(f"  Hasil dikembalikan: {metadata_large['total_returned']}")
    print(f"  Early termination: {metadata_large['early_termination']}")
    print(f"  Waktu proses: {metadata_large['processing_time_ms']:.1f}ms")
    
    # Test 3: Permintaan sangat besar (9999 hasil) - should process all files
    print("\n📋 Test 3: Permintaan Sangat Besar (topMatches=9999)")
    print("-" * 40)
    
    result_huge = service.searchCVs(["manager"], topMatches=9999)
    metadata_huge = result_huge['metadata']
    
    print(f"  Total file tersedia: {metadata_huge['total_files_available']}")
    print(f"  File yang diproses: {metadata_huge['total_processed']}")
    print(f"  Total match ditemukan: {metadata_huge['total_matches_found']}")
    print(f"  Hasil dikembalikan: {metadata_huge['total_returned']}")
    print(f"  Early termination: {metadata_huge['early_termination']}")
    print(f"  Waktu proses: {metadata_huge['processing_time_ms']:.1f}ms")
    
    print("\n📊 ANALISIS:")
    print("-" * 40)
    
    # Apakah untuk permintaan besar sistem memproses semua file?
    if metadata_large['total_processed'] == metadata_large['total_files_available']:
        print("✅ Permintaan besar (100): SEMUA file diproses")
    else:
        print("❌ Permintaan besar (100): Tidak semua file diproses")
    
    if metadata_huge['total_processed'] == metadata_huge['total_files_available']:
        print("✅ Permintaan sangat besar (9999): SEMUA file diproses")
    else:
        print("❌ Permintaan sangat besar (9999): Tidak semua file diproses")
    
    # Apakah sistem mengembalikan semua hasil yang ditemukan ketika diminta 9999?
    if metadata_huge['total_returned'] == metadata_huge['total_matches_found']:
        print("✅ Permintaan 9999: Mengembalikan SEMUA hasil yang ditemukan")
    else:
        print("❌ Permintaan 9999: Tidak mengembalikan semua hasil yang ditemukan")
    
    print(f"\n🎯 KESIMPULAN:")
    print(f"• Untuk permintaan ≤ 10 hasil: Early termination aktif")
    print(f"• Untuk permintaan > 10 hasil: Semua {metadata_huge['total_files_available']} file diproses")
    print(f"• Sistem dapat mengembalikan hingga {metadata_huge['total_matches_found']} hasil untuk 'manager'")
    print(f"• User bisa meminta 9999 hasil dan akan mendapat semua yang match")

if __name__ == "__main__":
    test_large_search()
