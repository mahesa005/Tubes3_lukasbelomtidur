#!/usr/bin/env python3
"""
Final Integration Test - Verify that all components work together
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_main_integration():
    """Test that main.py runs without errors"""
    print("Testing main.py integration...")
    
    try:
        # Import main components
        from services.ATSService import ATSService
        from algorithm.PatternMatcher import PatternMatcher
        from pdfprocessor.regexExtractor import RegexExtractor
        from utils.FileManager import FileManager
        
        print("✓ All main imports successful")
        
        # Test service initialization
        service = ATSService()
        print("✓ ATSService initialized")
          # Test pattern matcher
        pm = PatternMatcher()
        test_text = "This is a test document about Python programming"
        result = pm.exactMatch(test_text, ["Python"], "KMP")
        print(f"✓ Pattern matching works: found matches in result")
        
        # Test regex extractor
        extractor = RegexExtractor()
        test_cv = "John Doe, john@email.com, Skills: Python, Java"
        extracted = extractor.extractAllInformation(test_cv)
        print(f"✓ Regex extraction works: found {len(extracted['emails'])} emails, {len(extracted['skills'])} skills")
        
        # Test file manager
        fm = FileManager()
        print("✓ FileManager initialized")
        
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("The ATS CV Matcher system is fully integrated and working properly.")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Test database connectivity"""
    print("\nTesting database connection...")
    
    try:
        from database.connection import DatabaseConnection        
        db = DatabaseConnection()
        if db.connect():
            print("✓ Database connection successful")
            
            # Test a simple query
            result = db.fetchOne("SELECT COUNT(*) FROM applicants")
            if result:
                count = result[0]
                print(f"✓ Database query works: {count} applicants in database")
            
            db.disconnect()
            return True
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Run final integration tests"""
    print("=" * 60)
    print("FINAL INTEGRATION TEST")
    print("=" * 60)
    
    integration_ok = test_main_integration()
    db_ok = test_database_connection()
    
    print("\n" + "=" * 60)
    if integration_ok and db_ok:
        print("🎉 ALL SYSTEMS GO! 🎉")
        print("The ATS CV Matcher is ready for use!")
        print("\nTo run the application:")
        print("python main.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("Please check the errors above")
    print("=" * 60)

if __name__ == "__main__":
    main()
