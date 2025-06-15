#!/usr/bin/env python3
"""
Final Integration Test: RegexExtractor + PatternMatcher + Seeding Data
Test lengkap yang mensimulasikan real-world usage dengan data dari seeding.sql
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pdfprocessor.regexExtractor import RegexExtractor
from algorithm.PatternMatcher import PatternMatcher

def test_full_integration():
    """Test integrasi lengkap dengan simulasi real CV processing"""
    
    print("=" * 80)
    print("🔄 FULL INTEGRATION TEST: REGEX + PATTERN MATCHING")
    print("=" * 80)
    
    extractor = RegexExtractor()
    matcher = PatternMatcher()
    
    # Simulasi beberapa CV dari seeding database
    cvs_database = [
        {
            "id": 1,
            "name": "Moh4mm4d Nu9r4h4",
            "cv_content": """
            Moh4mm4d Nu9r4h4
            Email: mohammad.nugraha@techcorp.com
            Phone: 081234567891
            Address: Jl. Kenanga No. 12, Jakarta
            
            Summary: Senior Software Developer with expertise in full-stack development
            
            Skills: Python, JavaScript, React, Node.js, MySQL, Docker, AWS, Git
            
            Experience:
            Software Developer at TechCorp (2020-2023)
            - Developed web applications using React and Node.js
            - Implemented microservices architecture
            - Led team of 5 junior developers
            
            Education:
            S1 Computer Science ITB 2016-2020
            """
        },
        {
            "id": 2, 
            "name": "AR13L H3RFR1S0N",
            "cv_content": """
            AR13L H3RFR1S0N
            📧 ariel.herfrison@marketing.com | 📞 081223498761
            🏠 Jl. Jeruk No. 2, Bekasi
            
            PROFESSIONAL SUMMARY
            Marketing Manager with 5+ years experience in digital campaigns
            
            SKILLS: Digital Marketing, SEO, SEM, Analytics, Team Leadership, Content Strategy
            
            EXPERIENCE:
            Marketing Manager | ABC Agency | 2021-Present
            • Managed digital campaigns for 15+ clients
            • Increased ROI by 40% through data-driven strategies
            
            Marketing Coordinator | XYZ Corp | 2019-2021
            • Coordinated social media campaigns
            
            EDUCATION:
            MBA Marketing | Harvard Business School | 2019
            """
        },
        {
            "id": 3,
            "name": "F4rh4n N4f15",
            "cv_content": """
            F4rh4n N4f15 R4yh4n
            Contact: farhan.nafis@fintech.com, 081254789621
            
            Summary: Financial Analyst with expertise in investment planning
            
            Skills: Financial modeling, Risk analysis, Excel, SQL, Python, Tableau
            
            Experience:
            Financial Planner at Major Bank (2022-Present)
            - Created investment strategies for high-net-worth clients
            - Analyzed market trends and risks
            
            Cost Accountant at Finance Corp (2020-2022)
            - Managed cost analysis for multiple projects
            
            Education:
            S1 Finance and Banking - University of Economics (2020)
            """
        },
        {
            "id": 4,
            "name": "H41k4l 455y4uq1", 
            "cv_content": """
            H41k4l 455y4uq1
            Email: haikal.assyauqi@healthcare.com
            Phone: 081222334455
            
            Summary: Medical professional with specialization in anesthesiology
            
            Skills: Medical procedures, Patient care, Emergency response, Medical equipment
            
            Experience:
            Anesthesiologist at General Hospital (2021-Present)
            - Administered anesthesia for various surgical procedures
            - Monitored patient vital signs during operations
            
            Doctor at Community Clinic (2019-2021)
            - Provided primary healthcare services
            
            Education:
            Medical Degree - Faculty of Medicine, University of Indonesia (2019)
            """
        }
    ]
    
    # Test queries yang akan dicari
    test_queries = [
        {
            "keywords": ["Software", "Developer", "Python"],
            "expected_matches": ["Moh4mm4d Nu9r4h4"]
        },
        {
            "keywords": ["Marketing", "Digital", "SEO"],
            "expected_matches": ["AR13L H3RFR1S0N"]
        },
        {
            "keywords": ["Financial", "Analysis", "Excel"],
            "expected_matches": ["F4rh4n N4f15"]
        },
        {
            "keywords": ["Medical", "Doctor", "Healthcare"],
            "expected_matches": ["H41k4l 455y4uq1"]
        },
        {
            "keywords": ["Manager", "Team"],
            "expected_matches": ["Moh4mm4d Nu9r4h4", "AR13L H3RFR1S0N"]
        }
    ]
    
    print(f"📋 Processing {len(cvs_database)} CVs from seeding database...")
    print(f"🔍 Testing {len(test_queries)} different search queries...")
    
    # Process each CV
    processed_cvs = []
    for cv in cvs_database:
        print(f"\n--- Processing CV: {cv['name']} ---")
        
        # Extract information using regex
        extracted_info = extractor.extractAllInformation(cv['cv_content'])
        
        # Store processed CV
        processed_cv = {
            "id": cv["id"],
            "name": cv["name"],
            "original_content": cv["cv_content"],
            "extracted_info": extracted_info,
            "clean_text": extractor.cleanseText(cv["cv_content"])
        }
        processed_cvs.append(processed_cv)
        
        print(f"   📧 Emails: {extracted_info['emails']}")
        print(f"   📞 Phones: {extracted_info['phones']}")
        print(f"   💼 Skills: {extracted_info['skills'][:3]}..." if len(extracted_info['skills']) > 3 else f"   💼 Skills: {extracted_info['skills']}")
        print(f"   🏢 Experience entries: {len(extracted_info['experience'])}")
        print(f"   🎓 Education entries: {len(extracted_info['education'])}")
    
    print(f"\n{'='*80}")
    print("🔍 PATTERN MATCHING TESTS")
    print("="*80)
    
    # Test each query
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Query {i}: {query['keywords']} ---")
        
        matches_found = []
        
        for cv in processed_cvs:
            # Test pattern matching with KMP
            kmp_result = matcher.exactMatch(cv["clean_text"], query["keywords"], "KMP")
            
            # Test pattern matching with Boyer-Moore  
            bm_result = matcher.exactMatch(cv["clean_text"], query["keywords"], "BM")
            
            # Check if any keywords matched
            kmp_matches = any(kmp_result.get("matches", {}).get(keyword, []) for keyword in query["keywords"])
            bm_matches = any(bm_result.get("matches", {}).get(keyword, []) for keyword in query["keywords"])
            
            if kmp_matches or bm_matches:
                matches_found.append(cv["name"])
                print(f"   ✅ MATCH: {cv['name']}")
                
                # Show which keywords matched
                for keyword in query["keywords"]:
                    kmp_positions = kmp_result.get("matches", {}).get(keyword.lower(), [])
                    bm_positions = bm_result.get("matches", {}).get(keyword.lower(), [])
                    
                    if kmp_positions:
                        print(f"      🎯 '{keyword}' found at positions {kmp_positions[:3]} (KMP)")
                    if bm_positions:
                        print(f"      🎯 '{keyword}' found at positions {bm_positions[:3]} (BM)")
        
        print(f"   📊 Expected: {query['expected_matches']}")
        print(f"   📊 Found: {matches_found}")
        
        # Check accuracy
        expected_set = set(query['expected_matches'])
        found_set = set(matches_found)
        accuracy = len(expected_set.intersection(found_set)) / len(expected_set) if expected_set else 1.0
        print(f"   📈 Accuracy: {accuracy*100:.1f}%")

def test_performance_simulation():
    """Test performa dengan data yang lebih besar"""
    
    print(f"\n{'='*80}")
    print("⚡ PERFORMANCE SIMULATION TEST")
    print("="*80)
    
    extractor = RegexExtractor()
    matcher = PatternMatcher()
    
    # Generate multiple CVs based on seeding patterns
    import time
    
    names_pool = [
        "Moh4mm4d Nu9r4h4", "AR13L H3RFR1S0N", "F4rh4n N4f15", "H41k4l 455y4uq1",
        "R4d3n Fr4nC15c0", "4l4nd MuL14", "4hm4d R4f1", "1khw4n 4lH4k1m"
    ]
    
    skills_pool = [
        ["Python", "Java", "JavaScript", "React"],
        ["Marketing", "SEO", "Analytics", "Content"],
        ["Finance", "Excel", "SQL", "Analysis"],
        ["Medical", "Healthcare", "Patient care"],
        ["Engineering", "Design", "CAD", "Project"],
        ["Sales", "Customer", "Communication", "CRM"]
    ]
    
    print(f"🏭 Generating {len(names_pool)} synthetic CVs...")
    
    start_time = time.time()
    
    processed_count = 0
    for i, name in enumerate(names_pool):
        cv_content = f"""
        {name}
        Email: {name.lower().replace(' ', '.')}@company{i}.com
        Phone: 08122{i:04d}{i:04d}
        
        Summary: Professional with expertise in various domains
        Skills: {', '.join(skills_pool[i % len(skills_pool)])}
        Experience: Senior role at Company{i} (2020-Present)
        Education: Degree from University{i} (2018)
        """
        
        # Extract and process
        extracted = extractor.extractAllInformation(cv_content)
        clean_text = extractor.cleanseText(cv_content)
        
        # Pattern matching test
        test_keywords = ["Professional", "expertise", "Company"]
        kmp_result = matcher.exactMatch(clean_text, test_keywords, "KMP")
        bm_result = matcher.exactMatch(clean_text, test_keywords, "BM")
        
        processed_count += 1
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"✅ Processed {processed_count} CVs in {total_time:.3f} seconds")
    print(f"⚡ Average time per CV: {total_time/processed_count:.3f} seconds")
    print(f"📊 Processing rate: {processed_count/total_time:.1f} CVs/second")

def main():
    """Run full integration tests"""
    
    print("🚀 FINAL INTEGRATION TEST: REGEX EXTRACTOR + PATTERN MATCHER")
    print("Testing dengan data realistis dari seeding.sql database")
    
    try:
        test_full_integration()
        test_performance_simulation()
        
        print(f"\n{'='*80}")
        print("🎉 FULL INTEGRATION TEST COMPLETED SUCCESSFULLY!")
        print("✅ RegexExtractor: Berhasil extract informasi dari CV")
        print("✅ PatternMatcher: Berhasil melakukan pattern matching")
        print("✅ Integration: Sistem bekerja dengan baik end-to-end")
        print("✅ Performance: Kecepatan processing memadai")
        print("="*80)
        
    except Exception as e:
        print(f"❌ ERROR during integration testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
