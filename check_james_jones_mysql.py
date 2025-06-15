import mysql.connector
from mysql.connector import Error
from config import DATABASE_CONFIG

def check_james_jones():
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        
        print("=== Connected to MySQL Database ===")
        
        # Check table names
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("\n=== Database Tables ===")
        for table in tables:
            print(table[0])
        
        # Check for James Jones in ApplicantProfile
        print("\n=== Searching for James Jones in ApplicantProfile ===")
        cursor.execute("""
            SELECT applicant_id, first_name, last_name, date_of_birth, address, phone_number
            FROM ApplicantProfile 
            WHERE first_name LIKE '%James%' AND last_name LIKE '%Jones%'
        """)
        
        results = cursor.fetchall()
        if results:
            print(f"Found {len(results)} James Jones entries:")
            for row in results:
                print(f"  ID: {row[0]}, Name: {row[1]} {row[2]}, DOB: {row[3]}, Address: {row[4]}, Phone: {row[5]}")
        else:
            print("No James Jones found in ApplicantProfile")
        
        # Check for any CV paths with James Jones
        print("\n=== Searching for James Jones in ApplicationDetail (CV paths) ===")
        cursor.execute("""
            SELECT ad.detail_id, ad.applicant_id, ad.application_role, ad.cv_path,
                   ap.first_name, ap.last_name
            FROM ApplicationDetail ad
            JOIN ApplicantProfile ap ON ad.applicant_id = ap.applicant_id
            WHERE ap.first_name LIKE '%James%' AND ap.last_name LIKE '%Jones%'
        """)
        
        results = cursor.fetchall()
        if results:
            print(f"Found {len(results)} James Jones entries with CV:")
            for row in results:
                print(f"  Detail ID: {row[0]}, Applicant ID: {row[1]}, Role: {row[2]}")
                print(f"  CV Path: {row[3]}")
                print(f"  Name: {row[4]} {row[5]}")
                print("  ---")
        else:
            print("No James Jones found with CV paths")
            
        # Check if CV file with James Jones exists
        print("\n=== Searching for CV files containing 'James Jones' in path ===")
        cursor.execute("""
            SELECT ad.detail_id, ad.applicant_id, ad.cv_path,
                   ap.first_name, ap.last_name
            FROM ApplicationDetail ad
            JOIN ApplicantProfile ap ON ad.applicant_id = ap.applicant_id
            WHERE ad.cv_path LIKE '%James%Jones%' OR ad.cv_path LIKE '%James_Jones%'
        """)
        
        results = cursor.fetchall()
        if results:
            print(f"Found {len(results)} CV files with James Jones in path:")
            for row in results:
                print(f"  Detail ID: {row[0]}, Applicant ID: {row[1]}")
                print(f"  CV Path: {row[2]}")
                print(f"  DB Name: {row[3]} {row[4]}")
                print("  ---")
        else:
            print("No CV files with James Jones in path found")
    
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        print("Make sure MySQL server is running and credentials are correct")
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nMySQL connection closed.")

if __name__ == "__main__":
    check_james_jones()
