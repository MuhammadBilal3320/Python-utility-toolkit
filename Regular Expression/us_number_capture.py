import re

pattern = re.compile(r"(?:\+1[- ]?)?\d{3}[- ]\d{3}[- ]\d{4}")

with open('rough_data.txt', 'r') as file_object:
    content = file_object.read()
    numbers = pattern.findall(content)

for number in numbers:
    print(number)