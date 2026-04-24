"""
ui/notearmor_free.py
NoteArmor — Personal Use Edition, main window (minimal).

REMOVED vs previous Free Edition:
    - LicenseDialog       — license now embedded in HelpDialog
    - DonateDialog        — removed from UI entirely
    - ReadmeDialog        — not needed for personal use
    - PDF viewer          — complexity not warranted for personal use
    - open_feedback_page  — collapsed into Help menu link
    - open_homepage       — collapsed into Help menu link
    - Double close-confirm — single unsaved-changes check only
    - CRLF / encoding labels in status bar — noise reduction
    - char/word/line count label — reduced to Ln/Col only

PRESERVED:
    - All file open/save flows (plaintext + password-encrypted)
    - Tab management (new, close, autosave)
    - Status bar: Ln/Col, crypto status, zoom
    - Help menu: Help (F1), About
    - Zoom in/out/reset with Ctrl+wheel
    - Professional Blue theme at startup
"""

import os
import logging
import webbrowser
from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow, QLabel, QStatusBar, QFileDialog,
    QMessageBox, QTabWidget, QDialog,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import QTimer

from utils.editor import EnhancedTextEditor
from core.encryption import (
    encrypt_data, decrypt_data, CRYPTO_AVAILABLE,
    create_encrypted_file_content, parse_encrypted_file_content,
)
from utils.icon_manager import load_icon
from dialogs.save_dialog import SaveModeDialog
from dialogs.about_dialog import AboutDialog
from dialogs.help_dialog import HelpDialog
from dialogs.password_entry_dialog import PasswordEntryDialog
from config.app_config import ICON_PATH, HOMEPAGE, MAIL_TO

from resources import icons_rc   # noqa: F401
from resources import themes_rc  # noqa: F401
_ = icons_rc
_ = themes_rc

log = logging.getLogger(__name__)


