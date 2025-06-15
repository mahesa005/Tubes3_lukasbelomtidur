#!/usr/bin/env python3
"""
Simple test untuk tombol summary - standalone test
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

def test_summary_button_simple():
    """Test yang sangat sederhana untuk tombol summary"""
    
    print("🧪 SIMPLE SUMMARY BUTTON TEST")
    print("=" * 40)
    
    try:
        # Import PyQt5
        from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
        from PyQt5.QtCore import Qt
        
        # Import komponen kita
        from src.gui.SummaryWidget import SummaryWidget
        from src.services.ATSService import ATSService
        
        print("✅ All imports successful")
        
        # Create application
        app = QApplication(sys.argv)
        
        # Create main window
        window = QMainWindow()
        window.setWindowTitle("Test Summary Widget")
        window.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central = QWidget()
        window.setCentralWidget(central)
        layout = QHBoxLayout(central)
        
        # Create summary widget
        summary_widget = SummaryWidget()
        layout.addWidget(summary_widget)
        
        # Create test button
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        
        test_button = QPushButton("Test Summary")
        test_button.clicked.connect(lambda: test_summary_data(summary_widget))
        
        clear_button = QPushButton("Clear Summary")
        clear_button.clicked.connect(lambda: summary_widget.showInitialMessage())
        
        button_layout.addWidget(test_button)
        button_layout.addWidget(clear_button)
        button_layout.addStretch()
        
        layout.addWidget(button_widget)
        
        print("✅ UI created successfully")
        
        # Show window
        window.show()
        
        # Apply some styling
        window.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; color: white; }
            QWidget { background-color: #2b2b2b; color: white; }
            QPushButton { 
                background-color: #404040; 
                border: 1px solid #555; 
                padding: 10px; 
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #505050; }
        """)
        
        print("✅ Window displayed")
        print("📋 Instructions:")
        print("   1. Click 'Test Summary' to load test data")
        print("   2. Check if summary appears on the left")
        print("   3. Click 'Clear Summary' to reset")
        
        # Run app
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_summary_data(summary_widget):
    """Load test data into summary widget"""
    
    print("🔄 Loading test data into summary widget...")
    
    # Test data
    test_data = {
        'name': 'John Doe (Test)',
        'skills': 'Python, Java, JavaScript, SQL, Machine Learning, Data Analysis',
        'experience': 'Senior Software Developer at Tech Corp (2020-2023)\n• Led team of 5 developers\n• Developed AI-powered applications\n\nSoftware Engineer at StartupXYZ (2018-2020)\n• Built scalable web applications\n• Implemented CI/CD pipelines',
        'education': 'Master of Science in Computer Science\nUniversity of Technology (2016-2018)\n\nBachelor of Computer Science\nState University (2012-2016)',
        'birth_date': '1990-05-15',
        'phone_number': '081234567890',
        'cv_path': 'test/path/to/cv.pdf'
    }
    
    try:
        summary_widget.updateSummary(test_data)
        print("✅ Test data loaded successfully")
    except Exception as e:
        print(f"❌ Error loading test data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_summary_button_simple()
