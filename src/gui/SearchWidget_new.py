from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QRadioButton, QSpinBox, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal

class SearchWidget(QWidget):
    searchRequested = pyqtSignal(list, str, int)

    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setupConnections()

    def setupUI(self):
        layout = QVBoxLayout()

        self.keywordInput = QLineEdit()
        self.keywordInput.setPlaceholderText("Masukkan kata kunci, pisahkan dengan koma")

        self.kmpRadio = QRadioButton("KMP")
        self.bmRadio = QRadioButton("Boyer-Moore")
        self.kmpRadio.setChecked(True)

        algorithmLayout = QHBoxLayout()
        algorithmLayout.addWidget(self.kmpRadio)
        algorithmLayout.addWidget(self.bmRadio)

        self.topMatchesSpin = QSpinBox()
        self.topMatchesSpin.setRange(1, 9999)  # Tingkatkan batas maksimal ke 9999
        self.topMatchesSpin.setValue(5)
        self.topMatchesSpin.setSuffix(" hasil")

        self.searchButton = QPushButton("Cari")

        layout.addWidget(QLabel("Kata Kunci:"))
        layout.addWidget(self.keywordInput)
        layout.addWidget(QLabel("Algoritma:"))
        layout.addLayout(algorithmLayout)
        layout.addWidget(QLabel("Jumlah hasil maksimal:"))
        layout.addWidget(self.topMatchesSpin)
        layout.addWidget(self.searchButton)
        
        self.setLayout(layout)

    def setupConnections(self):
        self.searchButton.clicked.connect(self.onSearchClicked)

    def onSearchClicked(self):
        keywords = [k.strip() for k in self.keywordInput.text().split(',') if k.strip()]
        algorithm = "KMP" if self.kmpRadio.isChecked() else "Boyer-Moore"
        topMatches = self.topMatchesSpin.value()
        self.searchRequested.emit(keywords, algorithm, topMatches)
