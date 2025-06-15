#!/usr/bin/env python3
"""
Debug script untuk menganalisis kenapa path matching gagal
"""

import os
import sys
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

from database.connection import DatabaseConnection

def debug_path_matching():
    """Debug path matching antara search results dan database"""
    
    print("🔍 Debugging Path Matching...")
    print("=" * 60)
    
    # Connect to database
    db = DatabaseConnection()
    if not db.connect():
        print("❌ Failed to connect to database")
        return
    
    try:
        # Get sample paths from database
        cursor = db.connection.cursor()
        cursor.execute("""
            SELECT cv_path, application_id 
            FROM ApplicationDetail 
            ORDER BY application_id 
            LIMIT 10
        """)
        db_results = cursor.fetchall()
        cursor.close()
        
        print(f"📊 Sample database paths ({len(db_results)} entries):")
        for i, (cv_path, app_id) in enumerate(db_results, 1):
            print(f"  {i}. [{app_id}] {repr(cv_path)}")
        
        print("\n" + "=" * 60)
        
        # Get sample files from filesystem
        data_dir = current_dir / 'src' / 'archive' / 'data' / 'data'
        print(f"📁 Checking filesystem: {data_dir}")
        
        sample_files = []
        for root, dirs, files in os.walk(data_dir):
            for file in files[:3]:  # Just first 3 files per directory
                if file.endswith('.pdf'):
                    full_path = os.path.join(root, file)
                    sample_files.append(full_path)
                if len(sample_files) >= 10:
                    break
            if len(sample_files) >= 10:
                break
        
        print(f"📊 Sample filesystem paths ({len(sample_files)} entries):")
        for i, file_path in enumerate(sample_files, 1):
            print(f"  {i}. {repr(file_path)}")
        
        print("\n" + "=" * 60)
        
        # Test path conversion logic
        print("🔄 Testing path conversion logic:")
        base_dir = str(current_dir)
        
        for file_path in sample_files[:5]:
            print(f"\n  Original: {repr(file_path)}")
            
            # Method 1: os.path.relpath
            try:
                rel_path = os.path.relpath(file_path, base_dir)
                print(f"  Relative: {repr(rel_path)}")
            except (ValueError, OSError) as e:
                print(f"  Relative: ERROR - {e}")
                rel_path = file_path
            
            # Method 2: Normalize slashes
            normalized_rel = rel_path.replace('\\', '/')
            print(f"  Normalized: {repr(normalized_rel)}")
            
            # Check if this path exists in database
            path_in_db = any(normalized_rel == db_path for db_path, _ in db_results)
            print(f"  In Database: {'✅ YES' if path_in_db else '❌ NO'}")
            
            # Check variations
            if not path_in_db:
                # Try without src/archive prefix
                if normalized_rel.startswith('src/archive/'):
                    alt_path = normalized_rel[12:]  # Remove 'src/archive/'
                    alt_in_db = any(alt_path == db_path for db_path, _ in db_results)
                    print(f"  Alt path: {repr(alt_path)} -> {'✅ YES' if alt_in_db else '❌ NO'}")
        
        print("\n" + "=" * 60)
        print("🎯 Direct Path Comparison:")
        
        # Check if any of the problematic files from the log exist in database
        problem_files = [
            "src/archive/data/data/ARTS/78107631.pdf",
            "src/archive/data/data/ACCOUNTANT/14055988.pdf",
            "src/archive/data/data/ACCOUNTANT/17407184.pdf"
        ]
        
        for problem_file in problem_files:
            print(f"\n  Problem file: {repr(problem_file)}")
            found = False
            for db_path, app_id in db_results:
                if problem_file in db_path or db_path in problem_file:
                    print(f"    Similar DB entry: {repr(db_path)} [ID: {app_id}]")
                    found = True
            if not found:
                print(f"    ❌ No similar entries found in database")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.disconnect()

if __name__ == "__main__":
    debug_path_matching()
