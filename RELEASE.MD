# 🚀 NoteArmor Secured Notepad Pro v3.1.0 – Free Edition

We're proud to announce **NoteArmor Secured Notepad Pro v3.1.0 Free Edition**,
a privacy-first encrypted notepad built with **Python** and **PySide6**.
Designed for professionals, developers, and privacy-conscious users who need
real encryption without cloud dependency.

---

## ✨ Features

### 🔐 Encryption
- **Fernet encryption** — AES-128-CBC + HMAC-SHA256
- **PBKDF2-HMAC-SHA256** key derivation — 100,000 iterations
- New **v3 binary file format** — structured and forward-compatible
- New file extension: `.notearmor` (replaces `.txt.enc`)
- Password-protected save and open dialogs
- Zero plaintext written to disk during encryption
- Compiled encryption core — source-protected on Windows

### 🎨 Interface
- **Professional Blue** QSS theme — bundled via Qt resource system
- Multi-tab support — work with unlimited notes simultaneously
- Clean, minimal menu bar optimized for personal use
- Integrated **line numbering** and **current-line highlight**
- **Status bar** — Ln/Col, 🔒 Encrypted / Plaintext, Zoom %
- Mouse-scroll zoom — `Ctrl + Mouse Wheel`
- Window auto-centers on launch
- HiDPI / 4K display ready via PySide6 Qt6 rendering

### ⚙ Functionality
- **Autosave** — every 60 seconds for modified plaintext files
- Multi-tab management — new, close, unsaved-changes prompt
- Save As dialog — choose plaintext `.txt` or encrypted `.notearmor`
- Password entry dialog for encrypted open and save
- Unsaved changes prompt on tab close and app exit
- Frozen-safe path resolver — works compiled and from source
- Production logging — `WARNING` level to `notearmor.log`

---

## 🧩 Technical Overview

| Property | Details |
|---|---|
| Language | Python 3.12 |
| Framework | PySide6 6.5+ |
| Encryption | Fernet — AES-128-CBC + HMAC-SHA256 |
| Key Derivation | PBKDF2-HMAC-SHA256 — 100,000 iterations |
| File Format | `.notearmor` v3 binary |
| Supported OS | Windows 10/11 x64 |
| License | PU-NC v1.0 — Free for personal use |

---

## ⌨ Keyboard Shortcuts

| Action | Shortcut |
|---|---|
| New Tab | `Ctrl+N` |
| Open File | `Ctrl+O` |
| Save | `Ctrl+S` |
| Save As | `Ctrl+Shift+S` |
| Undo / Redo | `Ctrl+Z` / `Ctrl+Y` |
| Cut / Copy / Paste | `Ctrl+X` / `Ctrl+C` / `Ctrl+V` |
| Zoom In / Out | `Ctrl++` / `Ctrl+-` |
| Reset Zoom | `Ctrl+R` |
| Help | `F1` |
| Exit | `Ctrl+Q` |

---

## 🧠 Usage Guide

1. Launch `main.py` or the compiled `.exe`
2. Create new tabs with `Ctrl+N`
3. Write your notes freely across multiple tabs
4. Save encrypted: `Ctrl+Shift+S` → choose **Encrypted** → set password
5. Your file saves as `note_YYYYMMDD_HHMMSS.notearmor`
6. To open: `Ctrl+O` → select `.notearmor` → enter password to decrypt
7. Zoom with `Ctrl+Mouse Wheel` or `Ctrl++` / `Ctrl+-`

> ⚠️ **Critical:** There is no password recovery mechanism.
> A lost password means permanently lost data.
> Always store your password in a password manager.

---

## 📦 Free Edition vs Pro

| Feature | Free Edition | Pro Edition |
|---|---|---|
| Encrypted save / open | ✅ | ✅ |
| Multi-tab editing | ✅ | ✅ |
| Autosave | ✅ | ✅ |
| Professional Blue theme | ✅ | ✅ |
| Multiple themes | ❌ | ✅ |
| Keyfile encryption | ❌ | ✅ |
| Search & Replace UI | ❌ | ✅ |
| Syntax highlighting | ❌ | ✅ |

---

## 🧯 Installation (From Source)

```bash
