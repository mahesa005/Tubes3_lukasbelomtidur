# ===== src/gui/resultWidget.py =====
"""
Widget Hasil untuk menampilkan hasil pencarian CV
Tujuan: Menampilkan hasil pencarian dalam format yang mudah dibaca pengguna
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ResultWidget(QWidget):
    """
    Widget untuk menampilkan hasil pencarian CV
    
    Sinyal:
        resultSelected: Dipicu ketika pengguna memilih salah satu hasil
        viewCVRequested: Dipicu ketika pengguna ingin melihat CV asli
        
    TODO:
    - Desain layout untuk menampilkan hasil
    - Tampilkan jumlah kecocokan dan highlight keyword
    - Sediakan aksi (Ringkasan, Lihat CV)
    - Tangani sorting dan filtering
    """
    
    resultSelected = pyqtSignal(int)  # application_id
    viewCVRequested = pyqtSignal(str)  # cv_path
    
    def __init__(self):
        """Inisialisasi widget hasil"""
        super().__init__()
        self.searchResults = []
        self.initUI()
    
    def initUI(self):
        """
        Inisialisasi antarmuka pengguna
        
        TODO:
        - Buat layout untuk hasil
        - Tambahkan kartu/item hasil pencarian
        - Sertakan area scroll untuk banyak hasil
        - Tambahkan opsi sorting
        """
        pass
    
    def updateResults(self, results, searchTime):
        """
        Perbarui tampilan hasil pencarian
        
        Argumen:
            results (list): Daftar hasil pencarian
            searchTime (dict): Dictionary dengan waktu eksekusi
            
        TODO:
        - Bersihkan hasil sebelumnya
        - Buat kartu hasil untuk setiap hasil
        - Tampilkan informasi waktu pencarian
        - Urutkan berdasarkan relevansi kecocokan
        """
        pass
    
    def createResultCard(self, result):
        """
        Buat kartu untuk satu hasil pencarian
        
        Argumen:
            result (dict): Data hasil pencarian
            
        Return:
            QWidget: Widget kartu untuk hasil
            
        TODO:
        - Desain layout kartu
        - Tampilkan nama pelamar
        - Tampilkan jumlah kecocokan dan keyword
        - Tambahkan tombol Ringkasan dan Lihat CV
        """
        pass
    
    def onSummaryClicked(self, applicationId):
        """
        Tangani klik tombol Ringkasan
        
        Argumen:
            applicationId (int): ID aplikasi
        """
        pass
    
    def onViewCVClicked(self, cvPath):
        """
        Tangani klik tombol Lihat CV
        
        Argumen:
            cvPath (str): Path ke file CV
        """
        pass
    
    def clearResults(self):
        """Bersihkan semua hasil pencarian"""
        pass