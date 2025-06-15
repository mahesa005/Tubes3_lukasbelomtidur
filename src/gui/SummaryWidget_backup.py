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
        self.layout = QVBoxLayout()
        
        # Header
        self.headerLabel = QLabel("Ringkasan CV")
        self.headerLabel.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        self.headerLabel.setAlignment(Qt.AlignCenter)
        
        # Scroll area untuk content
        self.scroll = QScrollArea()
        self.content = QWidget()
        self.contentLayout = QVBoxLayout()
        self.content.setLayout(self.contentLayout)
        self.scroll.setWidget(self.content)
        self.scroll.setWidgetResizable(True)
        
        # Button untuk lihat CV
        self.viewCVBtn = QPushButton("Lihat CV")
        self.viewCVBtn.clicked.connect(lambda: self.viewCVRequested.emit(self.cvPath))
        self.viewCVBtn.setEnabled(False)  # Disabled until we have CV path
          # Layout utama
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.viewCVBtn)
        self.setLayout(self.layout)
        
        # Show initial message
        self.showInitialMessage()

    def showInitialMessage(self):
        """Show initial message when no summary is selected"""
        self.clearSummary()
        initial_label = QLabel("Pilih hasil pencarian untuk melihat ringkasan CV")
        initial_label.setAlignment(Qt.AlignCenter)
        initial_label.setStyleSheet("color: gray; font-style: italic; padding: 20px;")
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
            personal_info = f"Nama: {name}"
            if birth_date:
                personal_info += f"\nTanggal Lahir: {birth_date}"
            if phone_number:
                personal_info += f"\nNo. Telepon: {phone_number}"
            
            self.contentLayout.addWidget(self.createInfoSection("Informasi Personal", personal_info))
            self.contentLayout.addWidget(self.createInfoSection("Keterampilan", skills))
            self.contentLayout.addWidget(self.createInfoSection("Pengalaman Kerja", experience))
            self.contentLayout.addWidget(self.createInfoSection("Pendidikan", education))
            
            # Add CV path info
            if self.cvPath:
                cv_info = f"Path CV: {self.cvPath}"
                self.contentLayout.addWidget(self.createInfoSection("File CV", cv_info))
            
            print(f"✅ SummaryWidget: Summary updated successfully")
            
        except Exception as e:
            print(f"❌ SummaryWidget: Error updating summary: {e}")
            self.showErrorMessage(str(e))

    def showErrorMessage(self, error_msg):
        """Show error message"""
        self.clearSummary()
        error_label = QLabel(f"Error memuat ringkasan: {error_msg}")
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setStyleSheet("color: red; font-style: italic; padding: 20px;")
        self.contentLayout.addWidget(error_label)

    def createInfoSection(self, title, content):
        section = QGroupBox(title)
        layout = QVBoxLayout()
        label = QLabel(content)
        label.setWordWrap(True)
        layout.addWidget(label)
        section.setLayout(layout)
        return section

    def clearSummary(self):
        for i in reversed(range(self.contentLayout.count())):
            widget = self.contentLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)