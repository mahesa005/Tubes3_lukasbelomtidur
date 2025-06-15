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
        self.setLayout(self.layout)    def updateResults(self, results, searchTime):
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
        card = QGroupBox(result['name'])
        layout = QHBoxLayout()

        matchLabel = QLabel(f"Match: {result.get('match', 0)}%")
        summaryButton = QPushButton("Ringkasan")
        cvButton = QPushButton("Lihat CV")

        summaryButton.clicked.connect(lambda: self.resultSelected.emit(result.get('id', None)))
        cvButton.clicked.connect(lambda: self.viewCVRequested.emit(result['cv_path']))

        layout.addWidget(matchLabel)
        layout.addWidget(summaryButton)
        layout.addWidget(cvButton)
        card.setLayout(layout)
        return card

    def clearResults(self):
        for i in reversed(range(self.resultsLayout.count())):
            widget = self.resultsLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)