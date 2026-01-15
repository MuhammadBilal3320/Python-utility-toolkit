import re

with open("rough_data.txt", 'r') as file_object:
    content = file_object.read()
    content = re.sub(r'\b(\w+)\1+\b', r'\1', content, flags=re.IGNORECASE) # Remove the Duplicate without Space
    content = re.sub(r'\b(\w+)(?:\s+\1\b)+', r'\1', content, flags=re.IGNORECASE) # Remove the Duplicate with Space
    print(content)
    