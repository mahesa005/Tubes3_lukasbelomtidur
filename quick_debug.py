#!/usr/bin/env python3
"""
Quick Debug - Test simple pattern matching
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def quick_debug():
    """Quick debug untuk pattern matching"""
    
    print("=== Quick Pattern Matching Debug ===")
    
    # Test pattern matching dengan text sample
    sample_texts = [
        "I am a Python developer with 5 years experience",
        "Experienced in python programming and data science", 
        "Programming languages: Java, C++, Python, JavaScript",
        "Skills: machine learning, data analysis using python",
        "No programming languages mentioned here",
    ]
    
    keywords = ['Python']
    
    try:
        from src.algorithm.PatternMatcher import PatternMatcher
        matcher = PatternMatcher()
        
        print(f"Testing keyword: {keywords}")
        print()
        
        for i, text in enumerate(sample_texts, 1):
            print(f"Text {i}: {text}")
            
            # Test dengan KMP algorithm
            result = matcher.exactMatch(text, keywords, 'KMP')
            
            total_matches = sum(
                match_data['count'] 
                for match_data in result['matches'].values()
            )
            
            print(f"   Matches found: {total_matches}")
            if total_matches > 0:
                for keyword, data in result['matches'].items():
                    if data['count'] > 0:
                        print(f"   '{keyword}': {data['count']} occurrences")
                        print(f"   Positions: {data['positions']}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def test_file_manager():
    """Test apakah FileManager bisa akses file PDF"""
    print("=== Testing FileManager ===")
    
    try:
        from src.utils.FileManager import FileManager
        fm = FileManager()
        
        pdf_files = fm.listPDFFiles(str(fm.getDataDir()))
        print(f"Found {len(pdf_files)} PDF files")
        
        if pdf_files:
            print("First 5 files:")
            for i, file_path in enumerate(pdf_files[:5], 1):
                print(f"  {i}. {os.path.basename(file_path)}")
                
                # Test if file exists and is readable
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path)
                    print(f"     Size: {size:,} bytes")
                else:
                    print(f"     ❌ File not found!")
                    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_debug()
    print()
    test_file_manager()
