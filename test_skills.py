#!/usr/bin/env python3
"""
Test skill extraction untuk dataset accountant
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from services.ATSService import ATSService

def test_skill_extraction():
    print("🔧 Test Skill Extraction - Dataset Accountant")
    print("=" * 60)
    
    service = ATSService()
    
    # Test dengan beberapa sample teks yang mungkin ada di CV accountant
    test_texts = [
        "Senior Accountant with 5 years experience in financial reporting and QuickBooks",
        "CPA certified professional skilled in Excel, SAP, and budget analysis",
        "Accounting graduate with expertise in auditing, tax preparation and GAAP compliance",
        "Financial analyst with strong analytical skills and experience in cost accounting"
    ]
    
    print("🧪 Testing skill extraction:")
    print("-" * 40)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}:")
        print(f"Text: {text}")
        
        # Test skill extraction method
        skills = service._extractSkillsFromSummary(text)
        print(f"Extracted Skills: {skills}")
    
    # Test dengan CV asli dari dataset
    print("\n📋 Testing dengan CV asli dari dataset:")
    print("-" * 40)
    
    # Ambil beberapa CV untuk test
    cv_paths = service.getAllCVPaths()
    
    if cv_paths:
        # Test dengan 3 CV pertama
        for i, cv_path in enumerate(cv_paths[:3]):
            print(f"\nCV {i+1}: {Path(cv_path).name}")
            try:
                # Extract text dan cari skills
                text = service._extract_text_from_pdf(cv_path)
                if text:
                    skills = service._extractSkillsFromSummary(text[:1000])  # First 1000 chars
                    print(f"Found Skills: {skills}")
                    print(f"Text Preview: {text[:200]}...")
                else:
                    print("No text extracted")
            except Exception as e:
                print(f"Error: {e}")
    
    print(f"\n✅ Skill extraction sekarang menggunakan skills yang relevan untuk ACCOUNTANT dataset")

if __name__ == "__main__":
    test_skill_extraction()
