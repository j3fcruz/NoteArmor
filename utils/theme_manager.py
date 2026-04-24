"""
utils/theme_manager.py
NoteArmor Free Edition — Single-theme loader.

REMOVED vs Pro:
    - watch_system_theme()        — background thread that monitored Windows registry
    - is_dark_mode_enabled()      — Windows-specific dark mode detection
    - get_dark_theme()            — built-in dark fallback QSS
    - get_light_theme()           — built-in light fallback QSS
    - get_indigo_theme()          — built-in indigo fallback QSS
    - per-name keyword fallback logic inside load_theme()
    - THEMES dict import (not needed; only one theme exists)

PRESERVED:
    - load_theme()        — loads Professional Blue from Qt resource or local file
    - apply_global_theme() — applies current app stylesheet to a widget
    - resource_path()     — frozen-safe path helper (Nuitka / PyInstaller)
"""

import os
import sys

from PySide6.QtCore import QFile, QTextStream
from PySide6.QtWidgets import QApplication

from config.app_config import DEFAULT_THEME, DEFAULT_THEME_QSS


# ── Frozen-safe path helper ──────────────────────────────────────────────────

def resource_path(relative_path: str) -> str:
    """Return absolute path to resource (works in dev and PyInstaller)."""
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ── Theme Loader ─────────────────────────────────────────────────────────────

def load_theme(app: QApplication, theme_name: str = DEFAULT_THEME) -> bool:
    """
    Load the Professional Blue theme stylesheet.

    Fallback order:
      1. Qt resource (preferred — embedded in binary)
      2. Local file on disk

    The ``theme_name`` parameter is accepted for API compatibility but is
    ignored in the Free Edition — only Professional Blue is available.

    Returns True on success, False if no stylesheet could be loaded.
    """
    theme_file = DEFAULT_THEME_QSS

    # ── Try Qt resource ──────────────────────────────────────────────────────
    qfile = QFile(theme_file)
    if qfile.exists() and qfile.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(qfile)
        app.setStyleSheet(stream.readAll())
        qfile.close()
        return True

    # ── Try local file ───────────────────────────────────────────────────────
    local_path = resource_path(theme_file.replace(":/", ""))
    if os.path.exists(local_path):
        try:
            with open(local_path, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
            return True
        except OSError as exc:
            print(f"[Theme] Failed to load local theme file: {exc}")

    return False


# ── Widget Helper ─────────────────────────────────────────────────────────────

def apply_global_theme(widget) -> None:
    """Apply the current application stylesheet to a widget or dialog."""
    app = QApplication.instance()
    if app:
        widget.setStyleSheet(app.styleSheet())
