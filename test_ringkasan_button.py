#!/usr/bin/env python3
"""
Test khusus untuk tombol Ringkasan di ResultWidget
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

def test_ringkasan_button():
    """Test spesifik tombol Ringkasan"""
    
    print("🔍 TESTING TOMBOL RINGKASAN")
    print("=" * 40)
    
    try:
        from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
        from src.gui.ResultWidget import ResultWidget
        from src.gui.SummaryWidget import SummaryWidget
        from src.services.ATSService import ATSService
        
        print("✅ Imports successful")
        
        # Create app
        app = QApplication(sys.argv)
        
        # Create window
        window = QMainWindow()
        window.setWindowTitle("Test Tombol Ringkasan")
        window.setGeometry(100, 100, 1200, 700)
        
        # Create widgets
        central = QWidget()
        window.setCentralWidget(central)
        layout = QHBoxLayout(central)
        
        # Result widget (left)
        result_widget = ResultWidget()
        layout.addWidget(result_widget, 2)
        
        # Summary widget (right)  
        summary_widget = SummaryWidget()
        layout.addWidget(summary_widget, 1)
        
        print("✅ Widgets created")
        
        # Connect signals
        def on_result_selected(application_id):
            print(f"🔔 Signal received! application_id: {application_id}")
            
            try:
                # Get summary
                ats_service = ATSService()
                summary_data = ats_service.getSummary(application_id=application_id)
                
                # Convert to dict
                summary_dict = {
                    'name': summary_data.full_name,
                    'skills': ', '.join(summary_data.skills),
                    'experience': '\n'.join(summary_data.work_experience),
                    'education': '\n'.join(summary_data.education),
                    'birth_date': summary_data.birth_date,
                    'phone_number': summary_data.phone_number,
                    'cv_path': summary_data.cv_path
                }
                
                print(f"📋 Summary data: {summary_dict}")
                
                # Update summary widget
                summary_widget.updateSummary(summary_dict)
                print("✅ Summary updated in widget")
                
            except Exception as e:
                print(f"❌ Error getting summary: {e}")
                import traceback
                traceback.print_exc()
        
        # Connect signal
        result_widget.resultSelected.connect(on_result_selected)
        
        # Create test data
        test_results = [
            {
                'application_id': 1,
                'name': 'Larry Morris (Test)',
                'match_score': 85.5,
                'keywords': {'python': 3, 'java': 2},
                'cv_path': 'src\\archive\\data\\data\\FITNESS\\54259150.pdf'
            },
            {
                'application_id': 2,
                'name': 'Test User 2',
                'match_score': 75.2,
                'keywords': {'programming': 2, 'leadership': 1},
                'cv_path': 'src\\archive\\data\\data\\AGRICULTURE\\11676151.pdf'
            }
        ]
        
        test_metadata = {
            'processing_time_ms': 150.0,
            'total_matches': 2
        }
        
        # Load test data
        result_widget.updateResults(test_results, test_metadata)
        print("✅ Test data loaded")
        
        # Apply styling
        window.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; color: white; }
            QWidget { background-color: #2b2b2b; color: white; }
            QPushButton { 
                background-color: #404040; 
                border: 1px solid #555; 
                padding: 8px; 
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #505050; }
            QGroupBox {
                border: 1px solid #555555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #ffffff;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        # Show window
        window.show()
        
        print("📋 Instructions:")
        print("   1. Click tombol 'Ringkasan' pada salah satu result card")
        print("   2. Lihat apakah summary muncul di panel kanan")
        print("   3. Check console untuk debug messages")
        print("   4. Press Ctrl+C to exit")
        
        # Run
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ringkasan_button()
