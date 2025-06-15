import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from .SearchWidget import SearchWidget
from .ResultWidget import ResultWidget
from .SummaryWidget import SummaryWidget
from .CVViewer import CVViewer
from .styles import applyTheme
from src.services.ATSService import ATSService


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
        """Handler untuk request pencarian CV"""
        if self.searchWorker and self.searchWorker.isRunning():
            return
        
        self.statusBar().showMessage("Mencari CV...")
        self.searchWorker = SearchWorker(keywords, algorithm, topMatches)
        self.searchWorker.searchCompleted.connect(self.onSearchCompleted)
        self.searchWorker.searchError.connect(self.onSearchError)
        self.searchWorker.start()

    def onSearchCompleted(self, result):
        """Handler ketika pencarian selesai"""
        try:
            results = result.get('results', [])
            metadata = result.get('metadata', {})
            
            self.resultWidget.updateResults(results, metadata)
            
            processing_time = metadata.get('processing_time_ms', 0)
            total_matches = metadata.get('total_matches', 0)
            self.statusBar().showMessage(
                f"Pencarian selesai: {total_matches} hasil ditemukan dalam {processing_time:.1f}ms"
            )        except Exception as e:
            self.onSearchError(str(e))

    def onSearchError(self, error_msg):
        """Handler ketika terjadi error dalam pencarian"""
        QMessageBox.warning(self, "Error Pencarian", f"Terjadi error: {error_msg}")
        self.statusBar().showMessage("Error dalam pencarian")

    def onResultSelected(self, applicationId):
        """Handler ketika hasil dipilih untuk melihat ringkasan"""
        try:
            print(f"🔄 MainWindow: Result selected with application_id: {applicationId}")
            self.statusBar().showMessage("Mengambil ringkasan...")
            
            # Gunakan application_id untuk mendapatkan summary
            summary_data = self.atsService.getSummary(application_id=applicationId)
            print(f"📋 MainWindow: Got summary data: {summary_data}")
            
            # Convert SummaryData ke format yang diharapkan widget
            summary_dict = {
                'name': summary_data.full_name,
                'skills': ', '.join(summary_data.skills),
                'experience': '\n'.join(summary_data.work_experience),
                'education': '\n'.join(summary_data.education),
                'birth_date': summary_data.birth_date,
                'phone_number': summary_data.phone_number,
                'cv_path': summary_data.cv_path
            }
            
            print(f"📄 MainWindow: Converted to dict: {summary_dict}")
            
            self.summaryWidget.updateSummary(summary_dict)
            self.statusBar().showMessage("Ringkasan berhasil dimuat")
            
        except Exception as e:
            print(f"❌ MainWindow: Error in onResultSelected: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self, "Error", f"Gagal memuat ringkasan: {e}")
            self.statusBar().showMessage("Error memuat ringkasan")

    def onViewCVRequested(self, cvPath):
        """Handler untuk membuka CV viewer"""
        try:
            if not cvPath:
                QMessageBox.warning(self, "Error", "Path CV tidak valid")
                return
            
            viewer = CVViewer(cvPath, self)
            viewer.exec_()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Gagal membuka CV: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    applyTheme(app, 'dark')  # or 'light'
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
