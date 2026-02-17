from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from .animations import ParticleNetwork

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        header = QLabel("Security Dashboard")
        header.setObjectName("Header")
        layout.addWidget(header)

        # Visuals
        self.particles = ParticleNetwork()
        self.particles.setFixedHeight(150)
        layout.addWidget(self.particles)

        # Stats Grid
        stats_layout = QGridLayout()
        
        self.files_monitored = self.create_stat_card("Files Monitored", "0")
        stats_layout.addWidget(self.files_monitored, 0, 0)
        
        self.threat_level = self.create_stat_card("Threat Level", "Low")
        stats_layout.addWidget(self.threat_level, 0, 1)
        
        layout.addLayout(stats_layout)

        # Graph
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.figure.patch.set_facecolor('#1a1a2e')
        self.ax.set_facecolor('#1a1a2e')
        self.ax.tick_params(colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def create_stat_card(self, title, value):
        frame = QFrame()
        frame.setStyleSheet("background-color: #16213e; border-radius: 10px; padding: 10px;")
        layout = QVBoxLayout()
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        
        val_lbl = QLabel(value)
        val_lbl.setStyleSheet("color: #e94560; font-size: 20px; font-weight: bold;")
        
        layout.addWidget(title_lbl)
        layout.addWidget(val_lbl)
        frame.setLayout(layout)
        return frame

    def update_stats(self, file_count, threat):
        self.files_monitored.layout().itemAt(1).widget().setText(str(file_count))
        self.threat_level.layout().itemAt(1).widget().setText(threat)
