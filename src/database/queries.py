from .connection import DatabaseConnection
from .models import ApplicantProfile, ApplicationDetail
import logging
from src.models.ResultCard import ResultCard
from src.models.SummaryCard import SummaryData

def get_applicant_id_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    query = (
        "SELECT ap.applicant_id "
        "FROM ApplicantProfile ap "
        "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
        "WHERE ad.cv_path = %s;"
    )
    cursor.execute(query, (cv_path,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


def get_first_name_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    query = (
        "SELECT ap.first_name "
        "FROM ApplicantProfile ap "
        "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
        "WHERE ad.cv_path = %s;"
    )
    cursor.execute(query, (cv_path,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


def get_last_name_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    query = (
        "SELECT ap.last_name "
        "FROM ApplicantProfile ap "
        "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
        "WHERE ad.cv_path = %s;"
    )
    cursor.execute(query, (cv_path,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


def get_date_of_birth_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    query = (
        "SELECT ap.date_of_birth "
        "FROM ApplicantProfile ap "
        "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
        "WHERE ad.cv_path = %s;"
    )
    cursor.execute(query, (cv_path,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


def get_address_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    query = (
        "SELECT ap.address "
        "FROM ApplicantProfile ap "
        "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
        "WHERE ad.cv_path = %s;"
    )
    cursor.execute(query, (cv_path,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


def get_phone_number_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    query = (
        "SELECT ap.phone_number "
        "FROM ApplicantProfile ap "
        "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
        "WHERE ad.cv_path = %s;"
    )
    cursor.execute(query, (cv_path,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


def get_application_id_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    query = (
        "SELECT ad.application_id "
        "FROM ApplicationDetail ad "
        "WHERE ad.cv_path = %s;"
    )
    cursor.execute(query, (cv_path,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


def get_application_role_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    query = (
        "SELECT ad.application_role "
        "FROM ApplicationDetail ad "
        "WHERE ad.cv_path = %s;"
    )
    cursor.execute(query, (cv_path,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


def get_result_card_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT CONCAT(ap.first_name, ' ', ap.last_name) AS full_name, ad.cv_path "
        "FROM ApplicantProfile ap "
        "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
        "WHERE ad.cv_path = %s;", (cv_path,)
    )
    row = cursor.fetchone()
    cursor.close()
    if not row:
        return None
    full_name, path = row
    return ResultCard(full_name=full_name, cv_path=path)


def get_summary_data_by_cv_path(conn, cv_path):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT CONCAT(ap.first_name, ' ', ap.last_name) AS full_name, "
        "ap.date_of_birth, ap.phone_number, ad.cv_path "
        "FROM ApplicantProfile ap "
        "JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id "
        "WHERE ad.cv_path = %s;", (cv_path,)
    )
    row = cursor.fetchone()
    cursor.close()
    if not row:
        return None
    full_name, dob, phone, path = row
    dob_str = dob.isoformat() if dob else ""
    return SummaryData(
        full_name=full_name,
        birth_date=dob_str,
        phone_number=phone or "",
        skills=[],
        cv_path=path,
        work_experience=[],
        education=[]
    )

def get_all_cv_paths(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT cv_path FROM ApplicationDetail;")
    rows = cursor.fetchall()
    cursor.close()
    return [row[0] for row in rows]