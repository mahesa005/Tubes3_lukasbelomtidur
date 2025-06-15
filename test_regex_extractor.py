#!/usr/bin/env python3
"""
Test RegexExtractor module with comprehensive test cases
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pprint import pprint
from src.pdfprocessor.regexExtractor import RegexExtractor

def test_regex_extractor():
    """Test all RegexExtractor functions with sample CV text"""
    
    print("=== TESTING REGEX EXTRACTOR ===\n")
    
    # Sample CV text with various formats
    sample_cv_text = """
    John Doe Resume
    
    Contact Information:
    Email: john.doe@email.com, backup@gmail.com
    Phone: +62 812-3456-7890, 081234567891, (021) 1234-5678
    Alternative: +1-555-123-4567
    
    Professional Summary:
    Experienced software engineer with 5+ years of experience in web development, 
    machine learning, and system architecture. Proven track record of delivering 
    high-quality solutions in fast-paced environments.
    
    Skills: Python, JavaScript, SQL, Machine Learning, Docker, Kubernetes, Communication, Project Management
    
    Work Experience:
    Senior Software Engineer at Tech Corp (Jan 2020 - Present)
    - Led development of microservices architecture
    - Managed team of 5 developers
    
    Software Developer at StartupXYZ (Jun 2018 - Dec 2019)
    - Built REST APIs using Python and Flask
    - Implemented CI/CD pipelines
    
    Education:
    Bachelor of Computer Science, University of Technology (2014-2018)
    Master of Engineering, Institute of Technology (2018-2020)
    
    Certifications:
    AWS Certified Solutions Architect (2021)
    Google Cloud Professional (2020)
    
    Additional Information:
    Date of Birth: 15/06/1995
    Graduation Date: May 2018
    Last Update: 2023-12-01
    """
    
    # Initialize extractor
    extractor = RegexExtractor()
    
    print("--- Original CV Text ---")
    print(sample_cv_text[:200] + "...\n")
    
    # Test individual extraction methods
    print("1. EMAIL EXTRACTION:")
    emails = extractor.extractEmail(sample_cv_text)
    print(f"Found emails: {emails}")
    print()
    
    print("2. PHONE EXTRACTION (Raw):")
    phones_raw = extractor.extractPhone(sample_cv_text)
    print(f"Found phones (raw): {phones_raw}")
    print()
    
    print("3. PHONE EXTRACTION (Clean, 12 digits):")
    phones_clean = extractor.extractPhones(sample_cv_text, digit_length=12)
    print(f"Found phones (12 digits): {phones_clean}")
    print()
    
    print("4. PHONE EXTRACTION (Clean, 10 digits):")
    phones_clean_10 = extractor.extractPhones(sample_cv_text, digit_length=10)
    print(f"Found phones (10 digits): {phones_clean_10}")
    print()
    
    print("5. SUMMARY EXTRACTION:")
    summary = extractor.extractSummary(sample_cv_text)
    print(f"Summary: {summary}")
    print()
    
    print("6. SKILLS EXTRACTION:")
    skills = extractor.extractSkills(sample_cv_text)
    print(f"Skills: {skills}")
    print()
    
    print("7. EXPERIENCE EXTRACTION:")
    experience = extractor.extractExperience(sample_cv_text)
    print("Experience:")
    for i, exp in enumerate(experience, 1):
        print(f"  {i}. {exp}")
    print()
    
    print("8. EDUCATION EXTRACTION:")
    education = extractor.extractEducation(sample_cv_text)
    print("Education:")
    for i, edu in enumerate(education, 1):
        print(f"  {i}. {edu}")
    print()
    
    print("9. ALL INFORMATION EXTRACTION:")
    all_info = extractor.extractAllInformation(sample_cv_text)
    print("Complete extraction result:")
    pprint(all_info, width=80)
    print()
    
    # Test text cleaning functions
    messy_text = "  Hello,world!  Test•text▪with●bullets  extra   spaces  \n\n\n  "
    print("10. TEXT CLEANING:")
    print(f"Original messy text: '{messy_text}'")
    
    cleaned = extractor.cleanseText(messy_text)
    print(f"Cleaned text: '{cleaned}'")
    
    cleaned_n = extractor.cleanseTextN(messy_text)
    print(f"Cleaned (keep newlines): '{cleaned_n}'")
    
    separated = extractor.seperatePunctuations("Hello,world!Test.One")
    print(f"Separated punctuation: '{separated}'")
    print()


def test_with_actual_cv_format():
    """Test with more realistic CV format"""
    
    print("=== TESTING WITH REALISTIC CV FORMAT ===\n")
    
    realistic_cv = """
