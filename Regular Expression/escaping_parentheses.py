import re

pattern = re.compile(r"(03[- ]?\d{2})[- ]?(\d{7})")

with open("rough_data.txt", 'r') as file_object:
    content = file_object.read()
    phone_numbers = pattern.findall(content)

for phone_number in phone_numbers:
    print("\nFirst Group: ", phone_number[0])
    print("Second Group: ", phone_number[1])
    print("Full Number: ", phone_number[0] + phone_number[1], "\n")

print("Total Numbers: ", len(phone_numbers))
