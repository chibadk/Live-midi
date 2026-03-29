#!/usr/bin/env python3
"""
MIDI Maestro Live - Professional MIDI Live Player
Roland SC-88 Edition with PyQt6 GUI
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    """Initialize and run the application"""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("MIDI Maestro Live")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
