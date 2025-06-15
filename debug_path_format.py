#!/usr/bin/env python3

import sys
import os
sys.path.append('.')

from src.utils.FileManager import FileManager
from src.database.connection import DatabaseConnection
from config import DATA_DIR

def debug_path_formats():
    # Get some actual file paths
    fm = FileManager()
    pdf_files = fm.listPDFFiles(str(DATA_DIR))
    
    print("=== CURRENT WORKING DIRECTORY ===")
    print(f"CWD: {os.getcwd()}")
    print(f"DATA_DIR: {DATA_DIR}")
    print()
    
    print("=== SAMPLE FILE PATHS (FIRST 5) ===")
    for i, pdf_path in enumerate(pdf_files[:5]):
        print(f"{i+1}. Absolute: {pdf_path}")
        
        # Try different relative path conversions
        try:
            rel_path_1 = os.path.relpath(pdf_path)
            print(f"   os.relpath(): {rel_path_1}")
        except Exception as e:
            print(f"   os.relpath() failed: {e}")
        
        try:
            rel_path_2 = os.path.relpath(pdf_path, os.getcwd())
            print(f"   os.relpath(cwd): {rel_path_2}")
        except Exception as e:
            print(f"   os.relpath(cwd) failed: {e}")
            
        # Try to strip base directory
        try:
            if pdf_path.startswith(os.getcwd()):
                stripped = pdf_path[len(os.getcwd()):].lstrip('\\/')
                print(f"   Stripped: {stripped}")
        except Exception as e:
            print(f"   Strip failed: {e}")
        
        print()
    
    # Check database paths
    print("=== DATABASE PATHS (FIRST 5) ===")
    db = DatabaseConnection()
    if db.connect():
        cursor = db.connection.cursor()
        cursor.execute('SELECT cv_path FROM ApplicationDetail LIMIT 5')
        results = cursor.fetchall()
        for i, (path,) in enumerate(results):
            print(f"{i+1}. DB: {repr(path)}")
        cursor.close()
        db.disconnect()
    
if __name__ == "__main__":
    debug_path_formats()
