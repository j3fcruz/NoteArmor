"""
dialogs/help_dialog.py
NoteArmor Personal Use Edition — simplified help dialog.

REMOVED vs Free Edition:
    - "Free Edition" branding replaced with "Personal Use"
    - Encryption tech-spec details (simplified for end-users)
    - Pro version cross-references in troubleshooting

PRESERVED:
    - Quick Start guide
    - Keyboard shortcuts
    - Encryption & Security summary
    - Troubleshooting
    - License section (PU-NC v1.0)
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton, QLabel,
)
from PySide6.QtGui import QFont, QIcon

from config.app_config import APP_NAME, APP_VERSION, APP_DEVELOPER, AUTHOR, HELP_ICON_PATH
from resources import icons_rc  # noqa: F401

_HELP_HTML = """
<style>
  body  {{ font-family: Segoe UI, sans-serif; font-size: 13px; margin: 12px; }}
  h2   {{ color: #4a90d9; margin-top: 20px; margin-bottom: 4px; border-bottom: 1px solid #333; padding-bottom: 3px; }}
  h3   {{ margin-top: 12px; margin-bottom: 2px; color: #ccc; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: 6px; }}
  th, td {{ border: 1px solid #555; padding: 5px 8px; }}
  th   {{ background: #2a2a3a; }}
  code {{ background: #2a2a2a; padding: 1px 4px; border-radius: 3px; }}
  ul, ol {{ margin-top: 4px; padding-left: 20px; }}
  li   {{ margin-bottom: 3px; }}
  .warn  {{ color: #e57373; font-weight: bold; }}
  .block {{ background: #1e1e2e; border-left: 4px solid #4a90d9;
            padding: 10px 14px; border-radius: 4px; margin-top: 8px; }}
  .license-clause {{ margin-bottom: 6px; }}
  .restricted {{ color: #e57373; }}
  .allowed    {{ color: #81c784; }}
</style>

<h2>Welcome to {app_name} {app_version}</h2>
<div class="block">
  A privacy-first encrypted notepad for personal use.
  Write your notes, protect them with a password, and open them safely —
  only the correct password can decrypt your content.
</div>

<h2>Quick Start</h2>
<ol>
  <li>Launch the app — a blank <b>Untitled</b> tab opens automatically.</li>
  <li>Type your note.</li>
  <li><b>File → Save As</b> → choose <em>Mode 1: Password only</em>
      → set a strong password → save as <code>.notearmor</code>.</li>
  <li>To reopen: <b>File → Open</b> → select the <code>.notearmor</code> file
      → enter your password.</li>
</ol>

<h2>Keyboard Shortcuts</h2>
<table>
  <tr><th>Action</th><th>Shortcut</th></tr>
  <tr><td>New Tab</td><td><b>Ctrl + N</b></td></tr>
  <tr><td>Open File</td><td><b>Ctrl + O</b></td></tr>
  <tr><td>Save</td><td><b>Ctrl + S</b></td></tr>
  <tr><td>Save As</td><td><b>Ctrl + Shift + S</b></td></tr>
  <tr><td>Undo / Redo</td><td><b>Ctrl + Z / Y</b></td></tr>
  <tr><td>Cut / Copy / Paste</td><td><b>Ctrl + X / C / V</b></td></tr>
  <tr><td>Zoom In / Out</td><td><b>Ctrl + + / −</b> or Ctrl + scroll</td></tr>
  <tr><td>Reset Zoom</td><td><b>Ctrl + R</b></td></tr>
  <tr><td>Exit</td><td><b>Ctrl + Q</b></td></tr>
</table>

<h2>Encryption &amp; Security</h2>
<p>
  Your notes are encrypted with a strong symmetric cipher and a key derived
  from your password. Every save uses a fresh random salt — two saves of the
  same text produce completely different ciphertext.
</p>
<ul>
  <li>Use passwords of <b>12+ characters</b> with mixed types for best security.</li>
  <li>Store your <code>.txt.enc</code> files in a secure, backed-up location.</li>
  <li>Encrypted files are detected automatically by their extension.</li>
</ul>
<p class="warn">
  ⚠ Forgotten passwords cannot be recovered — there is no back door.
</p>

<h2>Troubleshooting</h2>
<h3>File won't open / wrong password error</h3>
<p>Passwords are case-sensitive. Verify you are entering the exact password used when saving.</p>
<h3>Slow startup</h3>
<p>Exclude the application folder from real-time antivirus scanning.</p>
<h3>Getting support</h3>
<p>Use <b>Help → Submit Feedback</b> or visit the Homepage link in the same menu.</p>

<h2>License — Personal Use &amp; Non-Commercial (PU-NC v1.0)</h2>
<p>Copyright © 2025 - 2026 {app_developer}. All rights reserved.</p>

<h3>You MAY:</h3>
<ul>
  <li class="allowed">✔ Use this software for personal, non-commercial purposes</li>
  <li class="allowed">✔ View and study the source code</li>
  <li class="allowed">✔ Modify the software for your own personal use</li>
</ul>

<h3>You MAY NOT:</h3>
<ul>
  <li class="restricted">✘ Use the software for any commercial purpose</li>
  <li class="restricted">✘ Sell, sublicense, or distribute the software</li>
  <li class="restricted">✘ Offer the software as a service (SaaS, hosted, or cloud-based)</li>
  <li class="restricted">✘ Rebrand, rename, or claim the software as your own</li>
  <li class="restricted">✘ Distribute derivative works publicly</li>
  <li class="restricted">✘ Remove or alter any copyright or attribution notices</li>
</ul>

<div class="block">
  <b>Disclaimer:</b> This software is provided "AS IS" without any warranty.
  {app_developer} is not liable for any damages, data loss, or issues arising
  from the use of this software.<br><br>
  <b>Contact:</b> contact@patronhubdevs.online
</div>

<p style="color:#666; font-size:11px; margin-top:14px;">
  By using {app_name}, you agree to the terms of the PU-NC License v1.0.
</p>
"""


class HelpDialog(QDialog):
    """Single-page help dialog for NoteArmor Personal Use Edition."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{APP_NAME} — Help")
        self.setMinimumSize(620, 560)
        self.setModal(True)
        self.setWindowIcon(QIcon(HELP_ICON_PATH))
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(10)

        header = QLabel(f"📘  {APP_NAME} — Help")
        header.setFont(QFont("Segoe UI", 13, QFont.Bold))
        layout.addWidget(header)

        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setHtml(
            _HELP_HTML.format(
                app_name=APP_NAME,
                app_version=APP_VERSION,
                app_developer=APP_DEVELOPER,
            )
        )
        layout.addWidget(browser)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setFixedWidth(90)
        close_btn.setDefault(True)
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)