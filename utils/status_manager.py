"""
modules/status_manager.py
Manages the status bar updates for the text editor application.
(PySide6 version)
"""

from PySide6.QtWidgets import QLabel


class StatusManager_:
    """Manages status bar updates per tab."""

    def __init__(self, parent, tab_manager):
        self.parent = parent
        self.tab_manager = tab_manager

        # ---- Status Bar (safe initialization) ----
        self.statusBar = parent.statusBar()
        if self.statusBar is None:
            self.statusBar = parent.statusBar()
            parent.setStatusBar(self.statusBar)

        # ---- Status Widgets ----
        self.line_col_label = QLabel("Ln 1, Col 1")
        self.char_count_label = QLabel("Length: 0")
        self.encoding_label = QLabel("UTF-8")
        self.crypto_status_label = QLabel("Plaintext")
        self.crlf_label = QLabel("CRLF")
        self.zoom_label = QLabel("Zoom: 100%")

        for widget in (
            self.line_col_label,
            "|",
            self.char_count_label,
            "|",
            self.encoding_label,
            "|",
            self.crypto_status_label,
            "|",
            self.crlf_label,
            "|",
            self.zoom_label,
        ):
            if isinstance(widget, str):
                self.statusBar.addPermanentWidget(QLabel(widget))
            else:
                self.statusBar.addPermanentWidget(widget)

    # -------------------------------------------------
    # Update Status Bar
    # -------------------------------------------------
    def update_status_bar(self):
        editor = self.tab_manager.current_editor()
        if not editor:
            return

        cursor = editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.line_col_label.setText(f"Ln {line}, Col {col}")

        char_count = len(editor.toPlainText())
        self.char_count_label.setText(f"Length: {char_count}")

        font_size = editor.font().pointSize()
        default_size = getattr(self.tab_manager, "default_font_size", font_size)
        zoom_percent = round((font_size / default_size) * 100)

        self.zoom_label.setText(f"Zoom: {zoom_percent}%")

        tab_data = self.tab_manager.current_tab_data() or {}
        encrypted = tab_data.get("encrypted", False)

        self.crypto_status_label.setText(
            "Encrypted (AES-256)" if encrypted else "Plaintext"
        )
