#!/usr/bin/env python3
"""
Debug script untuk mengecek path mismatch antara file system dan database
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

def debug_path_mismatch():
    """Debug path mismatch"""
    
    print("🔍 DEBUG: CV PATH MISMATCH")
    print("=" * 50)
    
    try:
        from src.database.connection import DatabaseConnection
        from src.utils.FileManager import FileManager
        from pathlib import Path
        
        # 1. Check database CV paths
        print("1. Checking database CV paths...")
        db = DatabaseConnection()
        if db.connect():
            query = "SELECT application_id, cv_path FROM ApplicationDetail LIMIT 10"
            db_results = db.fetchAll(query)
            
            print(f"Database CV paths (first 10):")
            db_paths = []
            for app_id, cv_path in db_results:
                print(f"  ID {app_id}: {cv_path}")
                db_paths.append(cv_path)
                
                # Check if file exists
                exists = os.path.exists(cv_path)
                print(f"    File exists: {exists}")
            
            db.disconnect()
        
        # 2. Check file system paths
        print(f"\n2. Checking file system paths...")
        file_manager = FileManager()
        
        # Get PDF files from data directory
        data_dir = Path("src/archive/data/data")
        if data_dir.exists():
            pdf_files = file_manager.listPDFFiles(str(data_dir))
            print(f"Found {len(pdf_files)} PDF files in file system")
            
            print(f"File system paths (first 10):")
            for i, pdf_path in enumerate(pdf_files[:10]):
                print(f"  {i+1}: {pdf_path}")
                
                # Normalize path untuk comparison
                normalized_path = pdf_path.replace('\\', '/')
                print(f"    Normalized: {normalized_path}")
        
        # 3. Check for matches
        print(f"\n3. Checking for path matches...")
        if 'db_paths' in locals() and 'pdf_files' in locals():
            matches = 0
            for db_path in db_paths:
                # Try different path formats
                db_path_normalized = db_path.replace('\\', '/')
                
                for fs_path in pdf_files:
                    fs_path_normalized = fs_path.replace('\\', '/')
                    
                    if db_path_normalized == fs_path_normalized:
                        matches += 1
                        print(f"  ✅ Match found: {db_path}")
                        break
                    elif db_path_normalized in fs_path_normalized or fs_path_normalized in db_path_normalized:
                        print(f"  ⚠️ Partial match: DB={db_path} FS={fs_path}")
                else:
                    print(f"  ❌ No match for: {db_path}")
            
            print(f"\nTotal exact matches: {matches}/{len(db_paths)}")
        
        # 4. Test specific path resolution
        print(f"\n4. Testing path resolution...")
        
        if db_paths:
            test_path = db_paths[0]
            print(f"Testing path: {test_path}")
            
            # Try absolute path
            abs_path = os.path.abspath(test_path)
            print(f"  Absolute path: {abs_path}")
            print(f"  Absolute exists: {os.path.exists(abs_path)}")
            
            # Try relative from different directories
            current_dir = os.getcwd()
            print(f"  Current directory: {current_dir}")
            
            relative_path = os.path.join(current_dir, test_path)
            print(f"  Relative path: {relative_path}")
            print(f"  Relative exists: {os.path.exists(relative_path)}")
        
    except Exception as e:
        print(f"❌ Error in debug: {e}")
        import traceback
        traceback.print_exc()

def test_database_query():
    """Test database query directly"""
    
    print(f"\n5. Testing database query directly...")
    
    try:
        from src.database.connection import DatabaseConnection
        
        db = DatabaseConnection()
        if db.connect():
            # Get some CV paths to test
            query = "SELECT cv_path FROM ApplicationDetail LIMIT 5"
            results = db.fetchAll(query)
            
            if results:
                test_paths = [row[0] for row in results]
                print(f"Test paths: {test_paths}")
                
                # Test batch query
                placeholders = ','.join(['%s'] * len(test_paths))
                batch_query = f"""
                    SELECT ad.cv_path, ap.first_name, ap.last_name, ad.application_id 
                    FROM ApplicationDetail ad
                    JOIN ApplicantProfile ap ON ad.applicant_id = ap.applicant_id
                    WHERE ad.cv_path IN ({placeholders})
                """
                
                cursor = db.connection.cursor()
                cursor.execute(batch_query, test_paths)
                batch_results = cursor.fetchall()
                cursor.close()
                
                print(f"Batch query results:")
                for row in batch_results:
                    cv_path, first_name, last_name, app_id = row
                    print(f"  {app_id}: {first_name} {last_name} -> {cv_path}")
                
                print(f"Query returned {len(batch_results)}/{len(test_paths)} results")
            
            db.disconnect()
        
    except Exception as e:
        print(f"❌ Error in database test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_path_mismatch()
    test_database_query()
