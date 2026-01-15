import re 

pattern = re.compile(r"(?:\w)+[- ]?(?:woman|man)+")

content = input("Enter Your Text: ")

super_heros = pattern.findall(content)

for super_hero in super_heros:
    print(super_hero)