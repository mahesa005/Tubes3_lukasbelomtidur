from .connection import DatabaseConnection
from .models import ApplicantProfile, ApplicationDetail
import logging
from src.models.ResultCard import ResultCard
from src.models.SummaryCard import SummaryData

def get_applicant_id_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    try:
        query = (
            "SELECT ap.applicant_id "
            "FROM ApplicantProfile ap "
            "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
            "WHERE ad.cv_path = %s;"
        )
        cursor.execute(query, (cv_path,))
        row = cursor.fetchone()
        cursor.fetchall()  # Consume any remaining results
        return row[0] if row else None
    except Exception as e:
        print(f"Error in get_applicant_id_by_cv_path: {e}")
        return None
    finally:
        cursor.close()


def get_first_name_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    try:
        query = (
            "SELECT ap.first_name "
            "FROM ApplicantProfile ap "
            "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
            "WHERE ad.cv_path = %s;"
        )
        cursor.execute(query, (cv_path,))
        row = cursor.fetchone()
        cursor.fetchall()  # Consume any remaining results
        return row[0] if row else None
    except Exception as e:
        print(f"Error in get_first_name_by_cv_path: {e}")
        return None
    finally:
        cursor.close()


def get_last_name_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    try:
        query = (
            "SELECT ap.last_name "
            "FROM ApplicantProfile ap "
            "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
            "WHERE ad.cv_path = %s;"
        )
        cursor.execute(query, (cv_path,))
        row = cursor.fetchone()
        cursor.fetchall()  # Consume any remaining results
        return row[0] if row else None
    except Exception as e:
        print(f"Error in get_last_name_by_cv_path: {e}")
        return None
    finally:
        cursor.close()


def get_date_of_birth_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    try:
        query = (
            "SELECT ap.date_of_birth "
            "FROM ApplicantProfile ap "
            "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
            "WHERE ad.cv_path = %s;"
        )
        cursor.execute(query, (cv_path,))
        row = cursor.fetchone()
        cursor.fetchall()  # Consume any remaining results
        return row[0] if row else None
    except Exception as e:
        print(f"Error in get_date_of_birth_by_cv_path: {e}")
        return None
    finally:
        cursor.close()


def get_address_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    try:
        query = (
            "SELECT ap.address "
            "FROM ApplicantProfile ap "
            "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
            "WHERE ad.cv_path = %s;"
        )
        cursor.execute(query, (cv_path,))
        row = cursor.fetchone()
        cursor.fetchall()  # Consume any remaining results
        return row[0] if row else None
    except Exception as e:
        print(f"Error in get_address_by_cv_path: {e}")
        return None
    finally:
        cursor.close()


def get_phone_number_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    try:
        query = (
            "SELECT ap.phone_number "
            "FROM ApplicantProfile ap "
            "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
            "WHERE ad.cv_path = %s;"
        )
        cursor.execute(query, (cv_path,))
        row = cursor.fetchone()
        cursor.fetchall()  # Consume any remaining results
        return row[0] if row else None
    except Exception as e:
        print(f"Error in get_phone_number_by_cv_path: {e}")
        return None
    finally:
        cursor.close()


def get_application_id_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    try:
        query = (
            "SELECT ad.application_id "
            "FROM ApplicationDetail ad "
            "WHERE ad.cv_path = %s;"
        )
        cursor.execute(query, (cv_path,))
        row = cursor.fetchone()
        cursor.fetchall()  # Consume any remaining results
        return row[0] if row else None
    except Exception as e:
        print(f"Error in get_application_id_by_cv_path: {e}")
        return None
    finally:
        cursor.close()


def get_application_role_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    try:
        query = (
            "SELECT ad.application_role "
            "FROM ApplicationDetail ad "
            "WHERE ad.cv_path = %s;"
        )
        cursor.execute(query, (cv_path,))
        row = cursor.fetchone()
        cursor.fetchall()  # Consume any remaining results
        return row[0] if row else None
    except Exception as e:
        print(f"Error in get_application_role_by_cv_path: {e}")
        return None
    finally:
        cursor.close()


def get_result_card_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT CONCAT(ap.first_name, ' ', ap.last_name) AS full_name, ad.cv_path "
            "FROM ApplicantProfile ap "
            "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
            "WHERE ad.cv_path = %s;", (cv_path,)
        )
        row = cursor.fetchone()
        # Consume any remaining results
        cursor.fetchall()
        if not row:
            return None
        full_name, path = row
        return ResultCard(full_name=full_name, cv_path=path)
    except Exception as e:
        print(f"Error in get_result_card_by_cv_path: {e}")
        return None
    finally:
        cursor.close()


def get_summary_data_by_cv_path(conn, cv_path):
    from src.pdfprocessor.pdfExtractor import PDFExtractor
    from src.pdfprocessor.regexExtractor import RegexExtractor
    
    cursor = conn.cursor()
    
    # Initialize extracted data variables
    skills_list = []
    work_experience_list = []
    education_list = []
    
    try:
        cursor.execute(
            "SELECT CONCAT(ap.first_name, ' ', ap.last_name) AS full_name, "
            "ap.date_of_birth, ap.phone_number, ad.cv_path "
            "FROM ApplicantProfile ap "
            "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
            "WHERE ad.cv_path = %s;", (cv_path,)
        )
        row = cursor.fetchone()
        # Consume any remaining results
        cursor.fetchall()
        if not row:
            return None
        full_name, dob, phone, path = row
        dob_str = dob.isoformat() if dob else ""
          # Extract CV data
        try:
            print("Attempting to extract CV data...")
            pdf_extractor = PDFExtractor()
            regex_extractor = RegexExtractor()
            
            # Create full path for PDF extraction
            pdf_full_path = f"src/archive/data/{cv_path}"
            print(f"PDF path: {pdf_full_path}")
            
            # Extract text from PDF
            extracted_text = pdf_extractor.PDFExtractForMatch(pdf_full_path)
            if extracted_text:
                print(f"PDF extracted successfully, {len(extracted_text)} characters")
                # Extract CV sections
                cv_sections = regex_extractor.extract_cv_sections(extracted_text)
                skills_list = cv_sections['skills']
                work_experience_list = cv_sections['work_experience']
                education_list = cv_sections['education']
                print(f"CV sections extracted: {len(skills_list)} skills, {len(work_experience_list)} experience, {len(education_list)} education")
            else:
                print("No text extracted from PDF")
        except Exception as cv_error:
            print(f"Error extracting CV data: {cv_error}")
            # Continue with empty lists if CV extraction fails
        
        return SummaryData(
            full_name=full_name,
            birth_date=dob_str,
            phone_number=phone or "",
            skills=skills_list,
            cv_path=path,
            work_experience=work_experience_list,
            education=education_list
        )
    except Exception as e:
        print(f"Error in get_summary_data_by_cv_path: {e}")
        return None
    finally:
        cursor.close()

def get_all_cv_paths(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT cv_path FROM ApplicationDetail;")
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        print(f"Error in get_all_cv_paths: {e}")
        return []
    finally:
        cursor.close()
