import re

pattern = re.compile(r"<[a-zA-Z0-9]+>")

with open("rough_data.txt", 'r') as file_object:
    content = file_object.read()
    tags = pattern.findall(content)

for tag in set(tags):
    print(tag)