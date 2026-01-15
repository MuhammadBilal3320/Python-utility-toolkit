import re

pattern = re.compile(r"^[a-zA-Z]+\w*[a-zA-Z0-9]$")

user_name = input("Enter User Name: ")

if pattern.match(user_name):
    print(f"{user_name} is valid User Name!")
else:
    print(f"{user_name} is Invalid User Name!")
