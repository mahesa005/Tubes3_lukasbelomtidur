import sys
import time
import webbrowser
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from tkinter import (
    Tk, Frame, Label, Entry, Button, Scale, Spinbox,
    Scrollbar, Canvas, StringVar, IntVar, BooleanVar, Checkbutton,  # TAMBAH BooleanVar dan Checkbutton
    messagebox, Toplevel, LEFT, RIGHT, BOTH, Y, X, W, HORIZONTAL, TOP, BOTTOM
)
from tkinter.ttk import Combobox

# ensure src folder is importable
sys.path.append(str(Path(__file__).parent / "src"))

from config import DATABASE_CONFIG, DATA_DIR
from src.database.connection import DatabaseConnection
from src.database.queries import get_all_cv_paths, get_summary_data_by_cv_path
from src.models.ResultCard import ResultCard
from src.algorithm.PatternMatcher import PatternMatcher
from src.pdfprocessor.pdfExtractor import PDFExtractor

DEFAULT_MAX_CV_LOAD = 100


class RetroStyle:
    # Windows 98/Vista colors
    BG_MAIN = "#c0c0c0"           # Classic gray
    BG_WINDOW = "#f0f0f0"         # Light gray
    BG_BUTTON = "#e0e0e0"         # Button gray
    BG_TITLEBAR = "#0a246a"       # Classic blue titlebar
    BG_CARD = "#ffffff"           # White cards
    BG_HIGHLIGHT = "#316ac5"      # Blue highlight
    BORDER_DARK = "#808080"       # Dark border
    BORDER_LIGHT = "#ffffff"      # Light border (3D effect)
    TEXT_MAIN = "#000000"         # Black text
    TEXT_BLUE = "#0000ff"         # Blue links
    TEXT_RED = "#ff0000"          # Red text


