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

#CARA AKSES DARI DATABASE

# def main():
#     cv = r'/Users/jonathankenanbudianto/Documents/coding/pyton/SEM4/tubesstima3/Tubes3_lukasbelomtidur/src/archive/data/data/CHEF/24673903.pdf '  # sesuaikan

#     db = DatabaseConnection()
#     db.connect()
#     db.useDatabase(DATABASE_CONFIG['database'])

#     # print("Applicant ID   :", get_applicant_id_by_cv_path(db.connection, cv))
#     # print("First  Name    :", get_first_name_by_cv_path(db.connection, cv))
#     # print("Last   Name    :", get_last_name_by_cv_path(db.connection, cv))
#     # print("Date of Birth  :", get_date_of_birth_by_cv_path(db.connection, cv))
#     # print("Address        :", get_address_by_cv_path(db.connection, cv))
#     # print("Phone Number   :", get_phone_number_by_cv_path(db.connection, cv))
#     # print("Application ID :", get_application_id_by_cv_path(db.connection, cv))
#     # print("Application Role:", get_application_role_by_cv_path(db.connection, cv))


#     print("All CV Paths     :", get_all_cv_paths(db.connection))

#     # rc = get_result_card_by_cv_path(db.connection, cv)
#     # print_resultcard(rc)

#     # sc = get_summary_data_by_cv_path(db.connection, cv)
#     # print_summarycard(sc)


#     db.disconnect()



# if __name__ == "__main__":
#     main()


#CARA AKSES PDF DARI CV PATH
def main():
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

    db.disconnect()

if __name__ == "__main__":
    main()