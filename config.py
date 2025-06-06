import os
from pathlib import Path

# Database configny 
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'ats_database',
    'port': 3306
}

# File Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'src' / 'archive' / 'data' / 'data'
RESUME_CSV_PATH = BASE_DIR / 'src' / 'archive' / 'Resume' / 'Resume.csv'

# Algorithm Settings
FUZZY_MATCH_THRESHOLD = 0.7  # buat fuzzy matching, minimum similarity
MAX_RESULTS_DISPLAY = 50     # maximal yang diperlihatkan resultny

# GUI Settings
WINDOW_TITLE = "ATS CV Digital - Pattern Matching System"
WINDOW_WIDTH = 1200 # atur atur lah ini
WINDOW_HEIGHT = 800

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = BASE_DIR / 'logs' / 'ats.log'