# dialog/donate_dialog.py
# ---------------------------------------------------------
# 💖 Donate Dialog - Secure Notepad Pro (PySide6 Version)
# ---------------------------------------------------------

import os
import sys
import webbrowser
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame, QGroupBox, QMessageBox, QApplication
)
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt

from config.app_config import (
    APP_NAME, GITHUB_ID, PAYPAL_ID, KOFI_ID,
    BTC_ID, ETH_ID, HASH_NAME, DONATE_ICON_PATH
)
from utils.icon_manager import load_icon
_ = load_icon
from resources import icons_rc
_ = icons_rc


class DonateDialog(QDialog):
    """Modern donation dialog supporting multi-platform links."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Support {APP_NAME}")
        self.setFixedSize(580, 680)
        self.setWindowIcon(QIcon(DONATE_ICON_PATH))
        self.setModal(True)
        self.setup_ui()

    # ---------------------------------------------------------
    # 🧱 Layout Structure
    # ---------------------------------------------------------
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(18)
        layout.setContentsMargins(22, 22, 22, 22)

        # --- Header ---
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        donate_icon = QLabel()
        donate_pixmap = QPixmap(DONATE_ICON_PATH)
        donate_icon.setPixmap(donate_pixmap.scaledToHeight(28, Qt.SmoothTransformation))
        header_layout.addWidget(donate_icon)

        header = QLabel(f"Support {APP_NAME}")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Segoe UI", 22, QFont.Bold))
        header_layout.addWidget(header)

        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Subtitle
        subtitle = QLabel("Help us continue improving this tool for the community.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #A0A0A0; font-size: 11pt;")
        layout.addWidget(subtitle)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        layout.addWidget(sep)

        # --- Why Support ---
        about = QTextEdit()
        about.setReadOnly(True)
        about.setMaximumHeight(160)
        about.setHtml(f"""
        <div style="font-size: 13px; line-height: 1.6;">
            <p><b>Why Support Us?</b></p>
            <p>{APP_NAME} is a privacy-first, open-source application built for professionals. 
            Your support allows us to:</p>
            <ul>
                <li>Develop innovative new features</li>
                <li>Maintain security and stability</li>
                <li>Offer detailed documentation and community support</li>
                <li>Keep the software open and accessible to everyone</li>
            </ul>
        </div>
        """)
        layout.addWidget(about)

        # --- Support Options ---
        support_group = QGroupBox("Ways to Support")
        support_layout = QVBoxLayout(support_group)
        support_layout.setSpacing(14)

        support_layout.addLayout(self._build_option(
            "⭐", "Star us on GitHub", "Follow and star our repository to support the project.",
            "Visit GitHub", lambda: webbrowser.open(GITHUB_ID)
        ))

        support_layout.addLayout(self._build_option(
            "💳", "Donate via PayPal", "Secure and convenient way to support us.",
            "Donate Now", lambda: webbrowser.open(PAYPAL_ID)
        ))

        support_layout.addLayout(self._build_option(
            "☕", "Buy us a Coffee", "Support development with small donations.",
            "Ko-fi", lambda: webbrowser.open(KOFI_ID)
        ))

        support_layout.addLayout(self._build_option(
            "🪙", "Cryptocurrency", "Support via Bitcoin or Ethereum.",
            "View Addresses", self.show_crypto_addresses
        ))

        layout.addWidget(support_group)

        # --- Thank You ---
        thanks = QLabel(
            f"Your support helps us deliver new updates and maintain {APP_NAME}.\n"
            "Every contribution motivates us to build better, faster, and safer tools."
        )
        thanks.setWordWrap(True)
        thanks.setAlignment(Qt.AlignCenter)
        thanks.setStyleSheet("""
            color: #A0A0A0;
            font-style: italic;
            padding: 12px;
            border-left: 4px solid #4F6BED;
            background-color: rgba(80, 80, 120, 0.15);
            border-radius: 8px;
        """)
        layout.addWidget(thanks)

        # --- Footer Buttons ---
        footer = QHBoxLayout()
        share_btn = QPushButton("Share with Friends")
        share_btn.setMinimumHeight(38)
        share_btn.clicked.connect(self.share_application)
        footer.addWidget(share_btn)

        footer.addStretch()

        close_btn = QPushButton("Close")
        close_btn.setMinimumHeight(38)
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.accept)
        footer.addWidget(close_btn)
        layout.addLayout(footer)

    # ---------------------------------------------------------
    # ⚙️ Helper - Donation Option Layout
    # ---------------------------------------------------------
    def _build_option(self, emoji, title, subtitle, button_text, action):
        layout = QHBoxLayout()
        icon = QLabel(emoji)
        icon.setFont(QFont("Segoe UI Emoji", 14))
        text_layout = QVBoxLayout()
        label = QLabel(title)
        label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        sub = QLabel(subtitle)
        sub.setStyleSheet("color: #888; font-size: 10pt;")
        text_layout.addWidget(label)
        text_layout.addWidget(sub)
        btn = QPushButton(button_text)
        btn.setFixedHeight(36)
        btn.setFixedWidth(135)
        btn.clicked.connect(action)
        layout.addWidget(icon)
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(btn)
        return layout

    # ---------------------------------------------------------
    # 💰 Show Crypto
    # ---------------------------------------------------------
    def show_crypto_addresses(self):
        msg = (
            f"<b>Bitcoin (BTC)</b><br>{BTC_ID}<br><br>"
            f"<b>Ethereum (ETH)</b><br>{ETH_ID}"
        )
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Information)
        box.setWindowTitle("Crypto Addresses")
        box.setTextFormat(Qt.RichText)
        box.setText(msg)
        box.setFont(QFont("Segoe UI", 10))
        copy_btn = QPushButton("Copy All")
        box.addButton(copy_btn, QMessageBox.ButtonRole.ActionRole)
        box.addButton(QMessageBox.StandardButton.Ok)
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(
            f"Bitcoin (BTC): {BTC_ID}\nEthereum (ETH): {ETH_ID}"
        ))
        box.exec()

    # ---------------------------------------------------------
    # 📢 Share Application
    # ---------------------------------------------------------
    def share_application(self):
        share_text = (
            f"Spread the word about {APP_NAME}!\n\n"
            "📣 Share on social media:\n"
            f"• Twitter: Use #{HASH_NAME}\n"
            "• LinkedIn: Post to your professional network\n"
            "• Reddit: Share in r/Python\n"
            "• Discord: Tell your dev communities\n\n"
            "Together, we grow open-source innovation."
        )

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Share & Support")
        msg_box.setText(share_text)
        msg_box.setFont(QFont("Segoe UI", 10))
        copy_btn = QPushButton("Copy Message")
        msg_box.addButton(copy_btn, QMessageBox.ButtonRole.ActionRole)
        msg_box.addButton(QMessageBox.StandardButton.Ok)
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(share_text))
        msg_box.exec()
