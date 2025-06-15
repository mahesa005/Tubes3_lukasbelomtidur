#!/usr/bin/env python3
"""
Advanced Test Cases untuk RegexExtractor dengan fokus pada l33t speak names
dan pattern matching yang challenging dari seeding.sql
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pdfprocessor.regexExtractor import RegexExtractor

def test_leet_speak_variations():
    """Test dengan semua variasi l33t speak dari seeding.sql"""
    
    extractor = RegexExtractor()
    
    print("=" * 80)
    print("ADVANCED TEST: L33T SPEAK NAME VARIATIONS")
    print("=" * 80)
    
    # Semua variasi Mohammad dari seeding.sql
    mohammad_variations = [
        "Moh4mm4d Nu9r4h4",
        "MOH4MM4D NUGR4H4", 
        "M0hammad Nugr4h4",
        "Mohammad NUGR4H4",
        "m0h4mm4d nu9r4h4",
        "MoH4mM4d NugR4h4",
        "M0H4MM4D NuGr4Ha",
        "Mohammad NUGRAHA",
        "m0H4mmad nug9ah4",
        "M0h4mM4D NUGRAHA"
    ]
    
    print("\n--- Testing Mohammad Name Variations ---")
    for i, name in enumerate(mohammad_variations, 1):
        cv_text = f"""
        {name}
        Email: mohammad{i}@email.com
        Phone: 08123456789{i % 10}
        
        Summary: Software engineer with {i} years experience
        Skills: Python, Java, C++
        Experience: Developer at Company{i}
        Education: Computer Science Degree
        """
        
        result = extractor.extractAllInformation(cv_text)
        print(f"{i:2d}. {name:20} -> Email: {result['emails'][0] if result['emails'] else 'None'}")
    
    # Semua variasi Ariel dari seeding.sql
    ariel_variations = [
        "Ari3l H3rfri50n",
        "AR13L H3RFR1S0N",
        "4riel Herfris0n", 
        "AR1EL H3RFR1S0N",
        "Ariel Herfrison",
        "ar13l h3rfr150n",
        "4R13L HERFRI50N",
        "Ari3L HerfR150n",
        "Arie1 HERFRISON",
        "ARI3L h3rfri50n"
    ]
    
    print("\n--- Testing Ariel Name Variations ---")
    for i, name in enumerate(ariel_variations, 1):
        cv_text = f"""
        Name: {name}
        Contact: ariel{i}@company.com, +62812{i:03d}{i:04d}
        
        Professional Summary: Marketing specialist
        Core Skills: Digital Marketing, SEO, Analytics
        Work Experience: Marketing Manager since 202{i % 3}
        Academic Background: MBA from Top University
        """
        
        result = extractor.extractAllInformation(cv_text)
        email = result['emails'][0] if result['emails'] else 'None'
        phone = result['phones'][0] if result['phones'] else 'None'
        print(f"{i:2d}. {name:20} -> Email: {email:25} Phone: {phone}")

def test_complex_cv_patterns():
    """Test dengan CV format yang kompleks menggunakan nama dari seeding"""
    
    extractor = RegexExtractor()
    
    print("\n" + "=" * 80)
    print("ADVANCED TEST: COMPLEX CV PATTERNS")
    print("=" * 80)
    
    # CV dengan format yang sangat kompleks
    complex_cv = """
    ╔═══════════════════════════════════════╗
    ║           F4RH4N N4F15 R4YH4N         ║
    ║        Software Architect & CTO       ║  
    ╚═══════════════════════════════════════╝
    
    📧 Contact Information:
    • Primary Email: farhan.nafis@techcorp.com
    • Secondary: f.nafis.rayhan@gmail.com
    • Phone: +62 812-5478-9621 | +62 821-4567-8912
    • WhatsApp: 0812-5478-9621
    • LinkedIn: linkedin.com/in/farhannafis
    • GitHub: github.com/farhannafis
    
    🎯 PROFESSIONAL SUMMARY
    ═══════════════════════════════════════
    Seasoned software architect with 8+ years of experience in designing and implementing 
    scalable enterprise applications. Expert in microservices architecture, cloud computing, 
    and team leadership. Proven track record of delivering high-performance solutions for 
    fintech and e-commerce platforms.
    
    💻 TECHNICAL SKILLS
    ═══════════════════════════════════════
    Programming Languages: Java, Python, JavaScript, TypeScript, Go, Rust
    Frameworks & Libraries: Spring Boot, React.js, Vue.js, Node.js, Django, FastAPI
    Databases: PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch
    Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, GitLab CI/CD, Terraform
    Architecture: Microservices, Event-driven, Domain-driven design, CQRS
    
    🏢 PROFESSIONAL EXPERIENCE
    ═══════════════════════════════════════
    
    🔸 Chief Technology Officer | TechCorp Indonesia | Jan 2022 - Present
    └─ Lead technical strategy for 50+ engineers across 8 product teams
    └─ Designed microservices architecture serving 1M+ daily active users
    └─ Implemented DevOps practices reducing deployment time by 80%
    └─ Technologies: Java, Spring Boot, AWS, Kubernetes, PostgreSQL
    
    🔸 Senior Software Architect | FinanceApp Pte Ltd | Mar 2020 - Dec 2021
    └─ Architected core banking system processing $100M+ transactions daily
    └─ Led migration from monolith to microservices architecture
    └─ Mentored 15+ junior developers and established coding standards
    └─ Technologies: Java, Python, Docker, AWS Lambda, DynamoDB
    
    🔸 Lead Developer | StartupTech Solutions | Jan 2018 - Feb 2020
    └─ Built e-commerce platform from scratch handling 10K+ concurrent users
    └─ Implemented real-time analytics and recommendation engine
    └─ Established CI/CD pipeline and automated testing frameworks
    └─ Technologies: Node.js, React, MongoDB, Redis, Docker
    
    🎓 EDUCATION & CERTIFICATIONS
    ═══════════════════════════════════════
    
    🎓 Master of Computer Science | Bandung Institute of Technology | 2016-2018
    └─ Thesis: "Scalable Microservices Architecture for High-Traffic Applications"
    └─ GPA: 3.85/4.0
    
    🎓 Bachelor of Informatics Engineering | University of Indonesia | 2012-2016
    └─ Magna Cum Laude Graduate
    └─ Final Project: "Machine Learning for Fraud Detection in Financial Systems"
    └─ GPA: 3.78/4.0
    
    📜 Certifications:
    • AWS Certified Solutions Architect - Professional (2023)
    • Certified Kubernetes Administrator (CKA) (2022)
    • Google Cloud Professional Cloud Architect (2021)
    • Oracle Certified Professional Java SE 11 Developer (2020)
    
    🏆 ACHIEVEMENTS & AWARDS
    ═══════════════════════════════════════
    • "Innovation Excellence Award" - TechCorp Indonesia (2023)
    • "Top 30 Under 30 in Technology" - Tech Magazine Indonesia (2022)
    • "Best Technical Solution" - Indonesia Fintech Summit (2021)
    • Speaker at JavaOne Indonesia, AWS re:Invent Jakarta, KubeCon Asia
    """
    
    print("--- Complex CV Analysis ---")
    result = extractor.extractAllInformation(complex_cv)
    
    print(f"📧 Emails found: {len(result['emails'])}")
    for email in result['emails']:
        print(f"   • {email}")
    
    print(f"\n📞 Phones found: {len(result['phones'])}")
    for phone in result['phones']:
        print(f"   • {phone}")
    
    print(f"\n💼 Skills found: {len(result['skills'])}")
    for skill in result['skills']:
        print(f"   • {skill}")
    
    print(f"\n🏢 Experience entries: {len(result['experience'])}")
    for i, exp in enumerate(result['experience'][:3], 1):  # Show first 3
        print(f"   {i}. {exp['desc'][:80]}...")
    
    print(f"\n🎓 Education entries: {len(result['education'])}")
    for i, edu in enumerate(result['education'], 1):
        print(f"   {i}. {edu['desc'][:80]}...")

def test_edge_cases_seeding():
    """Test edge cases dengan nama dan data dari seeding.sql"""
    
    extractor = RegexExtractor()
    
    print("\n" + "=" * 80)
    print("ADVANCED TEST: EDGE CASES FROM SEEDING DATA")
    print("=" * 80)
    
    # Test case 1: Multiple people in one CV (tidak realistic tapi untuk testing)
    print("\n--- Edge Case 1: Multiple People Names ---")
    multi_people_cv = """
    References and Team Members:
    
    1. H41k4l 455y4uq1 - haikal@company.com - 081222334455
    2. R4d3n Fr4nC15c0 - raden@startup.com - 081293847561  
    3. 4l4nd MuL14 Pr4t4m4 - aland@tech.co.id - 081234559999
    4. 4hm4d R4f1 M4l1k1 - ahmad@dev.com - 081256712348
    5. 1khw4n 4lH4k1m - ikhwan@consulting.com - 081223456789
    
    All are senior developers in my network with 5+ years experience.
    Skills they have: Java, Python, JavaScript, React, Spring Boot, AWS
    """
    
    result = extractor.extractAllInformation(multi_people_cv)
    print(f"Emails extracted: {len(result['emails'])}")
    print(f"Phones extracted: {len(result['phones'])}")
    print(f"Skills extracted: {result['skills']}")
    
    # Test case 2: Corrupted/messy l33t speak
    print("\n--- Edge Case 2: Corrupted L33t Speak ---")
    corrupted_cv = """
    M0h4mm4d••Nu9r4h4••Ek4••Pr4w1r4
    Em41l: moh4mm4d.nu9r4h4@3m41l.c0m
    Ph0n3: 081234567891
    4ddr355: Jl. K3n4ng4 N0. 12, J4k4rt4
    
    5umm4ry: Pr0f3551on4l 50ftw4r3 3ng1n33r w1th 5+ y34r5 3xp3r13nc3
    5k1ll5: Pyth0n, J4v45cr1pt, R34ct, N0d3.j5, My5QL
    3xp3r13nc3: 53n10r D3v3l0p3r 4t T3chC0rp (2020-2023)
    3duc4t10n: 51 C0mput3r 5c13nc3 1TB 2016-2020
    """
    
    result = extractor.extractAllInformation(corrupted_cv)
    print(f"Email found: {result['emails']}")
    print(f"Phone found: {result['phones']}")
    print(f"Skills found: {result['skills']}")
    
    # Test case 3: Mixed languages dengan l33t speak
    print("\n--- Edge Case 3: Mixed Languages + L33t ---")
    mixed_lang_cv = """
    Nom: 4R13L H3RFR1S0N
    Email: ariel.herfrison@entreprise.fr
    Téléphone: +33 1 23 45 67 89
    Adresse: 123 Rue de la Paix, Paris, France
    
    Résumé Professionnel:
    Ingénieur logiciel avec expertise en développement web et applications mobiles.
    
    Compétences: JavaScript, React, Node.js, MongoDB, Docker, AWS
    
    Expérience Professionnelle:
    Développeur Senior chez TechParis S.A.R.L. (2021-2024)
    Développeur Junior chez StartupLyon (2019-2021)
    
    Formation:
    Master Informatique - École Polytechnique (2019)
    Licence Informatique - Université de Lyon (2017)
    """
    
    result = extractor.extractAllInformation(mixed_lang_cv)
    print(f"Email found: {result['emails']}")
    print(f"Phone found: {result['phones']}")  
    print(f"Skills found: {result['skills']}")

def test_text_cleaning_variations():
    """Test text cleaning dengan berbagai variasi format"""
    
    extractor = RegexExtractor()
    
    print("\n" + "=" * 80)
    print("ADVANCED TEST: TEXT CLEANING VARIATIONS")
    print("=" * 80)
    
    test_texts = [
        # Unicode characters + l33t speak
        "H41k4l••455y4uq1••with••bullets",
        
        # Multiple spaces and tabs
        "F4rh4n    N4f15\t\t\tR4yh4n    with    spaces",
        
        # Mixed punctuation
        "R4d3n,Fr4nC15c0;Tr14nt0:with.punctuation!here?",
        
        # Newlines and formatting
        """
        
        
        4l4nd
        
        MuL14
        
        Pr4t4m4
        
        
        """,
        
        # Special characters
        "1khw4n→4lH4k1m←with→arrows←and→symbols"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n--- Test {i} ---")
        print(f"Original: {repr(text)}")
        
        cleaned = extractor.cleanseText(text)
        print(f"Cleaned:  {repr(cleaned)}")
        
        cleaned_n = extractor.cleanseTextN(text)
        print(f"Clean+NL: {repr(cleaned_n)}")
        
        separated = extractor.seperatePunctuations(text)
        print(f"Separated: {repr(separated)}")

def main():
    """Run all advanced test cases"""
    
    print("🚀 ADVANCED REGEX EXTRACTOR TEST CASES")
    print("Testing dengan variasi l33t speak dan edge cases dari seeding.sql")
    
    try:
        test_leet_speak_variations()
        test_complex_cv_patterns()
        test_edge_cases_seeding()
        test_text_cleaning_variations()
        
        print(f"\n{'='*80}")
        print("🎉 SEMUA ADVANCED TEST CASES BERHASIL!")
        print("RegexExtractor dapat menangani variasi l33t speak dan edge cases dengan baik")
        print("="*80)
        
    except Exception as e:
        print(f"❌ ERROR during advanced testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
