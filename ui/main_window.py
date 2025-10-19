"""
JARVIS AI Assistant - Main UI Window
Primary interface for JARVIS with chat, voice controls, and system monitoring
"""

import sys
import asyncio
import logging
from typing import Optional
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from .components import *

class JarvisMainWindow(QMainWindow):
    """Main JARVIS interface window"""
    
    command_received = pyqtSignal(str)
    voice_toggle_requested = pyqtSignal()
    
    def __init__(self, brain, voice_handler, config):
        super().__init__()
        
        self.brain = brain
        self.voice_handler = voice_handler
        self.config = config
        self.logger = logging.getLogger("JARVIS_UI")
        
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        
        self.is_listening = False
        self.is_dark_theme = True
        
        self.setup_window()
        self.create_widgets()
        self.setup_layouts()
        self.connect_signals()
        self.setup_voice_integration()
        
        self.start_background_tasks()
        
        self.logger.info("✅ JARVIS main window initialized")
    
    def setup_window(self):
        """Setup main window properties"""
        self.setWindowTitle("J.A.R.V.I.S - Just A Rather Very Intelligent System")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        self.setWindowIcon(QIcon("🤖"))
        
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #0a0a0a, stop: 1 #1a1a1a);
                color: #00d4ff;
                border: 2px solid #00d4ff;
            }
        """)
    
    def create_widgets(self):
        """Create all UI widgets"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.header = self.create_header()
        
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.left_panel = self.create_chat_panel()
        self.right_panel = self.create_control_panel()
        
        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setSizes([800, 400])
        
        self.create_status_bar()
    
    def create_header(self):
        """Create header with title and controls"""
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #1a1a1a, stop: 0.5 #2a2a2a, stop: 1 #1a1a1a);
                border-bottom: 2px solid #00d4ff;
            }
        """)
        
        layout = QHBoxLayout(header)
        
        title = QLabel("J.A.R.V.I.S")
        title.setStyleSheet("""
            QLabel {
                color: #00d4ff;
                font-family: 'Courier New', monospace;
                font-size: 36px;
                font-weight: bold;
                text-shadow: 0 0 20px #00d4ff;
                background: transparent;
                border: none;
            }
        """)
        layout.addWidget(title)
        
        layout.addStretch()
        
        self.voice_button = NeonButton("🎤 Voice", "#00ff00")
        self.voice_button.clicked.connect(self.toggle_voice)
        self.voice_button.setFixedSize(120, 40)
        
        self.theme_button = NeonButton("🌙 Theme", "#ffaa00")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setFixedSize(120, 40)
        
        self.settings_button = NeonButton("⚙️ Settings", "#aa00ff")
        self.settings_button.clicked.connect(self.show_settings)
        self.settings_button.setFixedSize(120, 40)
        
        layout.addWidget(self.voice_button)
        layout.addWidget(self.theme_button)
        layout.addWidget(self.settings_button)
        
        return header
    
    def create_chat_panel(self):
        """Create main chat interface panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        self.chat_display = QScrollArea()
        self.chat_display.setWidgetResizable(True)
        self.chat_display.setStyleSheet("""
            QScrollArea {
                background: rgba(10, 10, 10, 0.9);
                border: 1px solid #00d4ff;
                border-radius: 10px;
            }
            QScrollBar:vertical {
                background: #1a1a1a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #00d4ff;
                border-radius: 6px;
                min-height: 20px;
            }
        """)
        
        self.chat_content = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_display.setWidget(self.chat_content)
        
        welcome_bubble = ChatBubble("Welcome back, sir. How may I assist you today?", is_user=False)
        self.chat_layout.addWidget(welcome_bubble)
        
        layout.addWidget(self.chat_display, stretch=1)
        
        self.voice_waveform = VoiceWaveform()
        self.voice_waveform.hide()
        layout.addWidget(self.voice_waveform)
        
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Ask JARVIS anything...")
        self.text_input.setStyleSheet("""
            QLineEdit {
                background: rgba(26, 26, 26, 0.9);
                border: 2px solid #00d4ff;
                border-radius: 15px;
                padding: 15px;
                font-size: 16px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #00ffaa;
                box-shadow: 0 0 20px #00ffaa;
            }
        """)
        self.text_input.returnPressed.connect(self.send_text_command)
        
        self.send_button = NeonButton("Send", "#00d4ff")
        self.send_button.clicked.connect(self.send_text_command)
        self.send_button.setFixedSize(80, 50)
        
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.send_button)
        
        layout.addWidget(input_container)
        
        return panel
    
    def create_control_panel(self):
        """Create system monitoring and control panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        metrics_group = QGroupBox("System Status")
        metrics_group.setStyleSheet("""
            QGroupBox {
                color: #00d4ff;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #00d4ff;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background: #1a1a1a;
            }
        """)
        
        metrics_layout = QVBoxLayout(metrics_group)
        self.system_metrics = SystemMetricsWidget()
        metrics_layout.addWidget(self.system_metrics)
        
        layout.addWidget(metrics_group)
        
        actions_group = QGroupBox("Quick Actions")
        actions_group.setStyleSheet(metrics_group.styleSheet())
        
        actions_layout = QGridLayout(actions_group)


        quick_actions = [
            ("🌐 Search Web", "#00ff88", lambda: self.quick_command("search the web for")),
            ("📁 Open Finder", "#ff8800", lambda: self.quick_command("open finder")),
            ("🎵 Play Music", "#8800ff", lambda: self.quick_command("open music")),
            ("📧 Open Mail", "#ff0088", lambda: self.quick_command("open mail")),
            ("🖥️ System Info", "#00aaff", lambda: self.quick_command("show system information")),
            ("🗂️ Documents", "#ffaa00", lambda: self.quick_command("open documents folder"))
        ]
        
        for i, (text, color, action) in enumerate(quick_actions):
            button = NeonButton(text, color)
            button.clicked.connect(action)
            button.setFixedHeight(50)
            actions_layout.addWidget(button, i // 2, i % 2)
        
        layout.addWidget(actions_group)
        
        ai_group = QGroupBox("AI Status")
        ai_group.setStyleSheet(metrics_group.styleSheet())
        
        ai_layout = QVBoxLayout(ai_group)
        
        self.ai_status_label = QLabel("AI: Ready")
        self.ai_status_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-size: 14px;
                padding: 5px;
            }
        """)
        
        self.model_label = QLabel("Model: Auto-select")
        self.model_label.setStyleSheet(self.ai_status_label.styleSheet())
        
        ai_layout.addWidget(self.ai_status_label)
        ai_layout.addWidget(self.model_label)
        
        layout.addWidget(ai_group)
        
        layout.addStretch()
        
        return panel
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: #1a1a1a;
                color: #00d4ff;
                border-top: 1px solid #00d4ff;
                font-size: 12px;
            }
        """)
        
        self.voice_status = QLabel("Voice: Disabled")
        self.connection_status = QLabel("AI: Connected")
        self.time_label = QLabel()
        
        self.status_bar.addWidget(self.voice_status)
        self.status_bar.addPermanentWidget(self.connection_status)
        self.status_bar.addPermanentWidget(self.time_label)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
    
    def setup_layouts(self):
        """Setup main layout"""
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.splitter, stretch=1)
    
    def connect_signals(self):
        """Connect UI signals"""
        self.command_received.connect(self.process_command)
    
    def setup_voice_integration(self):
        """Setup voice handler integration"""
        if self.voice_handler and self.voice_handler.is_available():
            self.voice_handler.set_command_callback(self.on_voice_command)
            self.voice_handler.set_listening_callback(self.on_listening_state_changed)
        else:
            self.voice_button.setEnabled(False)
            self.voice_status.setText("Voice: Not Available")
    
    def start_background_tasks(self):
        """Start background monitoring tasks"""
        self.metrics_timer = QTimer()
        self.metrics_timer.timeout.connect(self.system_metrics.update_metrics)
        self.metrics_timer.start(2000)  
    
    def toggle_voice(self):
        """Toggle voice recognition"""
        if not self.voice_handler or not self.voice_handler.is_available():
            self.show_message("Voice recognition is not available on this system.")
            return
        
        if self.is_listening:
            self.voice_handler.stop_listening()
        else:
            self.voice_handler.start_listening()
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.is_dark_theme = not self.is_dark_theme
        
        if self.is_dark_theme:
            self.theme_button.setText("🌙 Dark")
        else:
            self.theme_button.setText("☀️ Light")
        
        self.show_message("Theme switching is in development.")
    
    def show_settings(self):
        """Show settings dialog"""
        self.show_message("Settings panel is in development.")
    
    def send_text_command(self):
        """Send text command"""
        text = self.text_input.text().strip()
        if text:
            self.add_chat_message(f"💬 You typed: {text}", is_user=True)
            self.text_input.clear()
            self.command_received.emit(text)
    
    def quick_command(self, command: str):
        """Execute a quick command"""
        self.add_chat_message(f"🎯 Quick: {command}", is_user=True)
        self.command_received.emit(command)
    
    def on_voice_command(self, command: str):
        """Handle voice command"""
        self.logger.info(f"🎤 Voice command received: {command}")
        self.add_chat_message(f"👤 You said: {command}", is_user=True)
        self.command_received.emit(command)
    
    def on_listening_state_changed(self, listening: bool):
        """Handle listening state change"""
        self.is_listening = listening
        
        if listening:
            self.voice_button.setText("🔴 Stop")
            self.voice_button.update_color("#ff0044")
            self.voice_status.setText("Voice: Listening")
            self.voice_waveform.show()
            self.voice_waveform.start_animation()
        else:
            self.voice_button.setText("🎤 Voice")
            self.voice_button.update_color("#00ff00")
            self.voice_status.setText("Voice: Ready")
            self.voice_waveform.hide()
            self.voice_waveform.stop_animation()
    
    @pyqtSlot(str)
    def process_command(self, command: str):
        """Process command and get response"""
        try:
            QTimer.singleShot(0, lambda: self._run_async_command(command))
        except Exception as e:
            self.logger.error(f"Error processing command: {e}")
            self.add_chat_message(f"❌ Error processing command: {e}", is_user=False)
    
    def _run_async_command(self, command: str):
        """Run async command in a new event loop"""
        import threading
        
        def run_in_thread():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                result = loop.run_until_complete(self._process_command_async(command))
                
                loop.close()
                
            except Exception as e:
                self.logger.error(f"Error in async command thread: {e}")
                QTimer.singleShot(0, lambda: self.add_chat_message(f"❌ Error: {e}", is_user=False))
        
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
    
    async def _process_command_async(self, command: str):
        """Process command asynchronously"""
        try:
            def update_status():
                self.ai_status_label.setText("AI: Processing...")
                self.ai_status_label.setStyleSheet("""
                    QLabel {
                        color: #ffaa00;
                        font-size: 14px;
                        padding: 5px;
                    }
                """)
            
            QTimer.singleShot(0, update_status)
            
            response = await self.brain.process_input(command)
            
            response_text = response.get("response", {}).get("text", "I didn't understand that.")
            
            def add_response():
                self.logger.info(f"🤖 Adding JARVIS response to chat: {response_text[:50]}...")
                self.add_chat_message(f"🤖 {response_text}", is_user=False)
                self.ai_status_label.setText("AI: Ready")
                self.ai_status_label.setStyleSheet("""
                    QLabel {
                        color: #00ff88;
                        font-size: 14px;
                        padding: 5px;
                    }
                """)
            
            QTimer.singleShot(0, add_response)
            
            if self.voice_handler:
                try:
                    await self.voice_handler.speak(response_text)
                except Exception as tts_error:
                    self.logger.warning(f"TTS error: {tts_error}")
            
            self.ai_status_label.setText("AI: Ready")
            self.ai_status_label.setStyleSheet("""
                QLabel {
                    color: #00ff00;
                    font-size: 14px;
                    padding: 5px;
                }
            """)
            
        except Exception as e:
            self.logger.error(f"❌ Command processing error: {e}")
            error_msg = "I encountered an error processing that command, sir."
            QTimer.singleShot(100, lambda: self.add_chat_message(error_msg, is_user=False))
            
            self.ai_status_label.setText("AI: Error")
            self.ai_status_label.setStyleSheet("""
                QLabel {
                    color: #ff0044;
                    font-size: 14px;
                    padding: 5px;
                }
            """)
    
    def add_chat_message(self, message: str, is_user: bool):
        """Add message to chat display"""
        self.logger.info(f"💬 Adding chat message: {'User' if is_user else 'JARVIS'}: {message[:50]}...")
        bubble = ChatBubble(message, is_user)
        self.chat_layout.addWidget(bubble)
        
        QTimer.singleShot(50, self.scroll_to_bottom)
    
    def scroll_to_bottom(self):
        """Scroll chat to bottom"""
        scrollbar = self.chat_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def show_message(self, message: str):
        """Show temporary message"""
        self.add_chat_message(message, is_user=False)
    
    def update_time(self):
        """Update time display"""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(current_time)
    
    def closeEvent(self, event):
        """Handle window close"""
        self.logger.info("🔄 Shutting down JARVIS interface...")
        
        if self.voice_handler:
            self.voice_handler.shutdown()
        
        if hasattr(self, 'timer'):
            self.timer.stop()
        if hasattr(self, 'metrics_timer'):
            self.metrics_timer.stop()
        
        event.accept()
        self.logger.info("✅ JARVIS interface shutdown complete")