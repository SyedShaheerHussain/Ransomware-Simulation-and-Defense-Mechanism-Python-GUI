from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                                 QPushButton, QGroupBox, QListWidget, QTextEdit, QMessageBox)
from PySide6.QtCore import Qt

class ForensicsPanel(QWidget):
    def __init__(self, pen_test, forensics):
        super().__init__()
        self.pen_test = pen_test
        self.forensics = forensics
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("Forensic Lab & Penetration Testing")
        header.setObjectName("Header")
        layout.addWidget(header)

        # 1. Pen-Testing Section
        pen_group = QGroupBox("Penetration Test Simulation (Offensive)")
        pen_layout = QVBoxLayout()
        
        self.scan_btn = QPushButton("🔍 Run Vulnerability Scan")
        self.scan_btn.clicked.connect(self.run_scan)
        pen_layout.addWidget(self.scan_btn)
        
        self.finding_list = QListWidget()
        self.finding_list.setFixedHeight(120)
        pen_layout.addWidget(QLabel("Scan Findings:"))
        pen_layout.addWidget(self.finding_list)
        
        self.exploit_btn = QPushButton("☣️ Launch Simulated Exploit")
        self.exploit_btn.clicked.connect(self.run_exploit)
        self.exploit_btn.setStyleSheet("background-color: #ff0055; color: white;")
        pen_layout.addWidget(self.exploit_btn)
        
        pen_group.setLayout(pen_layout)
        layout.addWidget(pen_group)

        # 2. Forensics Section
        for_group = QGroupBox("Digital Forensics (Defensive)")
        for_layout = QVBoxLayout()
        
        self.mem_btn = QPushButton("💾 Capture Memory Artifacts")
        self.mem_btn.clicked.connect(self.capture_mem)
        for_layout.addWidget(self.mem_btn)
        
        self.forensic_log = QTextEdit()
        self.forensic_log.setReadOnly(True)
        self.forensic_log.setStyleSheet("background-color: #0b0c15; color: #00ffea; font-family: 'Consolas';")
        for_layout.addWidget(self.forensic_log)
        
        for_group.setLayout(for_layout)
        layout.addWidget(for_group)

        layout.addStretch()
        self.setLayout(layout)

    def run_scan(self):
        results = self.pen_test.run_scan()
        self.finding_list.clear()
        for f in results['findings']:
            item = f"[{f['severity']}] {f['name']} ({f['id']})"
            self.finding_list.addItem(item)
        
        QMessageBox.information(self, "Scan Complete", f"Scan finished. Found {len(results['findings'])} potential issues.\nThreat Score: {results['threat_score']}")

    def run_exploit(self):
        item = self.finding_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Missing Target", "Please select a finding from the scan results first.")
            return
            
        vuln_id = item.text().split('(')[-1].strip(')')
        success, msg = self.pen_test.simulate_exploit(vuln_id)
        
        if success:
            QMessageBox.critical(self, "EXPLOIT SUCCESS", msg)
        else:
            QMessageBox.information(self, "Attack Blocked", msg)

    def capture_mem(self):
        artifacts = self.forensics.generate_memory_dump()
        self.forensic_log.append(f"\n--- Forensic Dump {artifacts['dump_id']} ---")
        self.forensic_log.append(f"Suspicious Strings: {', '.join(artifacts['suspicious_strings'])}")
        self.forensic_log.append(f"I/O Anomalies: {', '.join(artifacts['io_patterns'])}")
        self.forensic_log.append("Analysis Complete: Key artifacts found in memory.")
