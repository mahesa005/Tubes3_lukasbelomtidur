#!/usr/bin/env python3
"""
Debug script untuk mengecek signal-slot connection dalam GUI
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

def test_signal_slot_connections():
    """Test signal-slot connections in the GUI"""
    print("🔧 Testing Signal-Slot Connections...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from src.gui.MainWindow import MainWindow
        from src.gui.ResultWidget import ResultWidget
        from src.gui.SummaryWidget import SummaryWidget
        
        app = QApplication([])
        
        # Create main window
        window = MainWindow()
        
        print("✅ MainWindow created successfully")
        
        # Check if widgets are created
        print(f"✅ SearchWidget: {window.searchWidget}")
        print(f"✅ ResultWidget: {window.resultWidget}")
        print(f"✅ SummaryWidget: {window.summaryWidget}")
        
        # Manually test resultSelected signal
        print("\n🧪 Testing resultSelected signal manually...")
        
        # Simulate clicking on summary button
        test_application_id = 1
        print(f"🔄 Simulating resultSelected signal with application_id: {test_application_id}")
        
        # This should trigger the summary update
        window.onResultSelected(test_application_id)
        
        print("✅ Signal test completed - check console output for debug messages")
        
    except Exception as e:
        print(f"❌ Error in signal-slot test: {e}")
        import traceback
        traceback.print_exc()

def test_summary_widget_standalone():
    """Test SummaryWidget standalone"""
    print("\n🧪 Testing SummaryWidget Standalone...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from src.gui.SummaryWidget import SummaryWidget
        
        app = QApplication([])
        
        # Create summary widget
        summary_widget = SummaryWidget()
        
        # Test data
        test_data = {
            'name': 'Test User',
            'skills': 'Python, Java, JavaScript',
            'experience': 'Software Developer at ABC Company\nSenior Developer at XYZ Corp',
            'education': 'Bachelor in Computer Science\nMaster in Software Engineering',
            'birth_date': '1990-01-01',
            'phone_number': '081234567890',
            'cv_path': 'test/path/cv.pdf'
        }
        
        print(f"📄 Test data: {test_data}")
        
        # Update summary
        summary_widget.updateSummary(test_data)
        
        print("✅ SummaryWidget.updateSummary() executed successfully")
        
        # Show widget for visual test
        summary_widget.show()
        summary_widget.resize(400, 600)
        
        print("📋 SummaryWidget is displayed - check if content is visible")
        print("Press Ctrl+C to close")
        
        app.exec_()
        
    except Exception as e:
        print(f"❌ Error in SummaryWidget test: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main test function"""
    print("🔍 GUI DEBUG: Testing Summary Button Functionality")
    print("=" * 60)
    
    # Test 1: Signal-slot connections
    test_signal_slot_connections()
    
    # Test 2: SummaryWidget standalone
    test_summary_widget_standalone()

if __name__ == "__main__":
    main()
