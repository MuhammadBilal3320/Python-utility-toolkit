import re

pattern = re.compile(r"(?:https?\:\/\/)?(?:www\.)?[\w\-]+\.[\w\-]+[\/\w\-\.\?\=\&]*")

with open("rough_data.txt", 'r') as file_object:
    content = file_object.read()
    urls = pattern.findall(content)
    
for url in urls:
    print(url)
    
print("Total URLs: ", len(urls))