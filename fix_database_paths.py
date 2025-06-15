#!/usr/bin/env python3
"""
Script to fix the cv_path entries in the database to match the actual file system structure.
The database currently has paths like 'data/ROLE/file.pdf' but should have 'src/archive/data/data/ROLE/file.pdf'
"""

import logging
from src.database.connection import DatabaseConnection
from pathlib import Path
import os

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def fix_database_paths():
    logger = setup_logging()
    logger.info("Starting database path fix process...")
    
    db = DatabaseConnection()
    if not db.connect():
        logger.error("Failed to connect to database")
        return False
    
    try:        # Get all current cv_path entries
        logger.info("Fetching current cv_path entries from database...")
        query = "SELECT application_id, cv_path FROM ApplicationDetail WHERE cv_path IS NOT NULL"
        if not db.execute(query):
            logger.error("Failed to fetch cv_path entries")
            return False
        
        results = db.cursor.fetchall()
        logger.info(f"Found {len(results)} cv_path entries to update")
        
        # Track statistics
        updated_count = 0
        error_count = 0
        
        for application_id, current_path in results:
            # Convert from 'data/ROLE/file.pdf' to 'src/archive/data/data/ROLE/file.pdf'
            if current_path.startswith('data/'):
                # Remove 'data/' prefix and add correct prefix
                relative_part = current_path[5:]  # Remove 'data/' 
                new_path = f'src/archive/data/data/{relative_part}'
                
                # Verify the file actually exists
                project_root = Path(__file__).parent
                full_file_path = project_root / new_path
                  if full_file_path.exists():
                    # Update the database
                    update_query = "UPDATE ApplicationDetail SET cv_path = %s WHERE application_id = %s"
                    if db.execute(update_query, (new_path, application_id)):
                        logger.info(f"Updated application_id {application_id}: '{current_path}' -> '{new_path}'")
                        updated_count += 1
                    else:
                        logger.error(f"Failed to update application_id {application_id}")
                        error_count += 1
                else:
                    logger.warning(f"File does not exist for application_id {application_id}: {full_file_path}")
                    error_count += 1
            else:
                logger.info(f"Skipping application_id {application_id} - path doesn't start with 'data/': {current_path}")
        
        # Commit changes
        db.connection.commit()
        logger.info(f"Database path fix completed. Updated: {updated_count}, Errors: {error_count}")
        
        return updated_count > 0
        
    except Exception as e:
        logger.error(f"Error during database path fix: {e}")
        return False
    finally:
        db.disconnect()

def verify_fix():
    """Verify that the fix worked by checking a few sample paths"""
    logger = setup_logging()
    logger.info("Verifying database path fix...")
    
    db = DatabaseConnection()
    if not db.connect():
        logger.error("Failed to connect to database for verification")
        return
      try:
        # Get a sample of updated paths
        query = "SELECT application_id, cv_path FROM ApplicationDetail WHERE cv_path IS NOT NULL LIMIT 5"
        if db.execute(query):
            results = db.cursor.fetchall()
            logger.info("Sample of updated paths:")
            for application_id, cv_path in results:
                # Check if file exists
                project_root = Path(__file__).parent
                full_path = project_root / cv_path
                exists = "EXISTS" if full_path.exists() else "NOT FOUND"
                logger.info(f"  application_id {application_id}: {cv_path} [{exists}]")
    except Exception as e:
        logger.error(f"Error during verification: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    success = fix_database_paths()
    if success:
        verify_fix()
    else:
        print("Failed to fix database paths")
