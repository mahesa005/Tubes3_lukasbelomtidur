#!/usr/bin/env python3
"""
Check database content and status
"""

import os
import sys
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

from database.connection import DatabaseConnection

def check_database_content():
    """Check what's actually in the database"""
    
    print("🔍 Checking Database Content...")
    print("=" * 60)
    
    # Connect to database
    db = DatabaseConnection()
    if not db.connect():
        print("❌ Failed to connect to database")
        return
    
    try:
        cursor = db.connection.cursor()
        
        # Check all tables and their counts
        tables = ['ApplicantProfile', 'ApplicationDetail']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"📊 {table}: {count} records")
            
            if count > 0:
                # Show sample data
                cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                
                print(f"   Columns: {columns}")
                for i, row in enumerate(rows, 1):
                    print(f"   Row {i}: {row}")
                print()
        
        # Check if tables exist
        cursor.execute("SHOW TABLES")
        existing_tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Existing tables: {existing_tables}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.disconnect()

if __name__ == "__main__":
    check_database_content()
