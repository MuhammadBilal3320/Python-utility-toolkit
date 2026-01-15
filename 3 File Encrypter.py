import os
import shutil

# Function to determine the category of a file based on its extension
def get_category(file_name):
    """Extracts the file extension and returns it as an uppercase category name."""
    _, ext = os.path.splitext(file_name)  # Split file name and extension
    return ext[1:].upper() if ext else "OTHERS"  # Convert extension to uppercase, default to 'OTHERS'

# Function to organize files into folders based on their extensions
def organize_files(directory):
    """Organizes files in the specified directory by moving them into categorized folders."""
    if not os.path.exists(directory):  # Check if the directory exists
        print("Directory does not exist.")  # Print error message if directory is missing
        return  # Exit function if directory does not exist
    
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]  # Get all files in the directory
    
    for file in files:
        category = get_category(file)  # Determine category based on file extension
        category_path = os.path.join(directory, category)  # Define folder path for the category
        
        if not os.path.exists(category_path):  # Check if category folder exists
            os.makedirs(category_path)  # Create folder if it does not exist
        
        src_path = os.path.join(directory, file)  # Get source file path
        dest_path = os.path.join(category_path, file)  # Define destination path
        
        # Handle duplicate filenames by appending a counter
        counter = 1
        while os.path.exists(dest_path):  # Check if file with the same name already exists in the destination folder
            name, ext = os.path.splitext(file)  # Split file name and extension
            new_file_name = f"{name}_{counter}{ext}"  # Append counter to filename
            dest_path = os.path.join(category_path, new_file_name)  # Update destination path
            counter += 1  # Increment counter
        
        shutil.move(src_path, dest_path)  # Move the file to the categorized folder
        print(f"Moved: {file} -> {category}/")  # Print confirmation message

# Main execution block
if __name__ == "__main__":
    target_directory = os.getcwd()  # Use the current working directory as the target folder
    organize_files(target_directory)  # Call the function to organize files
