"""
main.py — NoteArmor Secure Notepad Pro (Free Edition)
Production entry point.

- WARNING level logging in production; DEBUG in dev
- No stdout handler in production
- Static imports only (Nuitka compatible)
"""

import sys
import logging

from PySide6.QtWidgets import QApplication, QMessageBox

from config.app_config import IS_PRODUCTION
from resources import icons_rc   # noqa: F401 — forces Qt resource registration
from resources import themes_rc  # noqa: F401

from ui.notearmor_free import EnhancedNotepad
from utils.theme_manager import load_theme
from utils.icon_manager import load_icon


def _configure_logging() -> None:
    level = logging.WARNING if IS_PRODUCTION else logging.DEBUG
    handlers: list[logging.Handler] = [
        logging.FileHandler("notearmor.log", encoding="utf-8"),
    ]
    if not IS_PRODUCTION:
        handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
    )


def main() -> None:
    """Start NoteArmor Secure Notepad Pro — Free Edition."""
    _configure_logging()
    log = logging.getLogger(__name__)

    try:
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(True)

        # Load Professional Blue theme
        try:
            load_theme(app)
        except (FileNotFoundError, ImportError, AttributeError) as err:
            log.warning("Theme load failed: %s — continuing without theme", err)

        # Initialise main window
        try:
            window = EnhancedNotepad()
        except Exception as exc:
            log.exception("Failed to initialise main window")
            QMessageBox.critical(
                None, "Startup Error",
                f"Failed to initialise main window:\n\n{exc}",
            )
            sys.exit(1)

        # Apply window icon
        try:
            icon = load_icon("icon.png")
            if icon:
                window.setWindowIcon(icon)
        except Exception as err:
            log.warning("Icon load failed: %s", err)

        try:
            window.show()
        except Exception as exc:
            log.exception("Failed to show main window")
            QMessageBox.critical(
                None, "Runtime Error",
                f"Failed to show main window:\n\n{exc}",
            )
            sys.exit(1)

        sys.exit(app.exec())

    except Exception as exc:
        logging.exception("Unhandled exception during startup")
        QMessageBox.critical(
            None, "Fatal Error",
            f"An unexpected error occurred:\n\n{exc}",
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
