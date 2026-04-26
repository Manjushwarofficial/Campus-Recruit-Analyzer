from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QAbstractItemView,
                             QHeaderView, QLabel, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt

class InboxWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Inbox")
        title.setObjectName("title")
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setObjectName("secondaryBtn")

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_btn)
        
        # Email Table
        self.email_table = QTableWidget()
        self.email_table.setColumnCount(3)
        self.email_table.setHorizontalHeaderLabels(["From", "Subject", "Date"])
        self.email_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.email_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.email_table.verticalHeader().setVisible(False)
        self.email_table.horizontalHeader().setStretchLastSection(True)
        self.email_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.email_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.email_table)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #F7F4F3; }
            QLabel#title { font-size: 32px; font-weight: bold; color: #564D4A; }
            QPushButton#secondaryBtn {
                background-color: transparent; color: #564D4A; border: 2px solid #564D4A;
                padding: 10px 24px; border-radius: 8px; font-size: 14px; font-weight: bold;
            }
            QPushButton#secondaryBtn:hover { background-color: #564D4A; color: #F7F4F3; }
            QTableWidget {
                border: 1px solid #E0D9D6;
                gridline-color: #E0D9D6;
                font-size: 14px;
                color: #564D4A; /* This fixes the white font */
            }
            QHeaderView::section {
                background-color: #E0D9D6;
                padding: 8px;
                border: none;
                font-weight: bold;
                color: #564D4A;
            }
        """)

    def populate_table(self, emails):
        self.email_table.setRowCount(len(emails))
        for row, email in enumerate(emails):
            self.email_table.setItem(row, 0, QTableWidgetItem(email["from"]))
            self.email_table.setItem(row, 1, QTableWidgetItem(email["subject"]))
            self.email_table.setItem(row, 2, QTableWidgetItem(email["date"]))

