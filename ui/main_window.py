"""
Main Window - PyQt6 GUI layout for MIDI Maestro Live
"""

import json
from pathlib import Path
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSplitter, QLabel, QPushButton, QSlider, QSpinBox,
                             QListWidget, QListWidgetItem, QFrame)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QColor, QIcon

from midi_engine.midi_handler import MIDIHandler
from midi_engine.sequencer import MIDISequencer
from config.theme_manager import ThemeManager


class MainWindow(QMainWindow):
    """Main application window with complete layout"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize managers
        self.midi_handler = MIDIHandler()
        self.sequencer = MIDISequencer(self.midi_handler)
        self.theme_manager = ThemeManager()
        
        # Load settings
        self.settings = self.load_settings()
        
        # Apply theme
        self.theme_manager.apply_theme(self.settings.get('theme', 'Dark'))
        self.setStyleSheet(self.theme_manager.get_stylesheet())
        
        # Window setup
        self.setWindowTitle("MIDI Maestro Live - Roland SC-88 Edition")
        self.setWindowIcon(QIcon("assets/icon.png") if Path("assets/icon.png").exists() else None)
        self.setGeometry(100, 100, 1400, 900)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # 1. TOP PANEL - Transport Controls
        top_panel = self.create_transport_panel()
        main_layout.addWidget(top_panel)
        
        # 2. MIDDLE PANEL - File List, Pads, Karaoke
        middle_panel = self.create_middle_panel()
        main_layout.addWidget(middle_panel, 1)
        
        # 3. BOTTOM PANEL - Mixer (16 channels)
        bottom_panel = self.create_mixer_panel()
        main_layout.addWidget(bottom_panel, 0)
        
        # Start update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_playback)
        self.update_timer.start(50)  # Update every 50ms
    
    def create_transport_panel(self) -> QFrame:
        """Create top panel with play/pause/stop and tempo control"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        panel.setFixedHeight(70)
        
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Transport buttons
        self.btn_play = QPushButton("▶ Play")
        self.btn_play.setFixedSize(80, 40)
        self.btn_play.clicked.connect(self.on_play)
        layout.addWidget(self.btn_play)
        
        self.btn_pause = QPushButton("⏸ Pause")
        self.btn_pause.setFixedSize(80, 40)
        self.btn_pause.clicked.connect(self.on_pause)
        layout.addWidget(self.btn_pause)
        
        self.btn_stop = QPushButton("⏹ Stop")
        self.btn_stop.setFixedSize(80, 40)
        self.btn_stop.clicked.connect(self.on_stop)
        layout.addWidget(self.btn_stop)
        
        # Tempo control
        layout.addSpacing(20)
        layout.addWidget(QLabel("Tempo:"))
        
        self.tempo_spinbox = QSpinBox()
        self.tempo_spinbox.setMinimum(25)
        self.tempo_spinbox.setMaximum(200)
        self.tempo_spinbox.setValue(100)
        self.tempo_spinbox.setSuffix("%")
        self.tempo_spinbox.setFixedWidth(80)
        self.tempo_spinbox.valueChanged.connect(self.on_tempo_changed)
        layout.addWidget(self.tempo_spinbox)
        
        # Time display
        layout.addSpacing(20)
        self.lbl_time = QLabel("00:00 / 00:00")
        self.lbl_time.setFont(QFont("Courier", 11))
        layout.addWidget(self.lbl_time)
        
        layout.addStretch()
        
        return panel
    
    def create_middle_panel(self) -> QWidget:
        """Create middle panel with file list, pads, and karaoke"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Left: File list
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("MIDI Files:"))
        
        self.file_list = QListWidget()
        self.file_list.setMinimumWidth(200)
        left_layout.addWidget(self.file_list)
        
        layout.addWidget(left_panel, 0)
        
        # Center: 16 Pads (4x4 grid)
        center_panel = self.create_pads_panel()
        layout.addWidget(center_panel, 1)
        
        # Right: Karaoke display
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Karaoke/Lyrics:"))
        
        self.karaoke_display = QLabel("Ready...")
        self.karaoke_display.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        self.karaoke_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.karaoke_display.setWordWrap(True)
        self.karaoke_display.setMinimumHeight(150)
        self.karaoke_display.setStyleSheet("background-color: #1a1a1a; color: #00ff00; padding: 10px;")
        right_layout.addWidget(self.karaoke_display)
        
        layout.addWidget(right_panel, 0)
        
        return widget
    
    def create_pads_panel(self) -> QFrame:
        """Create 16-pad grid (4x4)"""
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.pads = []
        
        for row in range(4):
            row_layout = QHBoxLayout()
            row_layout.setSpacing(5)
            
            for col in range(4):
                pad_num = row * 4 + col + 1
                pad = QPushButton(f"Pad {pad_num}")
                pad.setFixedSize(80, 80)
                pad.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                pad.setStyleSheet("background-color: #333; color: #0f0; border: 2px solid #0f0;")
                pad.clicked.connect(lambda checked, p=pad_num: self.on_pad_pressed(p))
                
                row_layout.addWidget(pad)
                self.pads.append(pad)
            
            layout.addLayout(row_layout)
        
        return panel
    
    def create_mixer_panel(self) -> QFrame:
        """Create 16-channel mixer (40% of window height)"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(QLabel("16-Channel GS Mixer:"))
        
        # Placeholder for mixer channels
        mixer_layout = QHBoxLayout()
        
        self.mixer_channels = []
        for channel in range(16):
            channel_widget = self.create_channel_widget(channel)
            mixer_layout.addWidget(channel_widget)
            self.mixer_channels.append(channel_widget)
        
        layout.addLayout(mixer_layout)
        
        return panel
    
    def create_channel_widget(self, channel: int) -> QFrame:
        """Create single mixer channel widget"""
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        widget.setFixedWidth(60)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(2)
        
        # Channel label
        label = QLabel(f"Ch {channel + 1}")
        label.setFont(QFont("Arial", 8))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        # Volume slider
        slider = QSlider(Qt.Orientation.Vertical)
        slider.setMinimum(0)
        slider.setMaximum(127)
        slider.setValue(100)
        slider.setFixedHeight(100)
        layout.addWidget(slider)
        
        # VU Meter placeholder
        vu_meter = QLabel("|||")
        vu_meter.setFont(QFont("Arial", 6))
        vu_meter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(vu_meter)
        
        # Mute/Solo buttons
        btn_layout = QHBoxLayout()
        btn_mute = QPushButton("M")
        btn_mute.setFixedSize(20, 20)
        btn_mute.setFont(QFont("Arial", 7))
        btn_layout.addWidget(btn_mute)
        
        btn_solo = QPushButton("S")
        btn_solo.setFixedSize(20, 20)
        btn_solo.setFont(QFont("Arial", 7))
        btn_layout.addWidget(btn_solo)
        
        layout.addLayout(btn_layout)
        
        return widget
    
    def load_settings(self) -> dict:
        """Load settings from JSON"""
        settings_file = Path("config/settings.json")
        if settings_file.exists():
            with open(settings_file) as f:
                return json.load(f)
        return {'theme': 'Dark', 'midi_output': 0, 'midi_input': 0}
    
    def on_play(self):
        """Handle play button"""
        if self.sequencer.is_paused:
            self.sequencer.resume()
        else:
            self.sequencer.play()
    
    def on_pause(self):
        """Handle pause button"""
        self.sequencer.pause()
    
    def on_stop(self):
        """Handle stop button"""
        self.sequencer.stop()
    
    def on_tempo_changed(self, value: int):
        """Handle tempo slider change"""
        tempo = value / 100.0
        self.sequencer.set_tempo(tempo)
    
    def on_pad_pressed(self, pad_num: int):
        """Handle pad button press"""
        print(f"Pad {pad_num} pressed")
        # Implement fanfare trigger logic
    
    def update_playback(self):
        """Update playback display (called by timer)"""
        self.sequencer.update()
        
        # Update time display
        current = self.sequencer.current_time
        duration = self.sequencer.get_duration()
        
        current_min, current_sec = int(current // 60), int(current % 60)
        duration_min, duration_sec = int(duration // 60), int(duration % 60)
        
        self.lbl_time.setText(f"{current_min:02d}:{current_sec:02d} / {duration_min:02d}:{duration_sec:02d}")
    
    def closeEvent(self, event):
        """Cleanup on close"""
        self.update_timer.stop()
        self.midi_handler.close()
        event.accept()