import sys
sys.path.append('.')

try:
    from src.services.ATSService import ATSService
    print("✅ Import ATSService successful")
    
    service = ATSService()
    print("✅ ATSService initialized")
    
    # Test dengan Boyer-Moore
    result = service.searchCVs(['teacher'], algorithm='Boyer-Moore', topMatches=1)
    print("✅ SUCCESS: Boyer-Moore algorithm works!")
    print(f"Results found: {len(result.get('results', []))}")
    print(f"Algorithm used: {result.get('metadata', {}).get('algorithm')}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
