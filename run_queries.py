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
from config import DATA_DIR, DATABASE_CONFIG
import os
from pathlib import Path


def main():
    cv = r'data/ACCOUNTANT/11163645.pdf'  # sesuaikan
    
    print("=== Database Queries ===")


    db = DatabaseConnection()   
    db.connect()
    db.useDatabase(DATABASE_CONFIG['database'])

    rel_paths = get_all_cv_paths(db.connection)

    for rel in rel_paths[:5]:           
        rel_stripped = rel.split('data/', 1)[-1]

        full_path = DATA_DIR / rel_stripped

        print(f"Rel: {rel}")
        print(f"Abs: {full_path}")
        print("Exists:", full_path.exists())

        if full_path.exists():
            rc = get_result_card_by_cv_path(db.connection, rel)
            print_resultcard(rc)
        print()

        print("=== Getting Summary Data ===")
        sc = get_summary_data_by_cv_path(db.connection, cv)
        print("=== Summary Card with Extracted CV Data ===")
        print_summarycard(sc)
        
        # Display extracted data summary
        if sc and (sc.skills or sc.work_experience or sc.education):
            print("\n=== EXTRACTED DATA SUMMARY ===")
            print(f"✓ Skills extracted: {len(sc.skills)} items")
            print(f"✓ Work Experience extracted: {len(sc.work_experience)} items")
            print(f"✓ Education extracted: {len(sc.education)} items")
            
            print(f"\n--- SKILLS LIST ---")
            if sc.skills:
                for i, skill in enumerate(sc.skills, 1):
                    print(f"{i}. {skill}")
            else:
                print("No skills found")
            
            print(f"\n--- WORK EXPERIENCE LIST ---")
            if sc.work_experience:
                for i, exp in enumerate(sc.work_experience, 1):
                    # Truncate long experiences for display
                    display_exp = exp[:100] + "..." if len(exp) > 100 else exp
                    print(f"{i}. {display_exp}")
            else:
                print("No work experience found")
            
            print(f"\n--- EDUCATION LIST ---")
            if sc.education:
                for i, edu in enumerate(sc.education, 1):
                    print(f"{i}. {edu}")
            else:
                print("No education found")
        else:
            print("\n=== No CV Data Extracted ===")
            print("✗ No skills, work experience, or education data was extracted")
        
    except Exception as db_error:
        print(f"[ERROR] Database error: {db_error}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    main()