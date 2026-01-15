import random
import string

def random_char(y):
    #return ''.join(random.choice(string.ascii_letters) for x in range(y))
     password_characters = string.ascii_letters + string.digits + string.punctuation
     return ''.join(random.choice(password_characters) for i in range(y))


name = input("Enter Your Message: ")
print("Your Original Message: ", name)
codeName = name.split(" ")
coOrDe = input("Code Or Decode: ")

if coOrDe == 'c':
    codeList = []
    for word in codeName:
        newString = word[:-len(word):-1] + random_char(3) + word[0]
        newString = random_char(3) + newString
        codeList.append(newString)
    print(" ".join(codeList))
elif coOrDe == 'd':
    codeList = []
    for word in codeName:
        deName = word[3:]
        deName = deName[-1] + deName[0:-1]
        deName = deName[:-3]
        deName = deName[0] + deName[:-len(deName):-1]
        codeList.append(deName)
    print(" ".join(codeList))

