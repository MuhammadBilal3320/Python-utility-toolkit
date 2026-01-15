import os
import sys
import concurrent.futures  # For multiprocessing
from multiprocessing import cpu_count  

# Function to get the size of a folder
def get_folder_size(folder):
    total_size = 0
    try:
        with os.scandir(folder) as entries:
            for entry in entries:
                try:
                    if entry.is_file(follow_symlinks=False):  
                        total_size += entry.stat().st_size  
                    elif entry.is_dir(follow_symlinks=False):  
                        total_size += get_folder_size(entry.path)  
                except (PermissionError, FileNotFoundError):  
                    continue  
    except (PermissionError, FileNotFoundError):  
        return 0  
    return total_size

# Function to format size in MB or GB
def format_size(size):
    return f"{size / (1024 * 1024 * 1024):.2f} GB" if size >= 1024**3 else f"{size / (1024 * 1024):.2f} MB"

# Function to analyze all folders in the current directory
def analyze_folders():
    current_directory = os.getcwd()  # Get current directory
    folder_sizes = []
    folders = [f for f in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, f))]

    if not folders:
        print("No folders found in the directory.")
        return

    print("\nAnalyzing folders...\n")

    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        results = {executor.submit(get_folder_size, os.path.join(current_directory, folder)): folder for folder in folders}
        
        with open("folder_sizes.txt", "w") as f:
            f.write("Folder Size Report\n")
            f.write("====================================================\n")
            f.write("|  No  |        Folder Name             |   Size   |\n")
            f.write("====================================================\n")

            for index, future in enumerate(concurrent.futures.as_completed(results), start=1):
                folder = results[future]
                size = future.result()
                folder_sizes.append((index, folder, size))

                # Progress bar
                progress = index / len(folders)
                bar_length = 40
                block = int(bar_length * progress)
                progress_bar = "█" * block + "-" * (bar_length - block)
                sys.stdout.write(f"\r[{progress_bar}] {progress * 100:.2f}% Completed")
                sys.stdout.flush()

                # Write folder size to the file
                formatted_size = format_size(size)
                report_line = f"| {index:<4} | {folder:<30} | {formatted_size:<8} |"
                print(report_line)
                f.write(report_line + "\n")

            total_size = sum(size for _, _, size in folder_sizes)
            total_size_formatted = format_size(total_size)
            total_line = f"| TOTAL | {'-'*30} | {total_size_formatted:<8} |"
            print(total_line)
            f.write(total_line + "\n")

    print("\nFolder sizes have been stored in 'folder_sizes.txt'")
    print(f"Total size of all folders: {total_size_formatted}")

if __name__ == "__main__":
    analyze_folders()
