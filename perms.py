from itertools import product
from hashlib import md5
import os

# ALLOWED CHARACTERS
SMALL = 'abcdefghijklmnopqrstuvwxyz'
CAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGITS = '1234567890'
SPECIAL_CHARS = '!@#$%^&*()_+'

# CHARACTER SET
CHAR_SET = SMALL + CAPS + DIGITS + SPECIAL_CHARS

# DEFINE THE MAX LENGTH OF THE PASSWORD
MAX_LEN = 8

# GET USER INPUT
mode = input("Choose method (1 for brute force, 2 for word list): ")
word_list_filename = None
if mode == '2':
    word_list_filename = input("Enter the word list filename: ")

# READ WORD LIST (if selected)
word_list = []
if mode == '2' and word_list_filename:
    if os.path.isfile(word_list_filename):
        try:
            with open(word_list_filename, 'r', encoding='utf-8') as file:
                word_list = [line.strip() for line in file]
        except UnicodeDecodeError:
            try:
                with open(word_list_filename, 'r', encoding='iso-8859-1') as file:
                    word_list = [line.strip() for line in file]
            except UnicodeDecodeError:
                print(f"Could not decode file {word_list_filename} with UTF-8 or ISO-8859-1 encoding.")
                exit(1)
    else:
        print(f"File {word_list_filename} does not exist in the current directory.")
        exit(1)

# GENERATE PASSWORDS FOR BRUTE FORCE
list_wrds = []
if mode == '1':
    for i in range(1, MAX_LEN + 1):
        perm_iter = product(CHAR_SET, repeat=i)
        for perm in perm_iter:
            password = ''.join(perm)
            list_wrds.append(password)

# COMBINE WORD LISTS AND BRUTE FORCE PASSWORDS
passwords_to_check = list_wrds if mode == '1' else word_list

# DEFINE THE TARGET HASH
target_hash = '2bdb742fc3d075ec6b73ea414f27819a'

# CHECK PASSWORDS AGAINST TARGET HASH
for wrd in passwords_to_check:
    wrd_hash = md5()
    wrd_hash.update(wrd.encode('utf-8'))
    wrd_hash_hex = wrd_hash.hexdigest()

    if wrd_hash_hex == target_hash:
        print("Cracked password:", wrd)
        break
else:
    print("Password not found within the given length limit")

