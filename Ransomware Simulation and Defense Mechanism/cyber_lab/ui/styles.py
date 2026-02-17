
NEON_STYLE = """
/* GLOBAL WINDOW AND WIDGETS */
QMainWindow {
    background-color: #0b0c15; /* Deep Void Dark */
}

QWidget {
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
    color: #e0e0e0;
}

QFrame#SideBar {
    background-color: rgba(16, 20, 30, 0.95);
    border-right: 1px solid rgba(0, 255, 234, 0.1); 
}

/* BUTTONS */
QPushButton {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 12px;
    color: #bdc3c7;
    text-align: left;
    font-weight: 500;
}

QPushButton:hover {
    background-color: rgba(0, 255, 234, 0.1); /* Neon Cyan Tint */
    border: 1px solid rgba(0, 255, 234, 0.5);
    color: #ffffff;
}

QPushButton:pressed {
    background-color: rgba(0, 255, 234, 0.2);
}

QPushButton:disabled {
    background-color: #1a1a2e;
    color: #555;
    border: 1px dashed #333;
}

/* NAV BUTTONS (SIDEBAR) */
QPushButton#NavBtn {
    border: none;
    padding-left: 20px;
    font-size: 15px;
}
QPushButton#NavBtn:checked {
    background-color: rgba(0, 255, 234, 0.15);
    border-left: 4px solid #00ffea;
    color: #00ffea;
    font-weight: bold;
}

/* ACTION BUTTONS (Hero) */
QPushButton#HeroBtn {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff0055, stop:1 #ff2e63);
    border: none;
    color: white;
    font-weight: bold;
    font-size: 15px;
    text-transform: uppercase;
}
QPushButton#HeroBtn:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff2e63, stop:1 #e94560);
    border: 1px solid #ff99aa;
}

/* GROUP BOXES & PANELS */
QGroupBox {
    border: 1px solid rgba(0, 255, 234, 0.4);
    border-radius: 10px;
    margin-top: 50px; /* Increased margin to prevent clipping at panel tops */
    padding-top: 30px; /* More space between title and content */
    background-color: #0d0f1a;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 25px;
    top: 5px; /* Pushing title DOWN into the margin for better visibility */
    padding: 4px 15px;
    color: #00ffea;
    font-weight: bold;
    font-size: 15px;
    background-color: #0d0f1a; /* Match groupbox bg better */
    border: 1px solid rgba(0, 255, 234, 0.3);
    border-radius: 5px;
}

/* SCROLL AREA FIX (SOLID DARK BACKGROUND) */
QScrollArea {
    background-color: #0b0c15;
    border: none;
}
QScrollArea > QWidget > QWidget {
    background-color: #0b0c15; /* Ensure content stack isn't white */
}

/* LIST WIDGETS */
QListWidget {
    background-color: #07080d;
    border: 1px solid rgba(0, 255, 234, 0.2);
    border-radius: 6px;
    color: #ffffff;
    padding: 5px;
    outline: none;
}
QListWidget::item {
    padding: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}
QListWidget::item:selected {
    background-color: rgba(0, 255, 234, 0.15);
    color: #ffffff;
    border-left: 5px solid #00ffea;
}

/* PROGRESS BARS */
QProgressBar {
    border: 1px solid #1a1a2e;
    border-radius: 8px;
    background-color: #05050a;
    text-align: center;
    color: #fff;
    font-weight: bold;
    height: 30px;
}
QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00ffea, stop:1 #00aaaa);
    border-radius: 6px;
}

/* LABELS (EXPLICIT COLORING) */
QLabel {
    color: #e0e0e0;
}
QLabel#Header {
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 32px;
    font-weight: 900;
    color: #ffffff;
    margin-top: 10px; /* Added clearance */
    margin-bottom: 25px;
}
QLabel#SubHeader {
    color: #00ffea;
    font-size: 16px;
    margin-bottom: 12px;
    font-weight: 500;
}

/* TEXT INPUTS */
QLineEdit, QTextEdit {
    background-color: #05050a;
    border: 1px solid #1f1f3a;
    border-radius: 6px;
    color: #00ffea;
    padding: 10px;
    selection-background-color: #ff0055;
    outline: none;
}
QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #00ffea;
}

/* SCROLLBARS */
QScrollBar:vertical {
    border: none;
    background: #0b0c15;
    width: 14px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #1f1f3a;
    min-height: 30px;
    border-radius: 7px;
    margin: 3px;
}
QScrollBar::handle:vertical:hover {
    background: #00ffea;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    border: none;
    background: #0b0c15;
    height: 14px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background: #1f1f3a;
    min-width: 30px;
    border-radius: 7px;
    margin: 3px;
}
QScrollBar::handle:horizontal:hover {
    background: #00ffea;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""
