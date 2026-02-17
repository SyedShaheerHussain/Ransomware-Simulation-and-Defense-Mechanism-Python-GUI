import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                               QPushButton, QStackedWidget, QFrame, QLabel, QScrollArea)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSizePolicy

from .styles import NEON_STYLE
from .animations import ParticleNetwork, ScanlineOverlay
from .overlays import EducationOverlay
from .dashboard import Dashboard
from .simulation_panel import SimulationPanel
from .defense_panel import DefensePanel
from .report_panel import ReportPanel
from .cyber_range_panel import CyberRangePanel
from .key_panel import KeyPanel
from .forensics_panel import ForensicsPanel

class MainWindow(QMainWindow):
    def __init__(self, core_modules):
        super().__init__()
        self.core = core_modules
        
        self.setWindowTitle("CyberLab: Ransomware Defense Simulator")
        self.resize(1100, 750)
        self.setStyleSheet(NEON_STYLE)

        # Main Layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Background Animations (Overlay)
        # We need a container that holds the particle widget UNDER the content?
        # Actually easier to put it inside the content stack or as a dedicated overlay.
        # For this setup, let's put it on top of central widget but transparent.
        # However, simple layouts are robust. Let's just modify the layout structure.
        
        # Sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Content Area with Scroll Support
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.content_stack = QStackedWidget()
        self.content_stack.setContentsMargins(10, 30, 10, 10) # Added top margin
        self.scroll_area.setWidget(self.content_stack)
        
        main_layout.addWidget(self.scroll_area)

        # Initialize Pages
        self.dashboard = Dashboard()
        self.simulation = SimulationPanel(
            self.core['sandbox'], 
            self.core['keys'], 
            self.core['encryption'], 
            self.core['decryption'],
            self.core.get('backup'),
            self.core.get('integrity'),
            self.core.get('simulator'),
            self.core.get('threat_intel'),
            self.core.get('mfa'),
            self.core.get('rbac'),
            self.core.get('audit')
        )
        self.defense = DefensePanel(
            self.core['monitor'], 
            self.core['defense'],
            self.core['logger'],
            self.core.get('threat_intel')
        )
        self.report_panel = ReportPanel(
            self.core['report_gen'],
            self.core['metrics']
        )

        self.content_stack.addWidget(self.dashboard)
        self.content_stack.addWidget(self.simulation)
        self.content_stack.addWidget(self.defense)
        self.content_stack.addWidget(self.report_panel)
        
        self.cyber_range_panel = CyberRangePanel(
            self.core['cyber_range'],
            self.core['net_sim'],
            self.core['social_eng']
        )
        self.content_stack.addWidget(self.cyber_range_panel)

        self.key_panel = KeyPanel(
            self.core['keys'],
            self.core['mfa']
        )
        self.content_stack.addWidget(self.key_panel)

        self.forensics_panel = ForensicsPanel(
            self.core['pen_test'],
            self.core['forensics']
        )
        self.content_stack.addWidget(self.forensics_panel)

        self.setCentralWidget(main_widget)
        
        # Scanlines (Top Overlay)
        self.scanlines = ScanlineOverlay(self)
        self.scanlines.resize(self.size())
        self.scanlines.raise_()
        self.scanlines.show()

        # Education Overlay
        self.overlay = EducationOverlay(self)
        self.overlay.move(self.width() - 320, self.height() - 120) # Bottom Right
        self.overlay.show_message("Welcome", "CyberLab initialized. Select a Sandbox to begin.")

    def resizeEvent(self, event):
        if hasattr(self, 'scanlines'):
            self.scanlines.resize(self.size())
        if hasattr(self, 'overlay'):
            self.overlay.move(self.width() - 320, self.height() - 120)
        super().resizeEvent(event)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("SideBar")
        sidebar.setFixedWidth(250)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(10)

        # App Title
        title = QLabel("🛡️ CYBER LAB")
        title.setStyleSheet("color: #00ffea; font-size: 22px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # User Profile Indicator
        user_info = QFrame()
        user_info.setStyleSheet("background-color: rgba(0, 255, 234, 0.05); border-radius: 5px; padding: 5px; border: 1px solid rgba(0, 255, 234, 0.1);")
        user_layout = QVBoxLayout(user_info)
        
        user_rbac = self.core.get('rbac')
        name = user_rbac.current_user if user_rbac else "Unknown"
        role = user_rbac.current_role if user_rbac else "N/A"
        
        user_lbl = QLabel(f"👤 {name}")
        user_lbl.setStyleSheet("font-weight: bold; color: white;")
        role_lbl = QLabel(f"Role: {role}")
        role_lbl.setStyleSheet("font-size: 11px; color: #00ffea;")
        
        user_layout.addWidget(user_lbl)
        user_layout.addWidget(role_lbl)
        layout.addWidget(user_info)
        layout.addSpacing(10)

        # Nav Buttons
        btn_dash = self.create_nav_btn("📊 Dashboard", 0)
        btn_sim = self.create_nav_btn("🧪 Simulation", 1)
        btn_def = self.create_nav_btn("🛡️ Defense Center", 2)
        btn_rep = self.create_nav_btn("📝 Reports & Ops", 3)
        btn_range = self.create_nav_btn("🎮 Cyber Range", 4)
        btn_keys = self.create_nav_btn("🔑 Key Vault", 5)
        btn_foren = self.create_nav_btn("🔬 Forensic Lab", 6)
        
        layout.addWidget(btn_dash)
        layout.addWidget(btn_sim)
        layout.addWidget(btn_def)
        layout.addWidget(btn_rep)
        layout.addWidget(btn_range)
        layout.addWidget(btn_keys)
        layout.addWidget(btn_foren)

        layout.addStretch()
        
        footer = QLabel("v1.0.0 | Educational Use Only")
        footer.setStyleSheet("color: #555; font-size: 10px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        sidebar.setLayout(layout)
        return sidebar

    def create_nav_btn(self, text, index):
        btn = QPushButton(text)
        btn.setObjectName("NavBtn")
        btn.setCheckable(True)
        btn.clicked.connect(lambda: self.switch_tab(index, btn))
        return btn

    def switch_tab(self, index, active_btn):
        self.content_stack.setCurrentIndex(index)
        # Uncheck all other nav buttons
        for child in self.sidebar.findChildren(QPushButton):
            if child != active_btn and child.objectName() == "NavBtn":
                child.setChecked(False)
        active_btn.setChecked(True)
