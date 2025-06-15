print("Testing Boyer-Moore algorithm fix...")

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

try:
    from algorithm.PatternMatcher import PatternMatcher
    
    pm = PatternMatcher()
    
    # Test data
    text = "I am a teacher with experience in education"
    keywords = ["teacher", "experience"]
    
    # Test both formats
    print("Testing KMP...")
    result1 = pm.exactMatch(text, keywords, "KMP")
    print(f"  KMP matches: {sum(r['count'] for r in result1['matches'].values())}")
    
    print("Testing Boyer-Moore...")
    result2 = pm.exactMatch(text, keywords, "Boyer-Moore")  # This was failing before
    print(f"  Boyer-Moore matches: {sum(r['count'] for r in result2['matches'].values())}")
    
    print("Testing BM...")
    result3 = pm.exactMatch(text, keywords, "BM")
    print(f"  BM matches: {sum(r['count'] for r in result3['matches'].values())}")
    
    print("\n✅ ALL ALGORITHM FORMATS WORK!")
    print("The error 'Algoritma tidak dikenali' should be fixed now.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
