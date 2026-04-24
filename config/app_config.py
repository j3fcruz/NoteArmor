# config/app_config.py
# ---------------------------------------------------------
# NoteArmor Free Edition — Configuration (v3.1)
# Compile-time constants only — no dotenv, no os.getenv.
#
# REMOVED vs Pro:
#   - All theme constants except BLUE (Professional Blue)
#   - THEMES dict collapsed to single-entry (Free Edition is single-theme)
#   - THEME_SHORTCUTS removed (no theme switching in Free Edition)
#   - GET_THEMES alias removed
#   - DARK_THEME_QSS / LIGHT_THEME_QSS aliases removed
# PRESERVED:
#   - All app metadata, asset paths, external links
#   - resource_path() — frozen-safe resolver (Nuitka / PyInstaller)
#   - DEFAULT_THEME / DEFAULT_THEME_QSS — used by theme_manager
#   - get_app_metadata() — used by dialogs
# ---------------------------------------------------------

import os
import sys
from datetime import datetime

# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------
APP_ENV = "production"
IS_PRODUCTION = True
IS_DEVELOPMENT = False

# ---------------------------------------------------------
# Application Metadata
# ---------------------------------------------------------
APP_NAME = "NoteArmor Secure Notepad Pro"
APP_TITLE = APP_NAME
HASH_NAME = "notearmor"
APP_VERSION = "3.1.0"
AUTHOR = "Marco Polo"
APP_DEVELOPER = "PatronHubDevs Technologies"
COPYRIGHT_YEAR = "2025"
COPYRIGHT = f"© {COPYRIGHT_YEAR} {APP_NAME}. All rights reserved."
ABOUT_APP = "Military-grade encryption meets modern note-taking."
DATE_STR = datetime.now().strftime("%B %d, %Y")

DESCRIPTION = (
    f"{APP_NAME} by {AUTHOR} is an enterprise-grade encrypted text editor "
    "built for professionals, developers, and privacy advocates. It combines "
    "elegant UI design with advanced cryptographic protection to keep your "
    "notes safe and secure."
)


# ---------------------------------------------------------
# Resource Path — Frozen-safe (Nuitka + PyInstaller)
# ---------------------------------------------------------
def resource_path(relative_path: str) -> str:
    """
    Resolve absolute path to a resource.
    Supports Qt resource paths, Nuitka frozen, PyInstaller frozen, and dev.
    """
    if relative_path.startswith(":/"):
        return relative_path

    try:
        if getattr(sys, "frozen", False):
            if hasattr(sys, "_MEIPASS"):
                # PyInstaller
                base_path = sys._MEIPASS
            else:
                # Nuitka: executable directory
                base_path = os.path.dirname(sys.executable)

            frozen_path = os.path.join(base_path, relative_path)
            if os.path.exists(frozen_path):
                return frozen_path

        # Development fallback
        dev_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", relative_path)
        )
        if os.path.exists(dev_path):
            return dev_path

        cwd_path = os.path.join(os.getcwd(), relative_path)
        return cwd_path if os.path.exists(cwd_path) else relative_path

    except Exception:
        return relative_path


# ---------------------------------------------------------
# Asset Paths (Qt resource paths only)
# ---------------------------------------------------------
ICON_PATH = ":/assets/icons/icon.png"
LOGO_PATH = ":/assets/logo/logo.png"
ABOUT_ICON_PATH = ":/assets/icons/about_icon.png"
DONATE_ICON_PATH = ":/assets/icons/donate_icon.png"
HELP_ICON_PATH = ":/assets/icons/help_icon.png"
LICENSE_ICON_PATH = ":/assets/icons/license_icon.png"
LOCK_ICON_PATH = ":/assets/icons/lock_icon.ico"
README_ICON_PATH = ":/assets/icons/readme_icon.png"
SAVE_ICON_PATH = ":/assets/icons/save_icon.ico"
TERMS_ICON_PATH = ":/assets/icons/terms_icon.png"

#MAYA_QR_PATH = ":/assets/resources/maya_qr.bin"
#MAYA_QR_KEY = b""  # Injected at build time — never from env

SCREENSHOT_PATH_IMAGES = [
    resource_path(os.path.join("assets", "screenshots", "Main.png")),
    resource_path(os.path.join("assets", "screenshots", "Encryption.png")),
    resource_path(os.path.join("assets", "screenshots", "Help.png")),
    resource_path(os.path.join("assets", "screenshots", "About.png")),
    resource_path(os.path.join("assets", "screenshots", "Donate.png")),
    resource_path(os.path.join("assets", "screenshots", "TermsandConditions.png")),
    resource_path(os.path.join("assets", "screenshots", "LicenseAgreement.png")),
]

# ---------------------------------------------------------
# External Links
# ---------------------------------------------------------
MAIL_TO = "mailto:contact@patronhubdevs.online"
HOMEPAGE = "https://www.patronhubdevs.online"
GITHUB_ID = "https://github.com/j3fcruz/Secured-Notepad"
KOFI_ID = "https://ko-fi.com/marcopolo55681"
PAYPAL_ID = "https://paypal.me/jofreydelacruz13"

BTC_NAME = "Bitcoin (BTC) Address"
BTC_ID = "1BcWJT8gBdZSPwS8UY39X9u4Afu1nZSzqk"

ETH_NAME = "Ethereum (ETH) Address"
ETH_ID = "0xcd5eef32ff4854e4cefa13cb308b727433505bf4"

# ---------------------------------------------------------
# Theme — Free Edition: Professional Blue only
# (All other theme constants removed.)
# ---------------------------------------------------------
BLUE = ":/assets/themes/professional_blue.qss"

DEFAULT_THEME_QSS = BLUE
DEFAULT_THEME = "Professional Blue Theme"


def get_app_metadata() -> dict:
    """Returns application metadata dict for UI consumption."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "author": AUTHOR,
        "company": APP_DEVELOPER,
        "copyright": COPYRIGHT,
        "env": APP_ENV,
    }
