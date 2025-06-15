# 🖥️ ATS - Applicant Tracking System

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)

**ATS (Applicant Tracking System)** adalah aplikasi desktop berbasis Python dengan GUI retro untuk melakukan pattern matching dan pencarian CV/resume menggunakan algoritma string matching yang canggih.

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)  
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Database Setup](#-database-setup)
- [Usage](#-usage)
- [Algorithm Details](#-algorithm-details)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🔍 **Advanced Search Capabilities**
- **Keyword-based CV search** dengan multiple keywords
- **Exact pattern matching** menggunakan algoritma KMP dan Boyer-Moore
- **Fuzzy matching** dengan adjustable similarity threshold
- **Case-sensitive/insensitive** search options
- **Real-time search results** dengan performance metrics

### 🎨 **Retro User Interface**
- **Windows 98-style GUI** dengan classic styling
- **Responsive design** yang dapat di-resize
- **Scrollable content** untuk large datasets
- **3D button effects** dan retro color scheme
- **Progress indicators** dan loading animations

### 📊 **Smart CV Management**
- **Dynamic CV loading** dengan user-configurable limits
- **Performance optimization** dengan multi-threading
- **Memory management** untuk large datasets
- **CV summary viewing** dengan structured data display
- **Direct PDF opening** dari aplikasi

### ⚡ **Performance Features**
- **Multi-threaded CV processing** untuk loading speed
- **Caching system** untuk hasil yang lebih cepat
- **Configurable batch sizes** (25-1000+ CVs)
- **Real-time performance metrics** (execution time tracking)
- **Memory usage optimization**

## 📸 Screenshots

### Main Application Window
```
🖥️ ATS - Applicant Tracking System
┌─────────────────────────────────────────────────────┐
│ 📁 CV Digital Pattern Matching System              │
│ Advanced Search & Analysis Tool - Version 1.0       │
├─────────────────────────────────────────────────────┤
│ Search Parameters:                                   │
│ Keywords: python, machine learning, data science    │
│ Algorithm: [Knuth-Morris-Pratt (KMP) ▼]            │
│ Max Results: [10] ☑ Case Sensitive                 │
│ Similarity: [████████░░] 70%                       │
│ [🔍 Search] [🗑️ Clear] [🔄 Reload]                 │
├─────────────────────────────────────────────────────┤
│ Search Results:                                      │
│ ┌─────────────────┐ ┌─────────────────┐            │
│ │ #1 - John Doe   │ │ #2 - Jane Smith │            │
│ │ Score: 15       │ │ Score: 12       │            │
│ │ python (8)      │ │ python (5)      │            │
│ │ [📄][📂]       │ │ [📄][📂]       │            │
│ └─────────────────┘ └─────────────────┘            │
└─────────────────────────────────────────────────────┘
```

### CV Loading Configuration Dialog
```
⚙️ CV Database Loading Configuration
┌─────────────────────────────────────────┐
│ 💾 Database Information                  │
│ 📊 Total CVs: 1,247 files              │
│ ⚡ Performance: More CVs = Better results│
├─────────────────────────────────────────┤
│ 🎯 Select Number of CVs to Load         │
│ Number of CVs: [100] (Maximum: 1,247)   │
│                                         │
│ 🚀 Quick Select:                        │
│ [25 CVs] [50 CVs] [100 CVs]            │
│ [200 CVs] [500 CVs] [All CVs]          │
├─────────────────────────────────────────┤
│ ⚠️ Performance Guide:                   │
│ 🟢 1-50 CVs: Very Fast (~10-20s)      │
│ 🟡 51-200 CVs: Fast (~20-40s)         │
│ 🟠 201-500 CVs: Medium (~40-80s)      │
│ 🔴 500+ CVs: Slower (~80+s)           │
└─────────────────────────────────────────┘
```

## 🔧 Requirements

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Linux Ubuntu 18.04+
- **Python**: 3.12+ (recommended) atau 3.10+
- **RAM**: Minimum 4GB, Recommended 8GB+ untuk dataset besar
- **Storage**: 1GB free space untuk aplikasi dan cache
- **Database**: MySQL 8.0+ atau MariaDB 10.4+

### Python Dependencies
```txt
mysql-connector-python>=8.0.33
PyPDF2>=3.0.1
tkinter (built-in with Python)
pathlib (built-in with Python)
concurrent.futures (built-in with Python)
```

## 🚀 Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/ats-applicant-tracking-system.git
cd ats-applicant-tracking-system
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux  
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install mysql-connector-python PyPDF2
```

### 4. Verify Installation
```bash
python --version  # Should show 3.12+
python -c "import tkinter; print('Tkinter OK')"
python -c "import mysql.connector; print('MySQL connector OK')"
```

## 🗄️ Database Setup

### 1. Install MySQL/MariaDB
```bash
# Windows (dengan chocolatey)
choco install mysql

# macOS (dengan homebrew)
brew install mysql

# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server
```

### 2. Create Database
```sql
-- Login ke MySQL
mysql -u root -p

-- Create database
CREATE DATABASE ats_database CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

```

### 3. Configure Database Connection
Edit file `config.py`:
```python
DATABASE_CONFIG = {
    "host": "localhost",
    "user": "<your username>",  # atau "root"
    "password": "<your_password>",
    "database": "ats_database",
    "port": 3306
}

# Path ke folder data CV
DATA_DIR = "data/cv_files"  # Sesuaikan dengan lokasi CV Anda
```

### 4. Setup Database Schema
```bash
# Jalankan script database setup (jika ada)
python setup_database.py

# Atau import schema manual jika ada file .sql
mysql -u ats_user -p ats_database < schema.sql
```

## 📁 Project Structure

```
ats-applicant-tracking-system/
├── 📄 main.py                 # Entry point aplikasi
├── 📄 config.py               # Konfigurasi database dan paths
├── 📄 requirements.txt        # Python dependencies
├── 📄 README.md              # Dokumentasi ini
├── 📄 LICENSE                # License file
├── 📁 src/                   # Source code utama
│   ├── 📁 database/          # Database connection & queries
│   │   ├── connection.py     # Database connection handler
│   │   └── queries.py        # SQL queries dan database operations
│   ├── 📁 algorithm/         # Pattern matching algorithms
│   │   └── PatternMatcher.py # KMP, Boyer-Moore implementations
│   ├── 📁 pdfprocessor/      # PDF text extraction
│   │   └── pdfExtractor.py   # PDF parsing dan text extraction
│   └── 📁 models/            # Data models
│       └── ResultCard.py     # CV result data structures
├── 📁 data/                  # Data directory
│   └── 📁 cv_files/          # CV/Resume files (PDF)
├── 📁 logs/                  # Application logs
└── 📁 cache/                 # Temporary cache files
```

## ⚙️ Configuration

### Environment Variables (Optional)
```bash
# .env file
ATS_DB_HOST=localhost
ATS_DB_USER=ats_user
ATS_DB_PASSWORD=your_password
ATS_DB_NAME=ats_database
ATS_DATA_DIR=./data/cv_files
ATS_CACHE_DIR=./cache
ATS_LOG_LEVEL=INFO
```


## 🎯 Usage

### 1. Start Application
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run application
python main.py
```

### 2. First Time Setup
1. **CV Loading Dialog** akan muncul
2. **Pilih jumlah CV** yang ingin di-load (25-1000+)
3. **Wait for loading** - progress akan ditampilkan
4. **Ready to search!** - aplikasi siap digunakan

### 3. Basic Search
1. **Enter keywords** separated by commas
   ```
   python, machine learning, data science
   ```
2. **Select algorithm**: KMP atau Boyer-Moore
3. **Adjust settings**: 
   - Max results (1-100)
   - Similarity threshold (0-100%)
   - Case sensitive (yes/no)
4. **Click Search** dan tunggu hasil

### 4. Advanced Features
- **View CV Summary**: Click 📄 button pada result card
- **Open PDF**: Click 📂 button untuk membuka file CV
- **Reload CVs**: Click 🔄 untuk load CV dengan jumlah berbeda
- **Clear Results**: Click 🗑️ untuk clear search results

## 🧮 Algorithm Details

### Exact Pattern Matching

#### **Knuth-Morris-Pratt (KMP)**
- **Time Complexity**: O(n + m)
- **Space Complexity**: O(m)
- **Best for**: General-purpose text search
- **Features**: Optimal for most use cases

#### **Boyer-Moore**  
- **Time Complexity**: O(n/m) best case, O(nm) worst case
- **Space Complexity**: O(σ + m) where σ is alphabet size
- **Best for**: Large texts, English language content
- **Features**: Very fast for natural language text

### Fuzzy Matching
- **Algorithm**: Levenshtein distance-based similarity
- **Configurable threshold**: 0-100% similarity
- **Use case**: Typos, variations, partial matches
- **Performance**: Optimized for CV content analysis

## 🔧 Troubleshooting

### Common Issues

#### ❌ Database Connection Error
```
Error: Unable to connect to database
```
**Solutions:**
1. Check MySQL service is running:
   ```bash
   # Windows
   net start mysql
   
   # macOS  
   brew services start mysql
   
   # Linux
   sudo systemctl start mysql
   ```
2. Verify credentials in `config.py`
3. Test connection manually:
   ```bash
   mysql -u ats_user -p
   ```

#### ❌ PDF Processing Error
```
Error loading CV: Permission denied
```
**Solutions:**
1. Check file permissions:
   ```bash
   chmod 644 data/cv_files/*.pdf  # Linux/macOS
   ```
2. Verify DATA_DIR path in config
3. Ensure PDFs are not corrupted

#### ❌ Memory Issues
```
MemoryError: Unable to allocate memory
```
**Solutions:**
1. Reduce CV loading count
2. Close other applications
3. Increase virtual memory/swap
4. Use 64-bit Python

#### ❌ GUI Display Issues
```
TclError: no display name and no $DISPLAY environment variable
```
**Solutions:**
1. **Linux SSH**: Enable X11 forwarding
   ```bash
   ssh -X username@hostname
   ```
2. **WSL**: Install X server (VcXsrv, Xming)
3. **Docker**: Use `--env DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix`

### Performance Optimization

#### Slow CV Loading
1. **Reduce thread count** if CPU overload:
   ```python
   # In _do_preload method
   with ThreadPoolExecutor(max_workers=2) as pool:  # Reduce from 4
   ```

2. **Process in smaller batches**:
   ```python
   DEFAULT_MAX_CV_LOAD = 50  # Start with smaller number
   ```

#### Search Performance
1. **Use exact matching** when possible (faster than fuzzy)
2. **Limit result count** to reasonable numbers (10-50)
3. **Case-insensitive search** is slightly faster

## 🤝 Contributing

### Development Setup
```bash
# Fork repository dan clone
git clone https://github.com/yourusername/ats-applicant-tracking-system.git
cd ats-applicant-tracking-system

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes dan test
python main.py

# Commit changes
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name

# Create Pull Request
```

### Coding Standards
- **Python Style**: Follow PEP 8
- **Docstrings**: Google-style docstrings
- **Type Hints**: Use type hints untuk functions
- **Error Handling**: Comprehensive try-catch blocks
- **Logging**: Use logging module instead of print

### Testing
```bash
# Run manual tests
python -m pytest tests/  # Jika ada test suite

# Test database connection
python -c "from src.database.connection import DatabaseConnection; db = DatabaseConnection(); print('OK' if db.connect() else 'FAIL')"

# Test PDF processing
python -c "from src.pdfprocessor.pdfExtractor import PDFExtractor; print('PDF OK')"
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 ATS Development Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👥 Authors & Contributors

- **Mahesa Fadhillah Andre** - *13523140* - [@mahesa005](https://github.com/mahesa005)
- **Jonathan Kenan Budianto** - *13523139* - [@jonathankenan](https://github.com/jonathankenan)
- **Lukas Raja Agripa** - *13523158* - [@rlukassa](https://github.com/rlukassa)

## 🔗 Links
- **Demo Video**: [YouTube Link]

## 📊 Project Status

- ✅ **Core Features**: Complete
- ✅ **Pattern Matching**: KMP & Boyer-Moore implemented
- ✅ **GUI Interface**: Retro Windows 98 style complete
- ✅ **Database Integration**: MySQL support complete
- 🟡 **Testing**: In progress
- 🟡 **Documentation**: In progress
- ⭕ **CI/CD Pipeline**: Planned
- ⭕ **Web Interface**: Future enhancement

---

## 🎉 Quick Start Summary

```bash
# 1. Clone & Setup
git clone <repo-url>
cd ats-applicant-tracking-system
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Install & Configure
pip install -r doc/requirement.txt
# Edit config.py with your database settings

# 3. Run
python main.py

# 4. First use
# - Select CV count in dialog
# - Wait for loading
# - Start searching!
```

**Happy CV Searching! 🔍✨**
