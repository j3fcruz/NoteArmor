<div align="center">

<img src="assets/icons/notearmor.ico" alt="NoteArmor Secure Notepad Pro" width="96" height="96"/>

# NoteArmor — Secured Notepad Pro

**Free Edition · v3.1.0** · Built by [PatronHubDevs Technologies](https://www.patronhubdevs.com) · 🇵🇭 Philippines

[![License: PU-NC v1.0](https://img.shields.io/badge/License-PU--NC%20v1.0-red.svg)](#-license)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![PySide6](https://img.shields.io/badge/UI-PySide6-41CD52?logo=qt)](https://doc.qt.io/qtforpython/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows)](https://github.com/j3fcruz/Secured-Notepad)
[![Offline](https://img.shields.io/badge/Offline-First-success)](#-privacy)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/j3fcruz/Secured-Notepad/pulls)

> **Military-grade encryption meets modern note-taking.**  
> A privacy-first, offline encrypted text editor built for professionals, developers, and security advocates — zero telemetry, zero cloud dependency, zero compromise.

[Download](#-installation) · [Screenshots](#-screenshots) · [Encryption Spec](#-encryption-specification) · [Upgrade to Pro](#-upgrade-to-pro)

---

</div>

## Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Encryption Specification](#-encryption-specification)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [Limitations](#-limitations-free-edition)
- [Upgrade to Pro](#-upgrade-to-pro)
- [Security Notes](#-security-notes)
- [Privacy](#-privacy)
- [License](#-license)
- [Author](#-author)
- [Support](#-support)

---

## Overview

**NoteArmor — Secured Notepad Pro (Free Edition)** is an enterprise-grade encrypted text editor built with **PySide6**, engineered for privacy-first users who refuse to trust plaintext. Every `.notearmor` file is encrypted locally using **AES-128-CBC via Fernet** with **PBKDF2-HMAC-SHA256** key derivation — no data ever leaves your machine.

Designed with a clean multi-tab interface, autosave, and a professional custom theme. Fully air-gap safe, fully offline, and fully yours.

This is the **Free / Personal Use Edition** — complete for individual, non-commercial use.

---

## Features

### Encrypted Note Storage
- Password-protected `.notearmor` files using Fernet + PBKDF2-HMAC-SHA256
- 100,000 KDF iterations with 16-byte cryptographically random salt
- File format v3: `[16B salt][4B meta_len][JSON metadata][Fernet token]`

### Multi-Tab Workflow
- Open and manage multiple notes simultaneously
- Per-tab encryption state tracking
- Autosave every 60 seconds for modified plaintext files

### Editor Experience
- Built-in line number gutter with current-line highlight
- Zoom control: `Ctrl++` / `Ctrl+-` / `Ctrl+R` and `Ctrl+Wheel`
- Live status bar: Ln/Col position, encryption status, zoom level

### Offline First
- Zero network calls, zero telemetry, fully air-gap safe
- No cloud sync, no external dependencies, no analytics

---

## Screenshots

| Main Editor | Encrypted Save |
|-------------|---------------|
| ![Main](assets/screenshots/Main.png) | ![Encryption](assets/screenshots/Encryption.png) |

| Help | About |
|------|-------|
| ![Help](assets/screenshots/Help.png) | ![About](assets/screenshots/About.png) |

| Donate | Terms & License |
|--------|----------------|
| ![Donate](assets/screenshots/Donate.png) | ![Terms](assets/screenshots/TermsandConditions.png) |

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

> ⚠️ **No Password Recovery:** There is no password recovery mechanism. A lost password means permanently lost data. Store your password securely.

---

## Project Structure

```
NoteArmor/
├── main.py                        # Entry point — logging, QApplication bootstrap
├── requirements.txt
│
├── config/
│   └── app_config.py              # App metadata, paths, constants (no .env)
│
├── core/
│   └── encryption.pyd             # Compiled encryption module (Nuitka — Windows x64)
│
├── ui/
│   └── notearmor_free.py          # Main window (QMainWindow) — tabs, menus, file I/O
│
├── dialogs/
│   ├── about_dialog.py            # About (app info + license text)
│   ├── help_dialog.py             # Help (quick start, shortcuts, troubleshooting)
│   ├── password_entry_dialog.py
│   ├── save_dialog.py             # Save mode selector (plaintext vs encrypted)
│   └── terms_conditions_dialog.py
│
├── utils/
│   ├── editor.py                  # EnhancedTextEditor — line numbers, zoom, highlight
│   ├── advanced_features.py       # Syntax highlighting, recent files (Pro carry-over)
│   ├── file_handler.py            # FileHandler class (legacy — not used by Free UI)
│   ├── tab_manager.py             # TabManager class (legacy — not used by Free UI)
│   ├── logger.py                  # Structured file + console logging
│   ├── icon_manager.py            # Qt resource icon loader
│   ├── theme_manager.py           # QSS theme loader
│   ├── status_manager.py          # Status bar helper
│   └── _path_utils.py             # PathResolver — frozen/dev path resolution
│
├── resources/
│   ├── icons_rc.py                # Qt compiled icon resources
│   ├── themes_rc.py               # Qt compiled theme (QSS) resources
│   └── screenshots_rc.py          # Qt compiled screenshot resources
│
└── assets/
    └── icons/
        └── notearmor.ico
```

---

## Installation

### Option 1 — Prebuilt Binary (Recommended)

1. Download the latest release from [Gumroad](https://patronhubdevs.gumroad.com/l/nwbebh) or [GitHub Releases](https://github.com/j3fcruz/Secured-Notepad/releases)
2. Extract the ZIP archive
3. Run `NoteArmor.exe`

> No Python installation required. Ships as a standalone executable.

### Option 2 — Run from Source

**Requirements:** Python 3.12, Windows 10/11 (x64)

```bash
# 1. Clone the repository
git clone https://github.com/j3fcruz/NoteArmor.git
cd Secured-Notepad

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install PySide6>=6.5.0 cryptography>=41.0.0
# or
pip install -r requirements.txt

# 4. Run
python main.py
```

> `pyotp`, `psutil`, `pytesseract`, `Pillow`, `reportlab`, and `nuitka` are in `requirements.txt` for the Pro build pipeline. **Not required** to run the Free Edition from source.

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
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

## Limitations (Free Edition)

| Feature | Free | Pro |
|---------|------|-----|
| AES-128 Encrypted Notes | ✅ | ✅ |
| Multi-Tab Editing | ✅ | ✅ |
| Autosave | ✅ | ✅ |
| Offline Operation | ✅ | ✅ |
| Professional Blue Theme | ✅ | ✅ |
| Theme Switching | ❌ | ✅ |
| Keyfile Authentication | ❌ | ✅ |
| TOTP (2FA) Authentication | ❌ | ✅ |
| AES-256 Encryption | ❌ | ✅ |
| Search & Replace | ❌ | ✅ |
| Syntax Highlighting | ❌ | ✅ |
| RSA-4096 Offline Licensing | ❌ | ✅ |
| Cython-Compiled Security Core | ❌ | ✅ |
| Priority Updates & Support | ❌ | ✅ |

---

## Upgrade to Pro

**NoteArmor Secure Notepad Pro** unlocks the full security stack:

- **AES-256 Encryption** — hardened beyond the Free Edition baseline
- **Triple-Layer Authentication** — Password + Keyfile + TOTP (2FA)
- **RSA-4096 Offline Licensing** — no internet required, no phone-home
- **Cython-Compiled Security Core** — `.pyd` modules, source not exposed
- **Theme Switching** — multiple UI themes including dark and high-contrast
- **Search & Replace + Syntax Highlighting** — full editor feature set
- **Priority Updates & Support**

> [**Upgrade on Gumroad →**](https://patronhubdevs.gumroad.com/l/nwbebh)

---

## Security Notes

- Passwords are held **in-memory only** within `tab_files` for the session duration
- No password is written to disk, logs, or any external store
- The autosave routine **skips encrypted tabs** — only plaintext files are autosaved
- Log output is written to `notearmor.log` at `WARNING` level in production builds
- `core/encryption.pyd` is a **Nuitka-compiled** Windows DLL — source not distributed

---

## Privacy

NoteArmor is engineered with a strict privacy-first architecture:

- **No telemetry** — zero usage data collected
- **No tracking** — no analytics, crash reporters, or fingerprinting
- **No internet required** — fully air-gap compatible
- **Files never leave your device** — all encryption and processing is local

---

## License

**NoteArmor Personal Use and Non-Commercial License (PU-NC) v1.0**  
Copyright © 2025 PatronHubDevs Technologies. All rights reserved.

- Redistribution of modified builds is not permitted
- Pro features may not be reverse-engineered or bypassed
- Attribution to PatronHubDevs Technologies must be retained

See [LICENSE](LICENSE) for full terms.

---

## Author

**Marco Polo**  
PatronHubDevs Technologies  
🇵🇭 Philippines  
[Website](https://www.patronhubdevs.com) · [GitHub](https://github.com/j3fcruz/Secured-Notepad) · [Gumroad](https://patronhubdevs.gumroad.com/l/nwbebh)

---

## Support

If NoteArmor keeps your notes safe, consider supporting development:

- ⭐ **Star** the repository
- 📢 **Share** it with your network
- 💎 **[Upgrade to Pro](https://patronhubdevs.gumroad.com/l/nwbebh)** to support continued development
- ☕ **[Ko-fi](https://ko-fi.com/marcopolo55681)** · 💸 **[PayPal](https://paypal.me/jofreydelacruz13)**

---

<div align="center">

**NoteArmor — Secured Notepad Pro** · PatronHubDevs Technologies · Philippines  
*Write. Encrypt. Protect.*

</div>
