from src.database.connection import DatabaseConnection
from src.database.queries import (
    get_applicant_id_by_cv_path,
    get_first_name_by_cv_path,
    get_last_name_by_cv_path,
    get_date_of_birth_by_cv_path,
    get_address_by_cv_path,
    get_phone_number_by_cv_path,
    get_application_id_by_cv_path,
    get_application_role_by_cv_path,
)
from config import DATABASE_CONFIG

def main():
    cv = 'C:\Users\Mahesa\OneDrive\ITB\Coding\College\Academic\IF\Smt-4\Strategi Algoritma\Tubes\Tubes 3\Tubes3_lukasbelomtidur\src\archive\data\data\DIGITAL-MEDIA\13343786.pdf'  # sesuaikan path-mu
    db = DatabaseConnection()
    db.connect()
    db.useDatabase(DATABASE_CONFIG['database'])

    print("Applicant ID   :", get_applicant_id_by_cv_path(db.connection, cv))
    print("First  Name    :", get_first_name_by_cv_path(db.connection, cv))
    print("Last   Name    :", get_last_name_by_cv_path(db.connection, cv))
    print("Date of Birth  :", get_date_of_birth_by_cv_path(db.connection, cv))
    print("Address        :", get_address_by_cv_path(db.connection, cv))
    print("Phone Number   :", get_phone_number_by_cv_path(db.connection, cv))
    print("Application ID :", get_application_id_by_cv_path(db.connection, cv))
    print("Application Role:", get_application_role_by_cv_path(db.connection, cv))

    db.disconnect()

if __name__ == "__main__":
    main()
