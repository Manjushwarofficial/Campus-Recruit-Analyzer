import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Email Settings")
        self.setMinimumWidth(400)
        self.setup_ui()
        self.apply_styles()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Email
        email_label = QLabel("Email Address:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("e.g., yourname@gmail.com")
        
        # Password
        password_label = QLabel("App Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter the app-specific password")

        # Info Label
        info_label = QLabel("<b>Note:</b> This is not your regular email password. Please generate an 'App Password' from your email provider's security settings.")
        info_label.setWordWrap(True)
        info_label.setObjectName("infoLabel")

        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Get Started")
        self.save_btn.setObjectName("primaryBtn")
        self.back_btn = QPushButton("Back")
        self.back_btn.setObjectName("secondaryBtn")
        
        button_layout.addStretch()
        button_layout.addWidget(self.back_btn)
        button_layout.addWidget(self.save_btn)

        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(info_label)
        layout.addStretch()
        layout.addLayout(button_layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #F7F4F3;
            }
            QLabel {
                font-size: 14px;
                color: #564D4A;
            }
            QLabel#infoLabel {
                font-size: 12px;
                color: #6B6360;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #CCC;
                border-radius: 6px;
                font-size: 14px;
                color: #564D4A;
                background-color: #FFFFFF; /* This removes the dark theme */
            }
            QPushButton#primaryBtn {
                background-color: #564D4A; color: #F7F4F3; border: none;
                padding: 12px 24px; border-radius: 8px; font-size: 14px; font-weight: bold;
            }
            QPushButton#primaryBtn:hover { background-color: #6B6360; }
            QPushButton#secondaryBtn {
                background-color: transparent; color: #564D4A; border: 2px solid #564D4A;
                padding: 10px 24px; border-radius: 8px; font-size: 14px; font-weight: bold;
            }
            QPushButton#secondaryBtn:hover { background-color: #564D4A; color: #F7F4F3; }
        """)
    
    def connect_signals(self):
        self.save_btn.clicked.connect(self.save_credentials)
        self.back_btn.clicked.connect(self.reject) # Closes dialog, returns 0

    def save_credentials(self):
        email = self.email_input.text()
        password = self.password_input.text()

        # Define a consistent stylesheet for the message boxes
        msg_box_style = """
            QMessageBox {
                background-color: #F7F4F3;
            }
            QLabel {
                min-width: 300px;
                color: #564D4A;
                font-size: 14px;
            }
            QPushButton {
                background-color: #564D4A;
                color: #F7F4F3;
                border: none;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #6B6360;
            }
        """

        if not email or not password:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Input Error")
            msg_box.setInformativeText("Please enter both email and password.")
            msg_box.setWindowTitle("Input Error")
            msg_box.setStyleSheet(msg_box_style)
            msg_box.exec_()
            return

        try:
            # Write credentials to the .env file in the project root
            with open('.env', 'w') as f:
                f.write(f'EMAIL_USER="{email}"\n')
                f.write(f'EMAIL_PASS="{password}"\n')
            self.accept() # Closes dialog, returns 1
        except Exception as e:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("File Error")
            msg_box.setInformativeText(f"Could not write to .env file: {e}")
            msg_box.setWindowTitle("File Error")
            msg_box.setStyleSheet(msg_box_style)
            msg_box.exec_()

