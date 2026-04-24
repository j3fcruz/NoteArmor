"""
dialogs/about_dialog.py
NoteArmor — Personal Use Edition
About dialog (simplified, corrected for Free Edition).

REMOVED vs Pro:
    - Libraries tab       — unnecessary for end users
    - Support tab         — links moved to Help menu in main window
    - Donate references   — not part of personal use edition UI
    - Enterprise/Pro feature descriptions

PRESERVED:
    - Header with app icon, name, version
    - About tab (corrected features for Free Edition)
    - App Info tab (corrected: PySide6, platform, python version)
    - License tab (PU-NC v1.0 full text)
"""

import sys
import webbrowser
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame, QTabWidget, QWidget
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt

from config.app_config import (
    APP_NAME, APP_VERSION, APP_DEVELOPER, AUTHOR,
    ABOUT_ICON_PATH, HOMEPAGE, GITHUB_ID
)
from utils.icon_manager import load_icon
from resources import icons_rc  # noqa: F401
_ = icons_rc

_PUNC_LICENSE = """\
NoteArmor Personal Use and Non-Commercial License (PU-NC)
Version 1.0
Copyright (c) 2026 PatronHub Devs

1. DEFINITIONS
"Software" refers to the NoteArmor application, including all source code,
binaries, and associated files.
"Author" refers to PatronHub Devs and its contributors.
"Personal Use" means use by an individual for private, non-commercial purposes.
"Commercial Use" includes any use intended for commercial advantage, monetary
compensation, or business operations.

2. GRANT OF LICENSE
Permission is hereby granted to any individual to:
  - Use the Software for personal, non-commercial purposes
  - View and study the source code
  - Modify the Software for personal use only

3. RESTRICTIONS
You are NOT permitted to:
  - Use the Software for any commercial purpose
  - Sell, sublicense, or distribute the Software (modified or unmodified)
  - Offer the Software as a service (SaaS, hosted, or cloud-based)
  - Rebrand, rename, or claim the Software as your own
  - Create derivative works intended for public distribution
  - Remove or alter any copyright or attribution notices

4. DISTRIBUTION
Redistribution of the Software, in whole or in part, is strictly prohibited
without explicit written permission from the Author.

5. INTELLECTUAL PROPERTY
All rights, title, and interest in the Software remain the exclusive property
of the Author. This license does not grant any ownership rights.

6. TERMINATION
This license is automatically terminated if you violate any of its terms.
Upon termination, you must cease all use of the Software and delete all copies.

7. DISCLAIMER OF WARRANTY
The Software is provided "AS IS", without warranty of any kind, express or
implied, including but not limited to:
  - Fitness for a particular purpose
  - Non-infringement
  - Security or reliability
The Author is not liable for any damages arising from the use of the Software.

8. LIMITATION OF LIABILITY
In no event shall the Author be liable for any claim, damages, or other
liability arising from:
  - Use of the Software
  - Inability to use the Software
  - Data loss or corruption

9. GOVERNING LAW
This license shall be governed by and interpreted in accordance with
applicable laws.

10. CONTACT
For permissions, licensing inquiries, or commercial use requests, contact:
Email: contact@patronhubdevs.online

By using this Software, you agree to the terms of this license.
"""


