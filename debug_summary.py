#!/usr/bin/env python3
"""
Simple Summary Debug Test
Test sederhana untuk debug masalah summary functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_summary_debug():
    """Debug test untuk summary"""
    
    print("=" * 60)
    print("🔧 SUMMARY DEBUG TEST")
    print("=" * 60)
    
    try:
        # Test import
        print("1. Testing imports...")
        from services.ATSService import ATSService
        from models.SummaryCard import SummaryData
        print("✅ Imports successful")
        
        # Test service creation
        print("\n2. Testing service creation...")
        service = ATSService()
        print("✅ ATSService created")
        
        # Test database connection
        print("\n3. Testing database connection...")
        if service.db.connect():
            print("✅ Database connected")
            
            # Test simple query
            result = service.db.fetchOne("SELECT COUNT(*) FROM ApplicantProfile")
            if result:
                print(f"✅ ApplicantProfile count: {result[0]}")
            
            result = service.db.fetchOne("SELECT COUNT(*) FROM ApplicationDetail") 
            if result:
                print(f"✅ ApplicationDetail count: {result[0]}")
                
            # Test get cv_path for detail_id = 1
            result = service.db.fetchOne("SELECT cv_path, applicant_id FROM ApplicationDetail WHERE detail_id = 1")
            if result:
                cv_path, applicant_id = result
                print(f"✅ detail_id 1: cv_path={cv_path}, applicant_id={applicant_id}")
                
                # Test get applicant info
                result2 = service.db.fetchOne("SELECT first_name, last_name, phone_number FROM ApplicantProfile WHERE applicant_id = %s", (applicant_id,))
                if result2:
                    first_name, last_name, phone_number = result2
                    print(f"✅ Applicant info: {first_name} {last_name}, phone: {phone_number}")
            
            service.db.disconnect()
        else:
            print("❌ Database connection failed")
            return
        
        # Test manual summary creation
        print("\n4. Testing manual summary creation...")
        
        # Create manual summary data untuk testing GUI
        manual_summary = {
            'name': 'AR13L H3RFR1S0N',
            'skills': 'Digital Marketing, SEO, Analytics, Team Leadership',
            'experience': 'Marketing Manager at ABC Agency (2021-Present)\nManaged digital campaigns for 15+ clients',
            'education': 'MBA Marketing - Harvard Business School (2019)',
            'birth_date': '2003-08-03',
            'phone_number': '082154321789',
            'cv_path': 'data/DIGITAL-MEDIA/15353911.pdf'
        }
        
        print("✅ Manual summary created:")
        for key, value in manual_summary.items():
            print(f"   {key}: {value}")
        
        # Test summary widget format
        print("\n5. Testing SummaryWidget format...")
        
        # Simulasi createInfoSection
        def simulate_info_section(title, content):
            print(f"   📋 Section: {title}")
            print(f"      Content: {content[:50]}..." if len(content) > 50 else f"      Content: {content}")
        
        simulate_info_section("Nama", manual_summary['name'])
        simulate_info_section("Keterampilan", manual_summary['skills'])
        simulate_info_section("Pengalaman", manual_summary['experience'])
        simulate_info_section("Pendidikan", manual_summary['education'])
        
        print(f"\n✅ SummaryWidget format simulation complete!")
        
        # Test dengan getSummary method yang sebenarnya
        print("\n6. Testing real getSummary method...")
        try:
            summary = service.getSummary(application_id=1)
            print(f"✅ Real summary created:")
            print(f"   Full Name: {summary.full_name}")
            print(f"   Phone: {summary.phone_number}")
            print(f"   CV Path: {summary.cv_path}")
            print(f"   Skills: {len(summary.skills)} items")
            print(f"   Experience: {len(summary.work_experience)} items")
            print(f"   Education: {len(summary.education)} items")
            
        except Exception as e:
            print(f"⚠️  getSummary error (expected if CV file not found): {e}")
        
        print(f"\n{'='*60}")
        print("🎉 SUMMARY DEBUG COMPLETED!")
        print("Main issue might be: CV files not existing in the file system")
        print("Solution: GUI should handle missing CV files gracefully")
        print("="*60)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

def test_gui_integration_fix():
    """Test untuk memperbaiki integrasi GUI"""
    
    print(f"\n{'='*60}")
    print("🔧 GUI INTEGRATION FIX")
    print("="*60)
    
    print("""
MASALAH YANG DITEMUKAN:
1. ❌ Summary widget tidak menampilkan data
2. ❌ Kemungkinan CV files tidak ditemukan
3. ❌ Error handling tidak adequate

SOLUSI YANG DIREKOMENDASIKAN:
1. ✅ Improve error handling di getSummary method
2. ✅ Add fallback data when CV files are missing  
3. ✅ Better user feedback in GUI
4. ✅ Test dengan mock data

LANGKAH PERBAIKAN:
1. Update getSummary untuk handle missing files
2. Update SummaryWidget untuk show error states
3. Add loading indicators
4. Add mock data fallback
""")

def main():
    """Run debug tests"""
    test_summary_debug()
    test_gui_integration_fix()

if __name__ == "__main__":
    main()
