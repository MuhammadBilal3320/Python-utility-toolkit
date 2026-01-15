import os
import time
import sys

def get_folder_size(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

def format_size(size):
    if size >= 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"
    else:
        return f"{size / (1024 * 1024):.2f} MB"

def animated_progress(progress):
    bar_length = 40
    block = int(bar_length * progress)
    progress_bar = "█" * block + "-" * (bar_length - block)
    sys.stdout.write(f"\r[{progress_bar}] {progress * 100:.2f}% Completed")
    sys.stdout.flush()

def analyze_folders(path):
    folder_sizes = []
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    total_folders = len(folders)
    total_size = 0
    
    print("\nFolder Size Analyzer")
    print("====================================================")
    print("|  No  |        Folder Name             |   Size   |")
    print("====================================================")
    
    if total_folders == 0:
        print("No folders found in the directory.")
        return
    
    print("Analyzing folders...\n")
    for index, folder in enumerate(folders, start=1):
        folder_path = os.path.join(path, folder)
        size = get_folder_size(folder_path)
        total_size += size
        folder_sizes.append((index, folder, size))
        
        progress = index / total_folders
        animated_progress(progress)
        time.sleep(0.1)  # Simulate loading
    
    print("\n")
    folder_sizes.sort(key=lambda x: x[2])
    
    with open("folder_sizes.txt", "w") as f:
        f.write("Folder Size Report\n")
        f.write("====================================================\n")
        f.write("|  No  |        Folder Name             |   Size   |\n")
        f.write("====================================================\n")
        for index, folder, size in folder_sizes:
            formatted_size = format_size(size)
            report_line = f"| {index:<4} | {folder:<30} | {formatted_size:<8} |"
            print(report_line)
            f.write(report_line + "\n")
        f.write("====================================================\n")
        total_size_formatted = format_size(total_size)
        total_line = f"| TOTAL | {'-'*30} | {total_size_formatted:<8} |"
        print(total_line)
        f.write(total_line + "\n")
    
    print("\nFolder sizes have been stored in 'folder_sizes.txt'")
    print(f"Total size of all folders: {total_size_formatted}")

if __name__ == "__main__":
    directory = os.getcwd()
    analyze_folders(directory)
