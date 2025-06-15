import mysql.connector
from mysql.connector import Error
from config import DATABASE_CONFIG

def test_database_connection():
    """Test koneksi ke database MySQL"""
    try:
        print("=== Testing Database Connection ===")
        print(f"Host: {DATABASE_CONFIG['host']}")
        print(f"User: {DATABASE_CONFIG['user']}")
        print(f"Database: {DATABASE_CONFIG['database']}")
        print(f"Port: {DATABASE_CONFIG['port']}")
        print(f"Password: {'*' * len(DATABASE_CONFIG['password'])}")
        
        # Connect to MySQL database
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        
        if connection.is_connected():
            print("\n✅ Successfully connected to MySQL database!")
            
            cursor = connection.cursor()
            
            # Get database info
            cursor.execute("SELECT VERSION()")
            db_info = cursor.fetchone()
            print(f"MySQL Server version: {db_info[0]}")
            
            # Check current database
            cursor.execute("SELECT DATABASE()")
            current_db = cursor.fetchone()
            print(f"Current database: {current_db[0]}")
            
            # List tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\nTables in database:")
            for table in tables:
                print(f"  - {table[0]}")
                
            # Count records in each table
            print(f"\nRecord counts:")
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"  - {table_name}: {count} records")
            
            cursor.close()
            connection.close()
            print("\n✅ Database connection test completed successfully!")
            
        else:
            print("❌ Failed to connect to database")
            
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("\nPossible issues:")
        print("1. MySQL server is not running")
        print("2. Database 'ats_cv_matcher' doesn't exist")
        print("3. Username/password is incorrect")
        print("4. MySQL service is not started")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_database_connection()
