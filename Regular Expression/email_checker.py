import re

pattern = re.compile(r"^(info\.)?[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

user_email = input("Enter Your Email: ")

if re.match(pattern, user_email):
    print("Your Entered Email", user_email, "is Valid! 😊")
else:
    print("Your Entered Email", user_email, "is Invalid! 😥")