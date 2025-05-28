# ===== src/gui/cvViewer.py =====
"""
CV Viewer untuk menampilkan file CV asli
Tujuan: Viewer untuk membuka dan menampilkan file PDF CV
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import subprocess
import os
import platform

class CVViewer(QDialog):
    """
    Dialog untuk melihat CV asli

    TODO:
    - Implementasi PDF viewer atau peluncur aplikasi eksternal
    - Menangani berbagai OS (Windows, Mac, Linux)
    - Memberikan fallback jika PDF viewer tidak tersedia
    - Tambahkan penanganan error
    """

    def __init__(self, cvPath, parent=None):
        """
        Inisialisasi CV viewer

        Argumen:
            cvPath (str): Path ke file CV
            parent (QWidget): Parent widget
        """
        super().__init__(parent)
        self.cvPath = cvPath
        self.initUI()

    def initUI(self):
        """
        Inisialisasi antarmuka pengguna

        TODO:
        - Atur properti dialog
        - Buat layout
        - Tambahkan kontrol (tombol Tutup, dll)
        - Coba buka CV
        """
        pass

    def openCV(self):
        """
        Buka file CV dengan aplikasi default

        TODO:
        - Deteksi OS
        - Gunakan perintah yang sesuai untuk membuka PDF
        - Tangani file tidak ditemukan
        - Tangani jika tidak ada PDF viewer terpasang
        """
        pass

    def openWithDefaultApp(self, filePath):
        """
        Buka file dengan aplikasi default OS

        Argumen:
            filePath (str): Path ke file

        Return:
            bool: True jika berhasil membuka
        """
        pass