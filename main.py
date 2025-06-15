from PyQt5.QtWidgets import QApplication
import sys
from src.gui.MainWindow import MainWindow
from src.gui.styles import applyTheme


def main():
    app = QApplication(sys.argv)

    # Terapkan tema dark yang modern
    applyTheme(app, theme='dark')

    # Buat dan tampilkan jendela utama
    window = MainWindow()
    window.setWindowTitle("CV Matcher - ATS System")
    window.resize(1000, 700)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
