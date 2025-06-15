import sys
import time
import webbrowser
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from tkinter import (
    Tk, Frame, Label, Entry, Button, Scale,
    Scrollbar, Canvas, StringVar, IntVar,
    messagebox, Toplevel, LEFT, RIGHT, BOTH, Y, X, W, HORIZONTAL, TOP, BOTTOM
)
from tkinter.ttk import Combobox, Spinbox

# ensure src folder is importable
sys.path.append(str(Path(__file__).parent / "src"))

from config import DATABASE_CONFIG, DATA_DIR
from src.database.connection import DatabaseConnection
from src.database.queries import get_all_cv_paths, get_summary_data_by_cv_path
from src.models.ResultCard import ResultCard
from src.algorithm.PatternMatcher import PatternMatcher
from src.pdfprocessor.pdfExtractor import PDFExtractor

# How many to load/test
MAX_CV_LOAD = 100


class ATSApp:
    def __init__(self, root, db_conn):
        self.root      = root
        self.db        = db_conn
        self.matcher   = PatternMatcher()
        self.extractor = PDFExtractor()
        self.cache     = {}

        root.title("ATS - Applicant Tracking System")
        root.geometry("900x750")

        self._build_ui()
        self._preload_all_cvs()

    def _build_ui(self):
        hdr = Frame(self.root); hdr.pack(pady=10)
        Label(hdr, text="ATS - Applicant Tracking System",
              font=("Helvetica",18,"bold")).pack()
        Label(hdr, text="CV Digital Pattern Matching System",
              font=("Helvetica",10)).pack()

        params = Frame(self.root, bd=1, relief="solid", padx=10, pady=10)
        params.pack(fill=X, padx=20, pady=10)

        Label(params, text="Keywords (comma-separated):").grid(row=0, column=0, sticky="w")
        self.keyword_var = StringVar()
        Entry(params, textvariable=self.keyword_var, width=50).grid(row=0, column=1, padx=5)

        Label(params, text="Algorithm:").grid(row=1, column=0, sticky="w", pady=(5,0))
        self.algo_var = StringVar(value="Knuth-Morris-Pratt (KMP)")
        Combobox(params, textvariable=self.algo_var,
                 values=["Knuth-Morris-Pratt (KMP)", "Boyer-Moore"], width=30)\
            .grid(row=1, column=1, padx=5, pady=(5,0), sticky="w")

        Label(params, text="Top N:").grid(row=2, column=0, sticky="w", pady=(5,0))
        self.top_n_var = IntVar(value=10)
        Spinbox(params, from_=1, to=100, textvariable=self.top_n_var, width=5)\
            .grid(row=2, column=1, padx=5, pady=(5,0), sticky="w")

        Label(params, text="Fuzzy Threshold (%):").grid(row=3, column=0, sticky="w", pady=(5,0))
        self.thresh_var = IntVar(value=70)
        Scale(params, from_=0, to=100, variable=self.thresh_var,
              orient=HORIZONTAL, length=200)\
            .grid(row=3, column=1, padx=5, pady=(5,0), sticky="w")

        Button(params, text="Search CV", command=self.on_search)\
            .grid(row=4, column=0, columnspan=2, pady=(10,0))

        self.time_var = StringVar()
        Label(self.root, textvariable=self.time_var,
              font=("Helvetica",10,"italic")).pack()

        container = Frame(self.root); container.pack(fill=BOTH, expand=True, padx=20, pady=10)
        self.canvas = Canvas(container, width=850)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        sb = Scrollbar(container, orient="vertical", command=self.canvas.yview)
        sb.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=sb.set)

        self.results_frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.results_frame, anchor="nw")
        self.results_frame.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        Label(self.results_frame,
              text="No search performed yet.\nEnter keywords and click Search CV.",
              font=("Helvetica",12), justify="center")\
            .pack(pady=20)


    def _preload_all_cvs(self):
        all_paths = get_all_cv_paths(self.db.connection)
        paths = all_paths[:MAX_CV_LOAD]
        print(f"[INFO] Preloading {len(paths)} CVs… (limited to {MAX_CV_LOAD})")
        start = time.time()
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = {
                pool.submit(
                    self.extractor.PDFExtractForMatch,
                    str((Path(DATA_DIR)/Path(p).relative_to("data")).resolve())
                ): p
                for p in paths
            }
            for fut in as_completed(futures):
                p = futures[fut]
                try:
                    self.cache[p] = fut.result()
                except Exception:
                    self.cache[p] = ""
        elapsed = (time.time()-start)*1000
        print(f"[INFO] Done preloading in {elapsed:.1f} ms")


    def on_search(self):
        for w in self.results_frame.winfo_children():
            w.destroy()

        kws       = [k.strip() for k in self.keyword_var.get().split(",") if k.strip()]
        algo      = "KMP" if "KMP" in self.algo_var.get().upper() else "BM"
        top_n     = self.top_n_var.get()
        threshold = self.thresh_var.get() / 100.0

        total_ex = total_fu = 0.0
        hits = []

        for path, txt in self.cache.items():
            ex = self.matcher.exactMatch(txt, kws, algorithm=algo)
            exact_map = {k: v["count"] for k,v in ex["matches"].items() if v["count"]>0}
            ex_total = sum(exact_map.values())
            total_ex += float(ex["execution_time_ms"].rstrip("ms"))

            if ex_total:
                hits.append((path, exact_map, ex_total, ex_total*1000))
                continue

            fu = self.matcher.fuzzyMatch(txt, kws, threshold)
            fu_map = fu["matches"]
            fu_total = sum(fu_map.values())
            total_fu += float(fu["execution_time_ms"].rstrip("ms"))

            if fu_total:
                hits.append((path, fu_map, fu_total, fu_total))

        self.time_var.set(f"Exact total: {total_ex:.1f} ms   Fuzzy total: {total_fu:.1f} ms")
        hits.sort(key=lambda x: x[3], reverse=True)

        for path, kwmap, total, score in hits[:top_n]:
            sd = get_summary_data_by_cv_path(self.db.connection, path)
            rc = ResultCard(full_name=sd.full_name,
                            cv_path=path,
                            matched_keywords=kwmap,
                            total_matches=total)

            card = Frame(self.results_frame, bd=1, relief="raised",
                         padx=20, pady=12)
            card.pack(fill=X, expand=True, padx=20, pady=8)

            Label(card, text=rc.full_name,
                  font=("Helvetica",14,"bold")).pack(anchor="w")

            if rc.matched_keywords:
                # wrap into matrix: 4 per row
                kwf = Frame(card); kwf.pack(anchor="w", padx=10, pady=(6,0))
                col = 0
                for k,v in rc.matched_keywords.items():
                    Label(kwf, text=f"{k}({v})",
                          relief="groove", padx=6, pady=2)\
                      .grid(row=0, column=col, padx=4, pady=2)
                    col = (col+1) % 4
            else:
                Label(card, text="No matches",
                      font=("Helvetica",10,"italic"))\
                    .pack(anchor="w", padx=10, pady=(6,0))

            Label(card, text=f"Total: {rc.total_matches}",
                  font=("Helvetica",9))\
                .pack(anchor="w", padx=10, pady=(4,0))

            btns = Frame(card); btns.pack(anchor="e", pady=(8,0), padx=10)
            Button(btns, text="Summary", command=lambda p=path: self.show_summary(p))\
                .pack(side=LEFT, padx=5)
            Button(btns, text="View CV", command=lambda p=path: self.open_cv(p))\
                .pack(side=LEFT)


    def show_summary(self, cv_path):
        sd = get_summary_data_by_cv_path(self.db.connection, cv_path)
        if not sd:
            return messagebox.showerror("Error", "Could not load summary")

        win = Toplevel(self.root)
        win.title("CV Summary")
        win.geometry("700x500")

        # --- Outer scrollable canvas/frame ---
        outer = Frame(win)
        outer.pack(fill=BOTH, expand=True)
        v_scroll = Scrollbar(outer, orient="vertical")
        v_scroll.pack(side=RIGHT, fill=Y)
        canvas = Canvas(outer, yscrollcommand=v_scroll.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        v_scroll.config(command=canvas.yview)

        content = Frame(canvas)
        canvas.create_window((0,0), window=content, anchor="nw")
        content.bind("<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # --- Header Bar ---
        hdr = Frame(content, bg="#333")
        hdr.pack(fill=X)
        Label(hdr, text=sd.full_name,
            bg="#333", fg="white",
            font=("Helvetica",14,"bold"),
            pady=8).pack(fill=X)

        # --- Basic Info ---
        info = Frame(content, pady=10, padx=12)
        info.pack(fill=X)
        Label(info, text=f"Birthdate: {sd.birth_date}", anchor="w").pack(fill=X)
        Label(info, text=f"Phone    : {sd.phone_number}", anchor="w").pack(fill=X)

        # --- Skills with horizontal scroll ---
        if sd.skills:
            Label(content, text="Skills:", font=("Helvetica",12,"bold"),
                anchor="w").pack(fill=X, padx=12, pady=(10,0))

            skill_outer = Frame(content)
            skill_outer.pack(fill=X, padx=12, pady=4)

            h_scroll = Scrollbar(skill_outer, orient=HORIZONTAL)
            h_scroll.pack(side=BOTTOM, fill=X)

            skill_canvas = Canvas(skill_outer, height=40,
                                xscrollcommand=h_scroll.set)
            skill_canvas.pack(side=TOP, fill=X, expand=True)
            h_scroll.config(command=skill_canvas.xview)

            skill_frame = Frame(skill_canvas)
            skill_canvas.create_window((0,0), window=skill_frame, anchor="nw")

            # add each skill label inline
            col = 0
            for skill in sd.skills:
                lbl = Label(skill_frame, text=skill,
                            relief="ridge", padx=6, pady=2)
                lbl.grid(row=0, column=col, padx=4, pady=2)
                col += 1

            # update scrollregion
            skill_frame.update_idletasks()
            skill_canvas.config(scrollregion=skill_canvas.bbox("all"))

        # --- Experience stacked ---
        if sd.work_experience:
            Label(content, text="Experience:", font=("Helvetica",12,"bold"),
                anchor="w").pack(fill=X, padx=12, pady=(10,0))
            for exp in sd.work_experience:
                box = Frame(content, bg="#EEE", padx=12, pady=8)
                box.pack(fill=X, padx=12, pady=4)
                Label(box, text=exp, justify="left", bg="#EEE",
                    wraplength=660).pack(fill=X)

        # --- Education stacked ---
        if sd.education:
            Label(content, text="Education:", font=("Helvetica",12,"bold"),
                anchor="w").pack(fill=X, padx=12, pady=(10,0))
            for edu in sd.education:
                box = Frame(content, bg="#EEE", padx=12, pady=8)
                box.pack(fill=X, padx=12, pady=4)
                Label(box, text=edu, justify="left", bg="#EEE",
                    wraplength=660).pack(fill=X)

        # make modal
        win.transient(self.root)
        win.grab_set()



    def open_cv(self, cv_path):
        full = Path(DATA_DIR)/Path(cv_path).relative_to("data")
        if full.exists():
            webbrowser.open_new(f"file://{full.resolve()}")
        else:
            messagebox.showerror("Not Found", f"{full} not found")


def main():
    db = DatabaseConnection()
    if not db.connect():
        print("❌ Unable to connect to DB.")
        sys.exit(1)
    db.useDatabase(DATABASE_CONFIG["database"])

    root = Tk()
    ATSApp(root, db)
    root.mainloop()
    db.disconnect()

if __name__ == "__main__":
    main()
