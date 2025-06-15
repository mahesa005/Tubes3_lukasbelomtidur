#!/usr/bin/env python3
"""
Quick Performance Test - Test actual search speed with smaller sample
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.ATSService import ATSService

def test_quick_search():
    """Test search performance with common keywords"""
    
    print("=== Quick CV Search Test ===")
    
    # Initialize service
    service = ATSService()
    
    # Test keywords
    keywords = ['Python', 'Java']
    
    print(f"Testing search with keywords: {keywords}")
    print(f"Cache stats before: {service.get_cache_stats()}")
    
    # Perform search with very small result set to get fast results
    start_time = time.time()
    
    result = service.searchCVs(keywords, algorithm='KMP', topMatches=3)
    
    end_time = time.time()
    search_time = end_time - start_time
    
    print(f"Search completed in: {search_time:.2f} seconds")
    print(f"Found {len(result['results'])} matches")
    print(f"Processing time from service: {result['metadata']['processing_time_ms']:.2f} ms")
    print(f"Total files processed: {result['metadata']['total_processed']}")
    
    # Show sample results
    if result['results']:
        print("--- Sample Results ---")
        for i, res in enumerate(result['results'][:3], 1):
            print(f"{i}. {res['name']} - Score: {res['match_score']:.1f}%")
            print(f"   Keywords: {res['keywords']}")
    
    print(f"Cache stats after: {service.get_cache_stats()}")

if __name__ == "__main__":
    test_quick_search()
