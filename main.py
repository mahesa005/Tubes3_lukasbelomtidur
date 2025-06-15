import sys
from pathlib import Path
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow

# tambahkan src ke path
sys.path.append(str(Path(__file__).parent / 'src'))
from utils.Logger import setupLogger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("src/UI/search.ui", self)   # sekarang `self` adalah QMainWindow, cocok dengan .ui

        # hook up the button:
        self.search_button.clicked.connect(self.on_search)
        def on_search(self):
        # Read the keyword line edit:
            keywords = self.keyword_input.text()  
            # Read the current text of the combo box:
            algorithm = self.algo_selector_box.currentText()  
            # Read the top-matches line edit (convert to int if you like):
            top_n_str = self.top_match_input.text()  
            try:
                top_n = int(top_n_str)
            except ValueError:
                top_n = None  # or default to 10, etc.

            # Now you have:
            print("Keywords:", keywords)
            print("Algorithm:", algorithm)
            print("Top N:", top_n)

def load_results(self):
    results = []

def main():
    logger = setupLogger()
    logger.info("Memulai Aplikasi ATS CV Digital")

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
