import re

email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

with open("rough_data.txt", 'r') as file_object:
    content = file_object.read()

censored = re.sub(email_pattern, "*****@example.com", content)

print(censored)