class EnhancedNotepad(QMainWindow):
    AUTOSAVE_INTERVAL_MS = 60_000

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Untitled — NoteArmor")
        self.setGeometry(100, 100, 900, 650)
        self._center()
        self.setWindowIcon(load_icon(ICON_PATH))

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_status_bar)
        self.setCentralWidget(self.tabs)

        self.tab_files = {}
        self.default_font_size = 12

        self._init_status_bar()
        self._init_menu()

        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.autosave_all_tabs)
        self.autosave_timer.start(self.AUTOSAVE_INTERVAL_MS)

        self.new_tab()

    def _center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # ── Helpers ───────────────────────────────────────────────────────────────

    def current_editor(self):
        w = self.tabs.currentWidget()
        return w if isinstance(w, EnhancedTextEditor) else None

    def current_tab_index(self):
        return self.tabs.currentIndex()

    def current_tab_data(self):
        return self.tab_files.get(self.current_tab_index(), {})

    # ── Status bar ────────────────────────────────────────────────────────────

    def _init_status_bar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.line_col_label    = QLabel("Ln 1, Col 1")
        self.crypto_status_label = QLabel("Plaintext")
        self.zoom_label        = QLabel("100%")

        for w in [self.line_col_label, "|", self.crypto_status_label, "|", self.zoom_label]:
            self.statusBar.addPermanentWidget(QLabel(w) if isinstance(w, str) else w)

        self.update_status_bar()

    def update_status_bar(self):
        if getattr(self, "_updating_status", False):
            return
        self._updating_status = True
        try:
            editor = self.current_editor()
            if not editor:
                return

            cursor = editor.textCursor()
            self.line_col_label.setText(
                f"Ln {cursor.blockNumber() + 1}, Col {cursor.columnNumber() + 1}"
            )

            font_size    = editor.font().pointSize()
            zoom_percent = round((font_size / self.default_font_size) * 100)
            self.zoom_label.setText(f"{zoom_percent}%")

            encrypted = self.current_tab_data().get("encrypted", False)
            self.crypto_status_label.setText("🔒 Encrypted" if encrypted else "Plaintext")
        finally:
            self._updating_status = False

    # ── Tab management ────────────────────────────────────────────────────────

    def new_tab(self, path=None, content="", encrypted=False, password=None):
        editor = EnhancedTextEditor()
        editor.setPlainText(content)
        editor.document().setModified(False)
        editor.cursorPositionChanged.connect(self.update_status_bar)
        editor.textChanged.connect(self.update_status_bar)
        editor.set_wheel_zoom_callback(self.zoom_editor)

        title = os.path.basename(path) if path else "Untitled"
        index = self.tabs.addTab(editor, title)
        self.tabs.setCurrentIndex(index)

        self.tab_files[index] = {
            "path":      path,
            "encrypted": encrypted,
            "password":  password,
        }

        if not self.default_font_size:
            self.default_font_size = editor.font().pointSize()

    def close_tab(self, index):
        editor = self.tabs.widget(index)
        if editor.document().isModified():
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                f"'{self.tabs.tabText(index)}' has unsaved changes. Save before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            )
            if reply == QMessageBox.Save:
                self.tabs.setCurrentIndex(index)
                if not self.save_file():
                    return
            elif reply == QMessageBox.Cancel:
                return

        self.tabs.removeTab(index)
        self.tab_files.pop(index, None)

    # ── Zoom ──────────────────────────────────────────────────────────────────

    def zoom_editor(self, delta):
        editor = self.current_editor()
        if not editor:
            return
        font = editor.font()
        font.setPointSize(max(8, min(48, font.pointSize() + delta)))
        editor.setFont(font)
        self.update_status_bar()

    def zoom_in(self):    self.zoom_editor(1)
    def zoom_out(self):   self.zoom_editor(-1)

    def reset_zoom(self):
        editor = self.current_editor()
        if editor:
            font = editor.font()
            font.setPointSize(self.default_font_size)
            editor.setFont(font)
            self.update_status_bar()

    # ── Menu bar ──────────────────────────────────────────────────────────────

    def _action(self, text, shortcut=None, slot=None):
        a = QAction(text, self)
        if shortcut:
            a.setShortcut(shortcut)
        if slot:
            a.triggered.connect(slot)
        return a

    def _init_menu(self):
        mb = self.menuBar()

        # ── File ─────────────────────────────────────────────────────────────
        fm = mb.addMenu("&File")
        fm.addAction(self._action("&New Tab",   "Ctrl+N",       self.new_tab))
        fm.addAction(self._action("&Open...",   "Ctrl+O",       self.open_file))
        fm.addAction(self._action("&Save",      "Ctrl+S",       self.save_file))
        fm.addAction(self._action("Save &As…",  "Ctrl+Shift+S", self.save_file_as))
        fm.addSeparator()
        fm.addAction(self._action("E&xit",      "Ctrl+Q",       self.close))

        # ── Edit ─────────────────────────────────────────────────────────────
        em = mb.addMenu("&Edit")
        em.addAction(self._action("&Undo",  "Ctrl+Z", lambda: self.current_editor().undo()))
        em.addAction(self._action("&Redo",  "Ctrl+Y", lambda: self.current_editor().redo()))
        em.addSeparator()
        em.addAction(self._action("Cu&t",   "Ctrl+X", lambda: self.current_editor().cut()))
        em.addAction(self._action("&Copy",  "Ctrl+C", lambda: self.current_editor().copy()))
        em.addAction(self._action("&Paste", "Ctrl+V", lambda: self.current_editor().paste()))

        # ── View ─────────────────────────────────────────────────────────────
        vm   = mb.addMenu("&View")
        zoom = vm.addMenu("&Zoom")
        zoom.addAction(self._action("Zoom In",       "Ctrl++", self.zoom_in))
        zoom.addAction(self._action("Zoom Out",      "Ctrl+-", self.zoom_out))
        zoom.addAction(self._action("Reset (100%)",  "Ctrl+R", self.reset_zoom))

        # ── Help ─────────────────────────────────────────────────────────────
        hm = mb.addMenu("&Help")
        hm.addAction(self._action("📘 Help",  "F1", self.show_help_dialog))
        hm.addSeparator()
        hm.addAction(self._action("About",           slot=self.show_about_dialog))
        hm.addAction(self._action("Website",         slot=lambda: webbrowser.open(HOMEPAGE)))
        hm.addAction(self._action("Contact / Feedback", slot=lambda: webbrowser.open(MAIL_TO)))

    # ── File — save ───────────────────────────────────────────────────────────

    def save_file_as(self):
        dialog = SaveModeDialog(self, crypto_available=True)
        if dialog.exec() != QDialog.Accepted:
            return False

        index = self.current_tab_index()

        if dialog.save_mode == "plaintext":
            path, _ = QFileDialog.getSaveFileName(
                self, "Save As", "untitled.txt", "Text Files (*.txt)"
            )
            return self._save_plaintext_flow(path, index) if path else False

        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        path, _  = QFileDialog.getSaveFileName(
            self, "Save Encrypted As", f"note_{date_str}.notearmor",
            "NoteArmor Encrypted Files (*.notearmor)",
        )
        if not path:
            return False
        return self._save_encrypted_flow(path, dialog.password, index)

    def save_file(self):
        index    = self.current_tab_index()
        tab_data = self.current_tab_data()
        path     = tab_data.get("path")

        if not path:
            return self.save_file_as()

        if not tab_data.get("encrypted"):
            return self._save_plaintext_flow(path, index)

        password = tab_data.get("password")
        if not password:
            QMessageBox.warning(
                self, "Error",
                "Password not found. Use 'Save As' to re-save with a new password.",
            )
            return False

        return self._save_encrypted_flow(path, password, index)

    def _save_plaintext_flow(self, path, index):
        if not path:
            return False
        try:
            editor = self.tabs.widget(index)
            with open(path, "w", encoding="utf-8") as f:
                f.write(editor.toPlainText())
            self.tab_files[index] = {"path": path, "encrypted": False, "password": None}
            self.tabs.setTabText(index, os.path.basename(path))
            editor.document().setModified(False)
            self.statusBar.showMessage(f"Saved: {os.path.basename(path)}", 4000)
            self.update_status_bar()
            return True
        except Exception as exc:
            QMessageBox.critical(self, "Save Error", f"Failed to save:\n{exc}")
            return False

    def _save_encrypted_flow(self, path, password, index):
        try:
            editor    = self.tabs.widget(index)
            plaintext = editor.toPlainText()

            try:
                token, salt, metadata = encrypt_data(plaintext, password)
            except Exception as exc:
                QMessageBox.critical(self, "Encryption Error", f"Failed to encrypt:\n{exc}")
                return False

            file_content = create_encrypted_file_content(token, salt, metadata)

            try:
                with open(path, "wb") as f:
                    f.write(file_content)
            except Exception as exc:
                QMessageBox.critical(self, "File Error", f"Failed to write file:\n{exc}")
                return False

            self.tab_files[index] = {"path": path, "encrypted": True, "password": password}
            self.tabs.setTabText(index, os.path.basename(path))
            editor.document().setModified(False)
            self.statusBar.showMessage(f"✓ Saved encrypted: {os.path.basename(path)}", 4000)
            self.update_status_bar()
            return True

        except Exception as exc:
            QMessageBox.critical(self, "Save Error", f"Unexpected error:\n{exc}")
            return False

    # ── File — open ───────────────────────────────────────────────────────────

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "",
            "All Files (*);;Text Files (*.txt);;Encrypted Files (*.notearmor)",
        )
        if not path:
            return

        try:
            # Plaintext
            if not path.endswith(".notearmor"):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        self.new_tab(path, f.read(), False)
                    self.statusBar.showMessage(f"Opened: {os.path.basename(path)}", 4000)
                except UnicodeDecodeError:
                    QMessageBox.warning(self, "Error", "File is not valid UTF-8 text.")
                return

            # Encrypted
            if not CRYPTO_AVAILABLE:
                QMessageBox.critical(
                    self, "Error",
                    "Cryptography library not available.\nInstall: pip install cryptography",
                )
                return

            with open(path, "rb") as f:
                file_data = f.read()

            try:
                salt, metadata_bytes, token = parse_encrypted_file_content(file_data)
            except ValueError as exc:
                QMessageBox.critical(self, "Corrupted File", f"Invalid file format:\n{exc}")
                return

            dlg = PasswordEntryDialog(self)
            if dlg.exec() != QDialog.Accepted:
                return

            try:
                plaintext, _ = decrypt_data(token, dlg.password, salt, metadata=metadata_bytes)
                self.new_tab(path, plaintext, True, dlg.password)
                self.statusBar.showMessage("✓ Decrypted successfully", 4000)
            except ValueError as exc:
                QMessageBox.warning(
                    self, "Wrong Password",
                    f"Could not decrypt file.\n\nCheck your password and try again.\n\nDetail: {exc}",
                )
            except Exception as exc:
                QMessageBox.critical(self, "Decryption Error", f"Unexpected error:\n{exc}")

        except Exception as exc:
            QMessageBox.critical(self, "File Error", f"Failed to open file:\n{exc}")

    # ── Autosave ──────────────────────────────────────────────────────────────

    def autosave_all_tabs(self):
        for i in range(self.tabs.count()):
            ed = self.tabs.widget(i)
            if not ed or not ed.document().isModified():
                continue
            path = self.tab_files.get(i, {}).get("path")
            if path:
                self._save_plaintext_flow(path, i)

    # ── Dialogs ───────────────────────────────────────────────────────────────

    def show_about_dialog(self):
        AboutDialog(self).exec()

    def show_help_dialog(self):
        HelpDialog(self).exec()

    # ── Close ─────────────────────────────────────────────────────────────────

    def closeEvent(self, event):
        unsaved = [
            i for i in range(self.tabs.count())
            if self.tabs.widget(i).document().isModified()
        ]

        for index in unsaved:
            self.tabs.setCurrentIndex(index)
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                f"'{self.tabs.tabText(index)}' has unsaved changes. Save before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            )
            if reply == QMessageBox.Save:
                if not self.save_file():
                    event.ignore()
                    return
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return

        event.accept()