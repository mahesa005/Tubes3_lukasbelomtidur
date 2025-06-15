#!/usr/bin/env python3
"""
Debug script untuk mengecek mengapa searchCVs tidak mengembalikan application_id
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

def debug_search_cvs():
    """Debug searchCVs method"""
    
    print("🔍 DEBUG: SEARCHCVS METHOD")
    print("=" * 50)
    
    try:
        from src.services.ATSService import ATSService
        
        # Create service
        ats_service = ATSService()
        
        # Test with simple search
        print("1. Testing searchCVs with 'python'...")
        result = ats_service.searchCVs(["python"], "KMP", 3)
        
        print(f"Search result type: {type(result)}")
        if isinstance(result, dict):
            print(f"Keys: {list(result.keys())}")
            
            if 'results' in result:
                results = result['results']
                print(f"Number of results: {len(results)}")
                
                for i, res in enumerate(results):
                    print(f"\nResult {i+1}:")
                    print(f"  Type: {type(res)}")
                    print(f"  Keys: {list(res.keys()) if isinstance(res, dict) else 'Not dict'}")
                    
                    if isinstance(res, dict):
                        print(f"  application_id: {res.get('application_id')} (type: {type(res.get('application_id'))})")
                        print(f"  name: {res.get('name')}")
                        print(f"  cv_path: {res.get('cv_path')}")
                        print(f"  match_score: {res.get('match_score')}")
                        
                        # Check if cv_path has corresponding database entry
                        cv_path = res.get('cv_path')
                        if cv_path:
                            print(f"  Testing database lookup for: {cv_path}")
                            
                            # Test direct database query
                            from src.database.connection import DatabaseConnection
                            db = DatabaseConnection()
                            if db.connect():
                                query = """
                                    SELECT ad.application_id, ap.first_name, ap.last_name 
                                    FROM ApplicationDetail ad
                                    JOIN ApplicantProfile ap ON ad.applicant_id = ap.applicant_id
                                    WHERE ad.cv_path = %s
                                """
                                cursor = db.connection.cursor()
                                cursor.execute(query, (cv_path,))
                                db_result = cursor.fetchone()
                                cursor.close()
                                db.disconnect()
                                
                                if db_result:
                                    app_id, first_name, last_name = db_result
                                    print(f"  Database result: ID={app_id}, Name={first_name} {last_name}")
                                else:
                                    print(f"  ❌ No database entry found for this CV path")
                            else:
                                print(f"  ❌ Database connection failed")
        
        # Test batch lookup method directly
        print(f"\n2. Testing _batch_get_cv_info directly...")
        
        if 'results' in locals() and results:
            cv_paths = [res['cv_path'] for res in results if res.get('cv_path')]
            print(f"Testing paths: {cv_paths}")
            
            batch_info = ats_service._batch_get_cv_info(cv_paths)
            print(f"Batch info result: {batch_info}")
            
            for path in cv_paths:
                if path in batch_info:
                    info = batch_info[path]
                    print(f"  ✅ {path}: ID={info.get('application_id')}, Name={info.get('first_name')} {info.get('last_name')}")
                else:
                    print(f"  ❌ {path}: Not found in batch info")
        
    except Exception as e:
        print(f"❌ Error in debug: {e}")
        import traceback
        traceback.print_exc()

def test_simple_search():
    """Test with very simple search to isolate the issue"""
    
    print(f"\n3. Testing simple search with known file...")
    
    try:
        from src.services.ATSService import ATSService
        from src.database.connection import DatabaseConnection
        
        # Get a known CV path from database first
        db = DatabaseConnection()
        if db.connect():
            query = "SELECT application_id, cv_path FROM ApplicationDetail LIMIT 1"
            result = db.fetchOne(query)
            db.disconnect()
            
            if result:
                known_app_id, known_cv_path = result
                print(f"Known file: ID={known_app_id}, Path={known_cv_path}")
                
                # Now test if this file would be found in search
                ats_service = ATSService()
                
                # Manually process this one file
                print(f"Testing if this file contains searchable text...")
                
                # Extract text
                from src.pdfprocessor.pdfExtractor import PDFExtractor
                pdf_extractor = PDFExtractor()
                
                text = pdf_extractor.PDFtoText(known_cv_path)
                print(f"Extracted text length: {len(text) if text else 0}")
                if text:
                    print(f"Text preview: {text[:200]}...")
                    
                    # Test pattern matching
                    from src.algorithm.PatternMatcher import PatternMatcher
                    pattern_matcher = PatternMatcher()
                    
                    # Test with common words
                    test_keywords = ["experience", "skills", "work", "education"]
                    for keyword in test_keywords:
                        matches = pattern_matcher.searchPattern(text, keyword, "KMP")
                        print(f"  Keyword '{keyword}': {len(matches)} matches")
                        
                        if matches:
                            print(f"    This file should appear in search results!")
                            break
                
    except Exception as e:
        print(f"❌ Error in simple test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_search_cvs()
    test_simple_search()
