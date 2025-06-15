#!/usr/bin/env python3
"""
Test the search functionality to see if CV files now correctly match database entries.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.ATSService import ATSService
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def test_search_functionality():
    logger = setup_logging()
    logger.info("Testing search functionality after path normalization...")
    
    # Initialize ATS service
    ats_service = ATSService()
    
    # Test search with common keywords
    test_keywords = ['python', 'java', 'engineer', 'manager', 'developer']
    
    for keywords in [['python'], ['engineer'], ['manager'], ['java', 'developer']]:
        logger.info(f"\n=== Testing search with keywords: {keywords} ===")
        try:
            results = ats_service.searchCVs(
                keywords=keywords,
                algorithm='KMP',
                topMatches=10
            )
            
            logger.info(f"Search completed in {results['metadata']['processing_time_ms']:.2f}ms")
            logger.info(f"Total matches found: {results['metadata']['total_matches_found']}")
            logger.info(f"Total processed: {results['metadata']['total_processed']}")
            
            # Check if results have valid application_id values
            valid_matches = 0
            for result in results['results']:
                if result['application_id'] is not None:
                    valid_matches += 1
                    logger.info(f"  ✓ Match: {result['name']} (ID: {result['application_id']}, Score: {result['match_score']:.1f}%)")
                else:
                    logger.warning(f"  ✗ No DB match: {result['name']} (Score: {result['match_score']:.1f}%)")
            
            logger.info(f"Valid database matches: {valid_matches}/{len(results['results'])}")
            
            if valid_matches > 0:
                logger.info("🎉 SUCCESS: Search is now finding database matches!")
            else:
                logger.warning("⚠️  Still no database matches found")
                
        except Exception as e:
            logger.error(f"Error during search: {e}")

def test_specific_database_file():
    """Test search with a specific file that we know exists in the database"""
    logger = setup_logging()
    logger.info("\n=== Testing with specific database file ===")
    
    # We know from the normalization log that these files exist in the database:
    # src/archive/data/data/FITNESS/54259150.pdf (application_id 1)
    # src/archive/data/data/AGRICULTURE/11676151.pdf (application_id 2)
    
    ats_service = ATSService()
    
    # Try to search for something that might be in fitness PDFs
    fitness_keywords = ['fitness', 'trainer', 'exercise', 'gym', 'health']
    
    logger.info(f"Testing search with fitness-related keywords: {fitness_keywords}")
    
    try:
        results = ats_service.searchCVs(
            keywords=fitness_keywords,
            algorithm='KMP',
            topMatches=5
        )
        
        logger.info(f"Fitness search results: {len(results['results'])} matches")
        
        for result in results['results']:
            logger.info(f"  - {result['name']} (ID: {result['application_id']}, Path: {result.get('cv_path', 'N/A')})")
            
    except Exception as e:
        logger.error(f"Error during fitness search: {e}")

if __name__ == "__main__":
    test_search_functionality()
    test_specific_database_file()
