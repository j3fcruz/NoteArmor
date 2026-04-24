"""
dialogs/save_dialog.py
NoteArmor Personal Use Edition — Password-only save dialog.

REMOVED vs Pro:
    - Mode 2: Password + Keyfile  (radio button, keyfile widget, browse/generate)
    - select_keyfile()            — file browser for keyfile selection
    - generate_keyfile()          — generates random 32-byte keyfile
    - self.keyfile_path attribute — no longer exposed
    - self.keyfile_widget         — QWidget container for keyfile UI
    - keyfile_input, browse_btn, gen_btn UI elements
    - keyfile validation in accept_dialog()

PRESERVED:
    - Mode 0: Plaintext (no encryption)
    - Mode 1: Password only
    - Password / confirm-password fields with show/hide toggle
    - Password-match live indicator
    - All validation logic for password strength and match
    - self.save_mode and self.password attributes (consumed by caller)

FIX:
    - Removed setMinimumHeight() — was clipping enc_group when revealed
    - adjustSize() called on mode toggle so dialog grows/shrinks cleanly
    - Removed addStretch() inside enc_group — caused uneven spacing
    - setFixedWidth(480) keeps width stable while height is layout-driven
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QButtonGroup, QMessageBox, QGroupBox, QFrame,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class SaveModeDialog(QDialog):
    """Dialog to choose between plaintext or password-encrypted save."""

    def __init__(self, parent=None, crypto_available=True):
        super().__init__(parent)
        self.setWindowTitle("Save Options")
        self.setFixedWidth(480)          # width is fixed; height is layout-driven
        self.crypto_available = crypto_available

        self.save_mode = "plaintext"
        self.password  = ""

        self._init_ui()
        self._center()

    def _center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 18, 20, 16)

        # ── Title ─────────────────────────────────────────────────────────────
        title = QLabel("Save Options")
        font  = QFont()
        font.setPointSize(13)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)

        subtitle = QLabel("Choose how to save your note.")
        subtitle.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(subtitle)

        self._separator(layout)
        self._create_mode_selection(layout)
        self._create_encryption_fields(layout)
        self._separator(layout)
        self._create_buttons(layout)
        self.setLayout(layout)

    def _separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

    # ── Mode selection ────────────────────────────────────────────────────────

    def _create_mode_selection(self, parent_layout):
        group  = QGroupBox("Save Mode")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 8, 10, 10)

        self.mode_buttons = QButtonGroup(self)

        plaintext = QRadioButton("💾  Plaintext — No encryption")
        plaintext.setChecked(True)
        self.mode_buttons.addButton(plaintext, 0)
        layout.addWidget(plaintext)

        enc_label = QLabel("🔐  Encrypted Mode:")
        enc_label.setStyleSheet("font-weight: bold; color: #aaa; font-size: 11px;")
        layout.addWidget(enc_label)

        mode1 = QRadioButton("🔒  Mode 1: Password only")
        self.mode_buttons.addButton(mode1, 1)
        layout.addWidget(mode1)

        self.mode_buttons.buttonClicked.connect(self._on_mode_changed)
        group.setLayout(layout)
        parent_layout.addWidget(group)

    # ── Encryption fields ─────────────────────────────────────────────────────

    def _create_encryption_fields(self, parent_layout):
        self.enc_group = QGroupBox("Encryption Settings")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 12)

        # Password
        pwd_label = QLabel("Password:")
        pwd_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(pwd_label)

        pwd_row = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter a strong password (min 6 chars)")
        self.password_input.setMinimumHeight(30)
        self.password_input.textChanged.connect(self._on_password_changed)
        pwd_row.addWidget(self.password_input)

        show_btn = QPushButton("👁")
        show_btn.setFixedSize(34, 30)
        show_btn.setCheckable(True)
        show_btn.setToolTip("Show / hide password")
        show_btn.toggled.connect(
            lambda c: self.password_input.setEchoMode(
                QLineEdit.Normal if c else QLineEdit.Password
            )
        )
        pwd_row.addWidget(show_btn)
        layout.addLayout(pwd_row)

        # Confirm password
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(confirm_label)

        confirm_row = QHBoxLayout()
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setPlaceholderText("Re-enter password to confirm")
        self.confirm_input.setMinimumHeight(30)
        self.confirm_input.textChanged.connect(self._on_password_changed)
        confirm_row.addWidget(self.confirm_input)

        show_confirm = QPushButton("👁")
        show_confirm.setFixedSize(34, 30)
        show_confirm.setCheckable(True)
        show_confirm.toggled.connect(
            lambda c: self.confirm_input.setEchoMode(
                QLineEdit.Normal if c else QLineEdit.Password
            )
        )
        confirm_row.addWidget(show_confirm)
        layout.addLayout(confirm_row)

        # Match indicator
        self.pwd_match_label = QLabel("")
        self.pwd_match_label.setStyleSheet("font-size: 11px;")
        self.pwd_match_label.setFixedHeight(18)
        layout.addWidget(self.pwd_match_label)

        self.enc_group.setLayout(layout)
        self.enc_group.setVisible(False)
        parent_layout.addWidget(self.enc_group)

    # ── Buttons ───────────────────────────────────────────────────────────────

    def _create_buttons(self, parent_layout):
        row = QHBoxLayout()

        cancel = QPushButton("Cancel")
        cancel.setFixedWidth(100)
        cancel.setMinimumHeight(34)
        cancel.clicked.connect(self.reject)
        row.addWidget(cancel)

        row.addStretch()

        save = QPushButton("💾  Save")
        save.setFixedWidth(120)
        save.setMinimumHeight(34)
        save.setDefault(True)
        save.clicked.connect(self._accept_dialog)
        row.addWidget(save)

        parent_layout.addLayout(row)

    # ── Handlers ──────────────────────────────────────────────────────────────

    def _on_mode_changed(self):
        mode_id = self.mode_buttons.checkedId()

        if mode_id == 0:
            self.save_mode = "plaintext"
            self.enc_group.setVisible(False)
        else:
            self.save_mode = "password_only"
            self.enc_group.setVisible(True)
            self.password_input.setFocus()

        # Let the layout recalculate and resize the dialog to fit
        self.adjustSize()
        self._on_password_changed()

    def _on_password_changed(self):
        p1 = self.password_input.text()
        p2 = self.confirm_input.text()

        if not p2:
            self.pwd_match_label.setText("")
        elif p1 == p2:
            self.pwd_match_label.setText("✔  Passwords match")
            self.pwd_match_label.setStyleSheet("color: #4caf50; font-size: 11px;")
        else:
            self.pwd_match_label.setText("✘  Passwords do not match")
            self.pwd_match_label.setStyleSheet("color: #f44336; font-size: 11px;")

    def _accept_dialog(self):
        if self.save_mode == "plaintext":
            self.accept()
            return

        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Password Required", "Please enter a password.")
            self.password_input.setFocus()
            return

        if len(password) < 6:
            QMessageBox.warning(
                self, "Password Too Short",
                "Password must be at least 6 characters.",
            )
            self.password_input.setFocus()
            return

        if password != self.confirm_input.text():
            QMessageBox.warning(
                self, "Passwords Don't Match",
                "The two passwords you entered don't match.\n"
                "Please re-enter them carefully.",
            )
            self.confirm_input.clear()
            self.confirm_input.setFocus()
            return

        self.password = password
        self.accept()