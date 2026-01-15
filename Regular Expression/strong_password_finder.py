import re

print("***** Password Checker *****")
print("Checking Password is Strong or Not!")

user_password = input("Enter Your Password: ")

pattern = re.compile(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+-=\|;':,./<>?]).{8,}$")

if pattern.search(user_password):
    print("Strong Password!")
else:
    print("Weak Password!")