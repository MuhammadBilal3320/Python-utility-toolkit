import re

pattern = re.compile(
    r'"(.*?)"\s*(?:--|Author:)\s*(.*)',
    re.DOTALL
)

with open("rough_data.txt", 'r', encoding='utf-8') as file_object:
    content = file_object.read()

matches = pattern.findall(content)

for quote, author in matches:
    cleaned_quote = " ".join(quote.splitlines()).strip()
    print(f'Quote: "{cleaned_quote}"')
    print(f'Author: {author.strip()}')
    print()
