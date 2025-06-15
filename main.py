import sys
from pathlib import Path
from tkinter import (
    Tk, Frame, Label, Entry, Button, Scrollbar, Canvas,
    StringVar, IntVar, messagebox, Toplevel, LEFT, RIGHT, BOTH, Y, X
)
from tkinter.ttk import Combobox, Spinbox

# Ensure src folder is importable
sys.path.append(str(Path(__file__).parent / "src"))
from config import DATABASE_CONFIG, DATA_DIR
from src.database.connection import DatabaseConnection
from src.database.queries import (
    get_all_cv_paths, get_result_card_by_cv_path, get_summary_data_by_cv_path
)
from src.algorithm.PatternMatcher import PatternMatcher
from src.pdfprocessor.pdfExtractor import PDFExtractor


def main():
    # Connect to DB at startup
    db = DatabaseConnection()
    if not db.connect():
        print("❌ Gagal koneksi ke database. Keluar.")
        sys.exit(1)
    db.useDatabase(DATABASE_CONFIG["database"])

    # Initialize GUI
    root = Tk()
    app = ATSApp(root, db)
    root.mainloop()
    db.disconnect()


class ATSApp:
    def __init__(self, root, db_conn):
        self.root = root
        self.db = db_conn
        self.matcher = PatternMatcher()
        self.extractor = PDFExtractor()

        root.title("ATS - Applicant Tracking System")
        root.geometry("900x750")  # slightly taller for time display

        # Header
        header = Frame(root)
        header.pack(pady=10)
        Label(header, text="ATS - Applicant Tracking System",
              font=("Helvetica", 18, "bold")).pack()
        Label(header, text="CV Digital Pattern Matching System",
              font=("Helvetica", 10)).pack()

        # Search parameters
        params = Frame(root, bd=1, relief="solid", padx=10, pady=10)
        params.pack(fill=X, padx=20, pady=10)

        Label(params, text="Keywords (comma-separated):").grid(row=0, column=0, sticky="w")
        self.keyword_var = StringVar()
        Entry(params, textvariable=self.keyword_var, width=50).grid(row=0, column=1, padx=5)

        Label(params, text="Algorithm:").grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.algo_var = StringVar(value="Knuth-Morris-Pratt (KMP)")
        Combobox(params, textvariable=self.algo_var,
                 values=["Knuth-Morris-Pratt (KMP)", "Boyer-Moore"], width=30
        ).grid(row=1, column=1, sticky="w", padx=5, pady=(5, 0))

        Label(params, text="Top N:").grid(row=2, column=0, sticky="w", pady=(5, 0))
        self.top_n_var = IntVar(value=10)
        Spinbox(params, from_=1, to=100, textvariable=self.top_n_var, width=5
        ).grid(row=2, column=1, sticky="w", padx=5, pady=(5, 0))

        Button(params, text="Search CV", command=self.on_search).grid(
            row=3, column=0, columnspan=2, pady=(10, 0)
        )

        # Time display label
        self.time_var = StringVar(value="")
        Label(root, textvariable=self.time_var, font=("Helvetica", 10, "italic")).pack()

        # Results container
        container = Frame(root)
        container.pack(fill=BOTH, expand=True, padx=20, pady=10)

        self.canvas = Canvas(container)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.results_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        self.results_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # placeholder
        Label(
            self.results_frame,
            text="No search performed yet. Enter keywords and click Search CV.",
            font=("Helvetica", 12)
        ).pack(pady=20)

    def on_search(self):
        # Clear any previous cards
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Collect inputs
        raw_kw = self.keyword_var.get().strip()
        keywords = [k.strip() for k in raw_kw.split(",") if k.strip()]
        algorithm = "KMP" if "KMP" in self.algo_var.get().upper() else "BM"
        top_n = self.top_n_var.get()

        # Fetch all CV paths
        cv_paths = get_all_cv_paths(self.db.connection)

        # accumulate timing
        total_exact_ms = 0.0
        total_fuzzy_ms = 0.0

        # Temporary result list
        result_paths = []

        for path in cv_paths:
            # build absolute path under DATA_DIR
            from pathlib import Path
            rel = Path(path)
            try:
                rel = rel.relative_to("data")
            except Exception:
                pass
            full_pdf = Path(DATA_DIR) / rel
            if not full_pdf.exists():
                continue

            # 1) extract text
            text = self.extractor.PDFExtractForMatch(str(full_pdf))

            # 2) exact match
            exact = self.matcher.exactMatch(text, keywords, algorithm)
            # parse execution time
            ex_ms = float(exact['execution_time_ms'].rstrip('ms'))
            total_exact_ms += ex_ms
            total_exact_count = sum(v['count'] for v in exact['matches'].values())
            if total_exact_count > 0:
                result_paths.append((path, ex_ms, 0.0))
                continue

            # 3) fuzzy fallback
            fuzzy = self.matcher.fuzzyMatch(text, keywords)
            fu_ms = float(fuzzy['execution_time_ms'].rstrip('ms'))
            total_fuzzy_ms += fu_ms
            fu_count = sum(fuzzy['matches'].values())
            if fu_count > 0:
                result_paths.append((path, 0.0, fu_ms))
                continue

        # Display total timings
        self.time_var.set(
            f"Total Exact: {total_exact_ms:.2f}ms   Total Fuzzy: {total_fuzzy_ms:.2f}ms"
        )

        # 4) render result cards
        for path, ex_ms, fu_ms in result_paths[:top_n]:
            card = Frame(self.results_frame, bd=1, relief="raised", padx=10, pady=5)
            card.pack(fill=X, pady=5)

            Label(
                card,
                text=f"{Path(path).name} — Exact: {ex_ms:.2f}ms   Fuzzy: {fu_ms:.2f}ms",
                font=("Helvetica", 12, "bold")
            ).pack(anchor="w")

            btn_frame = Frame(card)
            btn_frame.pack(anchor="e", pady=5)
            Button(
                btn_frame,
                text="Summary",
                command=lambda p=path: self.show_summary(p)
            ).pack(side=LEFT, padx=5)
            Button(
                btn_frame,
                text="View CV",
                command=lambda p=path: self.open_cv(p)
            ).pack(side=LEFT)

    def show_summary(self, cv_path):
        sc = get_summary_data_by_cv_path(self.db.connection, cv_path)
        summary = (
            f"Name            : {sc.full_name}\n"
            f"Date of Birth   : {sc.birth_date}\n"
            f"Phone Number    : {sc.phone_number}\n"
            f"Applied Role    : {sc.application_role}\n"
        )
        win = Toplevel(self.root)
        win.title("Applicant Summary")
        Label(win, text=summary, justify="left", font=("Helvetica", 10)).pack(padx=10, pady=10)

    def open_cv(self, cv_path):
        import os, webbrowser
        full = Path(DATA_DIR) / Path(cv_path).relative_to("data")
        if full.exists():
            webbrowser.open_new(r"file://" + str(full.resolve()))
        else:
            messagebox.showerror("File Not Found", f"CV file not found: {full}")
            
if __name__ == "__main__":
    main()