class CVLoadDialog:
    """Custom dialog untuk input MAX_CV_LOAD dengan retro styling - RESPONSIVE & SCROLLABLE"""
    
    def __init__(self, parent, total_cvs):
        self.result = None
        self.total_cvs = total_cvs
        
        # Create dialog window
        self.dialog = Toplevel(parent)
        self.dialog.title("CV Loading Configuration")
        self.dialog.geometry("600x500")  # Bigger size
        self.dialog.configure(bg=RetroStyle.BG_MAIN)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Make it resizable
        self.dialog.resizable(True, True)
        self.dialog.minsize(500, 400)  # Minimum size
        
        # Center the dialog
        self._center_dialog(parent)
        
        self._build_dialog()
        
    def _center_dialog(self, parent):
        """Center dialog on parent window"""
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 300
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 250
        self.dialog.geometry(f"+{x}+{y}")
        
    def _build_dialog(self):
        # Title bar
        title_bar = Frame(self.dialog, bg=RetroStyle.BG_TITLEBAR, height=35)
        title_bar.pack(fill=X)
        title_bar.pack_propagate(False)
        
        Label(title_bar, text="⚙️ CV Database Loading Configuration",
              bg=RetroStyle.BG_TITLEBAR, fg="white",
              font=("MS Sans Serif", 11, "bold")).pack(side=LEFT, padx=15, pady=8)
        
        # SCROLLABLE MAIN CONTENT
        main_frame = Frame(self.dialog, bg=RetroStyle.BG_MAIN)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar for scrollable content
        canvas = Canvas(main_frame, bg=RetroStyle.BG_WINDOW, relief="sunken", bd=2)
        scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview,
                             bg=RetroStyle.BG_BUTTON, relief="raised", bd=2)
        scrollable_frame = Frame(canvas, bg=RetroStyle.BG_WINDOW)
        
        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # RESPONSIVE CONTENT INSIDE SCROLLABLE FRAME
        self._build_scrollable_content(scrollable_frame)
        
        # FIXED BOTTOM BUTTONS (outside scroll area)
        self._build_bottom_buttons()
        
        # Bind mousewheel to canvas
        self._bind_mousewheel(canvas)
        
        # Make content responsive to window resize
        canvas.bind('<Configure>', self._on_canvas_configure)
        
    def _build_scrollable_content(self, parent):
        """Build the scrollable content inside the dialog"""
        
        # Info section with responsive layout
        info_section = Frame(parent, bg=RetroStyle.BG_WINDOW, relief="raised", bd=2)
        info_section.pack(fill=X, padx=15, pady=15)
        
        info_frame = Frame(info_section, bg=RetroStyle.BG_WINDOW, padx=20, pady=20)
        info_frame.pack(fill=X)
        
        Label(info_frame, text="💾 Database Information",
              font=("MS Sans Serif", 14, "bold"),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(anchor="w", pady=(0, 15))
        
        # Stats with responsive grid
        stats_frame = Frame(info_frame, bg=RetroStyle.BG_WINDOW)
        stats_frame.pack(fill=X, pady=10)
        
        Label(stats_frame, text=f"📊 Total CVs in database:",
              font=("MS Sans Serif", 11),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_BLUE).grid(row=0, column=0, sticky="w", pady=5)
        
        Label(stats_frame, text=f"{self.total_cvs} files",
              font=("MS Sans Serif", 11, "bold"),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_RED).grid(row=0, column=1, sticky="w", padx=10)
        
        Label(stats_frame, text="⚡ Performance:",
              font=("MS Sans Serif", 11),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_BLUE).grid(row=1, column=0, sticky="w", pady=5)
        
        Label(stats_frame, text="More CVs = Better results but slower loading",
              font=("MS Sans Serif", 9),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).grid(row=1, column=1, sticky="w", padx=10)
        
        # Configure grid weights for responsiveness
        stats_frame.grid_columnconfigure(1, weight=1)
        
        # Input section with responsive design
        input_section = Frame(parent, bg=RetroStyle.BG_WINDOW, relief="sunken", bd=2)
        input_section.pack(fill=X, padx=15, pady=15)
        
        input_frame = Frame(input_section, bg=RetroStyle.BG_WINDOW, padx=20, pady=20)
        input_frame.pack(fill=X)
        
        Label(input_frame, text="🎯 Select Number of CVs to Load",
              font=("MS Sans Serif", 12, "bold"),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(anchor="w", pady=(0, 15))
        
        # Responsive input row
        input_row = Frame(input_frame, bg=RetroStyle.BG_WINDOW)
        input_row.pack(fill=X, pady=10)
        
        Label(input_row, text="Number of CVs:",
              font=("MS Sans Serif", 10),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(side=LEFT)
        
        self.cv_count_var = IntVar(value=min(DEFAULT_MAX_CV_LOAD, self.total_cvs))
        spinbox = Spinbox(input_row, from_=1, to=self.total_cvs, 
                         textvariable=self.cv_count_var,
                         font=("MS Sans Serif", 10), width=12,
                         relief="sunken", bd=2, bg="white")
        spinbox.pack(side=LEFT, padx=15)
        
        Label(input_row, text=f"(Maximum: {self.total_cvs})",
              font=("MS Sans Serif", 9),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(side=LEFT, padx=(10, 0))
        
        # Quick select with responsive wrapping
        quick_section = Frame(input_frame, bg=RetroStyle.BG_WINDOW)
        quick_section.pack(fill=X, pady=15)
        
        Label(quick_section, text="🚀 Quick Select Options:",
              font=("MS Sans Serif", 10, "bold"),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(anchor="w", pady=(0, 10))
        
        # Responsive button grid
        quick_buttons = Frame(quick_section, bg=RetroStyle.BG_WINDOW)
        quick_buttons.pack(fill=X)
        
        quick_values = [25, 50, 100, 200, 500, self.total_cvs]
        row, col = 0, 0
        
        for val in quick_values:
            if val <= self.total_cvs:
                btn_text = "All CVs" if val == self.total_cvs else f"{val} CVs"
                btn = Button(quick_buttons, text=btn_text,
                           command=lambda v=val: self.cv_count_var.set(v),
                           font=("MS Sans Serif", 8, "bold"), width=10,
                           bg=RetroStyle.BG_BUTTON, relief="raised", bd=2,
                           cursor="hand2")
                btn.grid(row=row, column=col, padx=5, pady=3, sticky="ew")
                
                col += 1
                if col >= 3:  # 3 buttons per row for responsiveness
                    col = 0
                    row += 1
        
        # Configure button grid weights
        for i in range(3):
            quick_buttons.grid_columnconfigure(i, weight=1)
        
        # Performance guide - scrollable and responsive
        perf_section = Frame(parent, bg="#fffacd", relief="raised", bd=2)
        perf_section.pack(fill=X, padx=15, pady=15)
        
        perf_frame = Frame(perf_section, bg="#fffacd", padx=20, pady=15)
        perf_frame.pack(fill=X)
        
        Label(perf_frame, text="⚠️ Performance Guide & Recommendations:",
              font=("MS Sans Serif", 11, "bold"),
              bg="#fffacd", fg=RetroStyle.TEXT_RED).pack(anchor="w", pady=(0, 10))
        
        perf_items = [
            ("🟢 1-50 CVs:", "Very Fast loading (~10-20 seconds)", "Best for quick testing"),
            ("🟡 51-200 CVs:", "Fast loading (~20-40 seconds)", "Good balance of speed & results"),
            ("🟠 201-500 CVs:", "Medium loading (~40-80 seconds)", "More comprehensive search"),
            ("🔴 500+ CVs:", "Slower loading (~80+ seconds)", "Full database search")
        ]
        
        for range_text, time_text, desc_text in perf_items:
            item_frame = Frame(perf_frame, bg="#fffacd")
            item_frame.pack(fill=X, pady=2)
            
            Label(item_frame, text=range_text,
                  font=("MS Sans Serif", 9, "bold"),
                  bg="#fffacd", fg=RetroStyle.TEXT_MAIN).pack(side=LEFT, anchor="w")
            
            Label(item_frame, text=f"{time_text} - {desc_text}",
                  font=("MS Sans Serif", 8),
                  bg="#fffacd", fg=RetroStyle.TEXT_MAIN).pack(side=LEFT, padx=(10, 0))
        
        # Memory usage warning
        memory_section = Frame(parent, bg="#ffebee", relief="raised", bd=2)
        memory_section.pack(fill=X, padx=15, pady=15)
        
        memory_frame = Frame(memory_section, bg="#ffebee", padx=20, pady=15)
        memory_frame.pack(fill=X)
        
        Label(memory_frame, text="💾 Memory Usage Information:",
              font=("MS Sans Serif", 10, "bold"),
              bg="#ffebee", fg=RetroStyle.TEXT_RED).pack(anchor="w", pady=(0, 8))
        
        memory_text = "Each CV uses approximately 50-200KB of RAM when loaded. Loading 1000+ CVs may require 100-200MB of memory."
        Label(memory_frame, text=memory_text,
              font=("MS Sans Serif", 8),
              bg="#ffebee", fg=RetroStyle.TEXT_MAIN,
              wraplength=500, justify="left").pack(anchor="w")
        
    def _build_bottom_buttons(self):
        """Build fixed bottom buttons outside scroll area"""
        btn_container = Frame(self.dialog, bg=RetroStyle.BG_MAIN)
        btn_container.pack(fill=X, padx=10, pady=10)
        
        btn_frame = Frame(btn_container, bg=RetroStyle.BG_WINDOW, relief="raised", bd=2)
        btn_frame.pack(fill=X, padx=5, pady=5)
        
        button_area = Frame(btn_frame, bg=RetroStyle.BG_WINDOW)
        button_area.pack(fill=X, padx=20, pady=15)
        
        # Responsive button layout
        ok_btn = Button(button_area, text="🚀 Load CVs & Start", 
                       command=self._ok_clicked,
                       font=("MS Sans Serif", 10, "bold"), 
                       bg="#4CAF50", fg="white",
                       relief="raised", bd=3, cursor="hand2",
                       padx=20, pady=8)
        ok_btn.pack(side=RIGHT, padx=5)
        
        cancel_btn = Button(button_area, text="❌ Cancel", 
                           command=self._cancel_clicked,
                           font=("MS Sans Serif", 10), 
                           bg="#f44336", fg="white",
                           relief="raised", bd=3, cursor="hand2",
                           padx=20, pady=8)
        cancel_btn.pack(side=RIGHT, padx=5)
        
        # Show current selection
        self.selection_label = Label(button_area, 
                                    textvariable=self.cv_count_var,
                                    font=("MS Sans Serif", 12, "bold"),
                                    bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_BLUE)
        self.selection_label.pack(side=LEFT)
        
        Label(button_area, text="CVs selected",
              font=("MS Sans Serif", 10),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(side=LEFT, padx=(5, 0))
        
    def _bind_mousewheel(self, canvas):
        """Bind mousewheel scrolling to canvas"""
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
            
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)
        
    def _on_canvas_configure(self, event):
        """Handle canvas resize for responsiveness"""
        canvas = event.widget
        canvas.itemconfig(canvas.find_all()[0], width=event.width)
    
    def _ok_clicked(self):
        self.result = self.cv_count_var.get()
        self.dialog.destroy()
    
    def _cancel_clicked(self):
        self.result = None
        self.dialog.destroy()
    
    def show(self):
        # Set focus and wait
        self.dialog.focus_set()
        self.dialog.wait_window()
        return self.result


class ATSApp:
    def __init__(self, root, db_conn):
        self.root = root
        self.db = db_conn
        self.matcher = PatternMatcher()
        self.extractor = PDFExtractor()
        self.cache = {}
        self.max_cv_load = DEFAULT_MAX_CV_LOAD  # Will be set by user

        self._setup_retro_window()
        self._build_ui()
        self._ask_cv_load_count()

    def _setup_retro_window(self):
        self.root.title("ATS - Applicant Tracking System v1.0")
        self.root.geometry("1000x700")
        self.root.configure(bg=RetroStyle.BG_MAIN)

    def _ask_cv_load_count(self):
        """Ask user how many CVs to load"""
        # Get total CV count first
        all_paths = get_all_cv_paths(self.db.connection)
        total_cvs = len(all_paths)
        
        if total_cvs == 0:
            messagebox.showerror("No Data", "No CVs found in database!")
            self.root.destroy()
            return
        
        # Show custom dialog
        dialog = CVLoadDialog(self.root, total_cvs)
        user_choice = dialog.show()
        
        if user_choice is None:
            # User cancelled
            self.root.destroy()
            return
        
        self.max_cv_load = user_choice
        self._preload_cvs_with_progress()

    def _preload_cvs_with_progress(self):
        """Load CVs with progress indication"""
        all_paths = get_all_cv_paths(self.db.connection)
        paths = all_paths[:self.max_cv_load]
        
        # Show loading dialog
        self._show_loading_dialog(len(paths))
        
        # Start loading in background
        self.root.after(100, lambda: self._do_preload(paths))

    def _show_loading_dialog(self, count):
        """Show loading progress dialog"""
        self.loading_dialog = Toplevel(self.root)
        self.loading_dialog.title("Loading CVs...")
        self.loading_dialog.geometry("400x200")
        self.loading_dialog.configure(bg=RetroStyle.BG_MAIN)
        self.loading_dialog.transient(self.root)
        self.loading_dialog.grab_set()
        
        # Center dialog
        self.loading_dialog.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 100, 
            self.root.winfo_rooty() + 100
        ))
        
        # Content
        content = Frame(self.loading_dialog, bg=RetroStyle.BG_WINDOW, relief="raised", bd=2)
        content.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        Label(content, text="📁 Loading CV Database",
              font=("MS Sans Serif", 12, "bold"),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(pady=20)
        
        self.loading_status = StringVar(value=f"Preparing to load {count} CVs...")
        Label(content, textvariable=self.loading_status,
              font=("MS Sans Serif", 9),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_BLUE).pack(pady=10)
        
        # Simple progress indicator
        self.loading_dots = StringVar(value="")
        Label(content, textvariable=self.loading_dots,
              font=("MS Sans Serif", 16),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(pady=10)
        
        # Start dot animation
        self._animate_loading_dots()

    def _animate_loading_dots(self):
        """Animate loading dots"""
        if hasattr(self, 'loading_dialog') and self.loading_dialog.winfo_exists():
            current = self.loading_dots.get()
            if len(current) >= 6:
                self.loading_dots.set("●")
            else:
                self.loading_dots.set(current + "●")
            self.root.after(500, self._animate_loading_dots)

    def _do_preload(self, paths):
        """Actually preload the CVs"""
        self.loading_status.set(f"Loading {len(paths)} CVs from database...")
        start = time.time()
        
        loaded_count = 0
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
                    loaded_count += 1
                    
                    # Update progress
                    if hasattr(self, 'loading_status'):
                        self.loading_status.set(f"Loaded {loaded_count}/{len(paths)} CVs...")
                        self.root.update()
                        
                except Exception as e:
                    self.cache[p] = ""
                    print(f"Error loading {p}: {e}")
        
        elapsed = (time.time()-start)*1000
        
        # Close loading dialog
        if hasattr(self, 'loading_dialog'):
            self.loading_dialog.destroy()
        
        # Update status
        self.time_var.set(f"Successfully loaded {len(self.cache)} CVs in {elapsed:.1f}ms! Ready to search.")
        
        print(f"[INFO] Loaded {len(self.cache)} CVs in {elapsed:.1f} ms")

    def _create_retro_button(self, parent, text, command, width=None):
        """Create retro 3D button with classic Windows style"""
        btn = Button(parent, text=text, command=command,
                    bg=RetroStyle.BG_BUTTON,
                    fg=RetroStyle.TEXT_MAIN,
                    font=("MS Sans Serif", 8),
                    relief="raised", bd=2,
                    cursor="hand2",
                    activebackground="#d0d0d0",
                    width=width)
        
        # Classic button hover effect
        def on_enter(e):
            btn.configure(bg="#d8d8d8")
        def on_leave(e):
            btn.configure(bg=RetroStyle.BG_BUTTON)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        return btn

    def _create_3d_frame(self, parent, sunken=False):
        """Create classic 3D frame effect"""
        relief = "sunken" if sunken else "raised"
        return Frame(parent, bg=RetroStyle.BG_WINDOW, relief=relief, bd=2)

    def _build_ui(self):
        # Classic title bar effect
        title_frame = Frame(self.root, bg=RetroStyle.BG_TITLEBAR, height=30)
        title_frame.pack(fill=X)
        title_frame.pack_propagate(False)
        
        Label(title_frame, text="🖥️ ATS - Applicant Tracking System",
              bg=RetroStyle.BG_TITLEBAR, fg="white",
              font=("MS Sans Serif", 10, "bold")).pack(side=LEFT, padx=10, pady=5)
        
        # Show loaded CV count in title
        self.cv_count_label = Label(title_frame, text=f"[Loading CVs...]",
                                   bg=RetroStyle.BG_TITLEBAR, fg="yellow",
                                   font=("MS Sans Serif", 8))
        self.cv_count_label.pack(side=RIGHT, padx=10, pady=5)
        
        # Main header section
        header_frame = self._create_3d_frame(self.root)
        header_frame.pack(fill=X, padx=10, pady=10)
        
        Label(header_frame, text="📁 CV Digital Pattern Matching System",
              font=("MS Sans Serif", 12, "bold"),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(pady=10)
        
        Label(header_frame, text="Advanced Search & Analysis Tool - Version 1.0",
              font=("MS Sans Serif", 8),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_BLUE).pack(pady=(0, 10))

        # Parameters section with classic group box style
        params_outer = self._create_3d_frame(self.root, sunken=True)
        params_outer.pack(fill=X, padx=10, pady=10)
        
        # Group box label
        Label(params_outer, text=" Search Parameters ",
              font=("MS Sans Serif", 8, "bold"),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(anchor="nw", padx=10)
        
        params = Frame(params_outer, bg=RetroStyle.BG_WINDOW)
        params.pack(fill=X, padx=15, pady=10)

        # Keywords with classic styling
        Label(params, text="Keywords (comma-separated):",
              font=("MS Sans Serif", 8),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).grid(row=0, column=0, sticky="w", pady=2)
        
        self.keyword_var = StringVar()
        keyword_entry = Entry(params, textvariable=self.keyword_var,
                             font=("MS Sans Serif", 8),
                             width=50, relief="sunken", bd=2)
        keyword_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=2, sticky="ew")

        # Algorithm selection
        Label(params, text="Pattern Matching Algorithm:",
              font=("MS Sans Serif", 8),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).grid(row=1, column=0, sticky="w", pady=2)
        
        self.algo_var = StringVar(value="Knuth-Morris-Pratt (KMP)")
        algo_combo = Combobox(params, textvariable=self.algo_var,
                             values=["Knuth-Morris-Pratt (KMP)", "Boyer-Moore"],
                             font=("MS Sans Serif", 8),
                             width=25, state="readonly")
        algo_combo.grid(row=1, column=1, padx=10, pady=2, sticky="w")

        # Case Sensitive checkbox
        self.case_sensitive_var = BooleanVar(value=False)
        case_frame = Frame(params, bg=RetroStyle.BG_WINDOW)
        case_frame.grid(row=1, column=2, padx=10, pady=2, sticky="w")
        
        case_check = Checkbutton(case_frame, 
                                text="Case Sensitive",
                                variable=self.case_sensitive_var,
                                font=("MS Sans Serif", 8),
                                bg=RetroStyle.BG_WINDOW, 
                                fg=RetroStyle.TEXT_MAIN,
                                selectcolor="white",
                                activebackground=RetroStyle.BG_WINDOW,
                                activeforeground=RetroStyle.TEXT_MAIN,
                                relief="flat")
        case_check.pack(side=LEFT)

        # Top N with classic spinbox
        Label(params, text="Maximum Results:",
              font=("MS Sans Serif", 8),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).grid(row=2, column=0, sticky="w", pady=2)
        
        self.top_n_var = IntVar(value=10)
        topn_frame = Frame(params, bg=RetroStyle.BG_WINDOW)
        topn_frame.grid(row=2, column=1, padx=10, pady=2, sticky="w")
        
        Spinbox(topn_frame, from_=1, to=100, textvariable=self.top_n_var,
                font=("MS Sans Serif", 8), width=8,
                relief="sunken", bd=2,
                bg="white", fg=RetroStyle.TEXT_MAIN).pack(side=LEFT)
        
        Label(topn_frame, text="results",
              font=("MS Sans Serif", 8),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(side=LEFT, padx=(5, 0))

        # Fuzzy threshold with retro slider
        Label(params, text="Similarity Threshold:",
              font=("MS Sans Serif", 8),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).grid(row=3, column=0, sticky="w", pady=2)
        
        thresh_frame = Frame(params, bg=RetroStyle.BG_WINDOW)
        thresh_frame.grid(row=3, column=1, columnspan=2, padx=10, pady=2, sticky="w")
        
        self.thresh_var = IntVar(value=70)
        Scale(thresh_frame, from_=0, to=100, variable=self.thresh_var,
              orient=HORIZONTAL, length=200,
              font=("MS Sans Serif", 7),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN,
              relief="sunken", bd=2,
              troughcolor="#ffffff",
              activebackground=RetroStyle.BG_HIGHLIGHT).pack(side=LEFT)
        
        Label(thresh_frame, text="%",
              font=("MS Sans Serif", 8),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(side=LEFT, padx=(5, 0))

        # Search button with classic style
        btn_frame = Frame(params, bg=RetroStyle.BG_WINDOW)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=15)
        
        search_btn = self._create_retro_button(btn_frame, "🔍 Search Database", self.on_search, width=20)
        search_btn.pack(side=LEFT, padx=5)
        
        clear_btn = self._create_retro_button(btn_frame, "🗑️ Clear Results", self.clear_results, width=15)
        clear_btn.pack(side=LEFT, padx=5)
        
        # Reload button
        reload_btn = self._create_retro_button(btn_frame, "🔄 Reload CVs", self._reload_cvs, width=12)
        reload_btn.pack(side=LEFT, padx=5)

        # Configure grid weights
        params.grid_columnconfigure(1, weight=1)
        params.grid_columnconfigure(2, weight=0)

        # Status bar
        status_frame = self._create_3d_frame(self.root, sunken=True)
        status_frame.pack(fill=X, padx=10, pady=(0, 10))
        
        self.time_var = StringVar(value="Loading CVs...")
        Label(status_frame, textvariable=self.time_var,
              font=("MS Sans Serif", 8),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN,
              anchor="w").pack(fill=X, padx=5, pady=2)

        # Results section with classic styling
        results_outer = self._create_3d_frame(self.root, sunken=True)
        results_outer.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))
        
        Label(results_outer, text=" Search Results ",
              font=("MS Sans Serif", 8, "bold"),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(anchor="nw", padx=10)

        # Scrollable results container
        container = Frame(results_outer, bg=RetroStyle.BG_WINDOW)
        container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Canvas with classic scrollbar
        self.canvas = Canvas(container, bg=RetroStyle.BG_WINDOW,
                            relief="sunken", bd=2)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Classic scrollbar
        scrollbar = Scrollbar(container, orient="vertical", command=self.canvas.yview,
                             bg=RetroStyle.BG_BUTTON, relief="raised", bd=2)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Results frame with proper wrapping
        self.results_frame = Frame(self.canvas, bg=RetroStyle.BG_WINDOW)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        
        # Bind canvas resize to adjust frame width
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.results_frame.bind("<Configure>", self._on_frame_configure)

        # Initial message
        self._show_loading_message()

    def _show_loading_message(self):
        loading_frame = Frame(self.results_frame, bg=RetroStyle.BG_WINDOW)
        loading_frame.pack(expand=True, fill=BOTH, pady=50)
        
        Label(loading_frame, text="⏳",
              font=("MS Sans Serif", 24),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_BLUE).pack()
        
        Label(loading_frame, text="Loading CV Database...",
              font=("MS Sans Serif", 12, "bold"),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(pady=(10, 5))
        
        Label(loading_frame, text="Please wait while we prepare your search database",
              font=("MS Sans Serif", 8),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack()

    def _reload_cvs(self):
        """Reload CVs with new count"""
        self.cache.clear()
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self._show_loading_message()
        self._ask_cv_load_count()

    # Update CV count in title after loading
    def _update_cv_count_display(self):
        if hasattr(self, 'cv_count_label'):
            self.cv_count_label.config(text=f"[{len(self.cache)} CVs loaded]")


    def _on_canvas_configure(self, event):
        """Adjust the frame width when canvas is resized"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _on_frame_configure(self, event):
        """Update scroll region when frame size changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _show_welcome_message(self):
        welcome_frame = Frame(self.results_frame, bg=RetroStyle.BG_WINDOW)
        welcome_frame.pack(expand=True, fill=BOTH, pady=50)
        
        Label(welcome_frame, text="💾",
              font=("MS Sans Serif", 24),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_BLUE).pack()
        
        Label(welcome_frame, text="Welcome to ATS v1.0",
              font=("MS Sans Serif", 12, "bold"),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(pady=(10, 5))
        
        Label(welcome_frame, text="Enter search keywords and click 'Search Database' to begin",
              font=("MS Sans Serif", 8),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack()

    def clear_results(self):
        """Clear all search results"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self._show_welcome_message()
        self.time_var.set("Results cleared. Ready to search...")

    def _preload_all_cvs(self):
        all_paths = get_all_cv_paths(self.db.connection)
        paths = all_paths[:MAX_CV_LOAD]
        self.time_var.set(f"Loading {len(paths)} CV files from database...")
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
        self.time_var.set(f"Database loaded successfully! {len(paths)} files ready for search.")
        print(f"[INFO] Done preloading in {elapsed:.1f} ms")

    def on_search(self):
        # Clear previous results
        for w in self.results_frame.winfo_children():
            w.destroy()
        
        # Show searching message
        searching_frame = Frame(self.results_frame, bg=RetroStyle.BG_WINDOW)
        searching_frame.pack(expand=True, fill=BOTH, pady=50)
        
        Label(searching_frame, text="⏳",
              font=("MS Sans Serif", 16),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_BLUE).pack()
        
        Label(searching_frame, text="Searching database...",
              font=("MS Sans Serif", 10, "bold"),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(pady=10)
        
        self.root.update()

        kws = [k.strip() for k in self.keyword_var.get().split(",") if k.strip()]
        if not kws:
            messagebox.showwarning("Invalid Input", "Please enter at least one keyword to search.")
            self.clear_results()
            return
        
        algo = "KMP" if "KMP" in self.algo_var.get().upper() else "BM"
        top_n = self.top_n_var.get()
        threshold = self.thresh_var.get() / 100.0
        case_sensitive = self.case_sensitive_var.get()

        total_ex = total_fu = 0.0
        hits = []

        for path, txt in self.cache.items():
            # Apply case sensitivity
            search_text = txt if case_sensitive else txt.lower()
            search_keywords = kws if case_sensitive else [k.lower() for k in kws]
            
            ex = self.matcher.exactMatch(search_text, search_keywords, algorithm=algo)
            exact_map = {k: v["count"] for k,v in ex["matches"].items() if v["count"]>0}
            ex_total = sum(exact_map.values())
            total_ex += float(ex["execution_time_ms"].rstrip("ms"))

            if ex_total:
                hits.append((path, exact_map, ex_total, ex_total*1000))
                continue

            fu = self.matcher.fuzzyMatch(search_text, search_keywords, threshold)
            fu_map = fu["matches"]
            fu_total = sum(fu_map.values())
            total_fu += float(fu["execution_time_ms"].rstrip("ms"))

            if fu_total:
                hits.append((path, fu_map, fu_total, fu_total))

        # Clear searching message
        for w in self.results_frame.winfo_children():
            w.destroy()

        case_status = "Yes" if case_sensitive else "No"
        self.time_var.set(f"Search completed! Found {len(hits)} matches. Exact: {total_ex:.1f}ms | Fuzzy: {total_fu:.1f}ms | Case Sensitive: {case_status}")
        hits.sort(key=lambda x: x[3], reverse=True)

        if not hits:
            self._show_no_results()
            return

        # Create wrapped grid layout for results
        self._create_results_grid(hits[:top_n])

    def _show_no_results(self):
        no_results_frame = Frame(self.results_frame, bg=RetroStyle.BG_WINDOW)
        no_results_frame.pack(expand=True, fill=BOTH, pady=50)
        
        Label(no_results_frame, text="❌",
              font=("MS Sans Serif", 20),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_RED).pack()
        
        Label(no_results_frame, text="No Results Found",
              font=("MS Sans Serif", 12, "bold"),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(pady=(10, 5))
        
        Label(no_results_frame, text="Try different keywords or adjust the similarity threshold",
              font=("MS Sans Serif", 8),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack()

    def _create_results_grid(self, hits):
        """Create a wrapped grid layout for result cards"""
        cards_per_row = 2
        current_row = 0
        current_col = 0
        
        for i, (path, kwmap, total, score) in enumerate(hits):
            if current_col == 0:
                row_frame = Frame(self.results_frame, bg=RetroStyle.BG_WINDOW)
                row_frame.pack(fill=X, padx=5, pady=5)
            
            self._create_retro_result_card(row_frame, path, kwmap, total, i+1, current_col)
            
            current_col += 1
            if current_col >= cards_per_row:
                current_col = 0
                current_row += 1

    def _create_retro_result_card(self, parent, path, kwmap, total, rank, column):
        sd = get_summary_data_by_cv_path(self.db.connection, path)
        
        card = Frame(parent, bg=RetroStyle.BG_CARD, relief="raised", bd=3)
        card.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        
        header = Frame(card, bg=RetroStyle.BG_HIGHLIGHT, height=25)
        header.pack(fill=X)
        header.pack_propagate(False)
        
        Label(header, text=f"#{rank} - {sd.full_name}",
              bg=RetroStyle.BG_HIGHLIGHT, fg="white",
              font=("MS Sans Serif", 8, "bold")).pack(side=LEFT, padx=5, pady=3)
        
        Label(header, text=f"Score: {total}",
              bg=RetroStyle.BG_HIGHLIGHT, fg="yellow",
              font=("MS Sans Serif", 8, "bold")).pack(side=RIGHT, padx=5, pady=3)
        
        content = Frame(card, bg=RetroStyle.BG_CARD, padx=10, pady=10)
        content.pack(fill=BOTH, expand=True)
        
        if kwmap:
            Label(content, text="Matched Keywords:",
                  font=("MS Sans Serif", 7, "bold"),
                  bg=RetroStyle.BG_CARD, fg=RetroStyle.TEXT_MAIN).pack(anchor="w")
            
            kw_frame = Frame(content, bg=RetroStyle.BG_CARD)
            kw_frame.pack(fill=X, pady=(2, 8))
            
            col = 0
            for k, v in kwmap.items():
                if col >= 2:
                    kw_frame = Frame(content, bg=RetroStyle.BG_CARD)
                    kw_frame.pack(fill=X, pady=1)
                    col = 0
                
                Label(kw_frame, text=f"{k} ({v})",
                      bg=RetroStyle.BG_BUTTON, fg=RetroStyle.TEXT_MAIN,
                      font=("MS Sans Serif", 7),
                      relief="raised", bd=1,
                      padx=4, pady=1).pack(side=LEFT, padx=2)
                col += 1
        
        btn_frame = Frame(content, bg=RetroStyle.BG_CARD)
        btn_frame.pack(fill=X, pady=(5, 0))
        
        summary_btn = self._create_retro_button(btn_frame, "📄 Summary", 
                                               lambda p=path: self.show_summary(p), width=10)
        summary_btn.pack(side=LEFT, padx=2)
        
        view_btn = self._create_retro_button(btn_frame, "📂 Open CV", 
                                            lambda p=path: self.open_cv(p), width=10)
        view_btn.pack(side=LEFT, padx=2)

    def show_summary(self, cv_path):
        sd = get_summary_data_by_cv_path(self.db.connection, cv_path)
        if not sd:
            return messagebox.showerror("Error", "Could not load CV summary data.")

        win = Toplevel(self.root)
        win.title(f"CV Summary - {sd.full_name}")
        win.geometry("800x600")
        win.configure(bg=RetroStyle.BG_MAIN)
        win.transient(self.root)
        win.grab_set()
        
        title_bar = Frame(win, bg=RetroStyle.BG_TITLEBAR, height=25)
        title_bar.pack(fill=X)
        title_bar.pack_propagate(False)
        
        Label(title_bar, text=f"📄 CV Summary - {sd.full_name}",
              bg=RetroStyle.BG_TITLEBAR, fg="white",
              font=("MS Sans Serif", 8, "bold")).pack(side=LEFT, padx=10, pady=3)
        
        content_area = self._create_3d_frame(win, sunken=True)
        content_area.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        canvas = Canvas(content_area, bg=RetroStyle.BG_WINDOW, relief="flat")
        scrollbar = Scrollbar(content_area, orient="vertical", command=canvas.yview,
                             bg=RetroStyle.BG_BUTTON)
        scrollable_frame = Frame(canvas, bg=RetroStyle.BG_WINDOW)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_frame.bind("<Configure>", 
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        self._build_retro_summary(scrollable_frame, sd)

    def _build_retro_summary(self, parent, sd):
        # Personal info section
        info_section = self._create_3d_frame(parent)
        info_section.pack(fill=X, padx=10, pady=10)
        
        Label(info_section, text=" Personal Information ",
              font=("MS Sans Serif", 8, "bold"),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(anchor="nw", padx=5)
        
        info_content = Frame(info_section, bg=RetroStyle.BG_WINDOW, padx=15, pady=10)
        info_content.pack(fill=X)
        
        Label(info_content, text=f"📅 Birth Date: {sd.birth_date}",
              font=("MS Sans Serif", 8),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(anchor="w", pady=1)
        
        Label(info_content, text=f"📞 Phone: {sd.phone_number}",
              font=("MS Sans Serif", 8),
              bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(anchor="w", pady=1)
        
        # Skills section
        if sd.skills:
            skills_section = self._create_3d_frame(parent)
            skills_section.pack(fill=X, padx=10, pady=10)
            
            Label(skills_section, text=" Technical Skills ",
                  font=("MS Sans Serif", 8, "bold"),
                  bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(anchor="nw", padx=5)
            
            skills_content = Frame(skills_section, bg=RetroStyle.BG_WINDOW, padx=15, pady=10)
            skills_content.pack(fill=X)
            
            skills_frame = Frame(skills_content, bg=RetroStyle.BG_WINDOW)
            skills_frame.pack(fill=X)
            
            for i, skill in enumerate(sd.skills):
                if i % 3 == 0:
                    skill_row = Frame(skills_frame, bg=RetroStyle.BG_WINDOW)
                    skill_row.pack(fill=X, pady=2)
                
                Label(skill_row, text=skill,
                      bg=RetroStyle.BG_BUTTON, fg=RetroStyle.TEXT_MAIN,
                      font=("MS Sans Serif", 7),
                      relief="raised", bd=2,
                      padx=6, pady=2).pack(side=LEFT, padx=3)
        
        # Work Experience section
        if sd.work_experience:
            exp_section = self._create_3d_frame(parent)
            exp_section.pack(fill=X, padx=10, pady=10)
            
            Label(exp_section, text=" Work Experience ",
                  font=("MS Sans Serif", 8, "bold"),
                  bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(anchor="nw", padx=5)
            
            exp_content = Frame(exp_section, bg=RetroStyle.BG_WINDOW, padx=15, pady=10)
            exp_content.pack(fill=X)
            
            for i, exp in enumerate(sd.work_experience):
                exp_card = Frame(exp_content, bg="#ffffff", relief="sunken", bd=1)
                exp_card.pack(fill=X, pady=3)
                
                Label(exp_card, text=f"💼 Experience {i+1}",
                      font=("MS Sans Serif", 7, "bold"),
                      bg="#ffffff", fg=RetroStyle.TEXT_BLUE,
                      padx=8, pady=3).pack(anchor="w")
                
                Label(exp_card, text=exp,
                      font=("MS Sans Serif", 8),
                      bg="#ffffff", fg=RetroStyle.TEXT_MAIN,
                      wraplength=700, justify="left",
                      padx=8, pady=5).pack(fill=X)
        
        # Education section
        if sd.education:
            edu_section = self._create_3d_frame(parent)
            edu_section.pack(fill=X, padx=10, pady=10)
            
            Label(edu_section, text=" Education ",
                  font=("MS Sans Serif", 8, "bold"),
                  bg=RetroStyle.BG_WINDOW, fg=RetroStyle.TEXT_MAIN).pack(anchor="nw", padx=5)
            
            edu_content = Frame(edu_section, bg=RetroStyle.BG_WINDOW, padx=15, pady=10)
            edu_content.pack(fill=X)
            
            for i, edu in enumerate(sd.education):
                edu_card = Frame(edu_content, bg="#ffffff", relief="sunken", bd=1)
                edu_card.pack(fill=X, pady=3)
                
                Label(edu_card, text=f"🎓 Education {i+1}",
                      font=("MS Sans Serif", 7, "bold"),
                      bg="#ffffff", fg=RetroStyle.TEXT_BLUE,
                      padx=8, pady=3).pack(anchor="w")
                
                Label(edu_card, text=edu,
                      font=("MS Sans Serif", 8),
                      bg="#ffffff", fg=RetroStyle.TEXT_MAIN,
                      wraplength=700, justify="left",
                      padx=8, pady=5).pack(fill=X)

    def open_cv(self, cv_path):
        full = Path(DATA_DIR)/Path(cv_path).relative_to("data")
        if full.exists():
            webbrowser.open_new(f"file://{full.resolve()}")
        else:
            messagebox.showerror("File Not Found", f"Could not locate CV file:\n{full}")


def main():
    db = DatabaseConnection()
    if not db.connect():
        print("❌ Unable to connect to database.")
        sys.exit(1)
    db.useDatabase(DATABASE_CONFIG["database"])

    root = Tk()
    ATSApp(root, db)
    root.mainloop()
    db.disconnect()

if __name__ == "__main__":
    main()