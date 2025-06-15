#!/usr/bin/env python3
"""
Force broader search - bypass early termination for testing
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def force_broader_search():
    """Force search through more files to find Python/Java"""
    
    print("=== Force Broader Search Test ===")
    
    try:
        from src.services.ATSService import ATSService
        service = ATSService()
        
        # Get all PDF files
        from config import DATA_DIR
        pdf_files = service.fileManager.listPDFFiles(str(DATA_DIR))
        print(f"Total PDF files available: {len(pdf_files)}")
        
        # Test sample files manually
        keywords = ['Python', 'Java', 'python', 'java']
        found_files = []
        
        print("\nManually checking sample files...")
        test_sample = pdf_files[::100]  # Check every 100th file for efficiency
        print(f"Checking {len(test_sample)} sample files...")
        
        for i, pdf_path in enumerate(test_sample):
            try:
                print(f"Checking file {i+1}/{len(test_sample)}: {os.path.basename(pdf_path)}")
                
                # Extract text
                text = service.pdfExtractor.PDFExtractForMatch(pdf_path)
                if text:
                    text_lower = text.lower()
                    
                    # Check for keywords
                    for keyword in keywords:
                        if keyword.lower() in text_lower:
                            count = text_lower.count(keyword.lower())
                            print(f"  ✅ Found '{keyword}': {count} times")
                            found_files.append({
                                'file': os.path.basename(pdf_path),
                                'keyword': keyword,
                                'count': count,
                                'path': pdf_path
                            })
                            
                            # Show context
                            idx = text_lower.find(keyword.lower())
                            if idx >= 0:
                                start = max(0, idx - 40)
                                end = min(len(text), idx + len(keyword) + 40)
                                context = text[start:end].replace('\n', ' ')
                                print(f"     Context: ...{context}...")
                            break
                    else:
                        print(f"  ❌ No target keywords found")
                else:
                    print(f"  ❌ Failed to extract text")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
                
            # Don't check too many files to avoid taking too long
            if len(found_files) >= 5:
                print("Found enough samples, stopping manual check")
                break
        
        print(f"\n=== Summary ===")
        if found_files:
            print(f"✅ Found {len(found_files)} files with Python/Java keywords:")
            for item in found_files:
                print(f"  - {item['file']}: '{item['keyword']}' ({item['count']} times)")
                
            # Test search with one of the found files' directory
            print(f"\nNow testing if search algorithm can find these files...")
            
            for keyword in ['Python', 'Java']:
                print(f"\n--- Testing search for: {keyword} ---")
                result = service.searchCVs([keyword], algorithm='KMP', topMatches=1)
                metadata = result.get('metadata', {})
                
                print(f"📊 Results: {len(result['results'])}")
                print(f"🔍 Files processed: {metadata.get('total_processed', 'N/A')}")
                
                if result['results']:
                    print("✅ Search algorithm found matches!")
                    for res in result['results']:
                        print(f"  - {res['name']}: {res['keywords']}")
                else:
                    print("❌ Search algorithm didn't find matches")
        else:
            print("❌ No Python/Java keywords found in sample files")
            print("This might mean:")
            print("1. The CV dataset doesn't contain programming-related CVs")
            print("2. Keywords are written differently (e.g., 'Python programming', 'Java development')")
            print("3. Text extraction is not working properly")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    force_broader_search()
