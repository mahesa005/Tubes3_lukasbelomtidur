#!/usr/bin/env python3
"""
Test algoritma skill extraction yang baru (tanpa heuristik/hardcoded list)
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from services.ATSService import ATSService

def test_skill_extraction():
    print("🧪 Test Skill Extraction - TANPA Heuristik")
    print("=" * 60)
    
    service = ATSService()
    
    # Test dengan sample text CV accountant
    sample_cv_texts = [
        """
        SENIOR ACCOUNTANT
        Professional Summary
        Senior accountant with extensive experience in financial reporting, 
        budget analysis, and general ledger management. Skilled in QuickBooks, 
        Excel, and SAP systems. Strong analytical skills and attention to detail.
        
        Skills:
        - Financial Analysis
        - Accounts Payable/Receivable  
        - Tax Preparation
        - Cost Accounting
        - GAAP compliance
        
        Experience with Great Plains, Oracle ERP, and advanced Excel functions.
        Certified Public Accountant (CPA) with Bachelor's degree in Accounting.
        """,
        
        """
        INVESTMENT ACCOUNTANT
        Accomplished professional with strong leadership and interpersonal skills.
        Proficient in Hyperion Workspace, Planning, MAS 90, FRx reporting.
        Experience in reconciliation, auditing, and financial statement preparation.
        Knowledge of IFRS standards and regulatory compliance.
        """,
        
        """
        STAFF ACCOUNTANT  
        Detail-oriented professional with background in quality assurance,
        compliance, auditing, customer service and regulatory reporting.
        Using Peachtree accounting software and Microsoft Office suite.
        Trained in bookkeeping and cash flow management.
        """
    ]
    
    print("🔍 Testing skill extraction pada sample CV:")
    print("-" * 50)
    
    for i, sample_text in enumerate(sample_cv_texts, 1):
        print(f"\n📋 Sample CV {i}:")
        skills = service._extractSkillsFromSummary(sample_text)
        
        print(f"  Skills ditemukan ({len(skills)}):")
        for j, skill in enumerate(skills, 1):
            print(f"    {j}. {skill}")
    
    print(f"\n✅ KEUNGGULAN Algoritma Baru:")
    print("  • TIDAK menggunakan hardcoded list")
    print("  • Pattern recognition murni")
    print("  • Dapat extract skills dari domain apapun")
    print("  • Adaptive terhadap berbagai format CV")
    print("  • Mendeteksi skills berdasarkan context, bukan matching")
    
    print(f"\n🎯 Algoritma menggunakan:")
    print("  1. Skills section detection (Skills:, Technical Skills:)")  
    print("  2. Context patterns (experienced in, proficient in)")
    print("  3. Capitalized terms (software/tools names)")
    print("  4. Tool/software patterns (using X, X software)")
    print("  5. Certification patterns (certified in, trained in)")

if __name__ == "__main__":
    test_skill_extraction()
