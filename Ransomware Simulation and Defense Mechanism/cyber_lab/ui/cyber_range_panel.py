from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                                 QPushButton, QGroupBox, QProgressBar)
from PySide6.QtCore import Qt, QTimer

class CyberRangePanel(QWidget):
    def __init__(self, cyber_range, net_sim, social_eng):
        super().__init__()
        self.range_mode = cyber_range
        self.net_sim = net_sim
        self.social_eng = social_eng
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Cyber Range & Gamification")
        header.setObjectName("Header")
        layout.addWidget(header)

        # Scoreboard
        score_board = QGroupBox("Live Scoreboard (Red vs Blue)")
        sb_layout = QHBoxLayout()
        
        self.red_lbl = QLabel("RED TEAM: 0")
        self.red_lbl.setStyleSheet("color: #e74c3c; font-size: 24px; font-weight: bold;")
        
        self.vs_lbl = QLabel("VS")
        self.vs_lbl.setStyleSheet("color: #aaa; font-size: 18px;")
        
        self.blue_lbl = QLabel("BLUE TEAM: 0")
        self.blue_lbl.setStyleSheet("color: #3498db; font-size: 24px; font-weight: bold;")
        
        sb_layout.addWidget(self.blue_lbl)
        sb_layout.addWidget(self.vs_lbl)
        sb_layout.addWidget(self.red_lbl)
        score_board.setLayout(sb_layout)
        layout.addWidget(score_board)

        # Controls
        ctrl_group = QGroupBox("Simulation Controls")
        ctrl_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Range Round (60s)")
        self.start_btn.clicked.connect(self.start_round)
        self.start_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; font-weight: bold;")
        
        self.phish_btn = QPushButton("Test Awareness (Phishing)")
        self.phish_btn.clicked.connect(self.test_phishing)
        self.phish_btn.setStyleSheet("background-color: #e67e22; color: white; padding: 10px;")

        ctrl_layout.addWidget(self.start_btn)
        ctrl_layout.addWidget(self.phish_btn)
        ctrl_group.setLayout(ctrl_layout)
        layout.addWidget(ctrl_group)

        # Network Viz (Placeholder text for now)
        net_group = QGroupBox("Network Traffic Simulator")
        net_layout = QVBoxLayout()
        self.net_log = QLabel("Waiting for traffic...")
        self.net_log.setStyleSheet("font-family: Consolas; color: #00ff00; background-color: black; padding: 10px;")
        net_layout.addWidget(self.net_log)
        net_group.setLayout(net_layout)
        layout.addWidget(net_group)

        # Timer Display
        self.time_lbl = QLabel("Time Left: 0s")
        self.time_lbl.setAlignment(Qt.AlignCenter)
        self.time_lbl.setStyleSheet("font-size: 18px; color: white;")
        layout.addWidget(self.time_lbl)

        layout.addStretch()
        self.setLayout(layout)

        # Update Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_state)
        self.timer.start(500)

    def start_round(self):
        self.range_mode.start_round()
        self.net_sim.start_simulation()
        self.start_btn.setEnabled(False)
        self.start_btn.setText("Round Active...")

    def test_phishing(self):
        failed = self.social_eng.trigger_phishing_attempt(self)
        if failed:
            self.range_mode.update_score("encryption_success", points=50) # Huge penalty
        else:
            self.range_mode.update_score("attack_blocked", points=20) # Bonus

    def update_state(self):
        status = self.range_mode.get_status()
        
        # Update Score
        self.red_lbl.setText(f"RED TEAM: {status['red_score']}")
        self.blue_lbl.setText(f"BLUE TEAM: {status['blue_score']}")
        self.time_lbl.setText(f"Time Left: {status['time_left']}s")
        
        # Update Network
        tick = self.net_sim.simulate_tick()
        if tick:
            self.net_log.setText(f"[{tick['protocol']}] {tick['src']} -> {tick['dst']} ({tick['type']})")
        
        if not status['active'] and not self.start_btn.isEnabled():
            self.start_btn.setEnabled(True)
            self.start_btn.setText("Start Range Round (60s)")
            self.net_sim.stop_simulation()
