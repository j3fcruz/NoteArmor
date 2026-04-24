import re
"""
utils/advanced_features.py

Advanced features module for Secure Notepad Pro:
- Tab-based editing
- Recent files tracking
- Autosave & backup
- Syntax highlighting
- Theme switching
- Advanced encryption
- Search & replace
- Custom shortcuts
"""

import json
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import (
    QTabWidget, QMessageBox, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton, QCheckBox,
    QFileDialog, QTextEdit, QLineEdit, QInputDialog
)
from PySide6.QtGui import QSyntaxHighlighter, QColor, QTextCharFormat
from PySide6.QtCore import QTimer, Signal, QObject

# ===================== SYNTAX HIGHLIGHTER =====================
class PythonHighlighter(QSyntaxHighlighter):
    """Python syntax highlighter"""

    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#6366f1"))
        keyword_format.setFontWeight(75)
        keywords = ["def", "class", "import", "from", "if", "else", "elif",
                    "for", "while", "return", "True", "False", "None", "try", "except"]
        for word in keywords:
            self.highlighting_rules.append((f"\\b{word}\\b", keyword_format))

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#22c55e"))
        self.highlighting_rules.append((r'\".*?\"', string_format))
        self.highlighting_rules.append((r"'.*?'", string_format))

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#888888"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((r"#.*", comment_format))

    def highlightBlock(self, text):
        for pattern, char_format in self.highlighting_rules:
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, char_format)


class HTMLHighlighter(QSyntaxHighlighter):
    """HTML syntax highlighter"""

    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # HTML Tags
        tag_format = QTextCharFormat()
        tag_format.setForeground(QColor("#6366f1"))
        tag_format.setFontWeight(75)
        self.highlighting_rules.append((r"<[^>]*>", tag_format))

        # Attributes
        attr_format = QTextCharFormat()
        attr_format.setForeground(QColor("#0078D4"))
        self.highlighting_rules.append((r'\w+(?==)', attr_format))

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#22c55e"))
        self.highlighting_rules.append((r'\".*?\"', string_format))
        self.highlighting_rules.append((r"'.*?'", string_format))

    def highlightBlock(self, text):
        for pattern, char_format in self.highlighting_rules:
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, char_format)


# ===================== RECENT FILES MANAGER =====================
class RecentFilesManager:
    """Manage recent files list (last 10 files)"""

    def __init__(self, max_files=10):
        self.max_files = max_files
        self.config_file = Path.home() / ".secure_notepad" / "recent_files.json"
        self.config_file.parent.mkdir(exist_ok=True)
        self.recent_files = self.load()

    def add_file(self, file_path):
        file_path = str(Path(file_path).resolve())
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:self.max_files]
        self.save()

    def remove_file(self, file_path):
        file_path = str(Path(file_path).resolve())
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
            self.save()

    def get_files(self):
        return [f for f in self.recent_files if Path(f).exists()]

    def save(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.recent_files, f)
        except Exception as e:
            print(f"Error saving recent files: {e}")

    def load(self):
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading recent files: {e}")
        return []

    def clear(self):
        self.recent_files = []
        self.save()


# ===================== AUTOSAVE & BACKUP =====================
class AutosaveManager(QObject):
    """Manage autosave and backup functionality"""

    autosave_triggered = Signal()

    def __init__(self, interval_seconds=60):
        super().__init__()
        self.interval = interval_seconds * 1000
        self.backup_dir = Path.home() / ".secure_notepad" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        self.timer = QTimer()
        self.timer.timeout.connect(self.autosave_triggered)
        self.timer.setInterval(self.interval)

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def create_backup(self, file_path, content):
        try:
            if file_path:
                filename = Path(file_path).name
                backup_file = self.backup_dir / f"{filename}.backup.{datetime.now().timestamp()}"
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.cleanup_old_backups(filename)
        except Exception as e:
            print(f"Error creating backup: {e}")

    def cleanup_old_backups(self, filename):
        try:
            backups = sorted(self.backup_dir.glob(f"{filename}.backup.*"))
            for backup in backups[:-5]:
                backup.unlink()
        except Exception as e:
            print(f"Error cleaning backups: {e}")

    def get_backups(self, filename):
        try:
            return sorted(self.backup_dir.glob(f"{filename}.backup.*"), reverse=True)
        except:
            return []


