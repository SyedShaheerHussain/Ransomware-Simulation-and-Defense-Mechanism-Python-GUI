from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                                 QPushButton, QGroupBox, QLineEdit, QListWidget, QMessageBox)
from PySide6.QtCore import Qt, QTimer
# import qrcode # Optional, if we want to show QR code for MFA

class KeyPanel(QWidget):
    def __init__(self, key_manager, mfa_auth):
        super().__init__()
        self.keys = key_manager
        self.mfa = mfa_auth
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Advanced Key Management & Identity")
        header.setObjectName("Header")
        layout.addWidget(header)

        # 1. Key Lifecycle
        key_group = QGroupBox("Encryption Key Lifecycle")
        key_layout = QVBoxLayout()
        
        status_layout = QHBoxLayout()
        self.key_status_lbl = QLabel("Status: Checking...")
        self.key_age_lbl = QLabel("Age: 0s")
        status_layout.addWidget(self.key_status_lbl)
        status_layout.addWidget(self.key_age_lbl)
        key_layout.addLayout(status_layout)
        
        self.rotate_btn = QPushButton("🔄 Rotate Key (Archive Current)")
        self.rotate_btn.clicked.connect(self.rotate_key)
        self.rotate_btn.setStyleSheet("background-color: #f39c12; color: white; padding: 8px;")
        key_layout.addWidget(self.rotate_btn)
        
        self.archive_list = QListWidget()
        self.archive_list.setFixedHeight(100)
        key_layout.addWidget(QLabel("Archived Keys:"))
        key_layout.addWidget(self.archive_list)
        
        key_group.setLayout(key_layout)
        layout.addWidget(key_group)

        # 2. MFA Setup
        mfa_group = QGroupBox("Multi-Factor Authentication (MFA)")
        mfa_layout = QVBoxLayout()
        
        self.mfa_status_lbl = QLabel("MFA Status: DISABLED")
        self.mfa_status_lbl.setStyleSheet("color: #e74c3c; font-weight: bold;")
        mfa_layout.addWidget(self.mfa_status_lbl)
        
        self.enable_mfa_btn = QPushButton("Enable MFA (Simulate)")
        self.enable_mfa_btn.clicked.connect(self.enable_mfa)
        mfa_layout.addWidget(self.enable_mfa_btn)
        
        # Simulation Helper
        self.token_display = QLabel("Current Token: ---")
        self.token_display.setStyleSheet("font-family: Consolas; font-size: 16px; color: #4ecca3;")
        mfa_layout.addWidget(self.token_display)
        
        mfa_group.setLayout(mfa_layout)
        layout.addWidget(mfa_group)

        # 3. MFA Verification Test
        test_group = QGroupBox("Unlock / Decrypt Test")
        test_layout = QHBoxLayout()
        
        self.mfa_input = QLineEdit()
        self.mfa_input.setPlaceholderText("Enter 6-digit code")
        
        self.verify_btn = QPushButton("Verify & Unlock")
        self.verify_btn.clicked.connect(self.verify_code)
        
        test_layout.addWidget(self.mfa_input)
        test_layout.addWidget(self.verify_btn)
        test_group.setLayout(test_layout)
        layout.addWidget(test_group)

        layout.addStretch()
        self.setLayout(layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)

    def update_ui(self):
        # Keys
        status, age = self.keys.get_key_status()
        self.key_status_lbl.setText(f"Key Status: {status}")
        self.key_age_lbl.setText(f"Age: {age}")
        
        if status == "Expired":
             self.key_status_lbl.setStyleSheet("color: #e74c3c; font-weight: bold;")
        else:
             self.key_status_lbl.setStyleSheet("color: #27ae60; font-weight: bold;")

        # MFA
        if self.mfa.enabled:
            self.mfa_status_lbl.setText("MFA Status: ENABLED")
            self.mfa_status_lbl.setStyleSheet("color: #27ae60; font-weight: bold;")
            self.enable_mfa_btn.setEnabled(False)
            
            # Show token for convenience in sim
            token = self.mfa.generate_current_token()
            self.token_display.setText(f"Current Token (Sim): {token}")
        
        # Archives
        # (Optimization: Don't reload list every second in real app)
        if self.archive_list.count() == 0: 
             self.refresh_archives()

    def rotate_key(self):
        self.keys.generate_key()
        self.refresh_archives()
        QMessageBox.information(self, "Success", "Key Rotated Successfully!")

    def refresh_archives(self):
        self.archive_list.clear()
        for k in self.keys.list_archived_keys():
            self.archive_list.addItem(k)

    def enable_mfa(self):
        secret = self.mfa.enable_mfa()
        QMessageBox.information(self, "MFA Enabled", f"MFA is now active.\nSecret: {secret}\n\n(See 'Current Token' for codes)")

    def verify_code(self):
        code = self.mfa_input.text()
        if self.mfa.verify_token(code):
            QMessageBox.information(self, "Access Granted", "Identity Verified! Decryption Authenticated.")
        else:
            QMessageBox.warning(self, "Access Denied", "Invalid Token! Access Blocked.")
