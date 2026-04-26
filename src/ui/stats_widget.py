
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox
)
from PyQt5.QtCore import Qt

class StatsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Placement Statistics")
        title.setObjectName("title")
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Description
        desc = QLabel("Track your application status for top tier generative AI and hardware roles.")
        desc.setObjectName("statusLabel")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Table Setup
        self.table = QTableWidget(2, 4)
        self.table.setHorizontalHeaderLabels(["Company", "Role", "CTC (LPA)", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.NoFocus)
        
        # FIX: Increase row height to prevent QComboBox text clipping
        self.table.verticalHeader().setDefaultSectionSize(55)

        layout.addWidget(self.table)

        # Populate Mock Data
        mock_data = [
            ("OpenAI", "Generative AI Engineer", "30.0 - 45.0", "Not Applied"),
            ("NVIDIA", "Deep Learning SDE", "25.0 - 35.0", "Applied")
        ]

        for row_idx, (company, role, ctc, default_status) in enumerate(mock_data):
            # Read-only Cells
            comp_item = QTableWidgetItem(company)
            comp_item.setTextAlignment(Qt.AlignCenter)
            comp_item.setFlags(Qt.ItemIsEnabled)
            
            role_item = QTableWidgetItem(role)
            role_item.setTextAlignment(Qt.AlignCenter)
            role_item.setFlags(Qt.ItemIsEnabled)
            
            ctc_item = QTableWidgetItem(ctc)
            ctc_item.setTextAlignment(Qt.AlignCenter)
            ctc_item.setFlags(Qt.ItemIsEnabled)

            self.table.setItem(row_idx, 0, comp_item)
            self.table.setItem(row_idx, 1, role_item)
            self.table.setItem(row_idx, 2, ctc_item)

            # Status Dropdown Menu
            combo = QComboBox()
            combo.addItems(["Not Applied", "Applied", "In Progress", "Rejected"])
            combo.setCurrentText(default_status)
            self.table.setCellWidget(row_idx, 3, combo)

        layout.addStretch()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #F7F4F3; }
            
            QLabel#title {
                font-size: 32px;
                font-weight: bold;
                color: #564D4A;
            }
            QLabel#statusLabel {
                font-size: 13px;
                color: #564D4A;
                margin-bottom: 10px;
            }
            
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #E0D9D6;
                border-radius: 8px;
                color: #564D4A;
                font-size: 14px;
                gridline-color: transparent;
            }
            QTableWidget::item {
                border-bottom: 1px solid #E0D9D6;
                padding: 10px;
            }
            /* FIX: Prevent harsh dark background on row selection */
            QTableWidget::item:selected {
                background-color: #F7F4F3; 
                color: #564D4A;
            }
            QHeaderView::section {
                background-color: #EFEBE9;
                color: #564D4A;
                font-weight: bold;
                font-size: 14px;
                border: none;
                border-bottom: 2px solid #E0D9D6;
                padding: 12px;
            }
            
            /* FIX: Adjusted padding and min-height to stop clipping */
            QComboBox {
                background-color: #F7F4F3;
                border: 1px solid #E0D9D6;
                border-radius: 12px;
                padding: 2px 10px;
                min-height: 30px;
                color: #564D4A;
                font-weight: bold;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                selection-background-color: #564D4A;
                selection-color: #F7F4F3;
                border: 1px solid #E0D9D6;
            }
        """)
