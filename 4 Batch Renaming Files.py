import os
import re

def batch_rename(directory, pattern, replacement, extension, add_prefix, add_suffix, numbering):
    """Renames files in the specified directory based on user-defined criteria."""
    
    try:
        files = [f for f in os.listdir(directory) if f.endswith(extension) or extension == "all"]
        count = 1

        for filename in files:
            new_name = re.sub(pattern, replacement, filename) if pattern else filename

            # Adding prefix and suffix
            name, ext = os.path.splitext(new_name)
            new_name = f"{add_prefix}{name}{add_suffix}{ext}"

            # Adding numbering if enabled
            if numbering:
                new_name = f"{count}_{new_name}"
                count += 1

            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)

            if filename != new_name:  # Avoid renaming unchanged files
                os.rename(old_path, new_path)
                print(f'Renamed: {filename} -> {new_name}')
            else:
                print(f'Skipped: {filename}')
    
    except Exception as e:
        print(f'Error: {e}')

# Interactive User Input
directory_path = input("Enter the directory path: ").strip()
pattern = input("Enter the text/regex pattern to replace (leave empty for no changes): ").strip()
replacement = input("Enter the replacement text: ").strip()
extension = input("Enter file extension to filter (e.g., .txt, .jpg) or type 'all' for all files: ").strip()
add_prefix = input("Enter a prefix to add (leave empty for none): ").strip()
add_suffix = input("Enter a suffix to add (leave empty for none): ").strip()
numbering = input("Do you want to number files sequentially? (yes/no): ").strip().lower() == "yes"

# Call the function
batch_rename(directory_path, pattern, replacement, extension, add_prefix, add_suffix, numbering)
