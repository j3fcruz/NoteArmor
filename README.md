# NoteArmor — Secured Notepad Pro (Free Edition)

> **Military-grade encryption meets modern note-taking.**  
> A privacy-first, offline encrypted text editor built for professionals, developers, and privacy advocates.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![PySide6](https://img.shields.io/badge/PySide6-6.5%2B-green?logo=qt)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-PU--NC%20v1.0-red)
![Version](https://img.shields.io/badge/Version-3.1.0-orange)

---

## Overview

NoteArmor is an enterprise-grade encrypted text editor that keeps your notes safe without cloud dependency. Every file you protect is encrypted locally using **AES-128 via Fernet** with **PBKDF2-HMAC-SHA256** key derivation — no data ever leaves your machine.

This is the **Free / Personal Use Edition**. It is fully functional for individual, non-commercial use.

---

## Features

| Feature | Details |
|---|---|
| **Encrypted Save** | Password-protected `.notearmor` files using Fernet + PBKDF2 |
| **Plaintext Save** | Standard `.txt` files with UTF-8 encoding |
| **Multi-Tab Editing** | Open and manage multiple notes simultaneously |
| **Autosave** | Automatic save every 60 seconds for modified files |
| **Line Numbers** | Built-in line number gutter with current-line highlight |
| **Zoom Control** | `Ctrl++` / `Ctrl+-` / `Ctrl+R`, plus `Ctrl+Wheel` |
| **Status Bar** | Live Ln/Col position, encryption status, zoom level |
| **Professional Blue Theme** | Custom QSS theme, ships bundled via Qt resources |
| **Offline-First** | Zero network calls, zero telemetry, fully air-gap safe |

---

## Encryption Specification

```
Algorithm       : Fernet (AES-128-CBC + HMAC-SHA256)
Key Derivation  : PBKDF2-HMAC-SHA256
KDF Iterations  : 100,000
Salt            : 16 bytes, cryptographically random (os.urandom)
File Format v3  : [16B salt][4B meta_len][JSON metadata][Fernet token]
File Extension  : .notearmor
```

> ⚠️ **Password Warning:** There is no password recovery mechanism. A lost password means permanently lost data. Store your password securely.

---

## Screenshots

| Main Editor | Encrypted Save | Help |
|---|---|---|
| ![Main](assets/screenshots/Main.png) | ![Encryption](assets/screenshots/Encryption.png) | ![Help](assets/screenshots/Help.png) |

| About | Donate | Terms & License |
|---|---|---|
| ![About](assets/screenshots/About.png) | ![Donate](assets/screenshots/Donate.png) | ![Terms](assets/screenshots/TermsandConditions.png) |

---

## Requirements

- **OS:** Windows 10/11 (x64)
- **Python:** 3.12 (if running from source)
- **Dependencies:** see `requirements.txt`

```
PySide6>=6.5.0,<7.0
cryptography>=41.0.0
```

> `pyotp`, `psutil`, `pytesseract`, `Pillow`, `reportlab`, and `nuitka` are included in `requirements.txt` for the Pro build pipeline. They are **not required** to run the Free Edition from source.

---

## Installation (From Source)

```bash
# 1. Clone the repository
git clone https://github.com/j3fcruz/Secured-Notepad.git
cd Secured-Notepad

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux/macOS

# 3. Install dependencies
pip install PySide6>=6.5.0 cryptography>=41.0.0

# 4. Run
python main.py
```

---

## Project Structure

```
NoteArmor/
├── main.py                    # Entry point — logging, QApplication bootstrap
├── requirements.txt
│
├── config/
│   └── app_config.py          # App metadata, paths, constants (no .env)
│
├── core/
│   └── encryption.pyd         # Compiled encryption module (Nuitka — Windows x64)
│
├── ui/
│   └── notearmor_free.py      # Main window (QMainWindow) — tabs, menus, file I/O
│
├── dialogs/
│   ├── about_dialog.py        # About (app info + license text)
│   ├── help_dialog.py         # Help (quick start, shortcuts, troubleshooting)
│   ├── password_entry_dialog.py
│   ├── save_dialog.py         # Save mode selector (plaintext vs encrypted)
│   └── terms_conditions_dialog.py
│
├── utils/
│   ├── editor.py              # EnhancedTextEditor — line numbers, zoom, highlight
│   ├── advanced_features.py   # Syntax highlighting, recent files (Pro carry-over)
│   ├── file_handler.py        # FileHandler class (legacy path — not used by Free UI)
│   ├── tab_manager.py         # TabManager class (legacy path — not used by Free UI)
│   ├── logger.py              # Logger class (structured file + console logging)
│   ├── icon_manager.py        # Qt resource icon loader
│   ├── theme_manager.py       # QSS theme loader
│   ├── status_manager.py      # Status bar helper
│   └── _path_utils.py         # PathResolver — frozen/dev path resolution
│
├── resources/
│   ├── icons_rc.py            # Qt compiled icon resources
│   ├── themes_rc.py           # Qt compiled theme (QSS) resources
│   └── screenshots_rc.py      # Qt compiled screenshot resources
│
└── assets/
    └── icons/
        └── notearmor.ico
```

---

## Keyboard Shortcuts

| Action | Shortcut |
|---|---|
| New Tab | `Ctrl+N` |
| Open File | `Ctrl+O` |
| Save | `Ctrl+S` |
| Save As | `Ctrl+Shift+S` |
| Undo | `Ctrl+Z` |
| Redo | `Ctrl+Y` |
| Cut / Copy / Paste | `Ctrl+X` / `Ctrl+C` / `Ctrl+V` |
| Zoom In / Out | `Ctrl++` / `Ctrl+-` |
| Reset Zoom | `Ctrl+R` |
| Help | `F1` |
| Exit | `Ctrl+Q` |

---

## Security Notes

- Passwords are held **in-memory only** within the `tab_files` dict for the session.
- No password is written to disk, logs, or any external store.
- The autosave routine skips encrypted tabs — only plaintext files are autosaved automatically.
- Log output is written to `notearmor.log` at `WARNING` level in production builds.
- The `core/encryption.pyd` binary is a **Nuitka-compiled** Windows DLL. Source code is not included in this repository.

---

## Known Limitations (Free Edition)

- Single theme only (Professional Blue). Theme switching available in Pro.
- No keyfile support. Password-only encryption.
- No search & replace UI (module present but not wired to menu).
- Syntax highlighting available in code but not connected to Free Edition UI.
- Tab index key (`tab_files` dict) can desync if tabs are closed out-of-order — handle with care when modifying.

---

## Support & Donation

NoteArmor is free for personal use. If it saves your data or your sanity, consider supporting development:

- 🌐 Website: [patronhubdevs.com](https://www.patronhubdevs.com)
- ☕ Ko-fi: [ko-fi.com/marcopolo55681](https://ko-fi.com/marcopolo55681)
- 💸 PayPal: [paypal.me/jofreydelacruz13](https://paypal.me/jofreydelacruz13)


---

## License

**NoteArmor Personal Use and Non-Commercial License (PU-NC) v1.0**  
Copyright © 2025 PatronHubDevs Technologies. All rights reserved.

See [LICENSE](LICENSE) for full terms.

---

*Built with ❤️ by Marco Polo / PatronHubDevs Technologies*
