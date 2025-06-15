#!/usr/bin/env python3
"""
Check what tables exist in the database
"""

import sys
import os
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

from database.connection import DatabaseConnection

def check_database_tables():
    """Check what tables exist in the database"""
    
    try:
        # Initialize database connection
        db = DatabaseConnection()
        if not db.connect():
            print("❌ Failed to connect to database")
            return
            
        # Show all tables
        db.execute("SHOW TABLES")
        tables = db.cursor.fetchall()
        
        print(f"📊 Tables in database:")
        if tables:
            for table, in tables:
                print(f"   📋 {table}")
                
                # Get row count for each table
                try:
                    db.execute(f"SELECT COUNT(*) FROM {table}")
                    count = db.cursor.fetchone()[0]
                    print(f"      └─ Rows: {count}")
                except Exception as e:
                    print(f"      └─ Error counting rows: {e}")
        else:
            print("   ❌ No tables found")
        
        db.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database_tables()
