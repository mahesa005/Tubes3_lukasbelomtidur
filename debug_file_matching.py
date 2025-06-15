#!/usr/bin/env python3
"""
Debug script untuk mengecek file mana yang benar-benar sesuai antara database dan file system
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

def debug_actual_file_matching():
    """Debug file matching yang sebenarnya"""
    
    print("🔍 DEBUG: ACTUAL FILE MATCHING")
    print("=" * 50)
    
    try:
        from src.database.connection import DatabaseConnection
        from src.services.ATSService import ATSService
        
        # 1. Get files yang benar-benar ada di database dan file system
        print("1. Getting files that exist in BOTH database and file system...")
        
        db = DatabaseConnection()
        if db.connect():
            # Get all CV paths from database
            query = "SELECT application_id, cv_path FROM ApplicationDetail"
            db_results = db.fetchAll(query)
            
            print(f"Total database entries: {len(db_results)}")
            
            # Check which ones actually exist as files
            existing_files = []
            for app_id, cv_path in db_results:
                if os.path.exists(cv_path):
                    existing_files.append((app_id, cv_path))
                    if len(existing_files) <= 5:  # Show first 5
                        print(f"  ✅ ID {app_id}: {cv_path} (EXISTS)")
                elif len(existing_files) <= 5:
                    print(f"  ❌ ID {app_id}: {cv_path} (MISSING)")
            
            print(f"Files that exist: {len(existing_files)}/{len(db_results)}")
            
            db.disconnect()
            
            if not existing_files:
                print("❌ No files exist! This is the problem.")
                return
                
            # 2. Test search pada file yang benar-benar ada
            print(f"\n2. Testing search on existing files...")
            
            # Ambil 1 file yang benar-benar ada
            test_app_id, test_cv_path = existing_files[0]
            print(f"Testing with: ID={test_app_id}, Path={test_cv_path}")
            
            # Extract text dari file ini
            from src.pdfprocessor.pdfExtractor import PDFExtractor
            pdf_extractor = PDFExtractor()
            text = pdf_extractor.PDFtoText(test_cv_path)
            
            if text:
                print(f"Text extracted successfully: {len(text)} chars")
                print(f"Preview: {text[:200]}...")
                
                # Cari kata yang umum dalam text ini
                import re
                words = re.findall(r'\b\w+\b', text.lower())
                common_words = {}
                for word in words:
                    if len(word) > 3:  # Skip short words
                        common_words[word] = common_words.get(word, 0) + 1
                
                # Get top 5 most common words
                top_words = sorted(common_words.items(), key=lambda x: x[1], reverse=True)[:5]
                print(f"Top words in this file: {[word for word, count in top_words]}")
                
                # Test search dengan salah satu kata ini
                test_keyword = top_words[0][0] if top_words else "experience"
                print(f"\n3. Testing search with keyword: '{test_keyword}'")
                
                ats_service = ATSService()
                result = ats_service.searchCVs([test_keyword], "KMP", 5)
                
                if result and 'results' in result:
                    results = result['results']
                    print(f"Search found {len(results)} results")
                    
                    # Check if our test file is in results
                    found_test_file = False
                    for res in results:
                        res_path = res.get('cv_path', '')
                        app_id = res.get('application_id')
                        name = res.get('name')
                        
                        print(f"  Result: ID={app_id}, Name={name}")
                        print(f"    Path: {res_path}")
                        
                        # Check if this is our test file
                        if test_cv_path in res_path or res_path in test_cv_path:
                            found_test_file = True
                            print(f"    ✅ This is our test file!")
                            
                            if app_id is not None:
                                print(f"    ✅ application_id found: {app_id}")
                            else:
                                print(f"    ❌ application_id is None")
                    
                    if not found_test_file:
                        print(f"  ❌ Test file not found in search results")
                        print(f"  Expected path: {test_cv_path}")
                        
                        # Check path format differences
                        abs_test_path = os.path.abspath(test_cv_path)
                        print(f"  Absolute path: {abs_test_path}")
                        
                        for res in results:
                            res_path = res.get('cv_path', '')
                            if os.path.basename(test_cv_path) == os.path.basename(res_path):
                                print(f"  ⚠️ Same filename but different path: {res_path}")
                
            else:
                print("❌ Could not extract text from test file")
        
    except Exception as e:
        print(f"❌ Error in debug: {e}")
        import traceback
        traceback.print_exc()

def test_search_with_known_good_keyword():
    """Test search dengan keyword yang pasti ada"""
    
    print(f"\n4. Testing search with guaranteed keywords...")
    
    try:
        from src.services.ATSService import ATSService
        
        # Kata-kata yang pasti ada di CV
        guaranteed_keywords = ["experience", "skills", "work", "education", "and", "the"]
        
        ats_service = ATSService()
        
        for keyword in guaranteed_keywords[:2]:  # Test 2 keywords
            print(f"\nTesting keyword: '{keyword}'")
            
            result = ats_service.searchCVs([keyword], "KMP", 3)
            
            if result and 'results' in result:
                results = result['results']
                print(f"  Found {len(results)} results")
                
                for i, res in enumerate(results):
                    app_id = res.get('application_id')
                    name = res.get('name')
                    cv_path = res.get('cv_path')
                    
                    print(f"    {i+1}. ID={app_id}, Name={name}")
                    print(f"        Path: {cv_path}")
                    
                    if app_id is not None:
                        print(f"        ✅ Has application_id!")
                        return  # Found working result!
                    else:
                        print(f"        ❌ application_id is None")
            else:
                print(f"  No results found")
    
    except Exception as e:
        print(f"❌ Error in keyword test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_actual_file_matching()
    test_search_with_known_good_keyword()