CURRICULUM VITAE

PERSONAL INFORMATION
Name: Sarah Michelle Johnson
Email: sarah.johnson@professional.com
Phone: +62-21-5555-1234, 0812-9876-5432
Address: Jl. Sudirman No. 123, Jakarta 12190

OBJECTIVE
To obtain a challenging position as a Data Scientist where I can utilize my strong analytical 
skills and machine learning expertise to drive business insights and innovation.

TECHNICAL SKILLS: 
Data Analysis, Python Programming, R Statistical Computing, SQL Database Management, 
Machine Learning Algorithms, Deep Learning, TensorFlow, Scikit-learn, Tableau, Power BI

PROFESSIONAL EXPERIENCE
Data Analyst | PT Technology Solutions Indonesia | March 2021 - Present
• Developed predictive models using Python and scikit-learn
• Created interactive dashboards with Tableau and Power BI
• Collaborated with cross-functional teams to deliver data-driven solutions

Junior Data Scientist | CV Digital Analytics | January 2020 - February 2021
• Performed statistical analysis on large datasets
• Implemented machine learning models for customer segmentation
• Prepared technical reports and presentations for stakeholders

EDUCATION
Master of Science in Data Science | University of Indonesia | 2018 - 2020
Bachelor of Statistics | Bandung Institute of Technology | 2014 - 2018

CERTIFICATIONS
• Google Data Analytics Professional Certificate (2021)
• Microsoft Azure Data Scientist Associate (2020)
• Coursera Machine Learning Specialization (2019)

LANGUAGES
• Indonesian (Native)
• English (Fluent)
• Mandarin (Conversational)
"""
    
    extractor = RegexExtractor()
    
    print("--- Realistic CV Analysis ---")
    result = extractor.extractAllInformation(realistic_cv)
    
    print("Extraction Results:")
    pprint(result, width=80)
    print()
    
    # Test text cleaning on this CV
    print("--- Text Cleaning Results ---")
    cleaned = extractor.cleanseText(realistic_cv)
    print("First 300 chars of cleaned text:")
    print(cleaned[:300] + "...")
    print()


def test_edge_cases():
    """Test edge cases and error handling"""
    
    print("=== TESTING EDGE CASES ===\n")
    
    extractor = RegexExtractor()
    
    # Test with empty text
    print("1. Empty text test:")
    empty_result = extractor.extractAllInformation("")
    print("Empty text result:", empty_result)
    print()
    
    # Test with no relevant information
    print("2. No relevant info test:")
    irrelevant_text = "This is just some random text without any CV information."
    irrelevant_result = extractor.extractAllInformation(irrelevant_text)
    print("Irrelevant text result:", irrelevant_result)
    print()
    
    # Test with special characters
    print("3. Special characters test:")
    special_text = "Email: test@example.com\nPhone: +62•812•1234•5678\nSkills: C++, .NET, node.js"
    special_result = extractor.extractAllInformation(special_text)
    print("Special characters result:")
    pprint(special_result)
    print()


if __name__ == "__main__":
    try:
        test_regex_extractor()
        test_with_actual_cv_format()
        test_edge_cases()
        
        print("=== ALL TESTS COMPLETED SUCCESSFULLY ===")
        
    except Exception as e:
        print(f"ERROR during testing: {e}")
        import traceback
        traceback.print_exc()
