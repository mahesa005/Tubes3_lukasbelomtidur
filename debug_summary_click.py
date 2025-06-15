#!/usr/bin/env python3
"""
Debug script untuk mengetes tombol summary/ringkasan
Mari kita cek apakah ada masalah dengan flow dari tombol ke display
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

# Test imports
try:
    from src.services.ATSService import ATSService
    from src.database.connection import DatabaseConnection
    print("✅ Import ATSService berhasil")
except ImportError as e:
    print(f"❌ Error import ATSService: {e}")
    sys.exit(1)

def test_database_connection():
    """Test koneksi database"""
    print("\n=== Testing Database Connection ===")
    
    db = DatabaseConnection()
    try:
        if db.connect():
            print("✅ Database connection successful")
            
            # Test ambil beberapa application_id
            query = "SELECT application_id, cv_path FROM ApplicationDetail LIMIT 5"
            results = db.fetchAll(query)
            
            if results:
                print(f"✅ Found {len(results)} applications in database:")
                for app_id, cv_path in results:
                    print(f"   ID: {app_id}, CV: {cv_path}")
                return results[0][0]  # Return first application_id
            else:
                print("❌ No applications found in database")
                return None
        else:
            print("❌ Database connection failed")
            return None
    except Exception as e:
        print(f"❌ Database error: {e}")
        return None
    finally:
        db.disconnect()

def test_get_summary(application_id):
    """Test getSummary function"""
    print(f"\n=== Testing getSummary for application_id: {application_id} ===")
    
    try:
        ats_service = ATSService()
        summary_data = ats_service.getSummary(application_id=application_id)
        
        print("✅ getSummary executed successfully")
        print(f"📋 Summary Data:")
        print(f"   Full Name: {summary_data.full_name}")
        print(f"   Birth Date: {summary_data.birth_date}")
        print(f"   Phone: {summary_data.phone_number}")
        print(f"   CV Path: {summary_data.cv_path}")
        print(f"   Skills: {summary_data.skills}")
        print(f"   Work Experience: {summary_data.work_experience}")
        print(f"   Education: {summary_data.education}")
        
        # Check if we have any actual data
        has_data = any([
            summary_data.full_name,
            summary_data.phone_number,
            summary_data.skills,
            summary_data.work_experience,
            summary_data.education
        ])
        
        if has_data:
            print("✅ Summary contains data")
        else:
            print("⚠️ Summary is empty - this might be the issue!")
            
        return summary_data
        
    except Exception as e:
        print(f"❌ Error in getSummary: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_summary_dict_conversion(summary_data):
    """Test konversi ke format yang digunakan di GUI"""
    print(f"\n=== Testing Summary Dict Conversion ===")
    
    try:
        # Simulate conversion yang dilakukan di MainWindow.py
        summary_dict = {
            'name': summary_data.full_name,
            'skills': ', '.join(summary_data.skills),
            'experience': '\n'.join(summary_data.work_experience),
            'education': '\n'.join(summary_data.education),
            'birth_date': summary_data.birth_date,
            'phone_number': summary_data.phone_number,
            'cv_path': summary_data.cv_path
        }
        
        print("✅ Summary dict conversion successful:")
        for key, value in summary_dict.items():
            print(f"   {key}: {value[:100] if isinstance(value, str) and len(value) > 100 else value}")
            
        return summary_dict
        
    except Exception as e:
        print(f"❌ Error in dict conversion: {e}")
        return None

def test_gui_simulation():
    """Simulate GUI interaction"""
    print(f"\n=== Simulating GUI Interaction ===")
    
    # Test database
    app_id = test_database_connection()
    if not app_id:
        print("❌ Cannot test without valid application_id")
        return
    
    # Test getSummary
    summary_data = test_get_summary(app_id)
    if not summary_data:
        print("❌ Cannot test without valid summary data")
        return
    
    # Test conversion
    summary_dict = test_summary_dict_conversion(summary_data)
    if not summary_dict:
        print("❌ Cannot test without valid summary dict")
        return
    
    print("\n✅ All tests passed! The summary button should work.")
    print("🔍 If the GUI still shows nothing, the issue is likely in the SummaryWidget display logic.")

def main():
    print("🔧 DEBUG: Tombol Summary/Ringkasan")
    print("=" * 50)
    
    test_gui_simulation()

if __name__ == "__main__":
    main()
