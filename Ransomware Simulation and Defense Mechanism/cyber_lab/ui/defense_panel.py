from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QGroupBox, QTextEdit, QPushButton
from PySide6.QtCore import QTimer, Qt

class DefensePanel(QWidget):
    def __init__(self, monitor_engine, defense_system, logger_engine, threat_intel=None):
        super().__init__()
        self.monitor = monitor_engine
        self.defense = defense_system
        self.logger = logger_engine
        self.threat_intel = threat_intel
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("Defense Operations Center")
        header.setObjectName("Header")
        layout.addWidget(header)

        # Controls
        ctrl_group = QGroupBox("Active Protection")
        ctrl_layout = QVBoxLayout()
        
        self.monitor_chk = QCheckBox("Real-time File Monitoring")
        self.monitor_chk.toggled.connect(self.toggle_monitoring)
        ctrl_layout.addWidget(self.monitor_chk)

        self.restore_chk = QCheckBox("Auto-Restore (Backup & Recovery)")
        self.restore_chk.toggled.connect(self.toggle_restore)
        ctrl_layout.addWidget(self.restore_chk)

        self.honeypot_chk = QCheckBox("Deploy Honeypot Traps")
        self.honeypot_chk.toggled.connect(self.toggle_honeypots)
        ctrl_layout.addWidget(self.honeypot_chk)
        
        self.intel_btn = QPushButton("Check Threat Intel Feed")
        self.intel_btn.clicked.connect(self.check_threat_intel)
        ctrl_layout.addWidget(self.intel_btn)
        
        ctrl_group.setLayout(ctrl_layout)
        layout.addWidget(ctrl_group)

        # Live Logs
        log_group = QGroupBox("Security Logs")
        log_layout = QVBoxLayout()
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("background-color: #0f3460; color: #00ff00; font-family: Consolas;")
        log_layout.addWidget(self.log_view)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        # AI Stats
        ai_group = QGroupBox("AI Anomaly Engine")
        ai_layout = QHBoxLayout()
        
        self.risk_lbl = QLabel("Risk Score: 0%")
        self.risk_lbl.setStyleSheet("color: white; font-weight: bold;")
        ai_layout.addWidget(self.risk_lbl)
        
        self.baseline_lbl = QLabel("Baseline: Learning...")
        self.baseline_lbl.setStyleSheet("color: #f39c12;")
        ai_layout.addWidget(self.baseline_lbl)
        
        ai_group.setLayout(ai_layout)
        layout.addWidget(ai_group)

        # Alert Box
        self.alert_box = QLabel("SYSTEM SECURE")
        self.alert_box.setAlignment(Qt.AlignCenter)
        self.alert_box.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px; border-radius: 5px; font-weight: bold;")
        layout.addWidget(self.alert_box)

        self.setLayout(layout)

        # Timer to update logs
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_logs)
        self.timer.timeout.connect(self.update_ai_stats)
        self.timer.start(1000)

    def update_ai_stats(self):
        # Update Risk Score
        if hasattr(self.defense, 'risk_score'):
            score = self.defense.risk_score
            self.risk_lbl.setText(f"Risk Score: {int(score*100)}%")
            
            if score > 0.75:
                self.risk_lbl.setStyleSheet("color: #e74c3c; font-weight: bold;") # Red
            elif score > 0.4:
                self.risk_lbl.setStyleSheet("color: #f39c12; font-weight: bold;") # Orange
            else:
                self.risk_lbl.setStyleSheet("color: #2ecc71; font-weight: bold;") # Green

        # Update Baseline Status
        if hasattr(self.defense, 'baseline_status'):
            status = self.defense.baseline_status
            self.baseline_lbl.setText(f"Baseline: {status}")
            
            if status == "Active":
                self.baseline_lbl.setStyleSheet("color: #2ecc71;") 
            else:
                self.baseline_lbl.setStyleSheet("color: #f39c12;")

    def check_threat_intel(self):
        if self.threat_intel:
            summary = self.threat_intel.get_feed_summary()
            self.log_view.append(f"[INTEL] Connected to {summary['source']}")
            self.log_view.append(f"[INTEL] Loaded {summary['total_signatures']} signatures.")
            self.alert_box.setText("Threat Intelligence Feed Active")
            self.alert_box.setStyleSheet("background-color: #0f3460; color: #00ff00; padding: 10px; border-radius: 5px;")
        else:
            self.log_view.append("[INTEL] Threat Intelligence Module skipped")

    def toggle_monitoring(self, checked):
        if checked:
            self.monitor.start_monitoring()
            self.log_view.append("[SYSTEM] Monitoring ENABLED")
        else:
            self.monitor.stop_monitoring()
            self.log_view.append("[SYSTEM] Monitoring DISABLED")

    def toggle_restore(self, checked):
        self.defense.set_auto_restore(checked)
        status = "ENABLED" if checked else "DISABLED"
        self.log_view.append(f"[SYSTEM] Auto-Restore {status}")

    def toggle_honeypots(self, checked):
        if checked:
            self.defense.enable_honeypots()
            self.log_view.append("[SYSTEM] Honeypots DEPLOYED")
        else:
            self.log_view.append("[SYSTEM] Honeypot deployment cannot be undone in this version.")

    def update_logs(self):
        # Update logs from file
        logs = self.logger.get_logs(10)
        self.log_view.clear()
        for line in logs:
            self.log_view.append(line.strip())
        
        # Check defense status
        if self.defense.alarm_triggered:
            self.alert_box.setText("⚠️ RANSOMWARE ACTIVITY DETECTED!")
            self.alert_box.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px; border-radius: 5px; font-weight: bold; animation: blink 1s infinite;")
        else:
            self.alert_box.setText("SYSTEM SECURE")
            self.alert_box.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px; border-radius: 5px; font-weight: bold;")
