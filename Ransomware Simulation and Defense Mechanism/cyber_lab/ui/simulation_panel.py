from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                                 QProgressBar, QFileDialog, QMessageBox, QHBoxLayout)
from PySide6.QtCore import Qt, QThread, Signal
import time
import threading

class SimulationWorker(QThread):
    progress = Signal(int)
    finished = Signal()
    log = Signal(str)

    def __init__(self, engine, key, mode="encrypt"):
        super().__init__()
        self.engine = engine
        self.key = key
        self.mode = mode

    def run(self):
        if self.mode == "encrypt":
            self.engine.encrypt_sandbox(self.key, self.progress.emit)
        else:
            self.engine.decrypt_sandbox(self.key, self.progress.emit)
        self.finished.emit()

class SimulationPanel(QWidget):
    def __init__(self, sandbox_manager, key_manager, encryption_engine, decryption_engine, backup_engine, integrity_checker, simulator=None, threat_intel=None, mfa_auth=None, rbac=None, audit=None):
        super().__init__()
        self.sandbox = sandbox_manager
        self.keys = key_manager
        self.encryptor = encryption_engine
        self.decryptor = decryption_engine
        self.backup = backup_engine
        self.integrity = integrity_checker
        self.simulator = simulator
        self.threat_intel = threat_intel
        self.mfa = mfa_auth
        self.rbac = rbac
        self.audit = audit
        
        layout = QVBoxLayout()
        layout.setSpacing(20) # Standardized spacing for visibility
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("Simulation Control")
        header.setObjectName("Header")
        layout.addWidget(header)

        # Sandbox Controls
        sb_layout = QHBoxLayout()
        self.path_lbl = QLabel(f"Target: {self.sandbox.sandbox_path}")
        sb_layout.addWidget(self.path_lbl)
        
        reset_btn = QPushButton("Reset Sandbox")
        reset_btn.clicked.connect(self.reset_sandbox)
        sb_layout.addWidget(reset_btn)
        layout.addLayout(sb_layout)

        # Actions
        # Actions
        self.encrypt_btn = QPushButton("🚀 Launch Ransomware Attack")
        self.encrypt_btn.setObjectName("RunButton")
        self.encrypt_btn.clicked.connect(self.start_encryption)
        layout.addWidget(self.encrypt_btn)

        self.decrypt_btn = QPushButton("🔓 Decrypt & Restore")
        self.decrypt_btn.clicked.connect(self.start_decryption)
        layout.addWidget(self.decrypt_btn)

        # Advanced Controls
        adv_layout = QHBoxLayout()
        
        self.backup_btn = QPushButton("💾 Create Snapshot")
        self.backup_btn.clicked.connect(self.create_backup)
        adv_layout.addWidget(self.backup_btn)

        self.integrity_btn = QPushButton("🔍 Check Integrity")
        self.integrity_btn.clicked.connect(self.check_integrity)
        adv_layout.addWidget(self.integrity_btn)
        
        layout.addLayout(adv_layout)

        # Progress
        self.pbar = QProgressBar()
        layout.addWidget(self.pbar)

        self.status_lbl = QLabel("Ready")
        layout.addWidget(self.status_lbl)

        self.setLayout(layout)

    def reset_sandbox(self):
        self.sandbox.create_mock_files()
        self.status_lbl.setText("Sandbox reset with mock files.")

    def start_encryption(self):
        if self.rbac and not self.rbac.can("attack"):
            QMessageBox.critical(self, "Unauthorized", "Your role does not have permission to launch attacks.")
            if self.audit:
                self.audit.log_event(self.rbac.current_user, "UNAUTHORIZED_ATTACK_ATTEMPT", "User tried but failed RBAC check.")
            return

        if self.audit:
            self.audit.log_event(self.rbac.current_user, "ATTACK_START", "Encryption sequence initiated.")
            
        key = self.keys.load_key()
        # Use simulator if available, otherwise fallback
        if hasattr(self, 'simulator') and self.simulator:
            # For now, default to 'burst' for "Launch Attack"
            # In future iterations, we can add a combo box for mode selection
            self.status_lbl.setText("Starting Burst Attack Simulation...")
            # We need to run this in a thread to not block UI, 
            # modifying SimulationWorker to handle simulator would be best.
            # For simplicity in this step, I'll launch a thread that calls simulator.
            self.thread = threading.Thread(target=self.simulator.simulate_attack, args=(key, "burst", self.pbar.setValue))
            self.thread.start()
        else:
            self.worker = SimulationWorker(self.encryptor, key, "encrypt")
            self.worker.progress.connect(self.pbar.setValue)
            self.worker.finished.connect(lambda: self.status_lbl.setText("Encryption Complete!"))
            self.worker.start()
            self.status_lbl.setText("Encrypting...")

    def start_decryption(self):
        if self.rbac and not self.rbac.can("restore"):
            QMessageBox.critical(self, "Unauthorized", "Your role does not have permission to restore files.")
            return

        # MFA Check
        if self.mfa and self.mfa.enabled:
            from PySide6.QtWidgets import QInputDialog, QLineEdit
            token, ok = QInputDialog.getText(self, "MFA Verification", 
                                           "Enter 6-digit Authenticator Code:", 
                                           QLineEdit.Password)
            if not ok:
                return
            if not self.mfa.verify_token(token):
                QMessageBox.critical(self, "Access Denied", "Invalid MFA Token!")
                return

        if self.audit:
            self.audit.log_event(self.rbac.current_user, "RESTORE_START", "Decryption/MFA passed.")
            
        key = self.keys.load_key()
        self.worker = SimulationWorker(self.decryptor, key, "decrypt")
        self.worker.progress.connect(self.pbar.setValue)
        self.worker.finished.connect(lambda: self.status_lbl.setText("Decryption Complete!"))
        self.worker.start()
        self.status_lbl.setText("Decrypting...")

    def create_backup(self):
        path = self.backup.create_snapshot()
        if path:
            self.status_lbl.setText(f"Snapshot created at {path}")
        else:
            self.status_lbl.setText("Snapshot failed!")

    def check_integrity(self):
        self.integrity.establish_baseline()
        compromised = self.integrity.check_integrity()
        if not compromised:
            self.status_lbl.setText("Integrity Verified: System Secure")
        else:
            self.status_lbl.setText(f"dANGER: {len(compromised)} files compromised!")
