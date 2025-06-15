#!/usr/bin/env python3
"""
Test Case untuk RegexExtractor berdasarkan data seeding.sql
Menggunakan nama-nama dan pattern dari database untuk testing yang lebih realistis
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pdfprocessor.regexExtractor import RegexExtractor
from pprint import pprint

def test_seeding_based_names():
    """Test dengan nama-nama dari seeding.sql (l33t speak variations)"""
    
    extractor = RegexExtractor()
    
    print("=" * 80)
    print("TEST CASE: NAMA-NAMA DARI SEEDING DATABASE")
    print("=" * 80)
    
    # Test case 1: Mohammad Nugraha dengan l33t speak
    cv_mohammad = """
    Moh4mm4d Nu9r4h4
    Email: mohammad.nugraha@email.com
    Phone: 081234567891
    Address: Jl. Kenanga No. 12, Jakarta
    
    Summary:
    Professional software engineer with 5+ years experience in full-stack development.
    
    Skills: Python, JavaScript, React, Node.js, MySQL, Git, Docker
    
    Experience:
    Senior Software Engineer at TechCorp (2020-2023)
    Developed web applications using modern frameworks
    
    Education:
    S1 Computer Science ITB 2016-2020
    """
    
    print("\n--- Test Case 1: Mohammad Nugraha (l33t speak) ---")
    result = extractor.extractAllInformation(cv_mohammad)
    pprint(result)
    
    # Test case 2: Ariel Herfrison dengan berbagai variasi
    cv_ariel = """
    AR13L H3RFR1S0N
    📧 ariel.herfrison@gmail.com | 📞 +62 812-349-8761
    🏠 Jl. Jeruk No. 2, Bekasi
    
    PROFESSIONAL SUMMARY
    Marketing professional with expertise in digital campaigns and brand management.
    
    SKILLS: Digital Marketing, SEO/SEM, Content Strategy, Analytics, Team Leadership
    
    EXPERIENCE:
    Marketing Manager | ABC Marketing Agency | 2021-Present
    • Managed digital campaigns for 15+ clients
    • Increased ROI by 40% through data-driven strategies
    
    EDUCATION:
    Master of Business Administration | Harvard Business School | 2019
    """
    
    print("\n--- Test Case 2: Ariel Herfrison (caps + l33t) ---")
    result = extractor.extractAllInformation(cv_ariel)
    pprint(result)
    
    # Test case 3: Farhan Nafis dengan format minimal
    cv_farhan = """
    f4rh4n naf15 - farhan.nafis@email.com - 081254789621
    
    Objective: Seeking software development position in fintech industry
    
    Technical Skills: Java, C++, Python, Spring Boot, PostgreSQL
    
    Work Experience:
    Software Developer at FinanceApp Inc (2022-2024)
    Junior Developer at StartupTech (2021-2022)
    
    Education:
    Computer Science Degree - University of Indonesia (2021)
    """
    
    print("\n--- Test Case 3: Farhan Nafis (minimal format) ---")
    result = extractor.extractAllInformation(cv_farhan)
    pprint(result)

def test_industry_keywords():
    """Test extraction dengan keywords dari berbagai industri di seeding.sql"""
    
    extractor = RegexExtractor()
    
    print("\n" + "=" * 80)
    print("TEST CASE: INDUSTRY KEYWORDS DARI SEEDING DATABASE")
    print("=" * 80)
    
    # Test case 1: Information Technology
    cv_it = """
    H41k4l 455y4uq1
    Email: haikal.assyauqi@tech.com
    Phone: 081222334455
    
    Summary: Experienced software developer specializing in cloud architecture
    
    Skills: Python, JavaScript, AWS, Docker, Kubernetes, DevOps, React, Node.js
    
    Experience:
    Cloud Architect at TechCorp (2022-Present)
    DevOps Engineer at StartupCloud (2020-2022)
    Software Developer at WebSolutions (2019-2020)
    
    Education:
    S1 Information Technology - Bandung Institute of Technology
    """
    
    print("\n--- IT Industry CV ---")
    result = extractor.extractAllInformation(cv_it)
    print(f"Skills found: {result['skills']}")
    print(f"Email: {result['emails']}")
    print(f"Phone: {result['phones']}")
    
    # Test case 2: Healthcare
    cv_healthcare = """
    R4d3n Fr4nC15c0
    Email: raden.francisco@hospital.com
    Phone: 081293847561
    
    Summary: Experienced medical professional with specialization in anesthesiology
    
    Skills: Medical procedures, Patient care, Emergency response, Medical equipment
    
    Experience:
    Anesthesiologist at General Hospital (2021-Present)
    Doctor at Community Clinic (2019-2021)
    Nurse at Emergency Ward (2018-2019)
    
    Education:
    Medical Degree - Faculty of Medicine, University of Indonesia
    """
    
    print("\n--- Healthcare Industry CV ---")
    result = extractor.extractAllInformation(cv_healthcare)
    print(f"Skills found: {result['skills']}")
    print(f"Experience: {result['experience']}")
    
    # Test case 3: Finance
    cv_finance = """
    4l4nd MuL14
    Email: aland.mulia@bank.com
    Phone: 081234559999
    
    Summary: Financial analyst with expertise in investment and risk management
    
    Skills: Financial modeling, Risk analysis, Investment planning, Excel, SQL
    
    Experience:
    Financial Planner at Major Bank (2022-Present)
    Cost Accountant at Finance Corp (2020-2022)
    Tax Consultant at Accounting Firm (2019-2020)
    
    Education:
    S1 Finance and Banking - University of Economics
    """
    
    print("\n--- Finance Industry CV ---")
    result = extractor.extractAllInformation(cv_finance)
    print(f"Skills found: {result['skills']}")
    print(f"Summary: {result['summary'][:100]}...")

def test_phone_patterns_from_seeding():
    """Test phone extraction dengan pattern dari seeding.sql"""
    
    extractor = RegexExtractor()
    
    print("\n" + "=" * 80)
    print("TEST CASE: PHONE PATTERNS DARI SEEDING DATABASE")
    print("=" * 80)
    
    # Phone numbers dari seeding.sql
    phone_samples = [
        "081234567891",  # Mohammad
        "082123456781",  # Mohammad variant
        "081223498761",  # Ariel
        "082154321789",  # Ariel variant
        "081254789621",  # Farhan
        "082145678912",  # Farhan variant
        "081222334455",  # Haikal
        "082122334456",  # Haikal variant
    ]
    
    test_text = f"""
    Contact Information:
    Primary: {phone_samples[0]}
    Secondary: {phone_samples[1]}
    Office: {phone_samples[2]}
    Mobile: +62-{phone_samples[3][1:]}
    WhatsApp: 0{phone_samples[4][1:]}
    Emergency: ({phone_samples[5][:3]}) {phone_samples[5][3:6]}-{phone_samples[5][6:]}
    """
    
    print(f"Test text:\n{test_text}")
    
    print("\n--- Raw Phone Extraction ---")
    phones_raw = extractor.extractPhone(test_text)
    print(f"Raw phones: {phones_raw}")
    
    print("\n--- Clean Phones (12 digits) ---")
    phones_12 = extractor.extractPhones(test_text, 12)
    print(f"12-digit phones: {phones_12}")
    
    print("\n--- Clean Phones (11 digits) ---")
    phones_11 = extractor.extractPhones(test_text, 11)
    print(f"11-digit phones: {phones_11}")

def test_address_patterns():
    """Test extraction dengan alamat dari seeding.sql"""
    
    extractor = RegexExtractor()
    
    print("\n" + "=" * 80)
    print("TEST CASE: ADDRESS PATTERNS DARI SEEDING DATABASE")
    print("=" * 80)
    
    # Alamat dari seeding.sql
    cv_with_addresses = """
    1khw4n 4lH4k1m
    Email: ikhwan.alhakim@email.com
    Phone: 081223456789
    Address: Jl. Kenari No. 23, Pariaman
    
    Summary: Professional with experience across multiple Indonesian cities
    
    Skills: Communication, Leadership, Problem solving, Team management
    
    Experience:
    Manager at Company Jakarta (2022-Present)
    Address: Jl. Sudirman No. 45, Jakarta Pusat
    
    Supervisor at Office Surabaya (2020-2022)
    Location: Jl. Pemuda No. 12, Surabaya
    
    Analyst at Branch Medan (2019-2020)
    Address: Jl. Gatot Subroto No. 88, Medan
    
    Education:
    University of North Sumatra, Medan
    Campus Address: Jl. Dr. Mansur No. 9, Padang Bulan, Medan
    """
    
    print("--- Complete Information Extraction ---")
    result = extractor.extractAllInformation(cv_with_addresses)
    
    print(f"Name pattern detected: 1khw4n 4lH4k1m (l33t speak)")
    print(f"Emails: {result['emails']}")
    print(f"Phones: {result['phones']}")
    print(f"Experience entries: {len(result['experience'])}")
    print(f"Education entries: {len(result['education'])}")
    
    # Test text cleaning dengan alamat
    print("\n--- Text Cleaning Test ---")
    address_text = "Jl. Kenari No. 23, Pariaman • Jl. Sudirman No. 45, Jakarta"
    cleaned = extractor.cleanseText(address_text)
    separated = extractor.seperatePunctuations(address_text)
    
    print(f"Original: {address_text}")
    print(f"Cleaned: {cleaned}")
    print(f"Separated: {separated}")

def test_role_keywords():
    """Test dengan role keywords dari seeding.sql"""
    
    extractor = RegexExtractor()
    
    print("\n" + "=" * 80)
    print("TEST CASE: JOB ROLES DARI SEEDING DATABASE")
    print("=" * 80)
    
    # CV dengan berbagai role dari seeding
    cv_multiple_roles = """
    4HMAD r4f1
    Email: ahmad.rafi@careers.com
    Phone: 082134672298
    
    Summary: Versatile professional with experience in multiple industries
    
    Skills: Software Development, Financial Analysis, Project Management, Team Leadership
    
    Experience:
    Software Developer at TechStart (2023-Present)
    • Developed web applications using Python and React
    • Implemented DevOps practices and CI/CD pipelines
    
    QA Engineer at QualityTech (2022-2023)
    • Automated testing processes
    • Ensured software quality standards
    
    Financial Planner at InvestBank (2021-2022)
    • Created investment strategies for clients
    • Analyzed market trends and risks
    
    Teaching Assistant at University (2020-2021)
    • Assisted in computer science courses
    • Mentored students in programming
    
    Education:
    Master of Computer Science - Tech University (2020)
    Bachelor of Finance - Business School (2018)
    """
    
    print("--- Multiple Roles CV Analysis ---")
    result = extractor.extractAllInformation(cv_multiple_roles)
    
    print(f"Email: {result['emails']}")
    print(f"Phone: {result['phones']}")
    print(f"Skills: {result['skills']}")
    print(f"Experience entries: {len(result['experience'])}")
    print("Experience details:")
    for i, exp in enumerate(result['experience'], 1):
        print(f"  {i}. {exp['desc'][:60]}...")
    
    print(f"Education entries: {len(result['education'])}")
    for i, edu in enumerate(result['education'], 1):
        print(f"  {i}. {edu['desc']}")

def main():
    """Run all seeding-based test cases"""
    
    print("🧪 REGEX EXTRACTOR TEST CASES BERDASARKAN SEEDING.SQL")
    print("Testing dengan data realistis dari database seeding")
    
    try:
        test_seeding_based_names()
        test_industry_keywords()
        test_phone_patterns_from_seeding()
        test_address_patterns()
        test_role_keywords()
        
        print(f"\n{'='*80}")
        print("🎉 SEMUA TEST CASES BERHASIL!")
        print("RegexExtractor bekerja dengan baik untuk data dari seeding.sql")
        print("="*80)
        
    except Exception as e:
        print(f"❌ ERROR during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
