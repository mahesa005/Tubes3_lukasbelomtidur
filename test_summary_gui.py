#!/usr/bin/env python3
"""
Test script untuk menjalankan aplikasi dan test tombol summary
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

def test_app_launch():
    """Test launching the app"""
    print("🚀 Launching ATS CV Matcher App...")
    print("Instructions:")
    print("1. Cari CV dengan keywords seperti 'python' atau 'java'")
    print("2. Klik tombol 'Ringkasan' pada salah satu hasil")
    print("3. Lihat apakah ringkasan muncul di panel kanan")
    print("=" * 60)
    
    try:
        from src.gui.MainWindow import MainWindow
        from PyQt5.QtWidgets import QApplication
        from src.gui.styles import applyTheme
        
        app = QApplication(sys.argv)
        applyTheme(app, 'dark')
        
        window = MainWindow()
        window.show()
        
        print("✅ Application launched successfully!")
        print("📋 Test the Summary button by:")
        print("   1. Search for 'python' or 'java'")  
        print("   2. Click 'Ringkasan' button on any result")
        print("   3. Check if summary appears on the right panel")
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Error launching app: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_app_launch()
