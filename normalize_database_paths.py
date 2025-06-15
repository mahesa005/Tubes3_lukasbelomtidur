#!/usr/bin/env python3
"""
Script to normalize database cv_path entries to use forward slashes for cross-platform compatibility.
The database currently has paths with backslashes (Windows format) but the search system expects forward slashes.
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

def normalize_database_paths():
    logger = setup_logging()
    logger.info("Starting database path normalization process...")
    
    db = DatabaseConnection()
    if not db.connect():
        logger.error("Failed to connect to database")
        return False
    
    try:
        # Get all current cv_path entries
        logger.info("Fetching current cv_path entries from database...")
        query = "SELECT application_id, cv_path FROM ApplicationDetail WHERE cv_path IS NOT NULL"
        if not db.execute(query):
            logger.error("Failed to fetch cv_path entries")
            return False
        
        results = db.cursor.fetchall()
        logger.info(f"Found {len(results)} cv_path entries to normalize")
        
        # Track statistics
        updated_count = 0
        error_count = 0
        skipped_count = 0
        
        for application_id, current_path in results:
            # Convert backslashes to forward slashes
            normalized_path = current_path.replace('\\', '/')
            
            # Only update if the path actually changed
            if normalized_path != current_path:
                # Verify the file actually exists with normalized path
                project_root = Path(__file__).parent
                full_file_path = project_root / normalized_path
                
                if full_file_path.exists():
                    # Update the database
                    update_query = "UPDATE ApplicationDetail SET cv_path = %s WHERE application_id = %s"
                    if db.execute(update_query, (normalized_path, application_id)):
                        logger.info(f"Updated application_id {application_id}: '{current_path}' -> '{normalized_path}'")
                        updated_count += 1
                    else:
                        logger.error(f"Failed to update application_id {application_id}")
                        error_count += 1
                else:
                    logger.warning(f"File does not exist for application_id {application_id}: {full_file_path}")
                    error_count += 1
            else:
                logger.debug(f"Skipping application_id {application_id} - path already normalized: {current_path}")
                skipped_count += 1
        
        # Commit changes
        db.connection.commit()
        logger.info(f"Database path normalization completed. Updated: {updated_count}, Errors: {error_count}, Skipped: {skipped_count}")
        
        return updated_count > 0
        
    except Exception as e:
        logger.error(f"Error during database path normalization: {e}")
        return False
    finally:
        db.disconnect()

def verify_normalization():
    """Verify that the normalization worked by checking a few sample paths"""
    logger = setup_logging()
    logger.info("Verifying database path normalization...")
    
    db = DatabaseConnection()
    if not db.connect():
        logger.error("Failed to connect to database for verification")
        return
    
    try:
        # Get a sample of updated paths
        query = "SELECT application_id, cv_path FROM ApplicationDetail WHERE cv_path IS NOT NULL LIMIT 10"
        if db.execute(query):
            results = db.cursor.fetchall()
            logger.info("Sample of normalized paths:")
            for application_id, cv_path in results:
                # Check if file exists
                project_root = Path(__file__).parent
                full_path = project_root / cv_path
                exists = "EXISTS" if full_path.exists() else "NOT FOUND"
                format_type = "FORWARD SLASHES" if '/' in cv_path else "BACKSLASHES"
                logger.info(f"  application_id {application_id}: {cv_path} [{format_type}] [{exists}]")
                
        # Check for any remaining backslashes
        query_backslashes = "SELECT COUNT(*) FROM ApplicationDetail WHERE cv_path LIKE '%\\\\%'"
        if db.execute(query_backslashes):
            result = db.cursor.fetchone()
            backslash_count = result[0] if result else 0
            logger.info(f"Remaining paths with backslashes: {backslash_count}")
            
    except Exception as e:
        logger.error(f"Error during verification: {e}")
    finally:
        db.disconnect()

def test_path_matching():
    """Test if search paths will now match database paths"""
    logger = setup_logging()
    logger.info("Testing path matching between file system and database...")
    
    # Test a few sample files from the file system
    import os
    from pathlib import Path
    from config import DATA_DIR
    
    project_root = Path(__file__).parent
    data_dir = DATA_DIR
    
    # Get a few sample PDF files
    sample_files = []
    for role_dir in data_dir.iterdir():
        if role_dir.is_dir():
            pdf_files = list(role_dir.glob("*.pdf"))[:2]  # Just get 2 files per role
            sample_files.extend(pdf_files)
            if len(sample_files) >= 10:  # Limit to 10 samples
                break
    
    db = DatabaseConnection()
    if not db.connect():
        logger.error("Failed to connect to database for path matching test")
        return
    
    try:
        matched_count = 0
        total_tested = 0
        
        for file_path in sample_files:
            # Convert to relative path like the search system does
            relative_path = os.path.relpath(file_path, project_root)
            # Normalize to forward slashes like we did in the database
            normalized_path = relative_path.replace('\\', '/')
            
            # Check if this path exists in database
            query = "SELECT application_id FROM ApplicationDetail WHERE cv_path = %s"
            if db.execute(query, (normalized_path,)):
                result = db.cursor.fetchone()
                if result:
                    application_id = result[0]
                    logger.info(f"MATCH: {normalized_path} -> application_id {application_id}")
                    matched_count += 1
                else:
                    logger.warning(f"NO MATCH: {normalized_path}")
            total_tested += 1
                    
        logger.info(f"Path matching test completed: {matched_count}/{total_tested} files matched")
        
    except Exception as e:
        logger.error(f"Error during path matching test: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    success = normalize_database_paths()
    if success:
        verify_normalization()
        test_path_matching()
    else:
        print("Failed to normalize database paths")
