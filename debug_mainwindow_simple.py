#!/usr/bin/env python3
"""
Simple debug untuk mengecek apakah signal dari tombol Ringkasan sampai ke MainWindow
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

def test_main_window_connections():
    """Test apakah signal dari ResultWidget terhubung ke MainWindow"""
    
    print("🔍 TESTING MAINWINDOW SIGNAL CONNECTIONS")
    print("=" * 50)
    
    try:
        from PyQt5.QtWidgets import QApplication
        from src.gui.MainWindow import MainWindow
        from src.services.ATSService import ATSService
        
        app = QApplication(sys.argv)
        
        # Create MainWindow
        print("1. Creating MainWindow...")
        main_window = MainWindow()
        
        print("✅ MainWindow created successfully")
        print(f"   - ResultWidget: {main_window.resultWidget}")
        print(f"   - SummaryWidget: {main_window.summaryWidget}")
        print(f"   - ATSService: {main_window.atsService}")
        
        # Check if signal is connected
        print("\n2. Checking signal connections...")
        
        # Override onResultSelected with debug version
        original_method = main_window.onResultSelected
        
        def debug_onResultSelected(application_id):
            print(f"🔔 onResultSelected called with application_id: {application_id}")
            try:
                result = original_method(application_id)
                print("✅ onResultSelected completed successfully")
                return result
            except Exception as e:
                print(f"❌ Error in onResultSelected: {e}")
                import traceback
                traceback.print_exc()
        
        # Replace method
        main_window.onResultSelected = debug_onResultSelected
        
        # Create test data to populate ResultWidget
        print("\n3. Creating test search results...")
        
        # Simulate a search result
        ats_service = ATSService()
        try:
            result = ats_service.searchCVs("python", "KMP", 3)
            if result and result.get('results'):
                print(f"✅ Got {len(result['results'])} search results")
                main_window.resultWidget.updateResults(result['results'], result.get('metadata', {}))
                print("✅ ResultWidget updated with real data")
            else:
                print("⚠️ No search results, creating mock data...")
                mock_results = [
                    {
                        'application_id': 1,
                        'name': 'Test User 1',
                        'match_score': 85.5,
                        'keywords': {'python': 3, 'java': 2},
                        'cv_path': 'src\\archive\\data\\data\\FITNESS\\54259150.pdf'
                    }
                ]
                mock_metadata = {'processing_time_ms': 100, 'total_matches': 1}
                main_window.resultWidget.updateResults(mock_results, mock_metadata)
                print("✅ ResultWidget updated with mock data")
        except Exception as e:
            print(f"❌ Error getting search results: {e}")
        
        # Test manual signal emission
        print("\n4. Testing manual signal emission...")
        try:
            print("🧪 Manually emitting resultSelected signal with application_id=1")
            main_window.resultWidget.resultSelected.emit(1)
            print("✅ Signal emitted successfully")
        except Exception as e:
            print(f"❌ Error emitting signal: {e}")
        
        # Show window
        print("\n5. Displaying MainWindow...")
        main_window.show()
        main_window.resize(1200, 800)
        
        print("\n📋 INSTRUCTIONS:")
        print("1. Look at the MainWindow that just opened")
        print("2. Try clicking the 'Ringkasan' button on any result")
        print("3. Watch the console for debug messages")
        print("4. Check if summary appears on the right panel")
        print("5. Press Ctrl+C in console to exit")
        
        # Run the app
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Error in test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_main_window_connections()
