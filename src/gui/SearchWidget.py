"""
Widget Pencarian untuk input kata kunci dan pemilihan algoritma
Tujuan: Menyediakan antarmuka pencarian untuk pencocokan CV
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SearchWidget(QWidget):
    """
    Widget antarmuka pencarian
    
    Sinyal:
        searchRequested: Dipancarkan saat pencarian diminta
        
    TODO:
    - Membuat field input kata kunci
    - Menambahkan pemilihan algoritma (KMP/Boyer-Moore)
    - Menambahkan selector jumlah hasil teratas
    - Menyertakan tombol pencarian
    """
    
    searchRequested = pyqtSignal(list, str, int)  # keywords, algorithm, topMatches
    
    def __init__(self):
        """Inisialisasi widget pencarian"""
        super().__init__()
        self.initUI()
        self.setupConnections()
    
    def initUI(self):
        """
        Inisialisasi antarmuka pengguna
        
        TODO:
        - Membuat layout dengan semua komponen
        - Menambahkan input kata kunci (QLineEdit)
        - Menambahkan radio button algoritma
        - Menambahkan spinner jumlah hasil teratas
        - Menambahkan tombol pencarian
        - Memberi gaya pada komponen
        """
        pass
    
    def setupConnections(self):
        """Mengatur koneksi widget"""
        pass
    
    def onSearchClicked(self):
        """
        Menangani klik tombol pencarian
        
        TODO:
        - Validasi input
        - Parsing kata kunci (dipisahkan koma)
        - Mendapatkan algoritma yang dipilih
        - Mendapatkan jumlah hasil teratas
        - Memancarkan sinyal searchRequested
        """
        pass
    
    def clearSearch(self):
        """Menghapus input pencarian"""
        pass