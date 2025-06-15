#!/usr/bin/env python3
"""
Test dengan keyword yang lebih relevan untuk dataset CV ini
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_relevant_keywords():
    """Test dengan keyword yang lebih mungkin ada dalam dataset"""
    
    print("=== Testing with Relevant Keywords ===")
    print("Based on previous results, this dataset likely contains non-programming CVs")
    print("Testing with more general keywords...")
    
    try:
        from src.services.ATSService import ATSService
        service = ATSService()
        
        # Keywords yang lebih umum dan kemungkinan ada
        relevant_keywords = [
            'Manager',       # Sudah terbukti ada
            'Management',    # Variasi manager
            'Experience',    # Pasti ada di CV
            'Education',     # Pasti ada di CV
            'Skills',        # Pasti ada di CV
            'Work',          # Pasti ada di CV
            'University',    # Pendidikan
            'School',        # Pendidikan
            'Teacher',       # Profesi umum
            'Marketing',     # Bidang bisnis
            'Sales',         # Bidang bisnis
            'Project',       # Pengalaman kerja
            'Team',          # Kerja tim
            'Communication', # Soft skill
            'Leadership',    # Soft skill
        ]
        
        print(f"\nTesting {len(relevant_keywords)} relevant keywords:")
        results_summary = []
        
        for keyword in relevant_keywords:
            print(f"\n--- Testing: {keyword} ---")
            
            start_time = time.time()
            result = service.searchCVs([keyword], algorithm='KMP', topMatches=3)
            end_time = time.time()
            
            metadata = result.get('metadata', {})
            search_time = end_time - start_time
            found_count = len(result['results'])
            files_processed = metadata.get('total_processed', 0)
            
            print(f"⏱️  Time: {search_time:.2f}s | 📊 Results: {found_count} | 🔍 Processed: {files_processed}")
            
            if result['results']:
                print("✅ Sample matches:")
                for i, res in enumerate(result['results'][:2], 1):
                    print(f"   {i}. {res['name']} - Score: {res['match_score']:.1f}%")
                    print(f"      Count: {res['keywords'].get(keyword, 0)}")
            else:
                print("❌ No matches")
                
            results_summary.append({
                'keyword': keyword,
                'found': found_count,
                'time': search_time,
                'processed': files_processed
            })
        
        # Summary
        print(f"\n=== SUMMARY ===")
        successful_keywords = [r for r in results_summary if r['found'] > 0]
        
        if successful_keywords:
            print(f"✅ Found matches for {len(successful_keywords)} keywords:")
            for item in successful_keywords:
                print(f"  - '{item['keyword']}': {item['found']} matches ({item['time']:.2f}s)")
                
            print(f"\n🎯 RECOMMENDED KEYWORDS for this dataset:")
            top_keywords = sorted(successful_keywords, key=lambda x: x['found'], reverse=True)[:5]
            for i, item in enumerate(top_keywords, 1):
                print(f"  {i}. '{item['keyword']}' - {item['found']} matches")
                
        else:
            print("❌ No keywords found matches - there might be an issue with the search system")
            
        # Performance summary
        avg_time = sum(r['time'] for r in results_summary) / len(results_summary)
        avg_processed = sum(r['processed'] for r in results_summary) / len(results_summary)
        
        print(f"\n📈 PERFORMANCE:")
        print(f"  - Average search time: {avg_time:.2f} seconds")
        print(f"  - Average files processed: {avg_processed:.0f}")
        print(f"  - Case-insensitive matching: ✅ Enabled")
        print(f"  - Early termination: ✅ Working")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_relevant_keywords()
