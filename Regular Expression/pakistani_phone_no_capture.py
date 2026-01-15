import re

with open('rough_data.txt', encoding='utf-8') as file_object:
    text = file_object.read()
    

pattern = r"(?:\+92[- ]?|0)(?:\d{2,3})[- ]?\d{6,7}" 
# Explanation:
# (?:\+92[- ]?|0)   → Matches either '+92' (with optional dash or space) or '0' at the start
#                     Examples: '+92 ', '+92-', '0'
#
# (?:\d{2,3})       → Matches 2 or 3 digits (the area code or mobile prefix)
#                     Examples: '41', '333', '345'
#
# [- ]?             → Optionally matches a dash '-' or space ' '
#                     Examples: '-', ' ' (space), or nothing
#
# \d{6,7}           → Matches 6 or 7 digits (the main part of the phone number)
#                     Examples: '7654321', '1234567'
#
# Combined effect:
# Matches both mobile numbers (like '0301-2345678', '+92 333 2109876')
# and landline numbers (like '051-7654321', '+92-41-9988776')

numbers = re.findall(pattern, text)

print("Phone Numbers Found: ")
for num in numbers:
    print(num)
print("Total Phone Numbers: ", len(numbers))