import re

from src.database.connection import DatabaseConnection
from src.pdfprocessor.pdfExtractor import PDFExtractor
from src.pdfprocessor.regexExtractor import RegexExtractor

from src.database.queries import (
    get_applicant_id_by_cv_path,
    get_first_name_by_cv_path,
    get_last_name_by_cv_path,
    get_date_of_birth_by_cv_path,
    get_address_by_cv_path,
    get_phone_number_by_cv_path,
    get_application_id_by_cv_path,
    get_application_role_by_cv_path,
    get_result_card_by_cv_path,
    get_summary_data_by_cv_path,
    get_all_cv_paths,
)
from src.models.ResultCard import (
    print_resultcard,
)
from src.models.SummaryCard import (
    print_summarycard,
)
from config import DATABASE_CONFIG

def main():
    cv = r'data/FINANCE/12071138.pdf'  # sesuaikan
    
    # Initialize variables for extracted data
    skills_list = []
    work_experience_list = []
    education_list = []
    
    # Test PDF extraction
    print("=== Testing PDF Extraction ===")
    pdf_extractor = PDFExtractor()
    regex_extractor = RegexExtractor()
    
    # Create full path for PDF extraction (cv path is relative, need full path)
    pdf_full_path = f"src/archive/data/{cv}"
    
    try:
        extracted_text = pdf_extractor.PDFExtractForMatch(pdf_full_path)
        if extracted_text:
            print(f"[SUCCESS] PDF text extracted successfully!")
            print(f"Full path used: {pdf_full_path}")
            print(f"Total characters: {len(extracted_text)}")
            print(f"Full extracted text:")
            print("-" * 50)
            print(extracted_text)
            print("-" * 50)
              # Extract CV sections using RegexExtractor            print("\n=== Extracting CV Sections ===")
            cv_sections = regex_extractor.extract_cv_sections(extracted_text)
            
            # Store in variables for further use
            skills_list = cv_sections['skills']
            work_experience_list = cv_sections['work_experience']  
            education_list = cv_sections['education']
            
            print(f"\n--- EXTRACTED DATA SUMMARY ---")
            print(f"✓ Skills extracted: {len(skills_list)} items")
            print(f"✓ Work Experience extracted: {len(work_experience_list)} items")
            print(f"✓ Education extracted: {len(education_list)} items")
            
            print(f"\n--- SKILLS LIST (Array Format) ---")
            print(f"skills_list = {skills_list}")
            
            print(f"\n--- WORK EXPERIENCE LIST (Array Format) ---") 
            print(f"work_experience_list = {work_experience_list}")
            
            print(f"\n--- EDUCATION LIST (Array Format) ---")
            print(f"education_list = {education_list}")
            
            print(f"\n--- CLEAN SKILLS DISPLAY ---")
            if skills_list:
                for i, skill in enumerate(skills_list, 1):
                    print(f"{i}. {skill}")
            else:
                print("No skills found")
            
            print(f"\n--- WORK EXPERIENCE DISPLAY ---")
            if work_experience_list:
                for i, exp in enumerate(work_experience_list, 1):
                    # Truncate long experiences for display
                    display_exp = exp[:100] + "..." if len(exp) > 100 else exp
                    print(f"{i}. {display_exp}")
            else:
                print("No work experience found")
            
            print(f"\n--- EDUCATION DISPLAY ---")
            if education_list:
                for i, edu in enumerate(education_list, 1):
                    print(f"{i}. {edu}")
            else:                print("No education found")
            
            # These variables can now be used for database operations or further processing
            print(f"\n--- VARIABLES READY FOR USE ---")            
            print(f"skills_list: {type(skills_list)} with {len(skills_list)} items")
            print(f"work_experience_list: {type(work_experience_list)} with {len(work_experience_list)} items")
            print(f"education_list: {type(education_list)} with {len(education_list)} items")
            
        else:
            print("[FAILED] No text extracted from PDF")
    except Exception as e:
        print(f"[ERROR] Failed to extract PDF text: {e}")
    
    print("\n=== Database Queries ===")

    db = DatabaseConnection()
    db.connect()
    db.useDatabase(DATABASE_CONFIG['database'])

    try:
        rc = get_result_card_by_cv_path(db.connection, cv)
        print_resultcard(rc)

        sc = get_summary_data_by_cv_path(db.connection, cv)
        
        # Update summary card with extracted data if PDF extraction was successful
        if skills_list or work_experience_list or education_list:
            print("=== Updating Summary Card with Extracted Data ===")
            sc.skills = skills_list
            sc.work_experience = work_experience_list  
            sc.education = education_list
            print(f"✓ Added {len(skills_list)} skills to summary card")
            print(f"✓ Added {len(work_experience_list)} work experiences to summary card")
            print(f"✓ Added {len(education_list)} education entries to summary card")
        else:
            print("=== No Extracted Data Available ===")
            print("✗ No skills, work experience, or education data was extracted")
        
        print_summarycard(sc)
        
    except Exception as db_error:
        print(f"[ERROR] Database error: {db_error}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    main()
