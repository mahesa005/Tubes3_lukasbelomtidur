# ===== src/gui/styles.py =====
"""
Styles dan Tema untuk aplikasi ATS
Tujuan: Sentralisasi styling untuk konsistensi UI
"""

# Stylesheet tema gelap modern
DARK_THEME = """
QMainWindow {
    background-color: #2b2b2b;
    color: #ffffff;
}

QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
}

QPushButton {
    background-color: #404040;
    border: 1px solid #555555;
    border-radius: 5px;
    padding: 8px 15px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #505050;
    border-color: #777777;
}

QPushButton:pressed {
    background-color: #353535;
}

QLineEdit {
    background-color: #404040;
    border: 1px solid #555555;
    border-radius: 3px;
    padding: 5px;
}

QLineEdit:focus {
    border-color: #0078d4;
}

QTextEdit {
    background-color: #404040;
    border: 1px solid #555555;
    border-radius: 3px;
}

QScrollArea {
    background-color: #353535;
    border: none;
}

QLabel {
    color: #ffffff;
}

QGroupBox {
    font-weight: bold;
    border: 1px solid #555555;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}
"""

# Stylesheet tema terang
LIGHT_THEME = """
QMainWindow {
    background-color: #ffffff;
    color: #000000;
}

QWidget {
    background-color: #ffffff;
    color: #000000;
}

QPushButton {
    background-color: #f0f0f0;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 8px 15px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #e0e0e0;
    border-color: #999999;
}

QPushButton:pressed {
    background-color: #d0d0d0;
}

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 3px;
    padding: 5px;
}

QLineEdit:focus {
    border-color: #0078d4;
}

QTextEdit {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 3px;
}

QScrollArea {
    background-color: #f5f5f5;
    border: none;
}
"""

def applyTheme(app, theme='dark'):
    """
    Terapkan tema ke aplikasi

    Args:
        app (QApplication): Instance aplikasi Qt
        theme (str): Nama tema ('dark' atau 'light')
    """
    if theme == 'dark':
        app.setStyleSheet(DARK_THEME)
    else:
        app.setStyleSheet(LIGHT_THEME)