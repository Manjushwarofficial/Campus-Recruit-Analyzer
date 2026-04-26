from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QSpacerItem, QSizePolicy,
                             QStackedWidget, QMessageBox)
from PyQt5.QtCore import Qt

# Import all the necessary UI components
from ui.settings_dialog import SettingsDialog
from ui.inbox_widget import InboxWidget
from ui.navbar_widget import NavbarWidget
from ui.automation_widget import AutomationWidget
from ui.stats_widget import StatsWidget

from core.email_client import fetch_emails, get_email_credentials

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Campus Recruit Analyzer")
        self.setGeometry(100, 100, 1000, 700)
        
        # This is the main stack: it holds the welcome screen OR the main app view
        self.root_stack = QStackedWidget()
        self.setCentralWidget(self.root_stack)
        
        # Create the two main states of the application
        self.welcome_page = self._create_welcome_page()
        self.main_app_page = self._create_main_app_page()
        
        # Add these two states to the root stack
        self.root_stack.addWidget(self.welcome_page)
        self.root_stack.addWidget(self.main_app_page)
        
        self.apply_styles()
        self.connect_signals()
        
        # Define the message box style once to be reused everywhere
        self.msg_box_style = """
            QMessageBox { background-color: #F7F4F3; }
            QLabel { min-width: 300px; color: #564D4A; font-size: 14px; }
            QPushButton {
                background-color: #564D4A; color: #F7F4F3; border: none; padding: 10px;
                border-radius: 8px; font-size: 14px; font-weight: bold; min-width: 80px;
            }
            QPushButton:hover { background-color: #6B6360; }
        """

    def _create_main_app_page(self):
        """Creates the main application layout with Navbar and content area."""
        main_widget = QWidget()
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Left side: The new Navbar
        self.navbar = NavbarWidget()
        
        # Right side: A stacked widget for content (Inbox, Automation, Stats)
        self.content_stack = QStackedWidget()
        self.inbox_page = InboxWidget()
        self.automation_page = AutomationWidget()
        self.stats_page = StatsWidget()
        self.content_stack.addWidget(self.inbox_page)
        self.content_stack.addWidget(self.automation_page)
        self.content_stack.addWidget(self.stats_page)

        layout.addWidget(self.navbar)
        layout.addWidget(self.content_stack)

        return main_widget

    def _create_welcome_page(self):
        """Creates the initial welcome widget (this is your original code)."""
        welcome_widget = QWidget()
        layout = QVBoxLayout(welcome_widget)
        layout.setContentsMargins(50, 100, 50, 100)
        layout.setSpacing(40)
        
        title = QLabel("Campus Recruit Analyzer")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")
        layout.addWidget(title)
        
        subtitle = QLabel("Welcome! Ready to ace your campus placement journey?")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        description = QLabel("Practice Online Assessments, prepare for interview questions, track job opportunities, and boost your chances of landing your dream job with ease.")
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        description.setObjectName("description")
        layout.addWidget(description)
        
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.get_started_btn = QPushButton("Get Started")
        self.get_started_btn.setObjectName("primaryBtn")
        button_layout.addWidget(self.get_started_btn)
        
        self.configure_btn = QPushButton("Configure Settings")
        self.configure_btn.setObjectName("secondaryBtn")
        button_layout.addWidget(self.configure_btn)
        
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(button_layout)
        
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        return welcome_widget

    def apply_styles(self):
        """Applies the main stylesheet for the application."""
        self.setStyleSheet("""
            QMainWindow { background-color: #F7F4F3; }
            QLabel#title { font-size: 48px; font-weight: bold; color: #564D4A; margin: 20px 0; }
            QLabel#subtitle { font-size: 24px; color: #564D4A; margin: 10px 0; }
            QLabel#description { font-size: 16px; color: #564D4A; margin: 20px 40px; }
            QPushButton#primaryBtn {
                background-color: #564D4A; color: #F7F4F3; border: none; padding: 16px 32px;
                border-radius: 12px; font-size: 16px; font-weight: bold; min-width: 160px; margin: 0 10px;
            }
            QPushButton#primaryBtn:hover { background-color: #6B6360; }
            QPushButton#secondaryBtn {
                background-color: transparent; color: #564D4A; border: 2px solid #564D4A;
                padding: 14px 30px; border-radius: 12px; font-size: 16px;
                font-weight: bold; min-width: 160px; margin: 0 10px;
            }
            QPushButton#secondaryBtn:hover { background-color: #564D4A; color: #F7F4F3; }
        """)
    
    def connect_signals(self):
        """Connects signals from all components to their functions."""
        # Welcome page buttons
        self.get_started_btn.clicked.connect(self.on_get_started)
        self.configure_btn.clicked.connect(self.on_configure)

        # Navbar buttons
        self.navbar.inbox_clicked.connect(lambda: self.content_stack.setCurrentWidget(self.inbox_page))
        self.navbar.automation_clicked.connect(lambda: self.content_stack.setCurrentWidget(self.automation_page))
        self.navbar.stats_clicked.connect(lambda: self.content_stack.setCurrentWidget(self.stats_page))
        self.navbar.back_clicked.connect(lambda: self.root_stack.setCurrentWidget(self.welcome_page))
        
        # Inbox refresh button
        self.inbox_page.refresh_btn.clicked.connect(self.load_inbox)
    
    def on_get_started(self):
        """Handles the 'Get Started' button click."""
        email, password = get_email_credentials()
        if email and password:
            self.load_inbox()
        else:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("Setup Required")
            msg_box.setInformativeText("Please configure your email settings first.")
            msg_box.setWindowTitle("Setup Required")
            msg_box.setStyleSheet(self.msg_box_style)
            msg_box.exec_()
            self.on_configure()

    def on_configure(self):
        """Opens the settings dialog."""
        dialog = SettingsDialog(self)
        if dialog.exec_(): # Returns true if user clicks "Get Started" in dialog
            self.load_inbox()
            
    def load_inbox(self):
        """Fetches emails and switches to the main application view."""
        print("Fetching emails...")
        emails = fetch_emails()
        
        if isinstance(emails, str): # Check if fetch_emails returned an error string
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Error")
            msg_box.setInformativeText(emails)
            msg_box.setWindowTitle("Error")
            msg_box.setStyleSheet(self.msg_box_style)
            msg_box.exec_()
            return
            
        self.inbox_page.populate_table(emails)
        # This is the key change: switch from welcome screen to the main app view
        self.root_stack.setCurrentWidget(self.main_app_page)

