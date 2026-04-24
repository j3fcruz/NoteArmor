"""
utils/file_handler.py
File handling utilities for Secure Notepad Pro (PySide6).
"""

import os
from PySide6.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QLineEdit,
    QMessageBox,
)

from utils.encryption import (
    encrypt_data,
    decrypt_data,
    CRYPTO_AVAILABLE,
)


class FileHandler:
    """Handles file operations for Secure Notepad Pro."""

    def __init__(self, tab_manager):
        self.tab_manager = tab_manager

    # ---------- Open ----------
    def open_file(self):
        file_filter = (
            "All Files (*);;"
            "Text Files (*.txt);;"
            "Encrypted Files (*.txt.enc)"
        )

        file_path, _ = QFileDialog.getOpenFileName(
            self.tab_manager.tabs,
            "Open File",
            "",
            file_filter,
        )

        if not file_path:
            return

        try:
            if file_path.endswith(".enc"):
                if not CRYPTO_AVAILABLE:
                    raise RuntimeError(
                        "Cryptography module not available"
                    )

                with open(file_path, "rb") as f:
                    data = f.read()

                if len(data) < 16:
                    raise ValueError(
                        "Corrupted encrypted file"
                    )

                salt, token = data[:16], data[16:]

                password, ok = QInputDialog.getText(
                    self.tab_manager.tabs,
                    "Decrypt File",
                    f"Enter password for '{os.path.basename(file_path)}':",
                    QLineEdit.Password,
                )

                if not ok or not password:
                    return

                plaintext = decrypt_data(
                    token,
                    password,
                    salt,
                )

                self.tab_manager.new_tab(
                    file_path,
                    plaintext,
                    encrypted=True,
                    password=password,
                )

            else:
                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                ) as f:
                    content = f.read()

                self.tab_manager.new_tab(
                    file_path,
                    content,
                    encrypted=False,
                )

        except Exception as e:
            QMessageBox.critical(
                self.tab_manager.tabs,
                "Error",
                f"Failed to open file:\n{e}",
            )

    # ---------- Save ----------
    def save_file(self):
        editor = self.tab_manager.current_editor()
        if not editor:
            return False

        index = self.tab_manager.current_tab_index()
        tab_data = self.tab_manager.current_tab_data()

        path = tab_data.get("path")
        encrypted = tab_data.get("encrypted", False)
        password = tab_data.get("password")

        if path:
            if encrypted:
                return self._save_encrypted(
                    path,
                    password,
                    index,
                )
            return self._save_plaintext(path, index)

        return self.save_file_as()

    def save_file_as(self):
        from dialogs.save_dialog import SaveModeDialog

        dialog = SaveModeDialog(
            self.tab_manager.tabs,
            crypto_available=CRYPTO_AVAILABLE,
        )

        if dialog.exec() != dialog.Accepted:
            return False

        save_mode = dialog.save_mode
        password = dialog.password
        index = self.tab_manager.current_tab_index()

        if save_mode == "plaintext":
            file_path, _ = QFileDialog.getSaveFileName(
                self.tab_manager.tabs,
                "Save File As",
                "untitled.txt",
                "Text Files (*.txt)",
            )

            if file_path:
                return self._save_plaintext(
                    file_path,
                    index,
                )

        elif save_mode == "encrypted":
            if not password:
                QMessageBox.warning(
                    self.tab_manager.tabs,
                    "Error",
                    "Encryption password cannot be empty.",
                )
                return False

            file_path, _ = QFileDialog.getSaveFileName(
                self.tab_manager.tabs,
                "Save Encrypted File As",
                "untitled.txt.enc",
                "Encrypted Files (*.txt.enc)",
            )

            if file_path:
                return self._save_encrypted(
                    file_path,
                    password,
                    index,
                )

        return False

    # ---------- Internal ----------
    def _save_plaintext(self, path, index):
        try:
            editor = self.tab_manager.tabs.widget(index)

            with open(
                path,
                "w",
                encoding="utf-8",
            ) as f:
                f.write(editor.toPlainText())

            self.tab_manager.tab_files[index] = {
                "path": path,
                "encrypted": False,
                "password": None,
            }

            self.tab_manager.tabs.setTabText(
                index,
                os.path.basename(path),
            )

            editor.document().setModified(False)
            return True

        except Exception as e:
            QMessageBox.critical(
                self.tab_manager.tabs,
                "Error",
                f"Failed to save file:\n{e}",
            )
            return False

    def _save_encrypted(self, path, password, index):
        if not CRYPTO_AVAILABLE:
            QMessageBox.critical(
                self.tab_manager.tabs,
                "Error",
                "Cryptography not installed",
            )
            return False

        try:
            editor = self.tab_manager.tabs.widget(index)

            token, salt = encrypt_data(
                editor.toPlainText(),
                password,
            )

            with open(path, "wb") as f:
                f.write(salt + token)

            self.tab_manager.tab_files[index] = {
                "path": path,
                "encrypted": True,
                "password": password,
            }

            self.tab_manager.tabs.setTabText(
                index,
                os.path.basename(path),
            )

            editor.document().setModified(False)
            return True

        except Exception as e:
            QMessageBox.critical(
                self.tab_manager.tabs,
                "Error",
                f"Failed to encrypt file:\n{e}",
            )
            return False

    # ---------- Autosave ----------
    def autosave_all_tabs(self):
        for index in range(self.tab_manager.tabs.count()):
            editor = self.tab_manager.tabs.widget(index)

            if not editor.document().isModified():
                continue

            tab_data = self.tab_manager.tab_files.get(
                index,
                {},
            )

            path = tab_data.get("path")
            encrypted = tab_data.get("encrypted", False)
            password = tab_data.get("password")

            if not path:
                continue

            if encrypted:
                self._save_encrypted(
                    path,
                    password,
                    index,
                )
            else:
                self._save_plaintext(
                    path,
                    index,
                )
