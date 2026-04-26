from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal

class NavbarWidget(QWidget):
    # Define signals that will be emitted when buttons are clicked
    inbox_clicked = pyqtSignal()
    automation_clicked = pyqtSignal()
    stats_clicked = pyqtSignal()
    back_clicked = pyqtSignal() # New signal for the back button

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setup_ui()
        self.apply_styles()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 30, 10, 30)
        layout.setSpacing(15)

        self.inbox_btn = QPushButton("Inbox")
        self.automation_btn = QPushButton("Automation")
        self.stats_btn = QPushButton("Stats")

        layout.addWidget(self.inbox_btn)
        layout.addWidget(self.automation_btn)
        layout.addWidget(self.stats_btn)

        # Add a spacer to push the back button to the bottom
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.back_btn = QPushButton("Back to Home") # New button
        self.back_btn.setObjectName("backBtn") # For specific styling
        layout.addWidget(self.back_btn)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #E0D9D6;
            }
            QPushButton {
                background-color: transparent;
                color: #564D4A;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #CCC3C0;
            }
            QPushButton:focus {
                background-color: #F7F4F3; /* Active page style */
            }
            QPushButton#backBtn {
                font-size: 14px;
                text-align: center;
                border: 2px solid #564D4A;
            }
            QPushButton#backBtn:hover {
                 background-color: #564D4A;
                 color: #F7F4F3;
            }
        """)

    def connect_signals(self):
        self.inbox_btn.clicked.connect(self.inbox_clicked.emit)
        self.automation_btn.clicked.connect(self.automation_clicked.emit)
        self.stats_btn.clicked.connect(self.stats_clicked.emit)
        self.back_btn.clicked.connect(self.back_clicked.emit) # Connect new signal

