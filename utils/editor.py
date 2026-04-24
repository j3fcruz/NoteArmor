"""
utils/editor.py
---------
EnhancedTextEditor with line numbers, current-line highlighting,
and professional defaults (PySide6).
"""

from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPainter, QColor, QTextFormat, QFontDatabase


class LineNumberArea(QWidget):
    """Displays line numbers next to the text editor."""

    def __init__(self, editor: QPlainTextEdit):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class EnhancedTextEditor(QPlainTextEdit):
    DEFAULT_FONT_SIZE = 14

    def __init__(self, parent=None):
        super().__init__(parent)

        self._wheel_zoom_callback = None

        # ---------- Font ----------
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSize(self.DEFAULT_FONT_SIZE)
        self.setFont(font)

        self.setTabStopDistance(
            self.fontMetrics().horizontalAdvance(" ") * 4
        )

        # ---------- Line Numbers ----------
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    # ---------- Line Number Logic ----------
    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        return (
            3
            + self.fontMetrics().horizontalAdvance("9") * digits
            + 6
        )

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(
                0,
                rect.y(),
                self.lineNumberArea.width(),
                rect.height(),
            )

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#1e1e1e"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()

        top = int(
            self.blockBoundingGeometry(block)
            .translated(self.contentOffset())
            .top()
        )
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(QColor("#7a7a7a"))
                painter.drawText(
                    0,
                    top,
                    self.lineNumberArea.width() - 6,
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    str(block_number + 1),
                )

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(
                cr.left(),
                cr.top(),
                self.lineNumberAreaWidth(),
                cr.height(),
            )
        )

    # ---------- Current Line Highlight ----------
    def highlightCurrentLine(self):
        if self.isReadOnly():
            self.setExtraSelections([])
            return

        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor(45, 45, 45))
        selection.format.setProperty(
            QTextFormat.FullWidthSelection, True
        )
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()

        self.setExtraSelections([selection])

    # ---------- Ctrl + Wheel Zoom ----------
    def set_wheel_zoom_callback(self, callback):
        self._wheel_zoom_callback = callback

    def wheelEvent(self, event):
        if (
            event.modifiers() & Qt.ControlModifier
            and self._wheel_zoom_callback
        ):
            delta = 1 if event.angleDelta().y() > 0 else -1
            self._wheel_zoom_callback(delta)
            event.accept()
        else:
            super().wheelEvent(event)
