from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QStackedWidget, QScrollArea,
    QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer


class AutomationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_count = 0
        self.api_key = ""
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Automation")
        title.setObjectName("title")
        header_layout.addWidget(title)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Stacked Widget
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.stack.addWidget(self.build_api_screen())     # index 0
        self.stack.addWidget(self.build_process_screen()) # index 1
        self.stack.addWidget(self.build_chat_screen())    # index 2

        self.stack.setCurrentIndex(0)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #F7F4F3; }

            QLabel#title {
                font-size: 32px;
                font-weight: bold;
                color: #564D4A;
            }
            QLabel#sectionLabel {
                font-size: 16px;
                font-weight: bold;
                color: #564D4A;
            }
            QLabel#statusLabel {
                font-size: 13px;
                color: #564D4A;
            }
            QLabel#chatBubbleAI {
                font-size: 13px;
                color: #564D4A;
                padding: 8px 12px;
                border: 1px solid #E0D9D6;
                border-radius: 8px;
                background-color: #EFEBE9;
            }
            QLabel#chatBubbleUser {
                font-size: 13px;
                color: #564D4A;
                padding: 8px 12px;
                border: 1px solid #E0D9D6;
                border-radius: 8px;
                background-color: #F7F4F3;
            }

            QLineEdit {
                font-size: 13px;
                padding: 8px 12px;
                border: 1px solid #E0D9D6;
                border-radius: 8px;
                color: #564D4A;
                background-color: #FFFFFF;
            }
            QLineEdit:focus {
                border: 2px solid #564D4A;
            }

            QTextEdit {
                font-size: 12px;
                font-family: Courier;
                color: #564D4A;
                background-color: #FFFFFF;
                border: 1px solid #E0D9D6;
                border-radius: 8px;
                padding: 8px;
            }

            QPushButton#primaryBtn {
                background-color: #564D4A;
                color: #F7F4F3;
                border: none;
                padding: 10px 24px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#primaryBtn:hover {
                background-color: #3E3835;
            }

            QPushButton#secondaryBtn {
                background-color: transparent;
                color: #564D4A;
                border: 2px solid #564D4A;
                padding: 10px 24px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#secondaryBtn:hover {
                background-color: #564D4A;
                color: #F7F4F3;
            }

            QFrame#separator {
                color: #E0D9D6;
            }

            QScrollArea {
                border: 1px solid #E0D9D6;
                border-radius: 8px;
                background-color: #FFFFFF;
            }
        """)

    # ─────────────────────────────────────────────
    # SCREEN 0 — API Key Entry
    # ─────────────────────────────────────────────
    def build_api_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        lbl = QLabel("Connect LLM Pipeline")
        lbl.setObjectName("sectionLabel")
        layout.addWidget(lbl)

        desc = QLabel("Enter any API key to authenticate and begin placement email processing.")
        desc.setObjectName("statusLabel")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        row = QHBoxLayout()
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("sk-ant-••••••••••••••••")
        self.key_input.setEchoMode(QLineEdit.Password)
        row.addWidget(self.key_input)

        connect_btn = QPushButton("Connect")
        connect_btn.setObjectName("primaryBtn")
        connect_btn.clicked.connect(self.on_connect)
        row.addWidget(connect_btn)
        layout.addLayout(row)

        self.key_status = QLabel("")
        self.key_status.setObjectName("statusLabel")
        layout.addWidget(self.key_status)

        layout.addStretch()
        return screen

    # ─────────────────────────────────────────────
    # SCREEN 1 — Processing Log + Result
    # ─────────────────────────────────────────────
    def build_process_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        log_lbl = QLabel("Pipeline Status")
        log_lbl.setObjectName("sectionLabel")
        layout.addWidget(log_lbl)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setFixedHeight(160)
        layout.addWidget(self.log_box)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.HLine)
        layout.addWidget(sep)

        self.result_lbl = QLabel("Extracted Placement Data")
        self.result_lbl.setObjectName("sectionLabel")
        self.result_lbl.setVisible(False)
        layout.addWidget(self.result_lbl)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setFixedHeight(160)
        self.result_box.setVisible(False)
        layout.addWidget(self.result_box)

        self.chat_btn = QPushButton("AI Assistant for this Placement")
        self.chat_btn.setObjectName("secondaryBtn")
        self.chat_btn.setVisible(False)
        self.chat_btn.clicked.connect(self.goto_chat)
        layout.addWidget(self.chat_btn)

        layout.addStretch()
        return screen

    # ─────────────────────────────────────────────
    # SCREEN 2 — Chat
    # ─────────────────────────────────────────────
    def build_chat_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        lbl = QLabel("Placement Assistant")
        lbl.setObjectName("sectionLabel")
        layout.addWidget(lbl)

        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setSpacing(8)
        self.chat_layout.setContentsMargins(12, 12, 12, 12)
        self.chat_layout.addStretch()
        self.chat_scroll.setWidget(self.chat_container)
        layout.addWidget(self.chat_scroll, 1)

        row = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask about role, eligibility, process...")
        self.chat_input.returnPressed.connect(self.send_chat)
        row.addWidget(self.chat_input)

        send_btn = QPushButton("Send")
        send_btn.setObjectName("primaryBtn")
        send_btn.clicked.connect(self.send_chat)
        row.addWidget(send_btn)
        layout.addLayout(row)

        return screen

    # ─────────────────────────────────────────────
    # Logic
    # ─────────────────────────────────────────────
    def on_connect(self):
        key = self.key_input.text().strip()
        if not key:
            self.key_status.setText("Please enter any key to proceed.")
            return
        self.api_key = key
        self.key_status.setText("Authenticating...")
        QTimer.singleShot(1100, self.auth_success)

    def auth_success(self):
        self.key_status.setText("Connection established — gemini-2.5 online.")
        QTimer.singleShot(700, self.start_pipeline)

    def start_pipeline(self):
        self.stack.setCurrentIndex(1)
        steps = [
            (0,    ">> Initialising placement intelligence pipeline"),
            (500,  "-> Fetching email queue [T&P cell inbox]..."),
            (1000, "✓  1 unread placement email detected"),
            (1400, "-> Parsing email headers and body..."),
            (1900, "✓  Sender verified: manjushwar468@gmail.com"),
            (2300, "-> Sending to LLM for structured extraction..."),
            (2800, "⟳  Model: claude-sonnet-4 (processing)"),
            (3500, "✓  Extraction complete — confidence: 98.4%"),
            (3900, "-> Running eligibility validator..."),
            (4300, "✓  Schema validated — 1 active role found"),
            (4700, "⚑  No duplicate roles detected in DB"),
            (5100, "✓  Pipeline complete — ready for query"),
        ]
        for delay, msg in steps:
            QTimer.singleShot(delay, lambda m=msg: self.log_box.append(m))
        QTimer.singleShot(5400, self.show_result)

    def show_result(self):
        data = (
            "Company    : OpenAI\n"
            "Role       : GenAI Engineer\n"
            "Location   : Bangalore / Remote\n"
            "CTC        : Rs. 30,00,000 – 45,00,000 per annum\n"
            "Eligibility: CSE, ECE, IT, Data Science — CGPA >= 8\n"
            "Backlogs   : Not allowed\n"
            "Process    : OA -> Tech Interview x2 -> HR Round\n"
            "Perks      : Health Insurance, Relocation Bonus, ESOPs"
        )
        self.result_box.setText(data)
        self.result_lbl.setVisible(True)
        self.result_box.setVisible(True)
        self.chat_btn.setVisible(True)

    def goto_chat(self):
        self.stack.setCurrentIndex(2)
        self.add_bubble(
            "Placement email from InnovateTech Solutions processed. "
            "1 active role found: Software Development Engineer. "
            "Ask me anything about the role, eligibility, or process.",
            is_user=False
        )

    def add_bubble(self, text, is_user=False):
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        lbl.setObjectName("chatBubbleUser" if is_user else "chatBubbleAI")
        lbl.setAlignment(Qt.AlignRight if is_user else Qt.AlignLeft)

        row = QHBoxLayout()
        if is_user:
            row.addStretch()
            row.addWidget(lbl)
        else:
            row.addWidget(lbl)
            row.addStretch()

        self.chat_layout.insertLayout(self.chat_layout.count() - 1, row)
        QTimer.singleShot(
            100,
            lambda: self.chat_scroll.verticalScrollBar().setValue(
                self.chat_scroll.verticalScrollBar().maximum()
            )
        )

    def send_chat(self):
        q = self.chat_input.text().strip()
        if not q:
            return
        self.chat_input.clear()
        self.add_bubble(q, is_user=True)
        self.chat_count += 1

        if self.chat_count == 1:
            ql = q.lower()
            if any(w in ql for w in ["salary", "ctc", "pay", "compens"]):
                reply = "CTC is Rs. 12,00,000 – 18,00,000 per annum. Perks include Health Insurance, Relocation Bonus, and ESOPs."
            elif any(w in ql for w in ["process", "round", "interview", "selection"]):
                reply = "Selection process: Online Assessment → Technical Interview (x2) → HR/Cultural Fitment Interview."
            elif any(w in ql for w in ["eligible", "branch", "cgpa", "backlog"]):
                reply = "Eligible branches: CSE, ECE, IT, Data Science. Minimum CGPA: 7.5. No active backlogs allowed."
            elif any(w in ql for w in ["location", "where", "remote", "city"]):
                reply = "The role is based in Bangalore with a Remote option available."
            elif any(w in ql for w in ["role", "position", "job", "title"]):
                reply = "Open position: Software Development Engineer at InnovateTech Solutions."
            else:
                reply = (
                    "Summary — Company: InnovateTech Solutions, Role: SDE, "
                    "CTC: Rs. 30-45 LPA, Location: Bangalore / Remote. "
                    "Feel free to ask more specific questions."
                )
        else:
            reply = "No new job role found. No additional placement opportunities are currently available in the database."

        QTimer.singleShot(900, lambda: self.add_bubble(reply, is_user=False))