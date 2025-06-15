#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    print("Testing FileManager...")
    from src.utils.FileManager import FileManager
    print("✅ FileManager imported successfully")
    fm = FileManager()
    print("✅ FileManager instance created")
except Exception as e:
    print(f"❌ FileManager error: {e}")

try:
    print("Testing PDFExtractor...")
    from src.pdfprocessor.pdfExtractor import PDFExtractor
    print("✅ PDFExtractor imported successfully")
except Exception as e:
    print(f"❌ PDFExtractor error: {e}")

try:
    print("Testing ATSService...")
    from src.services.ATSService import ATSService
    print("✅ ATSService imported successfully")
except Exception as e:
    print(f"❌ ATSService error: {e}")

print("Import test completed.")
