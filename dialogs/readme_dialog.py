# dialog/readme_dialog.py

"""
Tabbed README dialog for NoteArmor Secured Notepad
Fully professional dialog showing all README sections with copy/save per tab and copy/save all functionality
"""

import os
import sys
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QTextBrowser, QFrame, QTabWidget, QWidget, QApplication, QListWidget, QListWidgetItem, QFileDialog, QMessageBox
)
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt
from config.app_config import (
    APP_NAME, APP_VERSION, APP_DEVELOPER, README_ICON_PATH,
    APP_TITLE, DATE_STR, LOGO_PATH, SCREENSHOT_PATH_IMAGES
)

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak

from resources import icons_rc, screenshots_rc
_ = icons_rc
_ = screenshots_rc


class ReadmeDialog(QDialog):
    """Professional tabbed README dialog (PySide6)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{APP_NAME} - README")
        self.setFixedSize(950, 850)
        self.setWindowIcon(QIcon(README_ICON_PATH))
        self.setModal(True)

        self.sections = {}  # Store tab title -> QTextBrowser or QWidget (screenshots)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- Header ---
        header_label = QLabel(f"{APP_NAME} v{APP_VERSION} - README")
        header_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        subtitle = QLabel(f"Developed by {APP_DEVELOPER}")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        main_layout.addWidget(separator)

        # --- Split layout: Sidebar + Tabs ---
        split_layout = QHBoxLayout()
        split_layout.setSpacing(10)

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)
        self.sidebar.itemClicked.connect(self.on_sidebar_clicked)
        split_layout.addWidget(self.sidebar)

        self.tab_widget = QTabWidget()
        self.setup_tabs()
        split_layout.addWidget(self.tab_widget, 1)
        main_layout.addLayout(split_layout)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        for text, handler in [
            ("📋 Copy Current Tab", self.copy_current_tab),
            ("📥 Save Current Tab", self.save_current_tab),
            ("📋 Copy All Tabs", self.copy_all_tabs),
            ("📄 Save All Tabs (Text)", self.save_all_tabs),
            ("📄 Export All Tabs (PDF)", self.export_all_tabs_to_pdf),
        ]:
            btn = QPushButton(text)
            btn.setMinimumHeight(38)
            btn.clicked.connect(handler)
            btn_layout.addWidget(btn)

        btn_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.setMinimumHeight(38)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)

        main_layout.addLayout(btn_layout)

    def setup_tabs(self):
        sections_content = {
            "Features": self.get_features_content(),
            "Usage": self.get_usage_content(),
            "Build & Packaging": self.get_build_content(),
            "License": self.get_license_content(),
            "Author": self.get_author_content(),
            "Notes": self.get_notes_content(),
            "Screenshots & Demo": None,
            "Version History": self.get_version_content(),
            "Credits & Acknowledgements": self.get_credits_content(),
            "Roadmap & Future Features": self.get_roadmap_content(),
            "Security & Privacy": self.get_security_content()
        }

        for title, content in sections_content.items():
            tab = QWidget()
            layout = QVBoxLayout(tab)

            if title == "Screenshots & Demo":
                scroll = QScrollArea()
                scroll.setWidgetResizable(True)
                container = QWidget()
                vbox = QVBoxLayout(container)
                vbox.setContentsMargins(10, 10, 10, 10)

                for path in SCREENSHOT_PATH_IMAGES:
                    lbl = QLabel()
                    pix = QPixmap(path)
                    if pix.isNull():
                        continue
                    pix = pix.scaledToWidth(850, Qt.SmoothTransformation)
                    lbl.setPixmap(pix)
                    lbl.setAlignment(Qt.AlignCenter)
                    vbox.addWidget(lbl)

                    name_label = QLabel(os.path.basename(path))
                    name_label.setAlignment(Qt.AlignCenter)
                    vbox.addWidget(name_label)

                scroll.setWidget(container)
                layout.addWidget(scroll)
                self.sections[title] = container
            else:
                browser = QTextBrowser()
                browser.setOpenExternalLinks(True)
                browser.setFont(QFont("Consolas", 10))
                browser.setHtml(self.markdown_to_html(content))
                layout.addWidget(browser)
                self.sections[title] = browser

            self.tab_widget.addTab(tab, title)
            self.sidebar.addItem(QListWidgetItem(title))

    # -------------------
    # Section Contents
    # -------------------
    def get_features_content(self):
        return (
            "## Features\n"
            "- AES-256-GCM encryption for secure note storage\n"
            "- Dark mode, zoom, line numbering\n"
            "- Modular architecture\n"
            "- High-DPI scaling\n"
            "- Cross-platform (Windows, Linux, macOS)\n"
        )

    def get_usage_content(self):
        return (
            "## Usage\n"
            "- Shortcuts:\n"
            "  - Ctrl+N = New File\n"
            "  - Ctrl+O = Open File\n"
            "  - Ctrl+S = Save File\n"
            "  - Ctrl+Shift+S = Save As (Encrypted / Plaintext)\n"
            "- Encrypted files use `.txt.enc` extension\n"
            "- Enter strong passwords for encryption\n"
        )

    def get_build_content(self):
        return (
            "## Build & Packaging\n"
            "1. Install PyInstaller:\n"
            "   pip install pyinstaller\n"
            "2. Build Command:\n"
            "   pyinstaller --onedir --noconsole --clean --uac-admin \\\n"
            "       --icon='assets/icons/icon.ico' \\\n"
            "       --name='NoteArmor' \\\n"
            "       --add-data 'ui;ui' \\\n"
            "       --add-data 'assets;assets' \\\n"
            "       notepad.py\n"
            "3. Run `NoteArmor.exe` from `dist/NoteArmor/`\n"
        )

    def get_license_content(self):
        return (
            "## License\n"
            "MIT License for core app.\n"
            "GPL v3 License for PyQt5 and certain dependencies.\n"
            "See LICENSE file for full details.\n"
        )

    def get_author_content(self):
        return (
            "## Author\n"
            "Marco Polo (PatronHub)\n"
            "- GitHub: https://github.com/j3fcruz\n"
            "- GitLab: https://gitlab.com/patronhubdevs/notearmor\n"
            "- Codeberg: https://codeberg.org/dariusmontelaro/NoteArmor\n"
            "- Ko-fi: https://ko-fi.com/marcopolo55681\n"
            "- Website: https://patronhubdevs.online\n"
        )

    def get_notes_content(self):
        return (
            "## Notes\n"
            "- Always backup encrypted files & passwords\n"
            "- Supports UTF-8 text files only\n"
            "- Recommended for note-taking, coding, personal documentation\n"
        )

    def get_screenshots_content(self):
        return (
            "## Screenshots & Demo\n"
            "Main Editor Window, Encryption Dialog, Help, About, Donate, Terms & License dialogs.\n"
            "Screenshots stored in `assets/screenshots/`.\n"
        )

    def get_version_content(self):
        return (
            "## Version History\n"
            "### [3.0.0] – 2025-11-15\n"
            "- 12+ Professional Themes\n"
            "- Real-time Theme Switching (keyboard shortcuts)\n"
            "- OCR Engine Support: Tesseract, EasyOCR, Hybrid modes\n"
            "- Image-to-Text Tool with multiple formats\n"
            "- Smart Fallback System for OCR engines\n"
            "- Multi-Tab Support\n"
            "- Auto-Save Functionality (60-second backups)\n"
            "- Enhanced error handling for OCR\n"
            "- Improved encryption and password flow\n"
            "- Theme selector with checkmark indicators\n"
            "- Professional modal dialogs\n"
            "- Modular OCR engine architecture\n\n"
            "### [2.0.0] – 2025-11-06\n"
            "- Theme Manager: Automatic dark/light theme switching\n"
            "- Icon Manager: Resource fallback\n"
            "- High-DPI Support\n"
            "- Modular Architecture\n"
            "- AES-GCM backend fully Python\n\n"
            "### [1.0.0] – 2025-10-28\n"
            "- Initial release: text editing, file operations, dark theme, line numbering, zoom controls\n"
        )

    def get_credits_content(self):
        return (
            "## Credits & Acknowledgements\n"
            "**Icons & Graphics:** GNU Licensed from IconArchive\n"
            "Screenshots & UI assets by Marco Polo (PatronHub)\n"
            "Libraries: PyQt5, Cryptography, PyInstaller\n"
            "Inspiration: AES-GCM concepts, modular Python patterns\n"
        )

    def get_roadmap_content(self):
        return (
            "## Roadmap & Future Features\n"
            "- Multi-device encrypted notes sync\n"
            "- Cloud backup (encrypted)\n"
            "- Mobile apps (iOS & Android)\n"
            "- Advanced search & tagging\n"
            "- Customizable themes & UI templates\n"
        )

    def get_security_content(self):
        return (
            "## Security & Privacy\n"
            "- AES-256-GCM encryption\n"
            "- HMAC-SHA256 integrity validation\n"
            "- Passwords never stored in plaintext\n"
            "- All sensitive operations local, no server required\n"
        )

    # -------------------
    # Clipboard / Save
    # -------------------
    def copy_current_tab(self):
        widget = self.tab_widget.currentWidget()
        browser = widget.findChild(QTextBrowser)
        if browser:
            QApplication.clipboard().setText(browser.toPlainText())
            QMessageBox.information(self, "Copied", "Current tab copied to clipboard!")

    def save_current_tab(self):
        widget = self.tab_widget.currentWidget()
        browser = widget.findChild(QTextBrowser)
        if not browser:
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, f"Save {self.tab_widget.tabText(self.tab_widget.currentIndex())}",
            "", "Text Files (*.txt);;All Files (*.*)"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(browser.toPlainText())
                QMessageBox.information(self, "Saved", f"Saved to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def copy_all_tabs(self):
        combined = []
        for title, widget in self.sections.items():
            combined.append(f"\n=== {title} ===\n")
            if isinstance(widget, QTextBrowser):
                combined.append(widget.toPlainText())
            else:
                for lbl in widget.findChildren(QLabel):
                    if lbl.text():
                        combined.append(lbl.text())
                    elif lbl.pixmap():
                        combined.append(f"[Image: {lbl.pixmap()}]")
        QApplication.clipboard().setText("\n".join(combined))
        QMessageBox.information(self, "Copied", "All tabs copied (text + image names)!")

    def save_all_tabs(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save All Tabs", "", "Text Files (*.txt);;All Files (*.*)")
        if not file_path:
            return
        try:
            combined = []
            for title, widget in self.sections.items():
                combined.append(f"\n=== {title} ===\n")
                if isinstance(widget, QTextBrowser):
                    combined.append(widget.toPlainText())
                else:
                    for lbl in widget.findChildren(QLabel):
                        if lbl.text():
                            combined.append(lbl.text())
                        elif lbl.pixmap():
                            combined.append(f"[Image: {lbl.pixmap()}]")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(combined))
            QMessageBox.information(self, "Saved", f"All tabs saved to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_sidebar_clicked(self, item):
        index = self.sidebar.row(item)
        self.tab_widget.setCurrentIndex(index)

    def markdown_to_html(self, text):
        html = text.replace("\n", "<br>").replace("## ", "<h3>").replace("**", "<b>")
        return html

    def export_all_tabs_to_pdf(self):
        """Full PDF export with images, watermark, and metadata"""
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak

        file_path, _ = QFileDialog.getSaveFileName(self, "Export All Tabs as PDF", "NoteArmor_README.pdf", "PDF Files (*.pdf)")
        if not file_path:
            return

        try:
            doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
            styles = getSampleStyleSheet()
            story = []

            # Title Page
            story.append(Spacer(1, 1 * inch))
            if os.path.exists(LOGO_PATH):
                img = Image(LOGO_PATH, width=2.5 * inch, height=2.5 * inch)
                img.hAlign = "CENTER"
                story.append(img)
                story.append(Spacer(1, 0.3 * inch))

            story.append(Paragraph(f"<b>{APP_TITLE}</b>", styles["Title"]))
            story.append(Paragraph(f"{APP_VERSION}", styles["Heading2"]))
            story.append(Spacer(1, 0.3 * inch))

            # Sections
            for title, widget in self.sections.items():
                story.append(Paragraph(f"<b>{title}</b>", styles["Heading2"]))
                story.append(Spacer(1, 0.1 * inch))
                if isinstance(widget, QTextBrowser):
                    for line in widget.toPlainText().split("\n"):
                        story.append(Paragraph(line.replace(" ", "&nbsp;"), styles["Normal"]))
                else:
                    for lbl in widget.findChildren(QLabel):
                        if lbl.text():
                            story.append(Paragraph(lbl.text(), styles["Normal"]))
                story.append(PageBreak())

            doc.build(story)
            QMessageBox.information(self, "Exported", f"PDF exported successfully:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"PDF export failed:\n{str(e)}")