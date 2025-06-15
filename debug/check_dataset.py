#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from services.ATSService import ATSService
from utils.FileManager import FileManager
from pdfprocessor.pdfExtractor import PDFExtractor

def check_dataset_content():
    """Check what's actually in the dataset"""
    print("Checking dataset content...")
    
    file_manager = FileManager()
    pdf_extractor = PDFExtractor()
    
    data_dir = r"c:\Users\MSI\Desktop\tubes3stima\Tubes3_lukasbelomtidur\Tubes3_lukasbelomtidur\src\archive\data\data"
    
    # Get some PDF files to check
    pdf_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
                if len(pdf_files) >= 10:  # Check first 10 files
                    break
        if len(pdf_files) >= 10:
            break
    
    print(f"Found {len(pdf_files)} PDF files to check")
    
    python_count = 0
    programming_keywords = ['python', 'java', 'javascript', 'c++', 'php', 'programming', 'developer', 'software']
    keyword_counts = {kw: 0 for kw in programming_keywords}
    
    for i, pdf_file in enumerate(pdf_files):
        print(f"Checking file {i+1}: {os.path.basename(pdf_file)}")
        try:
            text = pdf_extractor.PDFtoText(pdf_file)
            text_lower = text.lower()
            
            # Check for programming keywords
            for keyword in programming_keywords:
                if keyword in text_lower:
                    keyword_counts[keyword] += 1
                    print(f"  Found '{keyword}' in this file")
            
            # Show first 200 characters of text
            print(f"  Text preview: {text[:200]}...")
            print()
            
        except Exception as e:
            print(f"  Error processing file: {e}")
    
    print("\nSummary:")
    print("Programming keyword counts:")
    for keyword, count in keyword_counts.items():
        print(f"  {keyword}: {count} files")
    
    # Also test the search function
    print("\nTesting search function:")
    service = ATSService()
    
    test_keywords = ['python', 'Python', 'PYTHON', 'manager', 'experience', 'education']
    for keyword in test_keywords:
        result = service.searchCVs([keyword])
        print(f"  '{keyword}': {len(result.get('results', []))} results")

if __name__ == "__main__":
    check_dataset_content()
