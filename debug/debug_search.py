#!/usr/bin/env python3
"""
Debug CV Search - Cari tahu kenapa keyword "Python" tidak ditemukan
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_python_search():
    """Debug kenapa pencarian Python tidak menemukan hasil"""
    
    print("=== Debug: Pencarian Keyword 'Python' ===")
    
    try:
        from src.services.ATSService import ATSService
        service = ATSService()
        
        # Test berbagai variasi keyword Python
        test_keywords = [
            ['Python'],           # Original
            ['python'],           # lowercase
            ['PYTHON'],           # uppercase
            ['Programming'],      # keyword lain yang umum
            ['Java'],            # keyword lain
            ['Manager'],         # keyword yang tadi berhasil
        ]
        
        for keywords in test_keywords:
            print(f"\n--- Testing: {keywords} ---")
            
            start_time = time.time()
            result = service.searchCVs(keywords, algorithm='KMP', topMatches=3)
            end_time = time.time()
            
            print(f"⏱️  Time: {(end_time - start_time):.2f}s")
            print(f"📊 Results: {len(result['results'])}")
            
            metadata = result.get('metadata', {})
            print(f"🔍 Files processed: {metadata.get('total_processed', 'N/A')}")
            
            if result['results']:
                print("✅ Found matches:")
                for i, res in enumerate(result['results'][:2], 1):
                    print(f"   {i}. {res['name']} - Score: {res['match_score']:.1f}%")
                    print(f"      Keywords found: {res['keywords']}")
            else:
                print("❌ No matches found")
        
        # Test manual extraction dari satu file PDF
        print(f"\n--- Manual PDF Text Extraction Test ---")
        pdf_files = service.fileManager.listPDFFiles(str(service.fileManager.getDataDir()))
        
        if pdf_files:
            # Test beberapa file random
            test_files = pdf_files[:5]  # Test 5 file pertama
            
            for pdf_path in test_files:
                print(f"\nTesting file: {os.path.basename(pdf_path)}")
                
                try:
                    # Extract text
                    text = service.pdfExtractor.PDFExtractForMatch(pdf_path)
                    
                    if text:
                        print(f"📄 Text length: {len(text)} characters")
                        
                        # Check for Python keywords manually
                        text_lower = text.lower()
                        python_variants = ['python', 'Python', 'PYTHON']
                        
                        for variant in python_variants:
                            count = text.count(variant)
                            if count > 0:
                                print(f"✅ Found '{variant}': {count} times")
                                
                                # Show context
                                idx = text.find(variant)
                                if idx >= 0:
                                    start = max(0, idx - 30)
                                    end = min(len(text), idx + 30)
                                    context = text[start:end].replace('\n', ' ')
                                    print(f"   Context: ...{context}...")
                                break
                        else:
                            print("❌ No Python keyword found in this file")
                            
                        # Show sample text
                        sample = text[:200].replace('\n', ' ')
                        print(f"📝 Sample text: {sample}...")
                        
                    else:
                        print("❌ Failed to extract text")
                        
                except Exception as e:
                    print(f"❌ Error extracting from {pdf_path}: {e}")
        
    except Exception as e:
        print(f"❌ Error in debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_python_search()
