import re

pattern = re.compile(r"\b\w*at\w*\b", re.IGNORECASE)

with open("rough_data.txt", 'r') as file_object:
    content = file_object.read()
    matches = pattern.findall(content)
    
for match in matches:
    print(match)