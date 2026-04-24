# dialog/license_dialog.py

"""
License dialog for Secure Notepad Pro (MIT and GPL) – PySide6 version
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame, QTabWidget, QWidget, QApplication, QFileDialog, QMessageBox
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from config.app_config import APP_NAME, APP_DEVELOPER, LICENSE_ICON_PATH
from resources import icons_rc
_ = icons_rc


class LicenseDialog(QDialog):
    """License dialog for MIT and GPL"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{APP_NAME} - Open Source Licenses")
        self.setFixedSize(850, 850)
        self.setWindowIcon(QIcon(LICENSE_ICON_PATH))
        self.setModal(True)

        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_label = QLabel("Open Source Licenses")
        header_label.setFont(QFont("", 18, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Subtitle
        subtitle_label = QLabel(f"{APP_NAME} Pro - Proudly Built with Open Source")
        subtitle_label.setFont(QFont("", 11))
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # License Introduction
        intro_label = QLabel()
        intro_label.setWordWrap(True)
        intro_label.setText(
            f"{APP_NAME} is distributed under multiple open source licenses. "
            "We are committed to respecting the rights of developers and maintaining transparency. "
            "Below are the licenses governing this software and its components."
        )
        layout.addWidget(intro_label)

        # Tab Widget
        self.tab_widget = QTabWidget()
        self.setup_tabs()
        layout.addWidget(self.tab_widget)

        # License Summary
        summary_label = QLabel()
        summary_label.setWordWrap(True)
        summary_label.setText(
            "📋 MIT License: Permissive license allowing commercial and private use with minimal restrictions.\n"
            "📋 GPL License: Copyleft license ensuring derivative works remain open source.\n"
            "For more information, visit: opensource.org/licenses"
        )
        layout.addWidget(summary_label)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        download_btn = QPushButton("📥 Download License Files")
        download_btn.setMinimumHeight(38)
        download_btn.clicked.connect(self.download_licenses)
        button_layout.addWidget(download_btn)

        button_layout.addStretch()

        copy_btn = QPushButton("📋 Copy Current License")
        copy_btn.setFixedWidth(160)
        copy_btn.setMinimumHeight(38)
        copy_btn.clicked.connect(self.copy_current_license)
        button_layout.addWidget(copy_btn)

        close_btn = QPushButton("Close")
        close_btn.setFixedWidth(100)
        close_btn.setMinimumHeight(38)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def setup_tabs(self):
        """Setup license tabs"""
        # MIT License Tab
        mit_widget = QWidget()
        mit_layout = QVBoxLayout(mit_widget)
        mit_layout.setContentsMargins(0, 0, 0, 0)

        mit_header = QLabel("MIT License")
        mit_header.setFont(QFont("", 13, QFont.Bold))
        mit_layout.addWidget(mit_header)

        mit_desc = QLabel(
            "The MIT License is a permissive free software license originating at the Massachusetts Institute of Technology. "
            "It is one of the most permissive licenses available, allowing you to:"
        )
        mit_desc.setWordWrap(True)
        mit_layout.addWidget(mit_desc)

        mit_features = QLabel(
            "✓ Use commercially\n"
            "✓ Modify the source code\n"
            "✓ Distribute the software\n"
            "✓ Use for private purposes\n\n"
            "⚠ Include a copy of the license and copyright notice"
        )
        mit_layout.addWidget(mit_features)

        mit_text = QTextEdit()
        mit_text.setReadOnly(True)
        mit_text.setText(self.get_mit_license())
        mit_layout.addWidget(mit_text)

        self.tab_widget.addTab(mit_widget, "MIT License")

        # GPL v3 License Tab
        gpl_widget = QWidget()
        gpl_layout = QVBoxLayout(gpl_widget)
        gpl_layout.setContentsMargins(0, 0, 0, 0)

        gpl_header = QLabel("GPL v3 License")
        gpl_header.setFont(QFont("", 13, QFont.Bold))
        gpl_layout.addWidget(gpl_header)

        gpl_desc = QLabel(
            "The GNU General Public License v3 (GPLv3) is a free, copyleft license for software and other kinds of works. "
            "It ensures that:"
        )
        gpl_desc.setWordWrap(True)
        gpl_layout.addWidget(gpl_desc)

        gpl_features = QLabel(
            "✓ Software can be used freely\n"
            "✓ Source code is available to all users\n"
            "✓ Derivative works must also be GPL-licensed\n"
            "✓ Changes must be documented\n\n"
            "⚠ Derivative works must use the same license"
        )
        gpl_layout.addWidget(gpl_features)

        gpl_text = QTextEdit()
        gpl_text.setReadOnly(True)
        gpl_text.setText(self.get_gpl_license())
        gpl_layout.addWidget(gpl_text)

        self.tab_widget.addTab(gpl_widget, "GPL v3 License")

        # Third-Party Licenses Tab
        third_widget = QWidget()
        third_layout = QVBoxLayout(third_widget)
        third_layout.setContentsMargins(0, 0, 0, 0)

        third_header = QLabel("Third-Party Dependencies")
        third_header.setFont(QFont("", 13, QFont.Bold))
        third_layout.addWidget(third_header)

        third_text = QTextEdit()
        third_text.setReadOnly(True)
        third_text.setText(self.get_third_party_licenses())
        third_layout.addWidget(third_text)

        self.tab_widget.addTab(third_widget, "Third-Party")

    # -----------------------
    # License Texts
    # -----------------------
    def get_mit_license(self):
        return f"""MIT License

Copyright (c) 2024 {APP_DEVELOPER}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

    def get_gpl_license(self):
        return f"""GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.

TERMS AND CONDITIONS

0. Definitions.

"This License" refers to version 3 of the GNU General Public License.

"Copyright" also means copyright-like laws that apply to other kinds of works,
such as semiconductor masks.

"The Program" refers to any copyrightable work licensed under this License.
Each licensee is addressed as "you".

"Licensees" and "recipients" may be individuals or organizations.

"To modify" a work means to copy from or adapt all or part of the work in a
fashion requiring copyright permission, other than the making of an exact copy.
The resulting work is called a "modified version" of the earlier work or a work
"based on" the earlier work.

"A covered work" means either the unmodified Program or a work based on the Program.

"To propagate" a work means doing anything that, without permission, would make you
directly or secondarily liable for infringement under applicable copyright law.

For detailed information, please visit: https://www.gnu.org/licenses/gpl-3.0.html"""

    def get_third_party_licenses(self):
        return f"""THIRD-PARTY DEPENDENCIES AND LICENSES

1. PyQt5
   License: GPL v3
   Description: Python binding of the cross-platform GUI toolkit Qt
   Website: https://riverbankcomputing.com/software/pyqt/intro

2. Python Standard Library
   License: PSF License
   Description: Python's built-in modules and utilities
   Website: https://python.org

3. Cryptography Libraries (if used)
   License: Apache 2.0 / BSD
   Description: For encryption and secure operations
   Website: https://cryptography.io

4. Qt Framework
   License: LGPL v3 / Commercial
   Description: Core GUI framework used by PyQt5
   Website: https://www.qt.io/

ACKNOWLEDGMENTS

We thank the open source community for their contributions and support.
This software would not be possible without the dedication of countless
developers who have contributed to the projects above.

All third-party components maintain their original licenses and copyright notices.
Users are expected to respect these licenses when using or modifying this software.

For complete license information on each dependency, please visit their respective
project websites or contact the developers.

COMPLIANCE STATEMENT

{APP_NAME} is committed to compliance with all open source licenses.
We regularly audit our dependencies to ensure proper attribution and license compliance.

If you believe there is a licensing issue, please report it to: {APP_DEVELOPER}"""

    # -----------------------
    # Clipboard / Download
    # -----------------------
    def copy_current_license(self):
        """Copy current license text to clipboard"""
        current_widget = self.tab_widget.currentWidget()
        text_edit = current_widget.findChild(QTextEdit)
        if text_edit:
            QApplication.clipboard().setText(text_edit.toPlainText())
            print("License copied to clipboard!")

    def download_licenses(self):
        """Download license files"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save License Files",
            "",
            "Text Files (*.txt);;All Files (*.*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("=" * 80 + "\n")
                    f.write(f"{APP_NAME} - Open Source Licenses\n")
                    f.write("=" * 80 + "\n\n")

                    f.write("MIT LICENSE\n" + "-" * 80 + "\n")
                    f.write(self.get_mit_license() + "\n\n")

                    f.write("GPL v3 LICENSE\n" + "-" * 80 + "\n")
                    f.write(self.get_gpl_license() + "\n\n")

                    f.write("THIRD-PARTY DEPENDENCIES\n" + "-" * 80 + "\n")
                    f.write(self.get_third_party_licenses())

                QMessageBox.information(self, "Success", f"Licenses saved to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save licenses:\n{str(e)}")
