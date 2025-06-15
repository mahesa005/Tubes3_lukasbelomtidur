#!/usr/bin/env python3
"""
Check the join relationship between tables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.connection import DatabaseConnection

def check_table_relationship():
    """Check the structure and relationship between tables"""
    
    try:
        db = DatabaseConnection()
        db.connect()
        cursor = db.connection.cursor()
        
        # Check applicationdetail structure
        print("📋 Columns in applicationdetail table:")
        cursor.execute("DESCRIBE applicationdetail")
        columns = cursor.fetchall()
        for column in columns:
            field, type_, null, key, default, extra = column
            print(f"   {field} | {type_} | {key}")
        
        # Check sample data
        print("\n📄 Sample applicationdetail record:")
        cursor.execute("SELECT * FROM applicationdetail LIMIT 1")
        sample = cursor.fetchone()
        
        if sample:
            cursor.execute("SHOW COLUMNS FROM applicationdetail")
            column_names = [desc[0] for desc in cursor.fetchall()]
            
            for i, value in enumerate(sample):
                print(f"   {column_names[i]}: {value}")
        
        # Test the join
        print("\n🔗 Testing join query:")
        cursor.execute("""
            SELECT ad.cv_path, ap.first_name, ap.last_name, ad.application_id 
            FROM applicationdetail ad
            JOIN applicantprofile ap ON ad.application_id = ap.applicant_id
            LIMIT 3
        """)
        
        results = cursor.fetchall()
        print(f"   Join returned {len(results)} results:")
        for row in results:
            cv_path, first_name, last_name, app_id = row
            print(f"   {app_id} | {first_name} {last_name} | {cv_path}")
        
        db.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_table_relationship()