class AboutDialog(QDialog):
    """About dialog for NoteArmor Personal Use Edition."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"About {APP_NAME}")
        self.setFixedSize(560, 480)
        self.setModal(True)
        self.setWindowIcon(QIcon(ABOUT_ICON_PATH))
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(12)

        # ── Header ────────────────────────────────────────────────────────────
        header = QFrame()
        h_row  = QHBoxLayout(header)
        h_row.setContentsMargins(0, 0, 0, 0)
        h_row.setSpacing(14)

        icon_lbl = QLabel()
        icon_lbl.setFixedSize(64, 64)
        app_icon = load_icon(ABOUT_ICON_PATH)
        if app_icon and not app_icon.isNull():
            icon_lbl.setPixmap(app_icon.pixmap(64, 64))
        else:
            icon_lbl.setStyleSheet(
                "QLabel { background:#1a73e8; border-radius:32px;"
                " color:white; font-size:22px; font-weight:bold; }"
            )
            icon_lbl.setAlignment(Qt.AlignCenter)
            icon_lbl.setText("NA")
        h_row.addWidget(icon_lbl)

        title_col = QVBoxLayout()
        title_col.setSpacing(2)
        name_lbl = QLabel(APP_NAME)
        name_lbl.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_col.addWidget(name_lbl)

        ver_lbl = QLabel(f"Version {APP_VERSION}  —  Personal Use Edition")
        ver_lbl.setStyleSheet("color:#aaa; font-size:11px;")
        title_col.addWidget(ver_lbl)

        dev_lbl = QLabel(f"{APP_DEVELOPER}")
        dev_lbl.setStyleSheet("color:#888; font-size:10px;")
        title_col.addWidget(dev_lbl)

        h_row.addLayout(title_col)
        h_row.addStretch()
        layout.addWidget(header)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        layout.addWidget(sep)

        # ── Tabs ──────────────────────────────────────────────────────────────
        tabs = QTabWidget()
        tabs.addTab(self._tab_about(),    "About")
        tabs.addTab(self._tab_app_info(), "App Info")
        tabs.addTab(self._tab_license(),  "License")
        layout.addWidget(tabs, 1)

        # ── Footer ────────────────────────────────────────────────────────────
        footer = QHBoxLayout()
        footer.addStretch()
        ok_btn = QPushButton("OK")
        ok_btn.setFixedWidth(80)
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.accept)
        footer.addWidget(ok_btn)
        layout.addLayout(footer)

    # ── About tab ─────────────────────────────────────────────────────────────

    def _tab_about(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(14, 14, 14, 14)
        l.setSpacing(10)

        desc = QTextEdit()
        desc.setReadOnly(True)
        desc.setHtml(f"""
        <style>
          body {{ font-family: Segoe UI, sans-serif; font-size: 13px; }}
          h4   {{ margin-bottom: 4px; color: #4a90d9; }}
          li   {{ margin-bottom: 3px; }}
        </style>
        <h4>{APP_NAME}</h4>
        <p>
          A privacy-first encrypted notepad built for personal use.
          Write, encrypt, and protect your notes with a strong password —
          only you can decrypt them.
        </p>
        <h4>Features</h4>
        <ul>
          <li><b>Password Encryption</b> — Notes saved with Fernet
              (AES-128-CBC + HMAC-SHA256), key derived via PBKDF2-HMAC-SHA256.</li>
          <li><b>Plaintext Mode</b> — Save unencrypted <code>.txt</code> files when privacy
              is not needed.</li>
          <li><b>Multi-Tab</b> — Work on several notes simultaneously.</li>
          <li><b>Autosave</b> — Modified open files are saved automatically every minute.</li>
          <li><b>Zoom Support</b> — Ctrl + scroll or keyboard shortcuts to adjust font size.</li>
          <li><b>Lightweight</b> — Single-theme, minimal UI with no bloat.</li>
        </ul>
        <p style="color:#888; font-size:11px;">
          © 2026 {APP_DEVELOPER}. Personal use only — see License tab.
        </p>
        """)
        l.addWidget(desc)
        return w

    # ── App Info tab ──────────────────────────────────────────────────────────

    def _tab_app_info(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(14, 14, 14, 14)
        l.setSpacing(10)

        rows = [
            ("Application",  APP_NAME),
            ("Version",      APP_VERSION),
            ("Edition",      "Personal Use (Free)"),
            ("Developer",    AUTHOR),
            ("Organization", APP_DEVELOPER),
            ("Python",       f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"),
            ("GUI Framework","PySide6 (Qt6)"),
            ("Platform",     sys.platform.upper()),
            ("License",      "PU-NC v1.0 — Non-Commercial"),
            ("Contact",      "contact@patronhubdevs.online"),
        ]

        for label, value in rows:
            self._info_row(l, label, value)

        l.addStretch()

        link_row = QHBoxLayout()
        for text, url in [
            ("🌐 Website", HOMEPAGE),
            ("💻 GitHub",  GITHUB_ID),
        ]:
            btn = QPushButton(text)
            btn.setFixedHeight(32)
            btn.clicked.connect(lambda _, u=url: webbrowser.open(u))
            link_row.addWidget(btn)
        link_row.addStretch()
        l.addLayout(link_row)

        return w

    def _info_row(self, layout, label_text, value_text):
        row = QHBoxLayout()
        row.setSpacing(10)

        lbl = QLabel(f"{label_text}:")
        lbl.setFont(QFont("Segoe UI", 9, QFont.Bold))
        lbl.setFixedWidth(120)

        val = QLabel(value_text)
        val.setStyleSheet("color:#4a90d9; font-size:10px;")
        val.setWordWrap(True)

        row.addWidget(lbl)
        row.addWidget(val)
        layout.addLayout(row)

    # ── License tab ───────────────────────────────────────────────────────────

    def _tab_license(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(14, 14, 14, 14)
        l.setSpacing(8)

        hdr = QLabel("PU-NC License v1.0 — Personal Use & Non-Commercial")
        hdr.setFont(QFont("Segoe UI", 10, QFont.Bold))
        l.addWidget(hdr)

        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setFont(QFont("Consolas", 9))
        txt.setPlainText(_PUNC_LICENSE)
        l.addWidget(txt)

        copy_btn = QPushButton("📋 Copy License Text")
        copy_btn.setFixedHeight(32)
        copy_btn.clicked.connect(lambda: self._copy_license(txt.toPlainText()))
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(copy_btn)
        l.addLayout(btn_row)

        return w

    def _copy_license(self, text):
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(text)