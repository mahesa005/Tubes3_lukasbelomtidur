"""
Script untuk membuat database baru dari seeding.sql dan mengupdate konfigurasi
"""
import mysql.connector
from mysql.connector import Error
import os

def create_database_from_seeding():
    """Membuat database baru dari file seeding.sql"""
    
    # Konfigurasi koneksi (tanpa database spesifik)
    connection_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'port': 3306
    }
    
    new_database_name = 'ats_seeding_db'
    seeding_file = 'seeding.sql'
    
    try:
        # Connect ke MySQL server (tanpa database spesifik)
        print("🔌 Connecting to MySQL server...")
        connection = mysql.connector.connect(**connection_config)
        cursor = connection.cursor()
        
        # Drop database jika sudah ada
        print(f"🗑️ Dropping database '{new_database_name}' if exists...")
        cursor.execute(f"DROP DATABASE IF EXISTS {new_database_name}")
        
        # Buat database baru
        print(f"🆕 Creating new database '{new_database_name}'...")
        cursor.execute(f"CREATE DATABASE {new_database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # Gunakan database baru
        cursor.execute(f"USE {new_database_name}")
        print(f"✅ Using database '{new_database_name}'")
        
        # Baca dan eksekusi seeding.sql
        print(f"📄 Reading {seeding_file}...")
        with open(seeding_file, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Split SQL commands dan eksekusi satu per satu
        sql_commands = sql_content.split(';')
        
        print("🔄 Executing SQL commands...")
        for i, command in enumerate(sql_commands):
            command = command.strip()
            if command:  # Skip empty commands
                try:
                    cursor.execute(command)
                    if i % 50 == 0:  # Progress indicator
                        print(f"   Executed {i+1}/{len(sql_commands)} commands...")
                except Error as e:
                    if "Commands out of sync" not in str(e):
                        print(f"⚠️ Warning on command {i+1}: {e}")
        
        connection.commit()
        print("✅ All SQL commands executed successfully!")
        
        # Verify data
        cursor.execute("SELECT COUNT(*) FROM ApplicantProfile")
        applicant_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ApplicationDetail")
        application_count = cursor.fetchone()[0]
        
        print(f"📊 Database created successfully!")
        print(f"   - ApplicantProfile records: {applicant_count}")
        print(f"   - ApplicationDetail records: {application_count}")
        
        cursor.close()
        connection.close()
        
        # Update config.py
        update_config(new_database_name)
        
        return True
        
    except Error as e:
        print(f"❌ MySQL Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def update_config(database_name):
    """Update config.py dengan database baru"""
    print(f"⚙️ Updating config.py to use '{database_name}'...")
    
    try:
        # Baca config.py
        with open('config.py', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Ganti nama database
        old_line = "'database': 'ats_cv_matcher'"
        new_line = f"'database': '{database_name}'"
        
        if old_line in content:
            updated_content = content.replace(old_line, new_line)
            
            # Tulis kembali config.py
            with open('config.py', 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print(f"✅ config.py updated successfully!")
            print(f"   Changed: {old_line}")
            print(f"   To: {new_line}")
        else:
            print(f"⚠️ Could not find database config line in config.py")
            print("   Please manually update the database name in config.py")
            
    except Exception as e:
        print(f"❌ Error updating config.py: {e}")

if __name__ == "__main__":
    print("=== Creating Database from seeding.sql ===")
    
    if not os.path.exists('seeding.sql'):
        print("❌ seeding.sql file not found!")
        exit(1)
    
    if not os.path.exists('config.py'):
        print("❌ config.py file not found!")
        exit(1)
    
    success = create_database_from_seeding()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("📝 Next steps:")
        print("   1. Restart your application")
        print("   2. The app will now use the new database from seeding.sql")
        print("   3. You can verify the connection with: python test_database_connection.py")
    else:
        print("\n💥 Database setup failed!")
        print("   Please check the error messages above.")
