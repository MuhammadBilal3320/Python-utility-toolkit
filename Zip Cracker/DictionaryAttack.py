import pyzipper

# Path to your zip file and wordlist
zip_file = "secret.zip"
wordlist_file = "wordlist.txt"

found = False

# Open the ZIP file
with pyzipper.AESZipFile(zip_file) as zipf:
    # Open the password list file
    with open(wordlist_file, 'r', encoding='utf-8') as file:
        for line in file:
            password = line.strip()  # remove newlines and spaces
            try:
                zipf.extractall(pwd=bytes(password, 'utf-8'))
                print(f"[+] Password Found: {password}")
                found = True
                break
            except:
                pass  # wrong password, try next

if not found:
    print("[-] Password not found in wordlist.")
