import mysql.connector
from mysql.connector import Error
from config import DATABASE_CONFIG

def check_database_structure():
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        
        print("=== Connected to MySQL Database ===")
        
        # Check ApplicantProfile table structure
        print("\n=== ApplicantProfile Table Structure ===")
        cursor.execute("DESCRIBE applicantprofile")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[0]} - {col[1]} - {col[2]} - {col[3]} - {col[4]} - {col[5]}")
        
        # Check ApplicationDetail table structure
        print("\n=== ApplicationDetail Table Structure ===")
        cursor.execute("DESCRIBE applicationdetail")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[0]} - {col[1]} - {col[2]} - {col[3]} - {col[4]} - {col[5]}")
        
        # Search for James Jones specifically
        print("\n=== James Jones Details ===")
        cursor.execute("""
            SELECT applicant_id, first_name, last_name, date_of_birth, address, phone_number
            FROM applicantprofile 
            WHERE first_name = 'James' AND last_name = 'Jones'
        """)
        
        results = cursor.fetchall()
        if results:
            for row in results:
                applicant_id = row[0]
                print(f"James Jones found - ID: {applicant_id}")
                print(f"  Name: {row[1]} {row[2]}")
                print(f"  DOB: {row[3]}")
                print(f"  Address: {row[4]}")
                print(f"  Phone: {row[5]}")
                
                # Now check his CV applications
                print(f"\n=== CV Applications for James Jones (ID: {applicant_id}) ===")
                cursor.execute("""
                    SELECT * FROM applicationdetail WHERE applicant_id = %s
                """, (applicant_id,))
                
                cv_results = cursor.fetchall()
                if cv_results:
                    for cv_row in cv_results:
                        print(f"  Application: {cv_row}")
                else:
                    print(f"  No CV applications found for James Jones (ID: {applicant_id})")
        
        # Check if there's a CV file with James Jones name
        print("\n=== Checking for James Jones CV files ===")
        cursor.execute("SELECT COUNT(*) FROM applicationdetail WHERE cv_path LIKE '%James%Jones%'")
        count = cursor.fetchone()[0]
        print(f"CV files with 'James Jones' in path: {count}")
        
        if count > 0:
            cursor.execute("SELECT * FROM applicationdetail WHERE cv_path LIKE '%James%Jones%'")
            cv_files = cursor.fetchall()
            for cv_file in cv_files:
                print(f"  CV File: {cv_file}")
    
    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nMySQL connection closed.")

if __name__ == "__main__":
    check_database_structure()
