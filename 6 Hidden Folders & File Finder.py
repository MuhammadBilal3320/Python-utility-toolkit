#!/usr/bin/env python3
import os
import sys
import time

def is_hidden(filepath):
    """Check if a file or folder is hidden."""
    if sys.platform == "win32":
        import ctypes
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(filepath))
        return bool(attrs & 2)  # FILE_ATTRIBUTE_HIDDEN (2)
    else:
        return os.path.basename(filepath).startswith('.')

def find_hidden_items(directory):
    """Recursively find hidden files and folders with a progress percentage."""
    hidden_items = []
    total_items = sum(len(dirs) + len(files) for _, dirs, files in os.walk(directory))
    processed = 0
    bar_length = 30  # Length of the progress bar

    print("\nProcessing... Please wait.\n")

    for root, dirs, files in os.walk(directory):
        for item in dirs + files:  # Check both folders and files
            processed += 1
            full_path = os.path.join(root, item)

            # Calculate progress percentage
            percentage = (processed / total_items) * 100
            filled_blocks = int((processed / total_items) * bar_length)
            progress_bar = "█" * filled_blocks + "-" * (bar_length - filled_blocks)

            # Display progress bar and percentage
            print(f"\r[{progress_bar}] {percentage:.1f}%", end="", flush=True)

            if is_hidden(full_path):
                hidden_items.append((item, full_path))

    # Ensure final 100% display
    print(f"\r[{'█' * bar_length}] 100.0%\n")
    return hidden_items

def print_table(data, execution_time):
    """Print data in a tabular format with proper alignment and save to a file."""
    file_path = "hidden_files.txt"

    if not data:
        print("\nNo hidden files or folders found.")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("No hidden files or folders found.\n")
        return

    # Determine column widths
    col_widths = [
        max(len(str(idx + 1)) for idx in range(len(data))) + 2,  # Serial Number
        max(len(row[0]) for row in data) + 2,  # Name
        max(len(row[1]) for row in data) + 2   # Path
    ]

    # Print & Save header
    header = f"{'S.No'.ljust(col_widths[0])} {'Name'.ljust(col_widths[1])} {'Path'.ljust(col_widths[2])}"
    separator = "-" * (sum(col_widths) + 4)

    print("\n" + header)
    print(separator)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(header + "\n")
        file.write(separator + "\n")

        # Print & Save rows
        for idx, (name, path) in enumerate(data, start=1):
            row = f"{str(idx).ljust(col_widths[0])} {name.ljust(col_widths[1])} {path.ljust(col_widths[2])}"
            print(row)
            file.write(row + "\n")

    print(f"\nExecution Time: {execution_time:.2f} seconds")
    print(f"Results saved to: {file_path}")

# Use current directory as target
target_directory = "."

print(f"\nScanning for hidden files & folders in: {os.path.abspath(target_directory)}")

start_time = time.time()
hidden_items = find_hidden_items(target_directory)
execution_time = time.time() - start_time

print_table(hidden_items, execution_time)
