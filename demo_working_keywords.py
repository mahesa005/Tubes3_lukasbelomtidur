#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from services.ATSService import ATSService

def demonstrate_working_keywords():
    """Demonstrate keywords that actually work with this dataset"""
    print("=== ATS CV Search Demo ===")
    print("Demonstrating keywords that work with the current dataset")
    print()
    
    service = ATSService()
    
    # Keywords that should work based on the dataset content
    working_keywords = [
        "accountant",
        "accounting", 
        "financial",
        "experience",
        "skills",
        "professional",
        "manager",
        "education",
        "software",
        "analysis",
        "business"
    ]
    
    # Keywords that don't exist in this dataset
    missing_keywords = [
        "Python",
        "Java",
        "programming", 
        "developer",
        "web"
    ]
    
    print("✅ Keywords that WORK with this dataset:")
    print("-" * 50)
    for keyword in working_keywords:
        try:
            result = service.searchCVs([keyword])
            count = len(result.get('results', []))
            if count > 0:
                print(f"  {keyword:15} → {count} results found")
                
                # Show a sample result
                if result.get('results'):
                    sample = result['results'][0]
                    print(f"    📄 Sample: {sample.filename}")
                    print(f"    🎯 Score: {sample.match_score}")
                    if sample.matches:
                        print(f"    💡 Match: {sample.matches[0][:100]}...")
                    print()
            else:
                print(f"  {keyword:15} → 0 results")
        except Exception as e:
            print(f"  {keyword:15} → Error: {e}")
    
    print("\n❌ Keywords that DON'T work with this dataset:")
    print("-" * 50)
    for keyword in missing_keywords:
        try:
            result = service.searchCVs([keyword])
            count = len(result.get('results', []))
            print(f"  {keyword:15} → {count} results found")
        except Exception as e:
            print(f"  {keyword:15} → Error: {e}")
    
    print("\n📊 Dataset Summary:")
    print("-" * 50)
    print("This dataset contains CVs from the ACCOUNTANT category.")
    print("The CVs are focused on financial, accounting, and business roles.")
    print("For programming-related searches, you would need a different dataset")
    print("with software development CVs.")
    
    print("\n💡 Tip: Try searching for accounting and business-related keywords!")

if __name__ == "__main__":
    demonstrate_working_keywords()
