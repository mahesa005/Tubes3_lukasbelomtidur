#!/usr/bin/env python3
"""
Test sangat sederhana untuk tombol Ringkasan - standalone test
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

def test_button_click_simple():
    """Test tombol Ringkasan paling sederhana"""
    
    print("🧪 TEST TOMBOL RINGKASAN - SIMPLE VERSION")
    print("=" * 50)
    
    try:
        from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QLabel
        from src.gui.ResultWidget import ResultWidget
        from src.gui.SummaryWidget import SummaryWidget
        
        app = QApplication(sys.argv)
        
        # Create window
        window = QMainWindow()
        window.setWindowTitle("Test Tombol Ringkasan")
        window.setGeometry(100, 100, 1000, 600)
        
        central = QWidget()
        window.setCentralWidget(central)
        layout = QHBoxLayout(central)
        
        # Left: ResultWidget
        result_widget = ResultWidget()
        layout.addWidget(result_widget, 2)
        
        # Right: SummaryWidget + Status
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        status_label = QLabel("Status: Menunggu klik tombol Ringkasan...")
        status_label.setStyleSheet("padding: 10px; background-color: #333; color: white; border-radius: 5px;")
        right_layout.addWidget(status_label)
        
        summary_widget = SummaryWidget()
        right_layout.addWidget(summary_widget)
        
        layout.addWidget(right_panel, 1)
        
        # Signal handler with status updates
        def on_summary_requested(application_id):
            print(f"🔔 SIGNAL RECEIVED! application_id: {application_id}")
            status_label.setText(f"Status: Signal diterima untuk ID {application_id}")
            status_label.setStyleSheet("padding: 10px; background-color: #006600; color: white; border-radius: 5px;")
            
            try:
                # Get summary
                from src.services.ATSService import ATSService
                ats_service = ATSService()
                
                status_label.setText(f"Status: Mengambil data summary...")
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
                
                status_label.setText(f"Status: Menampilkan summary...")
                summary_widget.updateSummary(summary_dict)
                
                status_label.setText(f"Status: ✅ Summary berhasil ditampilkan!")
                status_label.setStyleSheet("padding: 10px; background-color: #006600; color: white; border-radius: 5px;")
                
                print("✅ Summary berhasil diupdate!")
                
            except Exception as e:
                print(f"❌ Error getting summary: {e}")
                status_label.setText(f"Status: ❌ Error: {e}")
                status_label.setStyleSheet("padding: 10px; background-color: #660000; color: white; border-radius: 5px;")
        
        # Connect signal
        result_widget.resultSelected.connect(on_summary_requested)
        
        # Create test data
        test_data = [
            {
                'application_id': 1,
                'name': 'Larry Morris (Test)',
                'match_score': 95.5,
                'keywords': {'python': 3, 'developer': 2},
                'cv_path': 'src\\archive\\data\\data\\FITNESS\\54259150.pdf'
            },
            {
                'application_id': 2,
                'name': 'Test User 2',
                'match_score': 87.2,
                'keywords': {'java': 2, 'programming': 1},
                'cv_path': 'src\\archive\\data\\data\\AGRICULTURE\\11676151.pdf'
            }
        ]
        
        metadata = {'processing_time_ms': 125, 'total_matches': 2}
        
        # Update results
        result_widget.updateResults(test_data, metadata)
        
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
        
        print("✅ Test window created successfully!")
        print("\n📋 INSTRUCTIONS:")
        print("1. Click tombol 'Ringkasan' pada salah satu result card")
        print("2. Watch status label di panel kanan")
        print("3. Check console untuk debug messages")
        print("4. Summary seharusnya muncul di panel kanan")
        print("\nIf button tidak berfungsi, kemungkinan ada masalah dengan signal connection.")
        
        # Run
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_button_click_simple()
