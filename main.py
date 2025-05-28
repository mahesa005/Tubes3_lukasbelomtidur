import sys
import os
from pathlib import Path

# Tambahkan direktori src ke path Python
sys.path.append(str(Path(__file__).parent / 'src'))

from PyQt5.QtWidgets import QApplication
from gui.MainWindow import MainWindow
from utils.logger import setupLogger

def main():
    """
    Fungsi utama untuk memulai aplikasi ATS

    TODO:
    - Inisialisasi sistem logging
    - Membuat instance QApplication
    - Inisialisasi dan tampilkan main window
    - Menangani keluar aplikasi
    """

    # Inisialisasi logging
    logger = setupLogger()
    logger.info("Memulai Aplikasi ATS CV Digital")

    try:
        # Membuat aplikasi Qt
        #ok
        app = QApplication(sys.argv)

        # Membuat dan menampilkan main window
        mainWindow = MainWindow()
        mainWindow.show()

        # Memulai event loop
        sys.exit(app.exec_())

    except Exception as e:
        logger.error(f"Terjadi error saat memulai aplikasi: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()