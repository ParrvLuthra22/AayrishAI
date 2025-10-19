"""
JARVIS AI Assistant - Futuristic UI Components
Custom PyQt6 widgets with JARVIS-style animations and effects
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import math
import random
from typing import List, Tuple

class NeonButton(QPushButton):
    """Glowing neon-style button"""
    
    def __init__(self, text: str, color: str = "#00BFFF"):
        super().__init__(text)
        self.glow_color = QColor(color)
        self.base_color = QColor(color).darker(150)
        self.is_glowing = False
        
        self.setFixedHeight(45)
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0,0,0,0.8), stop:1 rgba(0,20,40,0.8));
                border: 2px solid {color};
                border-radius: 22px;
                color: {color};
                font-size: 14px;
                font-weight: bold;
                padding: 8px 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0,50,100,0.3), stop:1 rgba(0,100,200,0.3));
                box-shadow: 0 0 20px {color};
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0,100,200,0.5), stop:1 rgba(0,150,255,0.5));
            }}
        """)
    
    def update_color(self, color: str):
        """Update button color"""
        self.glow_color = QColor(color)
        self.base_color = QColor(color).darker(150)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0,0,0,0.8), stop:1 rgba(0,20,40,0.8));
                border: 2px solid {color};
                border-radius: 22px;
                color: {color};
                font-size: 14px;
                font-weight: bold;
                padding: 8px 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0,50,100,0.3), stop:1 rgba(0,100,200,0.3));
                box-shadow: 0 0 20px {color};
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0,100,200,0.5), stop:1 rgba(0,150,255,0.5));
            }}
        """)

class VoiceWaveform(QWidget):
    """Animated voice waveform display"""
    
    def __init__(self):
        super().__init__()
        self.setFixedHeight(80)
        self.bars = []
        self.is_active = False
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_waveform)
        self.generate_bars()
    
    def generate_bars(self):
        """Generate random waveform bars"""
        self.bars = []
        for i in range(50):
            height = random.randint(5, 60)
            self.bars.append(height)
    
    def start_animation(self):
        """Start waveform animation"""
        self.is_active = True
        self.animation_timer.start(50)  
    
    def stop_animation(self):
        """Stop waveform animation"""
        self.is_active = False
        self.animation_timer.stop()
        self.generate_bars()
        self.update()
    
    def update_waveform(self):
        """Update waveform bars"""
        if self.is_active:
            for i in range(len(self.bars)):
                self.bars[i] = max(5, min(60, self.bars[i] + random.randint(-10, 10)))
        else:
            for i in range(len(self.bars)):
                self.bars[i] = max(5, self.bars[i] - 2)
        
        self.update()
    
    def paintEvent(self, event):
        """Paint the waveform"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        bar_width = width / len(self.bars)
        
        for i, bar_height in enumerate(self.bars):
            x = i * bar_width
            y = (height - bar_height) / 2
            
            gradient = QLinearGradient(0, y, 0, y + bar_height)
            if self.is_active:
                gradient.setColorAt(0, QColor("#00FFFF"))
                gradient.setColorAt(0.5, QColor("#0080FF"))
                gradient.setColorAt(1, QColor("#004080"))
            else:
                gradient.setColorAt(0, QColor("#004080"))
                gradient.setColorAt(1, QColor("#002040"))
            
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(x + 1, y, bar_width - 2, bar_height), 2, 2)

class ChatBubble(QWidget):
    """Chat message bubble with smooth animations"""
    
    def __init__(self, message: str, is_user: bool = False, timestamp: str = ""):
        super().__init__()
        self.message = message
        self.is_user = is_user
        self.timestamp = timestamp
        self.opacity = 0.0
        
        self.setup_ui()
        self.animate_in()
    
    def setup_ui(self):
        """Setup the chat bubble UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        
        if self.is_user:
            layout.addStretch()
        
        message_container = QFrame()
        message_container.setFixedWidth(min(600, len(self.message) * 8 + 100))
        
        if self.is_user:
            message_container.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(0,100,200,0.8), stop:1 rgba(0,150,255,0.8));
                    border-radius: 15px;
                    border: 1px solid #0080FF;
                }
            """)
        else:
            message_container.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(20,20,20,0.9), stop:1 rgba(40,40,40,0.9));
                    border-radius: 15px;
                    border: 1px solid #00BFFF;
                }
            """)
        
        msg_layout = QVBoxLayout(message_container)
        msg_layout.setContentsMargins(15, 10, 15, 10)
        
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                background: transparent;
                border: none;
            }
        """)
        
        time_label = QLabel(self.timestamp)
        time_label.setStyleSheet("""
            QLabel {
                color: #888;
                font-size: 10px;
                background: transparent;
                border: none;
            }
        """)
        time_label.setAlignment(Qt.AlignmentFlag.AlignRight if self.is_user else Qt.AlignmentFlag.AlignLeft)
        
        msg_layout.addWidget(message_label)
        msg_layout.addWidget(time_label)
        
        layout.addWidget(message_container)
        
        if not self.is_user:
            layout.addStretch()
    
    def animate_in(self):
        """Animate bubble entrance"""
        self.opacity_animation = QPropertyAnimation(self, b"opacity")
        self.opacity_animation.setDuration(300)
        self.opacity_animation.setStartValue(0.0)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.start()
    
    def get_opacity(self):
        return self.opacity
    
    def set_opacity(self, value):
        self.opacity = value
        self.setGraphicsEffect(self.create_opacity_effect())
    
    def create_opacity_effect(self):
        effect = QGraphicsOpacityEffect()
        effect.setOpacity(self.opacity)
        return effect

