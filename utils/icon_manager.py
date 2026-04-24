"""
utils/icon_manager.py
---------------
Enterprise-grade icon loader for Enhanced Notepad Pro.
Supports Qt resources and local fallback for PyInstaller / Nuitka.
"""

import os
import sys
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt


# -----------------------------------------------------
# Helper: Get Absolute Path
# -----------------------------------------------------
def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource.
    Works for:
    - Development
    - PyInstaller (--onefile / --onedir)
    - Nuitka
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# -----------------------------------------------------
# Load Icon
# -----------------------------------------------------
def load_icon(name: str = "icon.png") -> QIcon:
    """
    Load icon using the following priority:
    1. Qt Resource (.qrc)
    2. Local assets folder
    3. Transparent fallback icon
    """

    # ---- Qt Resource (Preferred) ----
    qrc_path = f":/assets/icons/{name}"
    icon = QIcon(qrc_path)
    if not icon.isNull():
        return icon

    # ---- Local File Fallback ----
    local_path = resource_path(
        os.path.join("assets", "icons", name)
    )

    if os.path.exists(local_path):
        icon = QIcon(local_path)
        if not icon.isNull():
            return icon

    # ---- Safe Fallback (No crash) ----
    placeholder = QPixmap(32, 32)
    placeholder.fill(Qt.transparent)
    return QIcon(placeholder)


# -----------------------------------------------------
# Apply Application Icon
# -----------------------------------------------------
def set_app_icon(app, name: str = "icon.png") -> QIcon:
    """
    Apply application-wide icon.
    Safe for early startup.
    """
    icon = load_icon(name)
    app.setWindowIcon(icon)
    return icon
