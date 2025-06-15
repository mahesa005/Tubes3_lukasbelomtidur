from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from ..src.gui.SearchWidget import SearchWidget
from ..src.gui.ResultWidget import ResultWidget
from ..src.gui.SummaryWidget import SummaryWidget
from ..src.gui.CVViewer import CVViewer
from ..src.gui.styles import applyTheme
from ..src.services.ATSService import ATSService
import sys

class SearchWorker(QThread):
    """Thread worker untuk pencarian CV agar tidak memblokir UI"""
    searchCompleted = pyqtSignal(dict)
    searchError = pyqtSignal(str)
    
    def __init__(self, keywords, algorithm, topMatches):
        super().__init__()
        self.keywords = keywords
        self.algorithm = algorithm
        self.topMatches = topMatches
        self.atsService = ATSService()
    
    def run(self):
        try:
            result = self.atsService.searchCVs(
                self.keywords, 
                self.algorithm, 
                self.topMatches
            )
            self.searchCompleted.emit(result)
        except Exception as e:
            self.searchError.emit(str(e))


class MainWindow(QMainWindow):    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ATS CV Matcher")
        self.setMinimumSize(1024, 768)
        self.atsService = ATSService()
        self.searchWorker = None
        self.initUI()
        self.setupConnections()

    def initUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.searchWidget = SearchWidget()
        self.resultWidget = ResultWidget()
        self.summaryWidget = SummaryWidget()

        splitter = QSplitter(Qt.Horizontal)
        leftPanel = QWidget()
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.searchWidget)
        leftLayout.addWidget(self.resultWidget)
        leftPanel.setLayout(leftLayout)

        splitter.addWidget(leftPanel)
        splitter.addWidget(self.summaryWidget)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        layout = QHBoxLayout()
        layout.addWidget(splitter)
        centralWidget.setLayout(layout)

        self.statusBar().showMessage("Ready")

    def setupConnections(self):
        self.searchWidget.searchRequested.connect(self.onSearchRequested)
        self.resultWidget.resultSelected.connect(self.onResultSelected)
        self.resultWidget.viewCVRequested.connect(self.onViewCVRequested)
        self.summaryWidget.viewCVRequested.connect(self.onViewCVRequested)

    def onSearchRequested(self, keywords, algorithm, topMatches):
        # Integrasi logika pencarian kamu di sini
        # Simulasi hasil pencarian:
        mockResults = [
            {"application_id": 1, "name": "John Doe", "match_score": 87, "keywords": keywords, "cv_path": "cv/john_doe.pdf"},
            {"application_id": 2, "name": "Jane Smith", "match_score": 73, "keywords": keywords, "cv_path": "cv/jane_smith.pdf"}
        ]
        self.resultWidget.updateResults(mockResults, {"time_ms": 12})

    def onResultSelected(self, applicationId):
        # Integrasi logika pemanggilan ringkasan
        # Simulasi ringkasan:
        summary = {
            "name": "John Doe",
            "summary": "Experienced developer with Python & ML background.",
            "skills": "Python, Machine Learning, PyQt",
            "education": "B.Sc. in Computer Science",
            "experience": "5 years as Software Engineer"
        }
        self.summaryWidget.updateSummary(summary)

    def onViewCVRequested(self, cvPath):
        viewer = CVViewer(cvPath)
        viewer.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    applyTheme(app, 'dark')  # or 'light'
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