class SystemMetricsWidget(QWidget):
    """Real-time system metrics display"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_metrics)
        self.update_timer.start(2000)  
    
    def setup_ui(self):
        """Setup metrics UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        title = QLabel("SYSTEM STATUS")
        title.setStyleSheet("""
            QLabel {
                color: #00BFFF;
                font-size: 16px;
                font-weight: bold;
                border-bottom: 2px solid #00BFFF;
                padding-bottom: 5px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        self.cpu_label = QLabel("CPU: 0%")
        self.cpu_bar = QProgressBar()
        self.setup_progress_bar(self.cpu_bar)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)
        
        self.memory_label = QLabel("Memory: 0%")
        self.memory_bar = QProgressBar()
        self.setup_progress_bar(self.memory_bar)
        layout.addWidget(self.memory_label)
        layout.addWidget(self.memory_bar)
        
        self.time_label = QLabel()
        self.time_label.setStyleSheet("""
            QLabel {
                color: #FFD700;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }
        """)
        layout.addWidget(self.time_label)
        
        layout.addStretch()
    
    def setup_progress_bar(self, bar: QProgressBar):
        """Setup progress bar styling"""
        bar.setFixedHeight(20)
        bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #004080;
                border-radius: 10px;
                text-align: center;
                background: rgba(0,0,0,0.5);
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00BFFF, stop:1 #0080FF);
                border-radius: 8px;
            }
        """)
    
    def update_metrics(self):
        """Update system metrics"""
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent()
            self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")
            self.cpu_bar.setValue(int(cpu_percent))
            
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            self.memory_label.setText(f"Memory: {memory_percent:.1f}%")
            self.memory_bar.setValue(int(memory_percent))
            
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_label.setText(current_time)
            
        except ImportError:
            self.cpu_label.setText("CPU: N/A")
            self.memory_label.setText("Memory: N/A")
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_label.setText(current_time)

class GlowingLabel(QLabel):
    """Label with glowing text effect"""
    
    def __init__(self, text: str, color: str = "#00BFFF"):
        super().__init__(text)
        self.glow_color = QColor(color)
        self.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 18px;
                font-weight: bold;
            }}
        """)
    
    def paintEvent(self, event):
        """Paint with glow effect"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        for i in range(3):
            pen = QPen(self.glow_color)
            pen.setWidth(i + 1)
            painter.setPen(pen)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        
        pen = QPen(QColor("white"))
        painter.setPen(pen)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())

class CircularProgress(QWidget):
    """Circular progress indicator"""
    
    def __init__(self, size: int = 100):
        super().__init__()
        self.setFixedSize(size, size)
        self.progress = 0
        self.color = QColor("#00BFFF")
    
    def set_progress(self, value: float):
        """Set progress value (0-100)"""
        self.progress = max(0, min(100, value))
        self.update()
    
    def paintEvent(self, event):
        """Paint circular progress"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect().adjusted(10, 10, -10, -10)
        
        pen = QPen(QColor("#004080"))
        pen.setWidth(8)
        painter.setPen(pen)
        painter.drawEllipse(rect)
        
        pen = QPen(self.color)
        pen.setWidth(8)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        start_angle = 90 * 16  
        span_angle = -(self.progress / 100) * 360 * 16
        painter.drawArc(rect, start_angle, span_angle)
        
        painter.setPen(QColor("white"))
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{int(self.progress)}%")
