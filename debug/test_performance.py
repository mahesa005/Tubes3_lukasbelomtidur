#!/usr/bin/env python3
"""
Performance test script untuk membandingkan kecepatan search sebelum dan sesudah optimasi
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.ATSService import ATSService

def test_search_performance():
    """Test performance dari search function"""
    print("=== ATS CV Matcher - Performance Test ===")
    
    # Initialize service
    service = ATSService()
    
    # Test keywords
    test_keywords = ['Python', 'Java', 'Manager']
    
    print(f"Testing search with keywords: {test_keywords}")
    print(f"Cache stats before: {service.get_cache_stats()}")
    
    # First search (cold cache)
    print("\n--- First search (cold cache) ---")
    start_time = time.time()
    results1 = service.searchCVs(test_keywords, algorithm='KMP', topMatches=5)
    first_time = time.time() - start_time
    
    print(f"First search completed in: {first_time:.2f} seconds")
    print(f"Found {len(results1['results'])} matches")
    print(f"Processing time from service: {results1['metadata']['processing_time_ms']:.2f} ms")
    
    # Second search (warm cache)
    print("\n--- Second search (warm cache) ---")
    start_time = time.time()
    results2 = service.searchCVs(test_keywords, algorithm='KMP', topMatches=5)
    second_time = time.time() - start_time
    
    print(f"Second search completed in: {second_time:.2f} seconds")
    print(f"Found {len(results2['results'])} matches")
    print(f"Processing time from service: {results2['metadata']['processing_time_ms']:.2f} ms")
    
    # Show improvement
    if first_time > 0:
        improvement = ((first_time - second_time) / first_time) * 100
        print(f"\n--- Performance Improvement ---")
        print(f"Speed improvement: {improvement:.1f}%")
        print(f"Cache stats after: {service.get_cache_stats()}")
    
    # Show some results
    if results2['results']:
        print(f"\n--- Sample Results ---")
        for i, result in enumerate(results2['results'][:3]):
            print(f"{i+1}. {result['name']} - Score: {result['match_score']:.1f}%")
            print(f"   Keywords: {result['keywords']}")

if __name__ == "__main__":
    test_search_performance()
