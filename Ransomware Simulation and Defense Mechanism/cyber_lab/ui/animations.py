import random
import math
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QColor, QBrush, QPen

class ParticleNetwork(QWidget):
    """
    Renders a floating particle network background.
    Nodes connect when close to each other, simulating network traffic/neural nets.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents) # Allow clicks through
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(30) # ~30 FPS
        
        # Config
        self.count = 40
        self.connect_dist = 100
        self.color = QColor(0, 255, 234, 150) # Neon Cyan
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.init_particles()

    def init_particles(self):
        self.particles = []
        w, h = self.width(), self.height()
        for _ in range(self.count):
            self.particles.append({
                'x': random.uniform(0, w),
                'y': random.uniform(0, h),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'size': random.uniform(1.5, 3.5)
            })

    def update_particles(self):
        w, h = self.width(), self.height()
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Bounce
            if p['x'] < 0 or p['x'] > w: p['vx'] *= -1
            if p['y'] < 0 or p['y'] > h: p['vy'] *= -1
            
        self.update() # Trigger repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Transparent background (parent widget handles bg color)
        
        pen = QPen(self.color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(QBrush(self.color))

        # Draw Particles & Connections
        for i, p1 in enumerate(self.particles):
            # Draw Node
            painter.drawEllipse(QPointF(p1['x'], p1['y']), p1['size'], p1['size'])
            
            # Connect to others
            for p2 in self.particles[i+1:]:
                dist = math.hypot(p1['x'] - p2['x'], p1['y'] - p2['y'])
                if dist < self.connect_dist:
                    alpha = int((1.0 - dist / self.connect_dist) * 100)
                    pen.setColor(QColor(0, 255, 234, alpha))
                    painter.setPen(pen)
                    painter.drawLine(QPointF(p1['x'], p1['y']), QPointF(p2['x'], p2['y']))

        painter.end()


class ScanlineOverlay(QWidget):
    """
    Renders horizontal scanlines for a CRT effect.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        # 1px line every 4px
        pen = QPen(QColor(0, 0, 0, 15)) # Reduced from 30 to 15 for better readability
        pen.setWidth(1)
        painter.setPen(pen)
        
        for y in range(0, self.height(), 4):
            painter.drawLine(0, y, self.width(), y)
        
        painter.end()
