import pyzipper
import itertools
import string
from tqdm import tqdm

zip_file = "secret.zip"

characters = string.ascii_lowercase
max_length = 4

found = False

with pyzipper.AESZipFile(zip_file) as zipf:
    for length in range(1, max_length + 1):
        print(f"Trying passwords of length {length}")
        for guess in tqdm(itertools.product(characters, repeat=length)):
            password = ''.join(guess)
            try:
                zipf.extractall(pwd=bytes(password, 'utf-8'))
                print(f"[+] Password Found: {password}")
                found = True
                break
            except:
                pass
        if found:
            break

if not found:
    print("[-] Password not found.")
