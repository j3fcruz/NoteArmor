"""
modules/tab_manager.py
Manages multiple text editor tabs with metadata tracking.
(PySide6 version)
"""

from PySide6.QtWidgets import QTabWidget, QMessageBox
from PySide6.QtCore import QObject
from utils.editor import EnhancedTextEditor


class TabManager_(QObject):
    """Handles multi-tab operations and metadata tracking."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # --- Status manager intentionally NOT connected here ---
        # self.tabs.currentChanged.connect(self.parent.status_manager.update_status_bar)

        # Metadata per tab:
        # {index: {"path": str | None, "encrypted": bool, "password": str | None}}
        self.tab_files = {}

        # Default font size reference for zoom calculations
        self.default_font_size = 12

    # -------------------------------------------------
    # External Status Manager Wiring
    # -------------------------------------------------
    def connect_status_manager(self, status_manager):
        self.tabs.currentChanged.connect(status_manager.update_status_bar)

    # -------------------------------------------------
    # Current State Helpers
    # -------------------------------------------------
    def current_editor(self):
        editor = self.tabs.currentWidget()
        return editor if isinstance(editor, EnhancedTextEditor) else None

    def current_tab_index(self):
        return self.tabs.currentIndex()

    def current_tab_data(self):
        return self.tab_files.get(self.current_tab_index(), {})

    # -------------------------------------------------
    # Tab Creation
    # -------------------------------------------------
    def new_tab(self, path=None, content="", encrypted=False, password=None):
        editor = EnhancedTextEditor()
        editor.setPlainText(content)
        editor.document().setModified(False)

        # Connect editor signals to status manager (if available)
        if hasattr(self.parent, "status_manager"):
            editor.cursorPositionChanged.connect(
                self.parent.status_manager.update_status_bar
            )
            editor.textChanged.connect(
                self.parent.status_manager.update_status_bar
            )

        title = path if path else "Untitled"
        index = self.tabs.addTab(editor, title)
        self.tabs.setCurrentIndex(index)

        self.tab_files[index] = {
            "path": path,
            "encrypted": encrypted,
            "password": password,
        }

        # Capture default font size once
        if not self.default_font_size:
            self.default_font_size = editor.font().pointSize()

    # -------------------------------------------------
    # Tab Closing
    # -------------------------------------------------
    def close_tab(self, index):
        editor = self.tabs.widget(index)
        if editor and editor.document().isModified():
            reply = QMessageBox.question(
                self.tabs,
                "Unsaved Changes",
                f"Tab '{self.tabs.tabText(index)}' has unsaved changes. Save?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            )

            if reply == QMessageBox.Save:
                self.tabs.setCurrentIndex(index)
                if hasattr(self.parent, "file_handler"):
                    if not self.parent.file_handler.save_file():
                        return
            elif reply == QMessageBox.Cancel:
                return

        self.tabs.removeTab(index)
        self.tab_files.pop(index, None)
