from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import subprocess
import platform
import os

class CVViewer(QDialog):
    def __init__(self, cvPath, parent=None):
        super().__init__(parent)
        self.cvPath = cvPath
        self.initUI()

    def initUI(self):
        self.setWindowTitle("CV Viewer")
        self.resize(400, 100)
        layout = QVBoxLayout()
        infoLabel = QLabel(f"CV path: {self.cvPath}")
        openButton = QPushButton("Buka CV")
        openButton.clicked.connect(self.openCV)
        layout.addWidget(infoLabel)
        layout.addWidget(openButton)
        self.setLayout(layout)

    def openCV(self):
        try:
            if platform.system() == 'Windows':
                os.startfile(self.cvPath)
            elif platform.system() == 'Darwin':
                subprocess.call(['open', self.cvPath])
            else:
                subprocess.call(['xdg-open', self.cvPath])
        except Exception as e:
            QMessageBox.warning(self, "Gagal Membuka CV", str(e))