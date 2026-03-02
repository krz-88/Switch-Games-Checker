# 🎮 Switch Games Checker

Switch Games Checker is a Python-based CLI tool that automatically scans all connected drives for:

- `.nsp`
- `.nsz`
- `.xci`
- `.xcz`

It organizes files by **Title ID** and detects duplicate:

- Base Games  
- Updates  
- DLC  

It also provides library statistics and a search function.

---

## ✅ Features

- Automatic scan of all connected drives (C, D, E, F, etc.)
- Duplicate detection by Title ID
- Update version comparison (shows highest version)
- Library statistics:
  - Base Games count
  - Updates count
  - DLC count
  - Unique Base Titles
  - Total files
- Optional logging system
- Clean CLI interface
- Compatible with:
  - Windows 10
  - Windows 11
  - Linux

---

## 📦 Requirements

- Python 3.10+
- `colorama`

Install dependencies:

```bash
py -m pip install -r requirements.txt
```

---

## 📁 Recommended Folder Structure

Prepare your directories like this:

```
X:\NSP\titles            <-- Base Games
X:\NSP\titles\updates    <-- Updates
X:\NSP\titles\DLC        <-- DLC
```

Where:

- `X` = your drive letter (C, D, E, F, G, etc.)
- You can use multiple drives
- The tool automatically scans all drives

---

## 🚀 Usage

Open a shell (CMD or PowerShell) in the project folder:

```bash
py switch_games_checker.py
```

Then use the interactive menu.

---

## 📝 Logs

If enabled from the menu, the tool automatically creates:

```
logs/
```

and stores results inside:

```
logs/switch_checker_log.txt
```

---

## 🛠 Build Standalone .exe

Install PyInstaller:

```bash
py -m pip install pyinstaller
```

Build single executable:

```bash
pyinstaller --onefile --clean switch_games_checker.py
```

The executable will be created in:

```
dist/switch_games_checker.exe
```

Python is NOT required on the target machine.

---

## 👤 Author

krz

---

## ⚠ Disclaimer

This tool does not download, modify, or distribute any game files.  
It only scans and analyzes files already present on your local drives.

---

## 📄 Main Script

Below is the main script entry point:

```python
if __name__ == "__main__":
    main()
```

The full source code is available in:

switch_games_checker.py
