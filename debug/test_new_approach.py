#!/usr/bin/env python3
"""
Test the new approach: Process all PDFs but stop when enough matches found
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_new_approach():
    """Test the concept of processing all files but stopping early"""
    
    print("=== Testing New Search Approach ===")
    print("Concept: Process ALL PDFs but stop when target matches reached")
    
    # Simulate file processing
    total_files = 2484  # Total PDF files
    target_matches = 5  # User wants top 5 matches
    
    matches_found = 0
    files_processed = 0
    batch_size = 50
    
    print(f"Total files available: {total_files}")
    print(f"Target matches: {target_matches}")
    print(f"Processing in batches of {batch_size}")
    print()
    
    start_time = time.time()
    
    # Simulate batch processing
    for i in range(0, total_files, batch_size):
        if matches_found >= target_matches:
            print(f"✅ Found {target_matches} matches! Stopping early.")
            break
            
        batch_end = min(i + batch_size, total_files)
        batch_size_actual = batch_end - i
        
        print(f"Processing batch {i//batch_size + 1}: files {i+1}-{batch_end}")
        
        # Simulate processing (some files match, some don't)
        # Let's say 10% of files have matches on average
        batch_matches = max(1, batch_size_actual // 10)  # At least 1 match per batch
        matches_found += batch_matches
        files_processed += batch_size_actual
        
        print(f"  Found {batch_matches} matches in this batch")
        print(f"  Total matches so far: {matches_found}")
        print(f"  Files processed so far: {files_processed}")
        print()
        
        # Simulate processing time
        time.sleep(0.1)  # 100ms per batch
    
    end_time = time.time()
    processing_time = (end_time - start_time) * 1000
    
    print("=== Results ===")
    print(f"✅ Search completed successfully!")
    print(f"📁 Total files available: {total_files}")
    print(f"🔍 Files actually processed: {files_processed}")
    print(f"🎯 Target matches: {target_matches}")
    print(f"📊 Actual matches found: {min(matches_found, target_matches)}")
    print(f"⚡ Processing time: {processing_time:.1f} ms")
    print(f"🚀 Early termination: {'Yes' if files_processed < total_files else 'No'}")
    print(f"💪 Efficiency: {((total_files - files_processed) / total_files * 100):.1f}% files saved")

if __name__ == "__main__":
    test_new_approach()
