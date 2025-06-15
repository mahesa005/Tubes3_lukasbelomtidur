#!/usr/bin/env python3
"""
Script untuk testing manual tombol summary dengan GUI minimal
"""

import sys
import os
sys.path.append('.')
sys.path.append('src')

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Import komponen yang diperlukan
from src.gui.ResultWidget import ResultWidget
from src.gui.SummaryWidget import SummaryWidget
from src.services.ATSService import ATSService

class TestSummaryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Summary Button")
        self.setGeometry(100, 100, 1000, 600)
        
        # Service
        self.atsService = ATSService()
        
        # Setup UI
        self.setupUI()
        self.setupConnections()
        
        # Load sample data
        self.loadSampleData()
    
    def setupUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout()
        
        # Left panel: Results
        self.resultWidget = ResultWidget()
        
        # Right panel: Summary  
        self.summaryWidget = SummaryWidget()
        
        layout.addWidget(self.resultWidget, 2)
        layout.addWidget(self.summaryWidget, 1)
        
        central_widget.setLayout(layout)
        
        # Status bar
        self.statusBar().showMessage("Ready - Click 'Ringkasan' button to test")
    
    def setupConnections(self):
        # Connect result selection to summary
        self.resultWidget.resultSelected.connect(self.onResultSelected)
        self.resultWidget.viewCVRequested.connect(self.onViewCVRequested)
        self.summaryWidget.viewCVRequested.connect(self.onViewCVRequested)
    
    def loadSampleData(self):
        """Load sample search results"""
        print("📋 Loading sample data...")
        
        try:
            # Get some real data from database
            result = self.atsService.searchCVs("python", "KMP", 5)
            results = result.get('results', [])
            metadata = result.get('metadata', {})
            
            if results:
                print(f"✅ Loaded {len(results)} sample results")
                self.resultWidget.updateResults(results, metadata)
            else:
                print("⚠️ No results found, creating mock data")
                self.createMockData()
                
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.createMockData()
    
    def createMockData(self):
        """Create mock data for testing"""
        mock_results = [
            {
                'application_id': 1,
                'name': 'Larry Morris',
                'match_score': 85.5,
                'keywords': {'python': 3, 'java': 2},
                'cv_path': 'src\\archive\\data\\data\\FITNESS\\54259150.pdf'
            },
            {
                'application_id': 2,
                'name': 'Test User 2',
                'match_score': 75.2,
                'keywords': {'python': 2, 'leadership': 1},
                'cv_path': 'src\\archive\\data\\data\\AGRICULTURE\\11676151.pdf'
            }
        ]
        
        mock_metadata = {
            'processing_time_ms': 150.0,
            'total_matches': 2
        }
        
        self.resultWidget.updateResults(mock_results, mock_metadata)
        print("✅ Mock data created")
    
    def onResultSelected(self, applicationId):
        """Handle summary button click"""
        try:
            print(f"🔄 Summary button clicked for application_id: {applicationId}")
            self.statusBar().showMessage("Loading summary...")
            
            # Get summary data
            summary_data = self.atsService.getSummary(application_id=applicationId)
            print(f"📋 Got summary data: {summary_data}")
            
            # Convert to dict format
            summary_dict = {
                'name': summary_data.full_name,
                'skills': ', '.join(summary_data.skills),
                'experience': '\n'.join(summary_data.work_experience),
                'education': '\n'.join(summary_data.education),
                'birth_date': summary_data.birth_date,
                'phone_number': summary_data.phone_number,
                'cv_path': summary_data.cv_path
            }
            
            print(f"📄 Converted summary: {summary_dict}")
            
            # Update summary widget
            self.summaryWidget.updateSummary(summary_dict)
            self.statusBar().showMessage("Summary loaded successfully!")
            
            print("✅ Summary updated in widget")
            
        except Exception as e:
            print(f"❌ Error in onResultSelected: {e}")
            import traceback
            traceback.print_exc()
            self.statusBar().showMessage(f"Error: {e}")
    
    def onViewCVRequested(self, cvPath):
        """Handle view CV request"""
        print(f"📄 View CV requested: {cvPath}")
        QMessageBox.information(self, "CV View", f"Would open CV: {cvPath}")

def main():
    print("🧪 Testing Summary Button Functionality")
    print("=" * 50)
    print("Instructions:")
    print("1. Window will show sample search results")
    print("2. Click 'Ringkasan' button on any result")
    print("3. Check if summary appears on the right panel")
    print("4. Watch console for debug messages")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    
    # Apply dark theme
    app.setStyleSheet("""
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
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
        QPushButton {
            background-color: #404040;
            border: 1px solid #555555;
            padding: 5px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QPushButton:pressed {
            background-color: #303030;
        }
    """)
    
    window = TestSummaryWindow()
    window.show()
    
    print("✅ Test window opened - click 'Ringkasan' buttons to test")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
