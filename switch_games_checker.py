import os
import re
import sys
import time
import platform
from datetime import datetime
from colorama import init, Fore, Style

# ==============================
# INIT COLORAMA + UTF8
# ==============================
init(autoreset=True)

if sys.platform == "win32":
    os.system("chcp 65001 > nul")

# ==============================
# EMOJI SYSTEM (CLEAN VERSION)
# ==============================
win_ver = platform.release()

# Emoji SOLO su Windows 11
if sys.platform == "win32" and win_ver != "10":
    ICON_GAME = "🎮 "
    ICON_SEARCH = "🔎 "
    ICON_STATS = "📊 "
    ICON_LOG = "📝 "
    ICON_EXIT = "💣 "
else:
    ICON_GAME = ""
    ICON_SEARCH = ""
    ICON_STATS = ""
    ICON_LOG = ""
    ICON_EXIT = ""

# ==============================
# COLORS
# ==============================
class C:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    WHITE = Fore.WHITE
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL

# ==============================
# CONFIG
# ==============================
GAME_EXTENSIONS = (".nsp", ".nsz", ".xci", ".xcz")
LOGS_ENABLED = False
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "switch_checker_log.txt")

# ==============================
# LOG SYSTEM
# ==============================
def ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def log_write(text):
    if not LOGS_ENABLED:
        return
    ensure_log_dir()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def log_session_start():
    if not LOGS_ENABLED:
        return
    ensure_log_dir()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "="*60 + "\n")
        f.write(f"SESSION START: {datetime.now()}\n")
        f.write("="*60 + "\n")

def toggle_logs():
    global LOGS_ENABLED
    LOGS_ENABLED = not LOGS_ENABLED
    if LOGS_ENABLED:
        log_session_start()

# ==============================
# HEADER
# ==============================
def print_header():
    width = 60
    line = "═" * width
    print(C.RED + C.BOLD + line)
    print(C.RED + C.BOLD + "SWITCH GAMES CHECKER".center(width))
    text = "by krz"
    padding = (width - len(text)) // 2
    print(" " * padding + C.WHITE + "by " + C.GREEN + "krz")
    print(C.RED + C.BOLD + line)

# ==============================
# DRIVE DETECTION
# ==============================
def get_target_paths(folder_name):
    paths = []
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        path = f"{letter}:\\{folder_name}"
        if os.path.exists(path):
            paths.append(path)
    return paths

