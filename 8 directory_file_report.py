# Import the os module to interact with the operating system (for working with files, folders, and paths)
import os

# Function to recursively write the directory structure into a text file
def write_directory_structure(path, file, prefix=""):
    try:
        # Get all items (files and folders) inside the given directory
        items = os.listdir(path)
    except PermissionError:
        # If access to a folder is denied (due to permissions), write a message and skip it
        file.write(f"{prefix}└── [Access Denied: {os.path.basename(path)}]\n")
        return  # Exit the function for this folder

    # Sort all items alphabetically to keep the report neat
    items.sort()
    # Get the total number of items in this folder
    total_items = len(items)

    # Loop through each item with its index (to check if it’s the last one)
    for index, item in enumerate(items):
        # Create the full path of the current item
        item_path = os.path.join(path, item)
        # Check if this is the last item in the folder
        is_last = index == total_items - 1
        # Choose the proper symbol depending on position (for tree-like look)
        connector = "└── " if is_last else "├─ "
        # Determine if the item is a directory or a file
        item_type = "Directory" if os.path.isdir(item_path) else "File"

        # Write the item name and type to the file with proper indentation
        file.write(f"{prefix}{connector}{item} — Type: {item_type}\n")

        # If the current item is a directory, explore it further (recursion)
        if os.path.isdir(item_path):
            # Update the prefix for nested levels (adds visual structure)
            new_prefix = prefix + ("    " if is_last else "│   ")
            # Recursively call the function for the subdirectory
            write_directory_structure(item_path, file, new_prefix)

            # After finishing the directory, mark it as finished in the report
            file.write(f"{prefix}│   └────── [Finished: {item}]\n")
            # Add an empty visual line after finishing one directory
            file.write(f"{prefix}│   \n")

# Function to create the directory report file and start the recursive process
def generate_report(root_path, output_file="directory_report.txt"):
    # Check if the given directory path exists
    if not os.path.exists(root_path):
        # Print an error if the directory does not exist and exit
        print("Directory not found. Please enter a valid path.")
        return

    # Open the output text file for writing (UTF-8 encoding to support special characters)
    with open(output_file, "w", encoding="utf-8") as f:
        # Write the top-level directory name to the report
        f.write(f"├─ {os.path.basename(root_path)} — Type: Directory\n")
        # Start writing the directory structure recursively
        write_directory_structure(root_path, f)
        # After finishing, add a final “Finished” marker for the root directory
        f.write(f"│   └────── [Finished: {os.path.basename(root_path)}]\n")

    # Print a confirmation message showing where the report was saved
    print(f"Directory report saved to: {output_file}")


# Run this part only when the script is executed directly (not imported as a module)
if __name__ == "__main__":
    # Ask the user to enter a folder path
    folder_path = input("Enter directory path: ").strip()
    # Generate the directory structure report
    generate_report(folder_path)
