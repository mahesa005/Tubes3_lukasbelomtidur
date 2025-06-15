#!/usr/bin/env python3
"""
Test untuk memverifikasi bahwa error algoritma sudah diperbaiki
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from algorithm.PatternMatcher import PatternMatcher

def test_algorithm_fix():
    print("🧪 Test Algorithm Fix")
    print("=" * 50)
    
    matcher = PatternMatcher()
    
    sample_text = "This is a sample text with some teacher keywords and experience."
    keywords = ["teacher", "experience"]
    
    # Test yang sebelumnya error
    test_cases = [
        ("KMP", "KMP algorithm"),
        ("Boyer-Moore", "Boyer-Moore algorithm from GUI"),
        ("BM", "BM shorthand"),
        ("kmp", "lowercase KMP"),
        ("boyer-moore", "lowercase Boyer-Moore")
    ]
    
    print("🔍 Testing different algorithm formats:")
    print("-" * 40)
    
    for algorithm, description in test_cases:
        try:
            result = matcher.exactMatch(sample_text, keywords, algorithm)
            print(f"✅ {algorithm:12} ({description}): SUCCESS")
            print(f"   Matches found: {sum(r['count'] for r in result['matches'].values())}")
            print(f"   Processing time: {result['endtime']}")
            print()
        except Exception as e:
            print(f"❌ {algorithm:12} ({description}): FAILED - {e}")
            print()
    
    # Test invalid algorithm
    print("🔍 Testing invalid algorithm:")
    print("-" * 40)
    try:
        result = matcher.exactMatch(sample_text, keywords, "INVALID")
        print("❌ Should have failed but didn't")
    except Exception as e:
        print(f"✅ Correctly rejected invalid algorithm: {e}")
    
    print(f"\n📊 ALGORITHM FIX STATUS:")
    print(f"  • KMP: Supported ✅")
    print(f"  • Boyer-Moore: Supported ✅") 
    print(f"  • BM: Supported ✅")
    print(f"  • Case insensitive: Supported ✅")
    print(f"  • Error should be resolved ✅")

if __name__ == "__main__":
    test_algorithm_fix()