# ===================== ADVANCED ENCRYPTION =====================
class EncryptionManager:
    """Manage advanced encryption options"""

    @staticmethod
    def get_encryption_methods():
        return {
            "AES-256-PBKDF2": "AES-256 with PBKDF2 (Standard)",
            "AES-256-Argon2": "AES-256 with Argon2 (Recommended)",
            "ChaCha20-Poly1305": "ChaCha20-Poly1305 (Modern)"
        }

    @staticmethod
    def encrypt_with_method(data, password, method="AES-256-PBKDF2"):
        try:
            from cryptography.hazmat.primitives import hashes, padding
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.primitives.kdf.argon2 import Argon2
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.backends import default_backend
            import os

            salt = os.urandom(16)

            if method == "AES-256-PBKDF2":
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100_000,
                    backend=default_backend()
                )
                key = kdf.derive(password.encode())
            elif method == "AES-256-Argon2":
                kdf = Argon2(time_cost=2, memory_cost=512, parallelism=2, hash_len=32)
                key = kdf.derive(password.encode())

            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
            encryptor = cipher.encryptor()

            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data.encode()) + padder.finalize()

            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            return salt + iv + ciphertext, method.encode()
        except Exception as e:
            raise Exception(f"Encryption failed: {e}")


# ===================== SEARCH & REPLACE =====================
class SearchReplaceDialog(QDialog):
    """Advanced search and replace dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find & Replace")
        self.setFixedSize(500, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Find:"))
        self.search_input = QLineEdit()
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("Replace:"))
        self.replace_input = QLineEdit()
        replace_layout.addWidget(self.replace_input)
        layout.addLayout(replace_layout)

        self.case_sensitive = QCheckBox("Case Sensitive")
        self.whole_words = QCheckBox("Whole Words Only")
        self.regex = QCheckBox("Regular Expression")
        options_layout = QHBoxLayout()
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.whole_words)
        options_layout.addWidget(self.regex)
        layout.addLayout(options_layout)

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMaximumHeight(120)
        layout.addWidget(QLabel("Results:"))
        layout.addWidget(self.results_text)

        btn_layout = QHBoxLayout()
        find_btn = QPushButton("Find All")
        replace_btn = QPushButton("Replace All")
        close_btn = QPushButton("Close")
        btn_layout.addWidget(find_btn)
        btn_layout.addWidget(replace_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        close_btn.clicked.connect(self.accept)

# ===================== CUSTOM SHORTCUTS MANAGER =====================
class ShortcutsDialog(QDialog):
    """Dialog to manage custom keyboard shortcuts"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Customize Shortcuts")
        self.setFixedSize(600, 400)
        self.config_file = Path.home() / ".secure_notepad" / "shortcuts.json"
        self.shortcuts = self.load_shortcuts()
        self.setup_ui()

    def setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Edit keyboard shortcuts:"))

        # Shortcuts list
        self.shortcuts_list = QListWidget()
        self.load_shortcuts_ui()
        layout.addWidget(self.shortcuts_list)

        # Buttons
        btn_layout = QHBoxLayout()
        reset_btn = QPushButton("Reset to Defaults")
        export_btn = QPushButton("Export")
        import_btn = QPushButton("Import")
        close_btn = QPushButton("Close")

        reset_btn.clicked.connect(self.reset_shortcuts)
        export_btn.clicked.connect(self.export_shortcuts)
        import_btn.clicked.connect(self.import_shortcuts)
        close_btn.clicked.connect(self.accept)

        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(import_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    def load_shortcuts_ui(self):
        """Load shortcuts into list widget"""
        for action, shortcut in self.shortcuts.items():
            item = QListWidgetItem(f"{action}: {shortcut}")
            self.shortcuts_list.addItem(item)

    def load_shortcuts(self):
        """Load shortcuts from config"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except:
            pass

        return {
            "New": "Ctrl+N",
            "Open": "Ctrl+O",
            "Save": "Ctrl+S",
            "Save As": "Ctrl+Shift+S",
            "Undo": "Ctrl+Z",
            "Redo": "Ctrl+Y",
            "Cut": "Ctrl+X",
            "Copy": "Ctrl+C",
            "Paste": "Ctrl+V",
            "Find": "Ctrl+F",
            "Replace": "Ctrl+H",
            "Zoom In": "Ctrl++",
            "Zoom Out": "Ctrl+-"
        }

    def save_shortcuts(self):
        """Save shortcuts to config"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.shortcuts, f, indent=2)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save shortcuts: {e}")

    def reset_shortcuts(self):
        """Reset shortcuts to defaults"""
        reply = QMessageBox.question(self, "Confirm", "Reset all shortcuts to defaults?")
        if reply == QMessageBox.Yes:
            self.shortcuts = self.load_shortcuts()
            self.save_shortcuts()
            self.shortcuts_list.clear()
            self.load_shortcuts_ui()

    def export_shortcuts(self):
        """Export shortcuts to file"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Shortcuts", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.shortcuts, f, indent=2)
                QMessageBox.information(self, "Success", "Shortcuts exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {e}")

    def import_shortcuts(self):
        """Import shortcuts from file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Shortcuts", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    self.shortcuts = json.load(f)
                self.save_shortcuts()
                self.shortcuts_list.clear()
                self.load_shortcuts_ui()
                QMessageBox.information(self, "Success", "Shortcuts imported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Import failed: {e}")


