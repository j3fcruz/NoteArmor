"""
dialogs/password_entry_dialog.py
NoteArmor Personal Use Edition — Password-only decrypt prompt.

REMOVED vs Pro:
    - keyfile_required parameter  — always False in Free Edition
    - keyfile UI block (label, input, browse button)
    - _browse_kf()                — file browser for keyfile
    - self.keyfile_path attribute — not needed without keyfile support
    - keyfile validation in _accept()

PRESERVED:
    - Password field with show/hide toggle
    - self.password attribute (consumed by caller)
    - QDialogButtonBox OK / Cancel
    - All password validation logic
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QDialogButtonBox, QFrame,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class PasswordEntryDialog(QDialog):
    """Password prompt shown when opening a password-encrypted file."""

    def __init__(self, parent=None, keyfile_required=False):
        # keyfile_required is accepted for API compatibility but ignored.
        super().__init__(parent)
        self.password = ""
        self.setWindowTitle("Open Encrypted File")
        self.setFixedSize(420, 200)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 18, 20, 16)

        # ── Title ─────────────────────────────────────────────────────────────
        title = QLabel("🔒  Decrypt File")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        layout.addWidget(sep)

        # ── Subtitle ──────────────────────────────────────────────────────────
        sub = QLabel("Enter the password used when saving this file:")
        sub.setStyleSheet("color: #aaa; font-size: 11px;")
        layout.addWidget(sub)

        # ── Password row ──────────────────────────────────────────────────────
        row = QHBoxLayout()
        row.setSpacing(6)

        self._pwd = QLineEdit()
        self._pwd.setEchoMode(QLineEdit.Password)
        self._pwd.setPlaceholderText("Enter password…")
        self._pwd.setMinimumHeight(32)
        self._pwd.returnPressed.connect(self._accept)
        row.addWidget(self._pwd)

        eye = QPushButton("👁")
        eye.setFixedSize(34, 32)
        eye.setCheckable(True)
        eye.setToolTip("Show / hide password")
        eye.toggled.connect(
            lambda c: self._pwd.setEchoMode(
                QLineEdit.Normal if c else QLineEdit.Password
            )
        )
        row.addWidget(eye)
        layout.addLayout(row)

        # ── Buttons ───────────────────────────────────────────────────────────
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self._accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

        self._pwd.setFocus()

    def _accept(self):
        self.password = self._pwd.text()
        if not self.password:
            QMessageBox.warning(self, "Password Required", "Please enter your password.")
            self._pwd.setFocus()
            return
        self.accept()