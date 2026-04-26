#!/usr/bin/env python3
"""
Email Automation Suite - Main Entry Point
"""
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from PyQt5.QtWidgets import QApplication
    from ui.main_window import MainWindow
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install PyQt5: pip install PyQt5")
    sys.exit(1)

def main():
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Campus Recruit Analyzer")
    app.setApplicationVersion("1.0.0")
    
    try:
        # Create and show main window
        window = MainWindow()
        window.show()
        
        print("Application started successfully")
        
        # Start event loop
        sys.exit(app.exec_())
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()