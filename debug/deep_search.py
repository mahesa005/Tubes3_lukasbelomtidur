#!/usr/bin/env python3
"""
Deep search - Cari lebih banyak file untuk memastikan ada Python/Java
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def deep_search_test():
    """Cari lebih dalam untuk memastikan ada keyword Python/Java"""
    
    print("=== Deep Search for Python/Java Keywords ===")
    
    try:
        from src.services.ATSService import ATSService
        service = ATSService()
        
        # Test dengan mencari lebih banyak results
        print("Testing with higher topMatches to search more files...")
        
        test_keywords = ['Python', 'Java', 'Programming', 'Developer']
        
        for keyword in test_keywords:
            print(f"\n--- Deep search for: {keyword} ---")
            
            start_time = time.time()
            result = service.searchCVs(
                [keyword], 
                algorithm='KMP', 
                topMatches=20  # Cari 20 hasil untuk memaksa scan lebih banyak file
            )
            end_time = time.time()
            
            metadata = result.get('metadata', {})
            print(f"⏱️  Search time: {(end_time - start_time):.2f} seconds")
            print(f"📊 Results found: {len(result['results'])}")
            print(f"🔍 Files processed: {metadata.get('total_processed', 'N/A')}")
            print(f"📁 Total files available: {metadata.get('total_files_available', 'N/A')}")
            
            if result['results']:
                print(f"✅ Found {len(result['results'])} matches for '{keyword}':")
                for i, res in enumerate(result['results'][:5], 1):
                    print(f"   {i}. {res['name']} - Score: {res['match_score']:.1f}%")
                    print(f"      Keywords: {res['keywords']}")
                    
                # Tambahan: cek file pertama untuk debug
                if result['results']:
                    first_result = result['results'][0]
                    cv_path = first_result['cv_path']
                    print(f"\n🔍 Checking first result file: {os.path.basename(cv_path)}")
                    
                    try:
                        text = service.pdfExtractor.PDFExtractForMatch(cv_path)
                        if text:
                            # Cari context sekitar keyword
                            text_lower = text.lower()
                            keyword_lower = keyword.lower()
                            
                            idx = text_lower.find(keyword_lower)
                            if idx >= 0:
                                start = max(0, idx - 50)
                                end = min(len(text), idx + len(keyword) + 50)
                                context = text[start:end].replace('\n', ' ')
                                print(f"📄 Context: ...{context}...")
                            else:
                                print(f"❓ Keyword not found in extracted text (this is strange)")
                        else:
                            print(f"❌ Could not extract text from file")
                    except Exception as e:
                        print(f"❌ Error checking file: {e}")
            else:
                print(f"❌ No matches found for '{keyword}'")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    deep_search_test()
