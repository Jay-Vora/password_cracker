#imports
from itertools import product
import hashlib 
import csv
import os
import base64


#CONSTANTS
#CONSTANTS OR ALLOWED CHARS
SMALL = 'abcdefghijklmnopqrstuvwxyz'
CAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGITS = '1234567890'
SPECIAL_CHARS = '!@#$%^&*()_+'

# CHARACTER SET
CHAR_SET = SMALL + CAPS + DIGITS + SPECIAL_CHARS

# DEFINE THE MAX LENGTH OF THE PASSWORD
MAX_LEN = 2

# ADDED THE SALTING LAYER FOR MORE SECURE SYSTEM
def salting(password):

    salt = os.urandom(16)
    salted_encoding = base64.b64encode(salt)
    salted_decoding = salted_encoding.decode('utf-8')
    password += salted_decoding
    
    return password

#all possible permutations
def perms_and_hashes(hash_function):
    #store all the possible perms in a dict 
    perms_dict = {}

    for i in range(1, MAX_LEN+1):
        perm_iter = product(CHAR_SET, repeat=i)

        for perm in perm_iter:

            password = ''.join(perm)
            pass_salting = salting(password)
            wrd_hash = hash_function()
            wrd_hash.update(pass_salting.encode('iso-8859-1'))
            wrd_hash_hex = wrd_hash.hexdigest()
            perms_dict[wrd_hash_hex] = (password, pass_salting)
    
    return perms_dict

# Using a dictionary instead of a switch function to get rid of if-elif statements

hash_dict = {
    'md5': hashlib.md5,
    '1': hashlib.md5,
    'sha1': hashlib.sha1,
    '2': hashlib.sha1,
    'sha224': hashlib.sha224,
    '3': hashlib.sha224,
    'sha256': hashlib.sha256,
    '4': hashlib.sha256,
    'sha384': hashlib.sha384,
    '5': hashlib.sha384,
    'sha512': hashlib.sha512,
    '6': hashlib.sha512
}       

def save_to_csv(rainbow_table, output_csv):

    if rainbow_table != None:
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Hash', 'Input']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key, value in rainbow_table.items():
                writer.writerow({'Hash':key, 'Input':value})

    else:
        output_csv = None
               
    return output_csv

#read the csv file containing the rainbow table
def read_csv(file_path):

    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader) # skip the header file
            my_dict = {}
            for row in reader:
                if len(row) == 2:  # Check if the row contains exactly two values
                    hash_value = row[0]
                    tuple_str = row[1]
                    try:
                        original_password, salted_password = eval(tuple_str)  # Convert the tuple string to a tuple
                        my_dict[hash_value] = (original_password, salted_password)
                    except Exception as e:
                        print(f"Error parsing tuple in row: {row}: {e}")
                else:
                    print(f"Ignoring row: {row}: Invalid structure (expected 2 values)")
        return my_dict
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

#target_hash = 'df7f95cac5274f809efc754d9b748637'

def search(target_hash, rainbow_table):

    if rainbow_table != None and target_hash != None:
        for key, value in rainbow_table.items():
            if target_hash == key:
                print(f"the pwd has been cracked! and password is {value[0]}\n")
                break
        else:
            print("password was not found for this hash!\n")
    else:
        return 0
    return 0

def main():
    #print(salting())
    while True:
        hash_algo = input('''Please input the hash name or associated number that you would like to use for cracking:
                        1) md5
                        2) sha1
                        3) sha224
                        4) sha256
                        5) sha384
                        6) sha512\n''').lower()
        
        hash_function = hash_dict.get(hash_algo)

        if hash_function is None:
            print("Invalid algorithm. Please choose a valid one.")
        else:
            rainbow_dict = perms_and_hashes(hash_function)
            save_to_csv(rainbow_dict, 'output.csv')
            target_hash = input("Please input a hash you want to look up in our rainbow table\n")
            my_dictionary = read_csv('output.csv')
            search(target_hash, my_dictionary)

        continue_choice = input("Do you want to continue? Type 'exit' to quit or press Enter to continue: ").strip().lower()
        if continue_choice == 'exit':
            print("Exiting the program.")
            break


if __name__ == '__main__':
    main()     