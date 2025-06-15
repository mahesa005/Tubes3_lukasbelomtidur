# ===== summaryWidget.py =====
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SummaryWidget(QWidget):
    viewCVRequested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.cvPath = ""  # Initialize cvPath
        self.initUI()

    def initUI(self):
        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Header
        self.headerLabel = QLabel("Ringkasan CV")
        self.headerLabel.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; background-color: #404040; border-radius: 5px;")
        self.headerLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.headerLabel)
        
        # Scroll area untuk content
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: 1px solid #555555; border-radius: 5px;")
        
        self.content = QWidget()
        self.contentLayout = QVBoxLayout()
        self.content.setLayout(self.contentLayout)
        self.scroll.setWidget(self.content)
        
        self.layout.addWidget(self.scroll)
        
        # Button untuk lihat CV
        self.viewCVBtn = QPushButton("Lihat CV")
        self.viewCVBtn.clicked.connect(lambda: self.viewCVRequested.emit(self.cvPath))
        self.viewCVBtn.setEnabled(False)  # Disabled until we have CV path
        self.viewCVBtn.setStyleSheet("QPushButton { padding: 8px; font-weight: bold; }")
        self.layout.addWidget(self.viewCVBtn)
        
        # Show initial message
        self.showInitialMessage()

    def showInitialMessage(self):
        """Show initial message when no summary is selected"""
        self.clearSummary()
        initial_label = QLabel("📋 Pilih hasil pencarian untuk melihat ringkasan CV")
        initial_label.setAlignment(Qt.AlignCenter)
        initial_label.setStyleSheet("color: gray; font-style: italic; padding: 40px; font-size: 14px;")
        initial_label.setWordWrap(True)
        self.contentLayout.addWidget(initial_label)

    def updateSummary(self, applicationData):
        """Update summary with application data"""
        try:
            print(f"🔄 SummaryWidget: Updating summary with data: {applicationData}")
            
            # Set CV path dan enable button jika ada path
            self.cvPath = applicationData.get('cv_path', '')
            self.viewCVBtn.setEnabled(bool(self.cvPath))
            
            # Clear existing content
            self.clearSummary()
            
            # Add sections dengan data yang ada
            name = applicationData.get('name', 'Tidak diketahui')
            skills = applicationData.get('skills', 'Tidak ada data keterampilan')
            experience = applicationData.get('experience', 'Tidak ada data pengalaman')
            education = applicationData.get('education', 'Tidak ada data pendidikan')
            birth_date = applicationData.get('birth_date', '')
            phone_number = applicationData.get('phone_number', '')
            
            # Section Informasi Personal
            personal_info = f"👤 {name}"
            if birth_date:
                personal_info += f"\n📅 Tanggal Lahir: {birth_date}"
            if phone_number:
                personal_info += f"\n📞 No. Telepon: {phone_number}"
            
            self.contentLayout.addWidget(self.createInfoSection("Informasi Personal", personal_info))
            self.contentLayout.addWidget(self.createInfoSection("🛠️ Keterampilan", skills))
            self.contentLayout.addWidget(self.createInfoSection("💼 Pengalaman Kerja", experience))
            self.contentLayout.addWidget(self.createInfoSection("🎓 Pendidikan", education))
            
            # Add CV path info
            if self.cvPath:
                cv_info = f"📁 {self.cvPath}"
                self.contentLayout.addWidget(self.createInfoSection("File CV", cv_info))
            
            # Add stretch to push content to top
            self.contentLayout.addStretch()
            
            print(f"✅ SummaryWidget: Summary updated successfully")
            
        except Exception as e:
            print(f"❌ SummaryWidget: Error updating summary: {e}")
            import traceback
            traceback.print_exc()
            self.showErrorMessage(str(e))

    def showErrorMessage(self, error_msg):
        """Show error message"""
        self.clearSummary()
        error_label = QLabel(f"❌ Error memuat ringkasan:\n{error_msg}")
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setStyleSheet("color: red; font-style: italic; padding: 20px; font-size: 12px;")
        error_label.setWordWrap(True)
        self.contentLayout.addWidget(error_label)

    def createInfoSection(self, title, content):
        """Create an info section with title and content"""
        section = QGroupBox(title)
        section.setStyleSheet("""
            QGroupBox {
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #ffffff;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout()
        label = QLabel(str(content))
        label.setWordWrap(True)
        label.setStyleSheet("padding: 10px; font-weight: normal; line-height: 1.4;")
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Allow text selection
        layout.addWidget(label)
        section.setLayout(layout)
        return section

    def clearSummary(self):
        """Clear all content from summary"""
        for i in reversed(range(self.contentLayout.count())):
            item = self.contentLayout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None)
