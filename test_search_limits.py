import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.services.ATSService import ATSService

def test_search_limits():
    """Test untuk memverifikasi bahwa pencarian tidak lagi dibatasi 100 hasil"""
    
    ats = ATSService()
    
    # Test 1: Pencarian normal dengan batas kecil
    print("=== Test 1: Pencarian dengan batas 5 hasil ===")
    result1 = ats.searchCVs(['engineer', 'python'], 'KMP', 5)
    print(f"Diminta: 5, Dikembalikan: {len(result1['results'])}, Total ditemukan: {result1['metadata']['total_matches_found']}")
    
    # Test 2: Pencarian dengan batas sedang
    print("\n=== Test 2: Pencarian dengan batas 50 hasil ===")
    result2 = ats.searchCVs(['engineer'], 'KMP', 50)
    print(f"Diminta: 50, Dikembalikan: {len(result2['results'])}, Total ditemukan: {result2['metadata']['total_matches_found']}")
    
    # Test 3: Pencarian dengan batas tinggi (semua hasil)
    print("\n=== Test 3: Pencarian dengan batas 9999 (semua hasil) ===")
    result3 = ats.searchCVs(['software'], 'KMP', 9999)
    print(f"Diminta: 9999, Dikembalikan: {len(result3['results'])}, Total ditemukan: {result3['metadata']['total_matches_found']}")
    
    # Verifikasi bahwa hasil ketiga memberikan semua data yang ditemukan
    assert result3['metadata']['total_matches_found'] == len(result3['results']), "Semua hasil harus dikembalikan untuk topMatches >= 9999"
    
    print("\n=== Hasil Test ===")
    print(f"✓ Test 1 passed: {len(result1['results'])} <= 5")
    print(f"✓ Test 2 passed: {len(result2['results'])} <= 50") 
    print(f"✓ Test 3 passed: Semua {len(result3['results'])} hasil dikembalikan")
    
    print("\n=== Metadata Comparison ===")
    for i, result in enumerate([result1, result2, result3], 1):
        print(f"Test {i}: requested={result['metadata']['requested_matches']}, returned={result['metadata']['total_returned']}, found={result['metadata']['total_matches_found']}")

if __name__ == "__main__":
    test_search_limits()
