import shutil
import pathlib
import os


while True:
    source_path_input = input("\nEnter Source Folder Path eg.(D:\\AWB\\MUHAMMAD BILAL): ")

    source_folder = pathlib.Path(source_path_input)

    source_file_extension_input = input("Which File Extension You want to Copy eg.(pdf, mp4, jpg etc.): ").lower()

    extension_files = list(source_folder.glob(f"*.{source_file_extension_input}"))

    print("\n")
    print("******************************************************")
    print("******************* Preview Files Start **************")
    print("******************************************************")
    for index, file in enumerate(extension_files):
        file_name = os.path.basename(file)
        name_without_ext = os.path.splitext(file_name)[0]
        print(f"File No# {index+1}: {name_without_ext}")
    print(f"Total Files Found: {len(extension_files)}")
    print("******************************************************")
    print("******************* Preview Files End *****************")
    print("******************************************************")
    
    confirmation = input("You Confirm this Files are Correct ? (yes/no): ")
    
    if confirmation.lower() in ['yes', 'y']:
        print("=======> Thank You for your Confirmation <=======")
        break

desination_path = input("Enter Destination Path: ")

for file in extension_files:
    print(f" - copying {file.name} --> {desination_path}")
    shutil.copy(file, desination_path)

