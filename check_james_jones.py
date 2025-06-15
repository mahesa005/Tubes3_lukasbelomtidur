import sqlite3

# Connect to database
conn = sqlite3.connect('ats_database.db')
cursor = conn.cursor()

# Check table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('=== Database Tables ===')
for table in tables:
    print(table[0])

print('\n=== Checking for James Jones ===')

# Try different table names
for table_name in ['applicantprofile', 'ApplicantProfile', 'applicant_profile', 'applicant']:
    try:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
        columns = [description[0] for description in cursor.description]
        print(f"\nTable '{table_name}' exists with columns: {columns}")
        
        # Check for James Jones
        try:
            cursor.execute(f"SELECT * FROM {table_name} WHERE first_name LIKE '%James%' AND last_name LIKE '%Jones%'")
            results = cursor.fetchall()
            if results:
                print(f"Found {len(results)} James Jones entries in {table_name}:")
                for row in results:
                    print(f"  {row}")
            else:
                print(f"No James Jones found in {table_name}")
        except Exception as e:
            print(f"Error searching for James Jones in {table_name}: {e}")
            
    except sqlite3.OperationalError:
        continue

conn.close()
