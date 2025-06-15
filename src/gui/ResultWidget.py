# ===== resultWidget.py =====
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ResultWidget(QWidget):
    resultSelected = pyqtSignal(int)
    viewCVRequested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.searchResults = []
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.scrollArea = QScrollArea()
        self.resultsContainer = QWidget()
        self.resultsLayout = QVBoxLayout()
        self.resultsContainer.setLayout(self.resultsLayout)
        self.scrollArea.setWidget(self.resultsContainer)
        self.scrollArea.setWidgetResizable(True)
        self.layout.addWidget(self.scrollArea)
        self.setLayout(self.layout)

    def updateResults(self, results, searchTime):
        self.clearResults()
        
        if not results:
            noResultLabel = QLabel("Tidak ada hasil ditemukan")
            noResultLabel.setAlignment(Qt.AlignCenter)
            self.resultsLayout.addWidget(noResultLabel)
            return
            
        for result in results:
            card = self.createResultCard(result)
            self.resultsLayout.addWidget(card)
            
        # Tampilkan informasi pencarian
        if isinstance(searchTime, dict):
            processing_time = searchTime.get('processing_time_ms', 0)
            total_matches = searchTime.get('total_matches', 0)
            info_text = f"Ditemukan {total_matches} hasil dalam {processing_time:.1f}ms"
        else:
            info_text = f"Pencarian selesai dalam {searchTime.get('time_ms', 0)}ms"
            
        infoLabel = QLabel(info_text)
        infoLabel.setStyleSheet("font-style: italic; color: gray;")
        self.resultsLayout.addWidget(infoLabel)

    def createResultCard(self, result):
        card = QGroupBox(result.get('name', 'Unknown'))
        layout = QVBoxLayout()

        # Header dengan nama dan score
        headerLayout = QHBoxLayout()
        nameLabel = QLabel(result.get('name', 'Unknown'))
        nameLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        scoreLabel = QLabel(f"Match: {result.get('match_score', 0):.1f}%")
        scoreLabel.setStyleSheet("color: green; font-weight: bold;")
        
        headerLayout.addWidget(nameLabel)
        headerLayout.addStretch()
        headerLayout.addWidget(scoreLabel)
        
        # Keywords yang ditemukan
        keywords = result.get('keywords', {})
        if keywords:
            keywordText = "Keywords: " + ", ".join([f"{k}({v})" for k, v in keywords.items()])
            keywordLabel = QLabel(keywordText)
            keywordLabel.setStyleSheet("font-size: 11px; color: gray;")
            keywordLabel.setWordWrap(True)
        else:
            keywordLabel = QLabel("No keywords matched")
            keywordLabel.setStyleSheet("font-size: 11px; color: gray;")

        # Buttons
        buttonLayout = QHBoxLayout()
        summaryButton = QPushButton("Ringkasan")
        cvButton = QPushButton("Lihat CV")
        
        summaryButton.setMaximumWidth(100)
        cvButton.setMaximumWidth(100)        # Connect buttons dengan data yang benar
        application_id = result.get('application_id')
        cv_path = result.get('cv_path', '')
        
        # Create proper signal connections dengan closure
        def create_summary_handler(app_id):
            def handler():
                print(f"🔔 Ringkasan button clicked for application_id: {app_id}")
                if app_id is not None:
                    self.resultSelected.emit(app_id)
                else:
                    print("❌ application_id is None, cannot emit signal")
            return handler
        
        def create_cv_handler(path):
            def handler():
                print(f"🔔 CV button clicked for path: {path}")
                self.viewCVRequested.emit(path)
            return handler
        
        # Connect buttons dengan proper handlers
        summaryButton.clicked.connect(create_summary_handler(application_id))
        cvButton.clicked.connect(create_cv_handler(cv_path))
        
        # Debug print untuk memastikan data terkirim
        print(f"🔗 ResultWidget: Creating button for application_id={application_id}, cv_path={cv_path}")

        buttonLayout.addWidget(summaryButton)
        buttonLayout.addWidget(cvButton)
        buttonLayout.addStretch()

        # Layout utama card
        layout.addLayout(headerLayout)
        layout.addWidget(keywordLabel)
        layout.addLayout(buttonLayout)
        
        card.setLayout(layout)
        return card

    def clearResults(self):
        for i in reversed(range(self.resultsLayout.count())):
            widget = self.resultsLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
