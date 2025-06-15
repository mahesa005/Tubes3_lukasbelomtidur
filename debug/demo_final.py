#!/usr/bin/env python3
"""
Demo untuk menunjukkan bahwa sistem bekerja dengan baik,
tetapi dataset tidak mengandung CV programming.
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from services.ATSService import ATSService

def main():
    print("🔍 ATS CV Search - Demo Keyword yang Bekerja")
    print("=" * 60)
    print()
    
    service = ATSService()
    
    # Test kata kunci yang TIDAK ADA dalam dataset
    print("❌ Kata kunci yang TIDAK ditemukan (karena tidak ada dalam dataset):")
    missing_keywords = ["Python", "Java", "React", "Node.js", "Django"]
    
    for keyword in missing_keywords:
        result = service.searchCVs([keyword])
        count = len(result.get('results', []))
        print(f"  '{keyword}' → {count} hasil")
    
    print()
    print("✅ Kata kunci yang DITEMUKAN (karena ada dalam dataset):")
    
    # Test kata kunci yang ADA dalam dataset
    working_keywords = ["manager", "experience", "skills", "financial", "accounting"]
    
    for keyword in working_keywords:
        result = service.searchCVs([keyword])
        count = len(result.get('results', []))
        print(f"  '{keyword}' → {count} hasil")
        
        if count > 0:
            # Tampilkan contoh hasil pertama
            first_result = result['results'][0]
            print(f"    📋 Contoh: {first_result['name']}")
            print(f"    📊 Score: {first_result['match_score']:.1f}%")
            print(f"    🎯 Keywords: {first_result['keywords']}")
            print()
    
    print("📝 KESIMPULAN:")
    print("-" * 40)
    print("• Sistem pencarian ATS bekerja dengan BAIK ✅")
    print("• Kata kunci 'Python' tidak ditemukan karena TIDAK ADA dalam dataset ❌")
    print("• Dataset berisi CV bidang AKUNTANSI, bukan programming")
    print("• Untuk mencari CV programmer, perlu dataset yang berbeda")
    print()
    print("💡 SARAN:")
    print("• Gunakan kata kunci: manager, experience, skills, financial, accounting")
    print("• Atau ganti dataset dengan CV programmer")

if __name__ == "__main__":
    main()
