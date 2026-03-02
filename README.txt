============================================================
                    SWITCH GAMES CHECKER
============================================================

Switch Games Checker is a Python-based CLI tool that scans
all connected drives for Nintendo Switch game files:

- .nsp
- .nsz
- .xci
- .xcz

It organizes files by Title ID and detects duplicate:

- Base Games
- Updates
- DLC

It also provides library statistics and a search function.

============================================================
REQUIREMENTS
============================================================

- Python 3.10 or newer
- colorama

Install dependencies with:

py -m pip install -r requirements.txt


============================================================
RECOMMENDED FOLDER STRUCTURE
============================================================

Prepare your directories like this:

X:\NSP\titles
X:\NSP\titles\updates
X:\NSP\titles\DLC

Where:

X = your drive letter (C, D, E, F, G, etc.)

You can use multiple drives.
The tool automatically scans all connected drives.


============================================================
USAGE
============================================================

Open CMD or PowerShell in the project folder and run:

py switch_games_checker.py

Use the interactive menu to:

1) Check Game Duplicates
2) Search Games
3) Show Stats
4) Enable / Disable Logs
5) Exit


============================================================
LOGS
============================================================

If enabled, the tool automatically creates:

logs\

And stores results inside:

logs\switch_checker_log.txt


============================================================
BUILD STANDALONE EXE
============================================================

Install PyInstaller:

py -m pip install pyinstaller

Build single executable:

pyinstaller --onefile --clean switch_games_checker.py

The executable will be created in:

dist\switch_games_checker.exe

Python is NOT required on the target machine.


============================================================
DISCLAIMER
============================================================

This tool does not download, modify, or distribute any game
files. It only scans and analyzes files already present on
your local drives.


Author: krz
============================================================