# main.py
import sys
from pathlib import Path
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox,
    QFrame, QLabel, QPushButton, QVBoxLayout
)
import pdb

sys.path.append(str(Path(__file__).parent / "src"))

from config                       import DATABASE_CONFIG
from src.database.connection     import DatabaseConnection
from src.database.queries        import get_all_cv_paths, get_result_card_by_cv_path
from src.algorithm.PatternMatcher import PatternMatcher


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("src/UI/search.ui", self)

        # don’t connect yet
        self.db      = None
        self.matcher = PatternMatcher()

        # wire the button
        self.search_button.clicked.connect(self.on_search)

    def on_search(self):
        print("[DEBUG] on_search fired")

        # 1) ensure we have a live DB connection
        if self.db is None:
            print("[DEBUG] self.db is None → creating new DatabaseConnection()")
            self.db = DatabaseConnection()
            ok = self.db.connect()
            print(f"[DEBUG] db.connect() returned {ok}")
            if not ok:
                QMessageBox.critical(self, "DB Error", "Gagal terhubung ke database.")
                return
            used = self.db.useDatabase(DATABASE_CONFIG["database"])
            print(f"[DEBUG] db.useDatabase(...) returned {used}")
        # 2) read user input
        raw_kw   = self.keyword_input.text()
        keywords = [k.strip() for k in raw_kw.split(",") if k.strip()]
        algo     = self.algo_selector_box.currentText()
        try:
            top_n = int(self.top_match_input.text())
        except ValueError:
            top_n = 10

        # 3) fetch CV paths and score
        cv_paths = get_all_cv_paths(self.db.connection)
        scored   = []
        for p in cv_paths:
            text  = self.matcher.load_text(p)
            score = self.matcher.score(text, keywords, algorithm=algo)
            scored.append((score, p))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:top_n]

        # 4) clear old results
        layout = self.result_frame.layout()
        for i in reversed(range(layout.count())):
            w = layout.itemAt(i).widget()
            if w:
                w.setParent(None)

        # 5) render new cards
        for score, path in top:
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            v    = QVBoxLayout(card)

            rc = get_result_card_by_cv_path(self.db.connection, path)
            v.addWidget(QLabel(f"{rc.full_name} — Score: {score:.2f}"))

            btn = QPushButton("Summary")
            btn.clicked.connect(lambda _, p=path: self.show_summary(p))
            v.addWidget(btn)

            layout.addWidget(card)

    def show_summary(self, cv_path):
        # …fetch + show summary similarly…
        pass


def main():
    app    = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
