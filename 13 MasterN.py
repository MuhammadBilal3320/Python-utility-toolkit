import os
import sys
import time
from datetime import datetime
from tabulate import tabulate

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: The 'watchdog' package is not installed. Please install it using 'pip install watchdog tabulate'.")
    sys.exit(1)

LOG_FILE = "file_activity_log.txt"
MONITORED_DIR = "D:\\"  # Change this to the directory you want to monitor
EXCLUDED_FOLDERS = ["$RECYCLE.BIN", "Temp", "AppData\\Local\\Temp"]
EXCLUDED_EXTENSIONS = [".tmp", ".bak"]
EXCLUDED_PREFIXES = ["~$", "~WRD", "~WRL"]

event_log = []  # List to store all event logs
serial_no = 1  # Counter for serial number
tracked_items = {}  # Dictionary to track file/folder paths

class FolderFileMonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        if should_ignore(event.src_path):
            return  
        is_directory = os.path.isdir(event.src_path) or not os.path.splitext(event.src_path)[1]
        action = "Folder Created" if is_directory else "File Created"
        log_event(action, event.src_path, is_directory)

    def on_deleted(self, event):
        if should_ignore(event.src_path):
            return  
        is_directory = os.path.isdir(event.src_path) or not os.path.splitext(event.src_path)[1]
        action = "Folder Deleted" if is_directory else "File Deleted"
        log_event(action, event.src_path, is_directory)
        tracked_items.pop(event.src_path, None)  

    def on_modified(self, event):
        if should_ignore(event.src_path) or event.src_path == os.path.abspath(LOG_FILE):
            return  
        is_directory = os.path.isdir(event.src_path) or not os.path.splitext(event.src_path)[1]
        action = "Folder Modified" if is_directory else "File Modified"
        log_event(action, event.src_path, is_directory)

    def on_moved(self, event):
        if should_ignore(event.src_path) or should_ignore(event.dest_path):
            return  
        is_directory = os.path.isdir(event.dest_path) or not os.path.splitext(event.dest_path)[1]
        if is_directory:
            action = "Folder Renamed" if os.path.dirname(event.src_path) == os.path.dirname(event.dest_path) else "Folder Moved"
            tracked_items.pop(event.src_path, None)  
            tracked_items[event.dest_path] = True  
        else:
            action = "File Renamed" if os.path.dirname(event.src_path) == os.path.dirname(event.dest_path) else "File Moved"
        log_event(action, f"{event.src_path} → {event.dest_path}", is_directory)


def should_ignore(path):
    """Ignore temp files, system folders, and Recycle Bin."""
    if any(folder in path for folder in EXCLUDED_FOLDERS):  # Ignore system folders
        return True

    item_name = os.path.basename(path)

    if any(path.endswith(ext) for ext in EXCLUDED_EXTENSIONS):  # Ignore temp file extensions
        return True

    if any(item_name.startswith(prefix) for prefix in EXCLUDED_PREFIXES):  # Ignore temp prefixes
        return True

    return False


def log_event(action, path, is_directory):
    """Log file and folder operations in a structured table format."""
    global serial_no
    item_name = os.path.basename(path)
    log_entry = [serial_no, item_name, "Folder" if is_directory else "File", action, path, datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')]

    event_log.append(log_entry)
    serial_no += 1  

    print("\n" + tabulate(event_log, headers=["S.No", "File/Folder", "Type", "Action", "Path", "Date"], tablefmt="grid"))

    with open(LOG_FILE, "w", encoding="utf-8") as log_file:
        log_file.write(tabulate(event_log, headers=["S.No", "File/Folder", "Type", "Action", "Path", "Date"], tablefmt="plain"))


def monitor_directory(directory):
    """Monitor file and folder operations in the given directory."""
    if not os.path.exists(directory):
        print(f"Error: Directory {directory} does not exist.")
        sys.exit(1)
    
    event_handler = FolderFileMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    print(f"Monitoring directory: {directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_directory(MONITORED_DIR)
