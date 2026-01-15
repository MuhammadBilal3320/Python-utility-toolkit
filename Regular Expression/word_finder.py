import re

user_word = input("Enter Your Word for Finding: ")

regex = r".*?"+user_word+r".*?"

pattern = re.compile(regex, re.IGNORECASE | re.DOTALL)

with open("rough_data.txt", 'r') as file_object:
    content = file_object.read()
    match_words = pattern.findall(content)
    
print(f"Found", len(match_words), "Matches for the word","\"",user_word,"\"")
