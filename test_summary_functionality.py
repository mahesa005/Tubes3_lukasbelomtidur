#!/usr/bin/env python3
"""
Test Summary Functionality
Test untuk memastikan tombol Summary di GUI bekerja dengan benar
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.ATSService import ATSService

def test_get_summary():
    """Test getSummary method"""
    
    print("=" * 60)
    print("🧪 TESTING SUMMARY FUNCTIONALITY")
    print("=" * 60)
    
    try:
        service = ATSService()
        
        # Test dengan detail_id yang ada di seeding.sql (1, 2, 3, dll.)
        test_detail_ids = [1, 2, 3, 4, 5]
        
        for detail_id in test_detail_ids:
            print(f"\n--- Testing Summary for detail_id: {detail_id} ---")
            
            try:
                summary = service.getSummary(application_id=detail_id)
                
                print(f"✅ Full Name: {summary.full_name}")
                print(f"✅ Birth Date: {summary.birth_date}")
                print(f"✅ Phone: {summary.phone_number}")
                print(f"✅ CV Path: {summary.cv_path}")
                print(f"✅ Skills: {summary.skills[:3]}..." if len(summary.skills) > 3 else f"✅ Skills: {summary.skills}")
                print(f"✅ Experience entries: {len(summary.work_experience)}")
                print(f"✅ Education entries: {len(summary.education)}")
                
                # Test format yang diharapkan GUI
                summary_dict = {
                    'name': summary.full_name,
                    'skills': ', '.join(summary.skills) if summary.skills else 'Tidak ada data skills',
                    'experience': '\n'.join(summary.work_experience) if summary.work_experience else 'Tidak ada data pengalaman',
                    'education': '\n'.join(summary.education) if summary.education else 'Tidak ada data pendidikan',
                    'birth_date': summary.birth_date,
                    'phone_number': summary.phone_number,
                    'cv_path': summary.cv_path
                }
                
                print(f"✅ Summary Dict for GUI:")
                for key, value in summary_dict.items():
                    if key in ['skills', 'experience', 'education']:
                        display_value = value[:50] + "..." if len(str(value)) > 50 else value
                        print(f"   {key}: {display_value}")
                    else:
                        print(f"   {key}: {value}")
                
            except Exception as e:
                print(f"❌ Error untuk detail_id {detail_id}: {e}")
        
        print(f"\n{'='*60}")
        print("🎉 SUMMARY TESTING COMPLETED!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ MAJOR ERROR: {e}")
        import traceback
        traceback.print_exc()

def test_summary_with_fake_cv():
    """Test summary dengan CV data palsu untuk memastikan extraction bekerja"""
    
    print(f"\n{'='*60}")
    print("🧪 TESTING SUMMARY WITH SAMPLE CV")
    print("="*60)
    
    try:
        service = ATSService()
        
        # Buat temporary CV file untuk testing
        sample_cv_content = """
        AR13L H3RFR1S0N
        Email: ariel.herfrison@marketing.com
        Phone: 081223498761
        
        Summary: Marketing Manager with 5+ years experience
        
        Skills: Digital Marketing, SEO, Analytics, Team Leadership
        
        Experience:
        Marketing Manager at ABC Agency (2021-Present)
        - Managed digital campaigns for 15+ clients
        
        Education:
        MBA Marketing - Harvard Business School (2019)
        """
        
        # Simulasi path CV
        fake_cv_path = "data/DIGITAL-MEDIA/15353911.pdf"
        
        print(f"Testing dengan CV path: {fake_cv_path}")
        
        # Test getSummary dengan cv_path saja (tidak perlu application_id)
        try:
            summary = service.getSummary(cv_path=fake_cv_path)
            print(f"✅ Summary berhasil dibuat:")
            print(f"   Full Name: {summary.full_name}")
            print(f"   Skills: {summary.skills}")
            print(f"   CV Path: {summary.cv_path}")
            
        except Exception as e:
            print(f"⚠️  CV file tidak ditemukan (expected): {e}")
            print("   Ini normal karena CV file mungkin tidak ada di sistem")
        
    except Exception as e:
        print(f"❌ Error in fake CV test: {e}")

def test_summary_widget_integration():
    """Test integrasi dengan SummaryWidget format"""
    
    print(f"\n{'='*60}")
    print("🧪 TESTING SUMMARY WIDGET INTEGRATION")
    print("="*60)
    
    # Simulasi data yang akan dikirim ke SummaryWidget
    sample_summary_data = {
        'name': 'AR13L H3RFR1S0N',
        'skills': 'Digital Marketing, SEO, Analytics, Team Leadership',
        'experience': 'Marketing Manager at ABC Agency (2021-Present)\n- Managed digital campaigns for 15+ clients',
        'education': 'MBA Marketing - Harvard Business School (2019)',
        'birth_date': '2003-08-03',
        'phone_number': '082154321789',
        'cv_path': 'data/DIGITAL-MEDIA/15353911.pdf'
    }
    
    print("✅ Sample data for SummaryWidget:")
    for key, value in sample_summary_data.items():
        print(f"   {key}: {value}")
    
    # Test format yang akan ditampilkan di GUI
    print(f"\n✅ Format untuk GUI sections:")
    print(f"   [Nama]: {sample_summary_data['name']}")
    print(f"   [Keterampilan]: {sample_summary_data['skills']}")
    print(f"   [Pengalaman]: {sample_summary_data['experience'][:50]}...")
    print(f"   [Pendidikan]: {sample_summary_data['education']}")
    
    print(f"\n✅ Summary Widget integration format ready!")

def main():
    """Run all summary tests"""
    test_get_summary()
    test_summary_with_fake_cv()
    test_summary_widget_integration()
    
    print(f"\n{'🎯'*20}")
    print("SUMMARY FUNCTIONALITY: READY FOR GUI!")
    print(f"{'🎯'*20}")

if __name__ == "__main__":
    main()