# ===================== TAB MANAGER =====================
class TabManager(QTabWidget):
    """Manage multiple file tabs with autosave and recent files"""

    def __init__(self, parent=None, autosave_interval=60):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.tab_files = {}

        # ---------------- Managers ----------------
        self.autosave_manager = AutosaveManager(interval_seconds=autosave_interval)
        self.recent_files_manager = RecentFilesManager()
        self.autosave_manager.autosave_triggered.connect(self.autosave_all_tabs)
        self.autosave_manager.start()

    # ---------------- Tab Methods ----------------
    def add_tab_file(self, file_path, content, is_encrypted=False):
        """Add new tab with file"""
        from utils.editor import EnhancedTextEditor

        editor = EnhancedTextEditor()
        editor.setPlainText(content)
        editor.document().setModified(False)

        tab_name = Path(file_path).name if file_path else "Untitled"
        tab_index = self.addTab(editor, tab_name)

        self.tab_files[tab_index] = {
            "path": file_path,
            "encrypted": is_encrypted,
            "modified": False,
        }

        # Update recent files
        if file_path:
            self.recent_files_manager.add_file(file_path)

        # Connect editor changes to mark tab as modified
        editor.textChanged.connect(lambda idx=tab_index: self.mark_tab_modified(idx, True))

        self.setCurrentIndex(tab_index)
        return editor

    def mark_tab_modified(self, index, modified=True):
        """Mark tab as modified (adds * to tab name)"""
        editor_info = self.tab_files.get(index)
        if editor_info:
            editor_info["modified"] = modified
            base_name = Path(editor_info["path"]).name if editor_info["path"] else "Untitled"
            tab_name = f"*{base_name}" if modified else base_name
            self.setTabText(index, tab_name)

    def autosave_all_tabs(self):
        """Autosave all modified tabs to backup directory"""
        for index, info in self.tab_files.items():
            editor = self.widget(index)
            if editor and info.get("modified"):
                content = editor.toPlainText()
                file_path = info.get("path")
                filename = Path(file_path).name if file_path else f"untitled_{index}.txt"
                self.autosave_manager.create_backup(filename, content)

    # ---------------- Save Methods ----------------
    def save_current_tab(self, save_as=False):
        """Save current tab content"""
        editor = self.currentWidget()
        if editor is None:
            return False

        index = self.currentIndex()
        info = self.tab_files.get(index, {})
        file_path = info.get("path")
        is_encrypted = info.get("encrypted", False)

        # If no file or save_as requested, ask for file path
        if not file_path or save_as:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save File As", file_path or "untitled.txt",
                "Text Files (*.txt);;Encrypted Files (*.txt.enc)"
            )
            if not file_path:
                return False
            info["path"] = file_path
            self.tab_files[index] = info

        content = editor.toPlainText()
        try:
            if is_encrypted:
                from utils.encryption import encrypt_data
                password, ok = QInputDialog.getText(
                    self, "Encryption Password", "Enter password:", QLineEdit.Password
                )
                if not ok or not password:
                    return False
                token, salt = encrypt_data(content, password)
                with open(file_path, "wb") as f:
                    f.write(salt + token)
            else:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

            editor.document().setModified(False)
            self.mark_tab_modified(index, False)

            # Update recent files
            if file_path:
                self.recent_files_manager.add_file(file_path)

            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")
            return False

    def save_all_tabs(self):
        """Save all open tabs"""
        success = True
        for i in range(self.count()):
            self.setCurrentIndex(i)
            if not self.save_current_tab():
                success = False
        return success

    # ---------------- Close Tabs ----------------
    def close_tab(self, index):
        """Close specific tab with unsaved check"""
        editor = self.widget(index)
        info = self.tab_files.get(index, {})
        if editor and editor.document().isModified():
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                f"Save changes to {self.tabText(index)}?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            )
            if reply == QMessageBox.Save:
                if not self.save_current_tab():
                    return
            elif reply == QMessageBox.Cancel:
                return
        self.removeTab(index)
        self.tab_files.pop(index, None)

    def close_all_tabs(self):
        """Close all tabs with unsaved check"""
        for i in reversed(range(self.count())):
            self.setCurrentIndex(i)
            self.close_tab(i)
        return True

    # ---------------- Tab Utilities ----------------
    def get_current_editor(self):
        """Get current tab's editor"""
        return self.currentWidget()

    def get_all_editors(self):
        """Get all tab editors"""
        return [self.widget(i) for i in range(self.count())]

    def rename_tab(self, index, new_name):
        """Rename a tab (without affecting file path)"""
        if 0 <= index < self.count():
            self.setTabText(index, new_name)

    def apply_theme_to_all_tabs(self, theme_name="dark"):
        """Apply stylesheet/theme to all tabs' editors"""
        stylesheet = ""
        for editor in self.get_all_editors():
            editor.setStyleSheet(stylesheet)