# ==============================
# PROGRESS BAR
# ==============================
def show_progress(current, total, start_time):
    percent = int((current / total) * 100)
    bar_length = 40
    filled = int(bar_length * current // total)
    bar = "█" * filled + "-" * (bar_length - filled)

    elapsed = time.time() - start_time
    speed = int(current / elapsed) if elapsed > 0 else 0

    print(f"\r{C.GREEN}{bar}{C.RESET} {percent}% ({current}/{total}) | {speed} files/sec", end="")

# ==============================
# TITLE ID PARSER
# ==============================
def extract_title_id(filename):
    match = re.search(r"\[([0-9A-Fa-f]{16})\]", filename)
    if match:
        return match.group(1).upper()
    return None

def extract_version(filename):
    match = re.search(r"[vV](\d+)", filename)
    if match:
        return int(match.group(1))
    return 0

# ==============================
# SCAN FILES
# ==============================
def scan_all_games():
    drives = get_target_paths("NSP")
    files = []
    for drive in drives:
        for root, dirs, filenames in os.walk(drive):
            for file in filenames:
                if file.lower().endswith(GAME_EXTENSIONS):
                    files.append(os.path.join(root, file))
    return files

# ==============================
# STATS
# ==============================
def show_stats():
    print("\n" + C.MAGENTA + C.BOLD + f"{ICON_STATS}SWITCH STATS")
    print("══════════════════════════════")

    files = scan_all_games()

    base = 0
    updates = 0
    dlc = 0
    base_ids = set()

    for path in files:
        lower = path.lower()
        tid = extract_title_id(path)

        if "update" in lower:
            updates += 1
        elif "dlc" in lower:
            dlc += 1
        else:
            base += 1
            if tid:
                base_ids.add(tid)

    print(C.GREEN + f"{ICON_GAME}Base Games: {base}")
    print(C.CYAN + f"Updates: {updates}")
    print(C.YELLOW + f"DLC: {dlc}")
    print(C.MAGENTA + f"Unique Base Titles: {len(base_ids)}")
    print(C.WHITE + f"Total Files: {len(files)}")
    print("══════════════════════════════\n")

# ==============================
# DUPLICATE CHECK
# ==============================
def check_game_duplicates():
    print(C.CYAN + "\nScanning Games...\n")

    files = scan_all_games()
    total = len(files)
    start_time = time.time()

    games = {}
    scanned = 0

    for full_path in files:
        scanned += 1
        show_progress(scanned, total, start_time)

        filename = os.path.basename(full_path)
        tid = extract_title_id(filename)
        if not tid:
            continue

        name = re.sub(r"\[.*?\]", "", filename)
        name = os.path.splitext(name)[0].strip()

        if tid not in games:
            games[tid] = {"name": name, "Base": [], "Updates": [], "DLC": []}

        lower = full_path.lower()

        if "update" in lower:
            games[tid]["Updates"].append(full_path)
        elif "dlc" in lower:
            games[tid]["DLC"].append(full_path)
        else:
            games[tid]["Base"].append(full_path)

    print("\n")

    duplicates_found = 0

    for tid, data in games.items():
        if len(data["Base"]) > 1 or len(data["Updates"]) > 1 or len(data["DLC"]) > 1:
            duplicates_found += 1

            print(C.RED + "════════════════════════════════════")
            print(C.YELLOW + f"{ICON_GAME}TITLE: {data['name']}")
            print(C.CYAN + f"TITLE ID: {tid}")
            print(C.RED + "════════════════════════════════════\n")

            for section in ["Base", "Updates", "DLC"]:
                if len(data[section]) > 1:
                    print(C.MAGENTA + f"{section} DUPLICATES:")
                    if section == "Updates":
                        versions = [(p, extract_version(p)) for p in data[section]]
                        versions.sort(key=lambda x: x[1], reverse=True)
                        highest = versions[0][1]

                        for path, ver in versions:
                            marker = " <-- Highest" if ver == highest else ""
                            print(C.RED + f"  {path} (v{ver}){marker}")
                            log_write(path)
                    else:
                        for path in data[section]:
                            print(C.RED + "  " + path)
                            log_write(path)
                    print()

    if duplicates_found == 0:
        print(C.GREEN + "No duplicate games found.\n")
    else:
        print(C.GREEN + f"\nDuplicate Game Titles Found: {duplicates_found}\n")

    print(C.RED + "════════════════════ DONE ════════════════════\n")

# ==============================
# SEARCH
# ==============================
def search_games():
    print()
    query = input(f"{ICON_SEARCH}Search: ").lower()
    files = scan_all_games()
    results = 0

    for path in files:
        if query in path.lower():
            print(C.GREEN + path)
            log_write(path)
            results += 1

    print(C.CYAN + f"\nResults Found: {results}\n")

# ==============================
# MENU
# ==============================
def main():
    while True:
        print()
        print_header()
        print()
        print(C.GREEN + f"1) {ICON_GAME}Check Game Duplicates")
        print(C.CYAN + f"2) {ICON_SEARCH}Search Games")
        print(C.MAGENTA + f"3) {ICON_STATS}Show Stats")

        if LOGS_ENABLED:
            print(C.BLUE + f"4) {ICON_LOG}Logs: Enabled")
        else:
            print(C.YELLOW + f"4) {ICON_LOG}Logs: Disabled")

        print(C.RED + f"5) {ICON_EXIT}Exit")

        choice = input("\nSelect: ")

        if choice == "1":
            check_game_duplicates()
        elif choice == "2":
            search_games()
        elif choice == "3":
            show_stats()
        elif choice == "4":
            toggle_logs()
        elif choice == "5":
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()