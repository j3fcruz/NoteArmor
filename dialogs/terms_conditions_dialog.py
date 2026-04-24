# dialog/terms_conditions_dialog.py

"""
Terms and Conditions dialog for Secure Notepad Pro (PySide6)
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame, QCheckBox
)
from PySide6.QtGui import QFont, QIcon, QTextDocument
from PySide6.QtCore import Qt
from config.app_config import APP_NAME, APP_VERSION, APP_DEVELOPER, AUTHOR, TERMS_ICON_PATH
from resources import icons_rc
_ = icons_rc


class TermsConditionsDialog(QDialog):
    """Terms and Conditions dialog for Secure Notepad Pro"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{APP_NAME} - Terms and Conditions")
        self.setWindowIcon(QIcon(TERMS_ICON_PATH))
        self.setFixedSize(750, 800)
        self.setModal(True)

        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_label = QLabel("Terms and Conditions")
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Subtitle
        subtitle_label = QLabel(f"{APP_NAME} Pro - Version {APP_VERSION}")
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # Terms Content
        self.terms_content = QTextEdit()
        self.terms_content.setReadOnly(True)
        self.terms_content.setHtml(f"""
        <div>
            <h3>1. Acceptance of Terms</h3>
            <p>By using {APP_NAME} Pro ("Software"), you agree to comply with and be bound by these Terms and Conditions. If you do not agree with any part of these terms, please do not use the Software.</p>

            <h3>2. License Grant</h3>
            <p>{APP_NAME} Pro is provided as-is with a personal, non-exclusive, non-transferable license. You may use this Software on a single device for personal and professional purposes. Redistribution or modification without explicit permission is prohibited.</p>

            <h3>3. User Responsibilities</h3>
            <p>You are responsible for:</p>
            <ul>
                <li>Maintaining the confidentiality of any encryption keys or passwords</li>
                <li>Creating regular backups of your important notes and documents</li>
                <li>Ensuring compliance with all applicable laws and regulations</li>
                <li>Using the Software for lawful purposes only</li>
            </ul>

            <h3>4. Data Security and Privacy</h3>
            <p>{APP_NAME} Pro employs industry-standard encryption to protect your data. However, no method of transmission or storage is completely secure. We recommend backing up your important data regularly. We do not store, monitor, or access your personal notes without your explicit consent.</p>

            <h3>5. Limitation of Liability</h3>
            <p>THE SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. IN NO EVENT SHALL {APP_DEVELOPER} BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES, INCLUDING DATA LOSS OR BUSINESS INTERRUPTION.</p>

            <h3>6. Disclaimer of Warranties</h3>
            <p>We make no warranties, express or implied, regarding the Software's fitness for a particular purpose, merchantability, or non-infringement. Use at your own discretion and risk.</p>

            <h3>7. Prohibited Uses</h3>
            <p>You may not use the Software to:</p>
            <ul>
                <li>Engage in illegal activities or violate any laws</li>
                <li>Harass, abuse, or threaten others</li>
                <li>Create malware or attempt unauthorized access</li>
                <li>Reverse engineer or attempt to decompile the Software</li>
                <li>Circumvent security measures or encryption</li>
            </ul>

            <h3>8. Intellectual Property</h3>
            <p>All intellectual property rights in {APP_NAME} Pro, including copyrights, trademarks, and patents, are owned by {APP_DEVELOPER}. You may not reproduce, distribute, or transmit the Software without explicit written permission.</p>

            <h3>9. Updates and Modifications</h3>
            <p>We reserve the right to modify, update, or discontinue the Software at any time. Changes may include feature updates, security patches, or interface improvements. You agree to accept such updates.</p>

            <h3>10. Termination</h3>
            <p>Your license to use the Software may be terminated if you violate these Terms and Conditions. Upon termination, you must cease all use and delete all copies from your devices.</p>

            <h3>11. Governing Law</h3>
            <p>These Terms and Conditions are governed by applicable laws. Any disputes shall be resolved through appropriate legal channels.</p>

            <h3>12. Contact Information</h3>
            <p>For questions or concerns about these Terms and Conditions, please contact:</p>
            <p><strong>Developer:</strong> {APP_DEVELOPER}<br/><strong>Author:</strong> {AUTHOR}</p>

            <h3>13. Entire Agreement</h3>
            <p>These Terms and Conditions constitute the entire agreement between you and {APP_DEVELOPER} regarding the Software and supersede all prior agreements and understandings.</p>

            <p><strong>Last Updated:</strong> {APP_VERSION}<br/>By using {APP_NAME} Pro, you acknowledge that you have read, understood, and agree to be bound by these Terms and Conditions.</p>
        </div>
        """)

        layout.addWidget(self.terms_content)

        # Acceptance Checkbox
        acceptance_layout = QHBoxLayout()
        self.accept_checkbox = QCheckBox("I have read and agree to the Terms and Conditions")
        acceptance_layout.addWidget(self.accept_checkbox)
        acceptance_layout.addStretch()
        layout.addLayout(acceptance_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.print_btn = QPushButton("Print")
        self.print_btn.setFixedWidth(100)
        self.print_btn.setMinimumHeight(38)
        self.print_btn.clicked.connect(self.print_terms)
        button_layout.addWidget(self.print_btn)

        button_layout.addStretch()

        self.accept_btn = QPushButton("Accept & Continue")
        self.accept_btn.setFixedWidth(150)
        self.accept_btn.setMinimumHeight(38)
        self.accept_btn.setEnabled(False)
        self.accept_btn.clicked.connect(self.accept_terms)
        self.accept_checkbox.stateChanged.connect(
            lambda: self.accept_btn.setEnabled(self.accept_checkbox.isChecked())
        )
        button_layout.addWidget(self.accept_btn)

        layout.addLayout(button_layout)

    def accept_terms(self):
        """Accept terms and close dialog"""
        if self.accept_checkbox.isChecked():
            self.accept()

    def print_terms(self):
        """Print terms and conditions"""
        try:
            from PySide6.QtPrintSupport import QPrinter, QPrintDialog

            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)

            if dialog.exec() == QDialog.Accepted:
                doc = QTextDocument()
                doc.setHtml(self.terms_content.toHtml())
                doc.print(printer)
        except Exception as e:
            print(f"Print error: {e}")
