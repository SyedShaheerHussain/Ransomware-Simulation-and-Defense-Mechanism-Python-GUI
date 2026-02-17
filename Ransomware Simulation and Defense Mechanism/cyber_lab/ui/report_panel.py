from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                                 QPushButton, QGroupBox, QTextEdit, QProgressBar)
from PySide6.QtCore import Qt, QTimer
import json

class ReportPanel(QWidget):
    def __init__(self, report_generator, metrics_engine):
        super().__init__()
        self.report_gen = report_generator
        self.metrics = metrics_engine
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Enterprise Reporting & Analytics")
        header.setObjectName("Header")
        layout.addWidget(header)

        # Live Metrics Dashboard
        metrics_group = QGroupBox("Live System Telemetry")
        metrics_layout = QHBoxLayout()
        
        self.enc_rate_lbl = self._create_metric_lbl("Encryption Rate: 0.0 file/s")
        self.cpu_lbl = self._create_metric_lbl("CPU Load: 0%")
        self.ram_lbl = self._create_metric_lbl("RAM Usage: 0%")
        self.rto_lbl = self._create_metric_lbl("Est. RTO: N/A")
        
        metrics_layout.addWidget(self.enc_rate_lbl)
        metrics_layout.addWidget(self.cpu_lbl)
        metrics_layout.addWidget(self.ram_lbl)
        metrics_layout.addWidget(self.rto_lbl)
        
        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)

        # Actions
        btn_group = QGroupBox("Incident Response")
        btn_layout = QHBoxLayout()
        
        self.gen_report_btn = QPushButton("Generate Forensic Report")
        self.gen_report_btn.clicked.connect(self.generate_report)
        self.gen_report_btn.setStyleSheet("""
            QPushButton {
                background-color: #e94560; color: white; padding: 10px;
                border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background-color: #c0392b; }
        """)
        btn_layout.addWidget(self.gen_report_btn)
        
        btn_group.setLayout(btn_layout)
        layout.addWidget(btn_group)

        # Report Viewer
        self.report_view = QTextEdit()
        self.report_view.setReadOnly(True)
        self.report_view.setPlaceholderText("Generated reports will appear here...")
        self.report_view.setStyleSheet("background-color: #0f3460; color: #e0e0e0; font-family: Consolas;")
        layout.addWidget(self.report_view)

        self.setLayout(layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(1000)

    def _create_metric_lbl(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("background-color: #16213e; color: #4ecca3; padding: 10px; border-radius: 5px; font-weight: bold; border: 1px solid #0f3460;")
        lbl.setAlignment(Qt.AlignCenter)
        return lbl

    def update_metrics(self):
        if self.metrics:
            m = self.metrics.get_metrics()
            self.enc_rate_lbl.setText(f"Enc Rate: {m['encryption_rate']}")
            self.cpu_lbl.setText(f"CPU: {m['cpu']}")
            self.ram_lbl.setText(f"RAM: {m['ram']}")
            
            # Simple RTO calc
            total = m['files_total']
            if total > 0:
                self.rto_lbl.setText(f"Impact: {total} files")
            else:
                self.rto_lbl.setText("System Healthy")

    def generate_report(self):
        # Mock stats for now, ideally passed from controller
        stats = {
            "encrypted_count": 0, # Should get from Metrics
            "defense_metrics": {"alerts": 0} 
        }
        if self.metrics:
            stats["encrypted_count"] = self.metrics.files_encrypted_total
            
        try:
            path = self.report_gen.generate_report(f"MANUAL_{int(QTimer.curr_time if hasattr(QTimer, 'curr_time') else 0)}", stats)
            self.report_view.append(f"Report Generated: {path}")
            self.report_view.append("-" * 30)
            
            # Preview (HTML is hard to show in QTextEdit, just show done)
            self.report_view.append("HTML Report saved. Open in browser to view timeline and graphs.")
            
        except Exception as e:
            self.report_view.append(f"Error generating report: {str(e)}")
