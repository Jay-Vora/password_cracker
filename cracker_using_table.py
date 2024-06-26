#imports
from itertools import product
import hashlib 
import csv
import os
import base64
import argon2
from concurrent.futures import ThreadPoolExecutor, as_completed

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


#helper function for standard hash functions
def compute_standard_hash(password, hash_function):
    pass_salting = salting(password)
    wrd_hash = hash_function()
    wrd_hash.update(pass_salting.encode('iso-8859-1'))
    wrd_hash_hex = wrd_hash.hexdigest()
    return wrd_hash_hex, password, pass_salting


#all possible permutations and their hashes with standardized algorithms using parallel processing 
def perms_and_hashes(hash_function):
    perms_dict = {}
    passwords = []

    for i in range(1, MAX_LEN + 1):
        perm_iter = product(CHAR_SET, repeat=i)
        for perm in perm_iter:
            passwords.append(''.join(perm))

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(compute_standard_hash, password, hash_function): password for password in passwords}
        for future in as_completed(futures):
            try:
                wrd_hash_hex, password, pass_salting = future.result()
                perms_dict[wrd_hash_hex] = (password, pass_salting)
            except Exception as e:
                print(f"An error occurred: {e}")

    return perms_dict

#get the parameters and their values for KDF and store them into a dictionary
def parameters_for_kdf(options):
    options = [option.strip() for option in options]

    parameter_values = {}
    for option in options:
        if option in ["time_cost", "memory_cost", "parallelism"]:
            value = input(f"Enter the value for {option}: ")
            parameter_values[option] = value
        elif option == "hash_len":
            value = input(f"Enter the value for {option} (or leave blank for default 32): ")
            if value == "":
                parameter_values[option] = 32
            elif int(value) == 32:
                parameter_values[option] = int(value)
            else:
                print("Invalid value for hash_len. Must be 32 or blank.")
                return None, None
        elif option == "salt_len":
            value = input(f"Enter the value for {option} (or leave blank for default 16): ")
            if value == "":
                parameter_values[option] = 16
            elif int(value) == 16:
                parameter_values[option] = int(value)
            else:
                print("Invalid value for salt_len. Must be 16 or blank.")
                return None, None

    argon2_hasher = argon2.PasswordHasher(
    time_cost=int(parameter_values.get("time_cost", 3)),
    memory_cost=int(parameter_values.get("memory_cost", 65536)),
    parallelism=int(parameter_values.get("parallelism", 4)),
    hash_len=int(parameter_values.get("hash_len", 32)),
    salt_len=int(parameter_values.get("salt_len", 16))
    )
    return parameter_values, argon2_hasher

#helper function for KDF
def compute_kdf_hash(password, kdf_instance):
    pass_salting = salting(password)
    encoded_hash = kdf_instance.hash(password.encode(), salt=pass_salting.encode())
    hash_value = encoded_hash.split('$')[-1]
    return hash_value, password, pass_salting

#function for KDF
def generate_password_hashes_with_kdf(kdf_instance):
    perms_dict = {}
    passwords = []

    for i in range(1, MAX_LEN + 1):
        perm_iter = product(CHAR_SET, repeat=i)
        for perm in perm_iter:
            passwords.append(''.join(perm))

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(compute_kdf_hash, password, kdf_instance): password for password in passwords}
        for future in as_completed(futures):
            try:
                hash_value, password, pass_salting = future.result()
                perms_dict[hash_value] = (password, pass_salting)
            except Exception as e:
                print(f"An error occurred: {e}")

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
    '6': hashlib.sha512,
    '7': argon2.PasswordHasher,
    'kdf':argon2.PasswordHasher
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
    
    while True:
        hash_algo = input('''Please input the hash name or associated number that you would like to use for cracking:
                        1) md5
                        2) sha1
                        3) sha224
                        4) sha256
                        5) sha384
                        6) sha512
                        7) kdf \n''').lower()
        
        hash_function = hash_dict.get(hash_algo)

        if hash_function is None:
            print("Invalid algorithm. Please choose a valid one.")
        else:
            if hash_algo == 'kdf' or hash_algo == '7':
                ask_for_params = input('''Please input the parameters initials you'd like to use for your KDF and separated by commas:
                                    1) time_cost
                                    2) memory_cost
                                    3) parallelism
                                    4) hash_len
                                    5) salt_len \n''').lower().split(',')
                parameters, argon2_hasher = parameters_for_kdf(ask_for_params)
                if argon2_hasher is None:
                    continue
                rainbow_dict = generate_password_hashes_with_kdf(argon2_hasher)

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