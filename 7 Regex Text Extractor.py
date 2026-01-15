import re
import os

def extract_from_file(file_name, output_file):
    extracted_data = {"Emails": [], "Phone Numbers": [], "Links": []}
    
    if os.path.isfile(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
        
        extracted_data["Emails"].extend(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content))
        extracted_data["Phone Numbers"].extend(re.findall(r'\b\d{10}\b|\(\d{3}\) \d{3}-\d{4}|\d{3}-\d{3}-\d{4}\b', content))
        extracted_data["Links"].extend(re.findall(r'https?://[\w.-]+(?:\.[\w.-]+)+[/\w._%+-]*', content))
    
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for category, items in extracted_data.items():
            out_file.write(f"{category}:\n")
            for item in set(items):  # Remove duplicates
                out_file.write(f" - {item}\n")
            out_file.write("\n")

# Example usage
file_name = input("Enter the file name: ")  # User input for file name
output_file = 'extracted_output.txt'  # Output file to save results
extract_from_file(file_name, output_file)

print(f"Extracted data saved in {output_file}")
