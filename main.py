import sys
import time
import webbrowser
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tkinter import (
    Tk, Frame, Label, Entry, Button, Scale,
    Scrollbar, Canvas, StringVar, IntVar,
    messagebox, Toplevel, LEFT, RIGHT, BOTH, Y, X, HORIZONTAL
)
from tkinter.ttk import Combobox, Spinbox

# ensure your src folder is on the import path
sys.path.append(str(Path(__file__).parent / "src"))

from config import DATABASE_CONFIG, DATA_DIR
from src.database.connection import DatabaseConnection
from src.database.queries import (
    get_all_cv_paths, get_summary_data_by_cv_path
)
from src.models.ResultCard import ResultCard
from src.algorithm.PatternMatcher import PatternMatcher
from src.pdfprocessor.pdfExtractor import PDFExtractor


class ATSApp:
    def __init__(self, root, db_conn):
        self.root      = root
        self.db        = db_conn
        self.matcher   = PatternMatcher()
        self.extractor = PDFExtractor()
        self.cache     = {}   # { cv_path: cleansed_text }
        
        root.title("ATS - Applicant Tracking System")
        root.geometry("900x750")

        self._build_ui()
        self._preload_all_cvs()

    def _build_ui(self):
        # --- Header ---
        hdr = Frame(self.root)
        hdr.pack(pady=10)
        Label(hdr, text="ATS - Applicant Tracking System",
              font=("Helvetica",18,"bold")
        ).pack()
        Label(hdr, text="CV Digital Pattern Matching System",
              font=("Helvetica",10)
        ).pack()

        # --- Search Controls ---
        params = Frame(self.root, bd=1, relief="solid", padx=10, pady=10)
        params.pack(fill=X, padx=20, pady=10)

        # Keywords
        Label(params, text="Keywords (comma-sep):").grid(row=0, column=0, sticky="w")
        self.keyword_var = StringVar()
        Entry(params, textvariable=self.keyword_var, width=50).grid(row=0, column=1, padx=5)

        # Algorithm
        Label(params, text="Algorithm:").grid(row=1, column=0, sticky="w", pady=(5,0))
        self.algo_var = StringVar(value="Knuth-Morris-Pratt (KMP)")
        Combobox(params, textvariable=self.algo_var,
                 values=["Knuth-Morris-Pratt (KMP)","Boyer-Moore"],
                 width=30
        ).grid(row=1, column=1, padx=5, pady=(5,0), sticky="w")

        # Top N
        Label(params, text="Top N:").grid(row=2, column=0, sticky="w", pady=(5,0))
        self.top_n_var = IntVar(value=10)
        Spinbox(params, from_=1, to=100, textvariable=self.top_n_var,
                width=5
        ).grid(row=2, column=1, padx=5, pady=(5,0), sticky="w")

        # Fuzzy threshold slider
        Label(params, text="Fuzzy Threshold (%):").grid(row=3, column=0, sticky="w", pady=(5,0))
        self.thresh_var = IntVar(value=70)
        Scale(params, from_=0, to=100, variable=self.thresh_var,
              orient=HORIZONTAL, length=200
        ).grid(row=3, column=1, padx=5, sticky="w", pady=(5,0))

        # Search button
        Button(params, text="Search CV", command=self.on_search
        ).grid(row=4, column=0, columnspan=2, pady=(10,0))

        # timing display
        self.time_var = StringVar()
        Label(self.root, textvariable=self.time_var,
              font=("Helvetica",10,"italic")
        ).pack()

        # --- Results Area (scrollable) ---
        container = Frame(self.root)
        container.pack(fill=BOTH, expand=True, padx=20, pady=10)
        self.canvas = Canvas(container)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.results_frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.results_frame, anchor="nw")
        # auto-scrollregion
        self.results_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        Label(
            self.results_frame,
            text="No search performed yet.\nEnter keywords and click Search CV.",
            font=("Helvetica",12),
            justify="center"
        ).pack(pady=20)

    def _preload_all_cvs(self):
        """
        One-time PDF→text extraction & cleaning.
        """
        cv_paths = get_all_cv_paths(self.db.connection)
        if not cv_paths:
            print("[WARN] No CVs found in database.")
            return

        print(f"[INFO] Preloading {len(cv_paths)} CVs…")
        start = time.time()
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = {
                pool.submit(
                    self.extractor.PDFExtractForMatch,
                    str((Path(DATA_DIR)/Path(p).relative_to("data")).resolve())
                ): p
                for p in cv_paths
            }
            for fut in as_completed(futures):
                p = futures[fut]
                try:
                    self.cache[p] = fut.result()
                except Exception as err:
                    print(f"[ERROR] {p} → {err}")
                    self.cache[p] = ""

        elapsed = (time.time()-start)*1000
        print(f"[INFO] Done preloading in {elapsed:.1f} ms")

    def on_search(self):
        # clear previous
        for w in self.results_frame.winfo_children():
            w.destroy()

        # inputs
        kws      = [k.strip() for k in self.keyword_var.get().split(",") if k.strip()]
        algo     = "KMP" if "KMP" in self.algo_var.get().upper() else "BM"
        top_n    = self.top_n_var.get()
        threshold= self.thresh_var.get() / 100.0

        total_ex, total_fu = 0.0, 0.0
        hits = []

        # for each cached CV text
        for path, txt in self.cache.items():
            # exact
            ex = self.matcher.exactMatch(txt, kws, algorithm=algo)
            # build exact dict
            exact_kw = {kw:info["count"] for kw,info in ex["matches"].items() if info["count"]>0}
            ex_total = sum(exact_kw.values())
            total_ex += float(ex.get("execution_time_ms","0ms").rstrip("ms"))

            if ex_total>0:
                score = ex_total*1000    # ensures exact hits always outrank fuzzy
                hits.append((path, exact_kw, ex_total, score))
                continue

            # fuzzy fallback
            fu = self.matcher.fuzzyMatch(txt, kws, threshold=threshold)
            fuzzy_kw = fu["matches"]
            fu_total = sum(fuzzy_kw.values())
            total_fu += float(fu.get("execution_time_ms","0ms").rstrip("ms"))

            if fu_total>0:
                score = fu_total
                hits.append((path, fuzzy_kw, fu_total, score))

        # show timing
        self.time_var.set(
            f"Exact total: {total_ex:.1f} ms   Fuzzy total: {total_fu:.1f} ms"
        )

        # sort by composite score desc
        hits.sort(key=lambda x: x[3], reverse=True)

        # render top N
        for path, kwmap, total, score in hits[:top_n]:
            # get name from DB
            sc = get_summary_data_by_cv_path(self.db.connection, path)
            rc = ResultCard(
                full_name       = sc.full_name,
                cv_path         = path,
                matched_keywords= kwmap,
                total_matches   = total
            )

            # wide result card
            card = Frame(self.results_frame, bd=1, relief="raised", padx=15, pady=10)
            card.pack(fill=X, pady=5, padx=5)

            # name header
            Label(card, text=rc.full_name,
                  font=("Helvetica",14,"bold")
            ).pack(anchor="w")

            # matches line
            if rc.matched_keywords:
                items = [f"{k}({v})" for k,v in rc.matched_keywords.items()]
                Label(card,
                      text="Matches: " + ", ".join(items),
                      font=("Helvetica",10),
                      wraplength=800
                ).pack(anchor="w", pady=(4,0), padx=(5,0))
            else:
                Label(card,
                      text="No matches",
                      font=("Helvetica",10,"italic")
                ).pack(anchor="w", pady=(4,0), padx=(5,0))

            # total
            Label(card,
                  text=f"Total: {rc.total_matches}",
                  font=("Helvetica",9)
            ).pack(anchor="w", padx=(5,0), pady=(2,0))

            # action buttons
            btns = Frame(card)
            btns.pack(anchor="e", pady=(8,0))
            Button(btns, text="Summary",
                   command=lambda p=path: self.show_summary(p)
            ).pack(side=LEFT, padx=5)
            Button(btns, text="View CV",
                   command=lambda p=path: self.open_cv(p)
            ).pack(side=LEFT)

    def show_summary(self, cv_path):
        sc = get_summary_data_by_cv_path(self.db.connection, cv_path)
        text = (
            f"Name          : {sc.full_name}\n"
            f"Date of Birth : {sc.birth_date}\n"
            f"Phone Number  : {sc.phone_number}\n"
            f"Applied Role  : {sc.application_role}"
        )
        win = Toplevel(self.root)
        win.title("Applicant Summary")
        Label(win, text=text, justify="left", font=("Helvetica",10)).pack(padx=10, pady=10)

    def open_cv(self, cv_path):
        full = Path(DATA_DIR)/Path(cv_path).relative_to("data")
        if full.exists():
            webbrowser.open_new(f"file://{full.resolve()}")
        else:
            messagebox.showerror("File Not Found", f"CV not found:\n{full}")


def main():
    db = DatabaseConnection()
    if not db.connect():
        print("❌ Gagal koneksi ke database.")
        sys.exit(1)
    db.useDatabase(DATABASE_CONFIG["database"])

    root = Tk()
    ATSApp(root, db)
    root.mainloop()

    db.disconnect()


if __name__ == "__main__":
    main()
