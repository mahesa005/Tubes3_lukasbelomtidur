# ===== styles.py =====
DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}
QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
}
QPushButton {
    background-color: #3c3c3c;
    color: white;
    border-radius: 8px;
    padding: 8px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #505050;
}
QLineEdit, QTextEdit, QSpinBox {
    background-color: #404040;
    border: 1px solid #666;
    padding: 5px;
    border-radius: 5px;
    color: #ffffff;
}
QGroupBox {
    border: 1px solid #555;
    border-radius: 5px;
    margin-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
    font-weight: bold;
}
"""

LIGHT_THEME = """ QMainWindow {
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
    if theme == 'dark':
        app.setStyleSheet(DARK_THEME)
    else:
        app.setStyleSheet(LIGHT_THEME)

