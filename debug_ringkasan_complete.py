#!/usr/bin/env python3
"""
Debug script untuk mengecek flow signal tombol Ringkasan dari awal sampai akhir
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

def debug_ringkasan_flow():
    """Debug complete flow tombol Ringkasan"""
    
    print("🔍 DEBUG: COMPLETE RINGKASAN BUTTON FLOW")
    print("=" * 60)
    
    # Step 1: Test ResultWidget signal emission
    print("\n1️⃣ TESTING RESULTWIDGET SIGNAL EMISSION")
    print("-" * 40)
    
    try:
        from PyQt5.QtWidgets import QApplication
        from src.gui.ResultWidget import ResultWidget
        
        app = QApplication([])
        
        # Create result widget
        result_widget = ResultWidget()
        
        # Track signal emission
        signal_received = False
        received_app_id = None
        
        def signal_handler(app_id):
            nonlocal signal_received, received_app_id
            signal_received = True
            received_app_id = app_id
            print(f"📡 Signal received! application_id: {app_id}")
        
        # Connect signal
        result_widget.resultSelected.connect(signal_handler)
        
        # Create test data
        test_results = [
            {
                'application_id': 123,
                'name': 'Test User',
                'match_score': 85.5,
                'keywords': {'python': 3},
                'cv_path': 'test/path.pdf'
            }
        ]
        
        test_metadata = {'processing_time_ms': 100, 'total_matches': 1}
        
        # Update results (this creates the button)
        result_widget.updateResults(test_results, test_metadata)
        
        print("✅ ResultWidget created with test data")
        print(f"✅ Signal connected: {result_widget.resultSelected}")
        
        # Manually emit signal to test
        print("\n🧪 Testing manual signal emission...")
        result_widget.resultSelected.emit(123)
        
        if signal_received and received_app_id == 123:
            print("✅ Signal emission works correctly!")
        else:
            print("❌ Signal emission failed!")
            
    except Exception as e:
        print(f"❌ Error in step 1: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 2: Test ATSService getSummary
    print("\n2️⃣ TESTING ATSSERVICE GETSUMMARY")
    print("-" * 40)
    
    try:
        from src.services.ATSService import ATSService
        
        ats_service = ATSService()
        
        # Test with known application_id
        print("🔄 Testing getSummary with application_id=1...")
        summary_data = ats_service.getSummary(application_id=1)
        
        print(f"✅ getSummary returned: {type(summary_data)}")
        print(f"   Name: {summary_data.full_name}")
        print(f"   Skills: {summary_data.skills}")
        print(f"   CV Path: {summary_data.cv_path}")
        
        # Test conversion to dict
        summary_dict = {
            'name': summary_data.full_name,
            'skills': ', '.join(summary_data.skills),
            'experience': '\n'.join(summary_data.work_experience),
            'education': '\n'.join(summary_data.education),
            'birth_date': summary_data.birth_date,
            'phone_number': summary_data.phone_number,
            'cv_path': summary_data.cv_path
        }
        
        print("✅ Dict conversion successful")
        
    except Exception as e:
        print(f"❌ Error in step 2: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 3: Test SummaryWidget updateSummary
    print("\n3️⃣ TESTING SUMMARYWIDGET UPDATESUMMARY")
    print("-" * 40)
    
    try:
        from src.gui.SummaryWidget import SummaryWidget
        
        summary_widget = SummaryWidget()
        
        # Test with the summary dict from step 2
        print("🔄 Testing updateSummary...")
        summary_widget.updateSummary(summary_dict)
        
        print("✅ updateSummary completed")
        
        # Show widget for visual test
        summary_widget.show()
        summary_widget.resize(400, 600)
        
        print("📱 SummaryWidget displayed - check if content is visible")
        
    except Exception as e:
        print(f"❌ Error in step 3: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 4: Test complete integration
    print("\n4️⃣ TESTING COMPLETE INTEGRATION")
    print("-" * 40)
    
    try:
        from src.gui.MainWindow import MainWindow
        
        # Create main window
        main_window = MainWindow()
        
        print("✅ MainWindow created")
        print(f"✅ ResultWidget: {main_window.resultWidget}")
        print(f"✅ SummaryWidget: {main_window.summaryWidget}")
        
        # Check signal connection
        print("\n🔗 Checking signal connections...")
        
        # Test the onResultSelected method directly
        print("🧪 Testing onResultSelected directly...")
        main_window.onResultSelected(1)
        
        print("✅ onResultSelected executed")
        
        # Show main window
        main_window.show()
        
        print("📱 MainWindow displayed")
        
    except Exception as e:
        print(f"❌ Error in step 4: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🔚 DEBUG COMPLETE")
    print("If all steps passed, the Ringkasan button should work!")
    print("Check the displayed windows and console output.")
    print("=" * 60)

def check_button_creation():
    """Check if buttons are created correctly in ResultWidget"""
    
    print("\n🔧 CHECKING BUTTON CREATION IN RESULTWIDGET")
    print("-" * 50)
    
    try:
        from PyQt5.QtWidgets import QApplication, QPushButton
        from src.gui.ResultWidget import ResultWidget
        
        app = QApplication([])
        
        result_widget = ResultWidget()
        
        # Test data
        test_results = [
            {
                'application_id': 456,
                'name': 'Debug User',
                'match_score': 92.1,
                'keywords': {'java': 2, 'programming': 1},
                'cv_path': 'debug/test.pdf'
            }
        ]
        
        # Before adding results
        print(f"Before updateResults - widget count: {result_widget.resultsLayout.count()}")
        
        # Add results
        result_widget.updateResults(test_results, {'total_matches': 1, 'processing_time_ms': 50})
        
        # After adding results
        print(f"After updateResults - widget count: {result_widget.resultsLayout.count()}")
        
        # Check the created widgets
        for i in range(result_widget.resultsLayout.count()):
            widget = result_widget.resultsLayout.itemAt(i).widget()
            if widget:
                print(f"Widget {i}: {type(widget).__name__}")
                
                # Look for buttons in the widget
                buttons = widget.findChildren(QPushButton)
                print(f"  Buttons found: {len(buttons)}")
                for j, button in enumerate(buttons):
                    print(f"    Button {j}: '{button.text()}'")
                    if button.text() == "Ringkasan":
                        print(f"    ✅ Found Ringkasan button!")
                        
                        # Test button click
                        print("    🧪 Testing button click...")
                        button.click()
                        print("    ✅ Button clicked!")
        
        print("✅ Button creation check completed")
        
    except Exception as e:
        print(f"❌ Error checking buttons: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_ringkasan_flow()
    check_button_creation()
    
    print("\n🎯 INSTRUCTIONS:")
    print("1. Check console output for any errors")
    print("2. Look at the displayed windows")  
    print("3. If widgets are displayed but empty, there might be a layout issue")
    print("4. If no errors but no content, check signal-slot connections")
    
    # Keep app running to see windows
    try:
        import sys
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            print("\n⏳ Keeping windows open... Press Ctrl+C to exit")
            sys.exit(app.exec_())
    except:
        pass
