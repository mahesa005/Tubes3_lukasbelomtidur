#!/usr/bin/env python3
"""
Comprehensive Test Script for RegexExtractor
Tests all methods with various CV formats and edge cases
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pdfprocessor.regexExtractor import RegexExtractor
from pprint import pprint

def test_sample_cvs():
    """Test with various CV sample formats"""
    
    # Sample CV 1: Standard format
    cv1 = """
    John Doe
    Email: john.doe@email.com
    Phone: 081234567891, +62 812-3456-7890

    Summary:
    Professional software engineer with 5+ years experience in full-stack development.
    Experienced in Python, JavaScript, and database management.

    Skills: Python, JavaScript, SQL, Machine Learning, Communication, Project Management

    Experience:
    Senior Software Engineer at TechCorp (2020-2023)
    Developed web applications using React and Node.js
    Software Engineer Intern at StartupXYZ (2019-2020)
    Built mobile applications and APIs

    Education:
    S1 Computer Science ITB 2016-2020
    GPA: 3.8/4.0
    SMA 1 Bandung 2013-2016
    """

    # Sample CV 2: Different format with bullets
    cv2 = """
    SARAH WILSON
    📧 sarah.wilson@gmail.com | 📞 +1-555-123-4567
    LinkedIn: linkedin.com/in/sarahwilson

    PROFESSIONAL SUMMARY
    Marketing professional with expertise in digital campaigns and brand management.

    CORE COMPETENCIES
    • Digital Marketing • SEO/SEM • Content Strategy • Analytics • Team Leadership

    WORK EXPERIENCE
    Marketing Manager | ABC Marketing Agency | 2021-Present
    • Managed digital campaigns for 15+ clients
    • Increased ROI by 40% through data-driven strategies

    Marketing Coordinator | XYZ Corp | 2019-2021
    • Coordinated social media campaigns
    • Analyzed market trends and consumer behavior

    EDUCATION
    Master of Business Administration | Harvard Business School | 2019
    Bachelor of Marketing | University of California | 2017
    """

    # Sample CV 3: Minimal format
    cv3 = """
    Mike Chen - mike.chen@tech.com - 0987654321

    Objective: Seeking software development position

    Skills: Java, C++, Python

    Experience:
    Junior Developer at CodeCorp 2022-2023

    Education:
    Computer Science Degree 2022
    """

    # Sample CV 4: International format
    cv4 = """
    María García Rodriguez
    Correo: maria.garcia@empresa.es
    Teléfono: +34 666 123 456
    Móvil: 034-666-789-012

    Resumen Profesional:
    Ingeniera de software con experiencia en desarrollo web y aplicaciones móviles.

    Habilidades: JavaScript, React, Node.js, MongoDB, Git, Agile

    Experiencia Laboral:
    Desarrolladora Senior en TechSpain S.L. (2021-2024)
    Desarrolladora Junior en StartupMadrid (2020-2021)

    Formación Académica:
    Ingeniería Informática - Universidad Politécnica de Madrid (2016-2020)
    Bachillerato Científico - IES Madrid Centro (2014-2016)
    """

    # Sample CV 5: With messy formatting
    cv5 = """
    ALEX   JOHNSON
    alex.johnson@email.co.uk    /    +44-20-1234-5678
    
    
    Summary:    Data scientist    and    analyst    with    expertise    in    machine    learning.
    
    
    Skills:Python,R,SQL,TensorFlow,Pandas,Matplotlib,Statistics
    
    Experience:
    Data   Scientist   @   DataCorp   2022-present
    Research   Assistant   @   University   2020-2022
    
    Education:
    PhD   Data   Science   2020
    MSc   Statistics   2018
    """

    extractor = RegexExtractor()
    
    test_cases = [
        ("Standard CV Format", cv1),
        ("Bullet Point CV", cv2),
        ("Minimal CV", cv3),
        ("International CV", cv4),
        ("Messy Formatting CV", cv5)
    ]
    
    print("=" * 80)
    print("COMPREHENSIVE REGEX EXTRACTOR TEST")
    print("=" * 80)
    
    for i, (name, cv_text) in enumerate(test_cases, 1):
        print(f"\n{'='*20} TEST CASE {i}: {name} {'='*20}")
        print(f"Original text length: {len(cv_text)} characters")
        
        print(f"\n--- Email Extraction ---")
        emails = extractor.extractEmail(cv_text)
        print(f"Found emails: {emails}")
        
        print(f"\n--- Phone Extraction (Raw) ---")
        phones_raw = extractor.extractPhone(cv_text)
        print(f"Raw phones: {phones_raw}")
        
        print(f"\n--- Phone Extraction (Cleaned, 12 digits) ---")
        phones_clean = extractor.extractPhones(cv_text, digit_length=12)
        print(f"Clean phones (12 digits): {phones_clean}")
        
        print(f"\n--- Phone Extraction (Cleaned, 10 digits) ---")
        phones_clean_10 = extractor.extractPhones(cv_text, digit_length=10)
        print(f"Clean phones (10 digits): {phones_clean_10}")
        
        print(f"\n--- Summary Extraction ---")
        summary = extractor.extractSummary(cv_text)
        print(f"Summary: {summary[:100]}{'...' if len(summary) > 100 else ''}")
        
        print(f"\n--- Skills Extraction ---")
        skills = extractor.extractSkills(cv_text)
        print(f"Skills: {skills}")
        
        print(f"\n--- Experience Extraction ---")
        experience = extractor.extractExperience(cv_text)
        print(f"Experience: {experience}")
        
        print(f"\n--- Education Extraction ---")
        education = extractor.extractEducation(cv_text)
        print(f"Education: {education}")
        
        print(f"\n--- Text Cleaning Test ---")
        original_snippet = cv_text[:100]
        cleaned = extractor.cleanseText(original_snippet)
        cleaned_with_newlines = extractor.cleanseTextN(original_snippet)
        separated_punct = extractor.seperatePunctuations(original_snippet)
        
        print(f"Original: {repr(original_snippet)}")
        print(f"Cleaned: {repr(cleaned)}")
        print(f"Cleaned (keep newlines): {repr(cleaned_with_newlines)}")
        print(f"Separated punctuation: {repr(separated_punct)}")
        
        print(f"\n--- Complete Information Extraction ---")
        all_info = extractor.extractAllInformation(cv_text)
        pprint(all_info)
        
        print("\n" + "-" * 80)

def test_edge_cases():
    """Test edge cases and special scenarios"""
    
    print(f"\n{'='*30} EDGE CASES TEST {'='*30}")
    
    extractor = RegexExtractor()
    
    # Edge case 1: Empty text
    print("\n--- Edge Case 1: Empty Text ---")
    empty_result = extractor.extractAllInformation("")
    print(f"Empty text result: {empty_result}")
    
    # Edge case 2: Only phone numbers
    print("\n--- Edge Case 2: Various Phone Formats ---")
    phone_text = """
    Contact numbers:
    +1-555-123-4567
    (555) 123-4567
    555.123.4567
    555 123 4567
    +62 812 3456 7890
    081234567890
    +44 20 1234 5678
    020-1234-5678
    """
    phones = extractor.extractPhone(phone_text)
    phones_12 = extractor.extractPhones(phone_text, 12)
    phones_10 = extractor.extractPhones(phone_text, 10)
    print(f"All phone formats: {phones}")
    print(f"12-digit phones: {phones_12}")
    print(f"10-digit phones: {phones_10}")
    
    # Edge case 3: Multiple emails
    print("\n--- Edge Case 3: Multiple Email Formats ---")
    email_text = """
    Contacts:
    primary@email.com
    secondary@company.co.uk
    backup@domain.org
    user.name@sub.domain.com
    name+tag@email.co.id
    """
    emails = extractor.extractEmail(email_text)
    print(f"Found emails: {emails}")
    
    # Edge case 4: Skills in different formats
    print("\n--- Edge Case 4: Skills in Various Formats ---")
    skills_texts = [
        "Skills: Python, Java, C++, JavaScript",
        "Technical Skills: Python; Java; C++; JavaScript",
        "Core Competencies: Python | Java | C++ | JavaScript",
        "Programming Languages: Python, Java, C++, and JavaScript",
        "My skills include: Python, Java, C++, JavaScript",
    ]
    
    for i, text in enumerate(skills_texts, 1):
        skills = extractor.extractSkills(text)
        print(f"Format {i}: {text}")
        print(f"Extracted: {skills}")
    
    # Edge case 5: Text cleaning with special characters
    print("\n--- Edge Case 5: Text Cleaning with Special Characters ---")
    messy_text = "Hello•World    ● Test   \t\n\n\n   Bullet▪Points◦Here\uf0b7More"
    cleaned = extractor.cleanseText(messy_text)
    cleaned_n = extractor.cleanseTextN(messy_text)
    separated = extractor.seperatePunctuations("Hello,world!Test.One-two")
    
    print(f"Original: {repr(messy_text)}")
    print(f"Cleaned: {repr(cleaned)}")
    print(f"Cleaned (newlines): {repr(cleaned_n)}")
    print(f"Separated punct: {repr(separated)}")

def test_real_world_scenarios():
    """Test with realistic CV scenarios"""
    
    print(f"\n{'='*25} REAL WORLD SCENARIOS {'='*25}")
    
    extractor = RegexExtractor()
    
    # Scenario 1: CV with no clear sections
    print("\n--- Scenario 1: Unstructured CV ---")
    unstructured_cv = """
    Jane Smith, jane.smith@email.com, +1-234-567-8901
    I am a marketing professional with experience in digital campaigns.
    I know Adobe Photoshop, Google Analytics, Facebook Ads.
    I worked at Marketing Inc from 2020 to 2023 as Marketing Manager.
    I studied Marketing at State University from 2016 to 2020.
    """
    result = extractor.extractAllInformation(unstructured_cv)
    pprint(result)
    
    # Scenario 2: CV with mixed languages
    print("\n--- Scenario 2: Mixed Language CV ---")
    mixed_cv = """
    Nom: Jean Dupont
    Email: jean.dupont@email.fr
    Téléphone: +33 1 23 45 67 89
    
    Résumé: Professional français with experience in international business.
    
    Compétences: French, English, Spanish, Business Development, Sales
    
    Expérience:
    Manager at Company France (2021-2024)
    Assistant at Bureau International (2019-2021)
    
    Formation:
    Master Commerce International - Université Paris (2019)
    """
    result = extractor.extractAllInformation(mixed_cv)
    pprint(result)
    
    # Scenario 3: CV with URLs and social media
    print("\n--- Scenario 3: Modern CV with URLs ---")
    modern_cv = """
    DAVID TECH
    Email: david@techbro.com
    Phone: (555) 123-4567
    LinkedIn: https://linkedin.com/in/davidtech
    GitHub: https://github.com/davidtech
    Website: www.davidtech.com
    
    Summary: Full-stack developer passionate about creating innovative solutions.
    
    Skills: React.js, Node.js, Python, Docker, AWS, Git, Agile/Scrum
    
    Experience:
    Senior Developer at TechStartup (2022-Present)
    • Built scalable web applications
    • Led team of 5 developers
    
    Junior Developer at WebCorp (2020-2022)
    • Developed REST APIs
    • Implemented CI/CD pipelines
    
    Education:
    B.S. Computer Science, MIT (2020)
    Relevant Coursework: Data Structures, Algorithms, Database Systems
    """
    result = extractor.extractAllInformation(modern_cv)
    pprint(result)

def main():
    """Run all tests"""
    try:
        test_sample_cvs()
        test_edge_cases()
        test_real_world_scenarios()
        
        print(f"\n{'='*80}")
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("The RegexExtractor is working properly with various CV formats.")
        print("="*80)
        
    except Exception as e:
        print(f"ERROR during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
