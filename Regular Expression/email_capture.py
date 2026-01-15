import re

pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

with open("rough_data.txt", 'r') as file_object:
    content = file_object.read()
    emails = pattern.findall(content)

for email in emails:
    print(email)

print("Total Email: ", len(emails))