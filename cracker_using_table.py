#imports
from itertools import product
import hashlib 
import csv


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

#all possible permutations
def perms_and_hashes(hash_function):
    #store all the possible perms in a dict 
    perms_dict = {}

    for i in range(1, MAX_LEN+1):
        perm_iter = product(CHAR_SET, repeat=i)

        for perm in perm_iter:

            password = ''.join(perm)
            wrd_hash = hash_function()
            wrd_hash.update(password.encode('iso-8859-1'))
            wrd_hash_hex = wrd_hash.hexdigest()
            perms_dict[password] = wrd_hash_hex
    
    return perms_dict

#determining which algorithm is being used
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
            fieldnames = ['Input', 'Hash']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key, value in rainbow_table.items():
                writer.writerow({'Input':key, 'Hash':value})

    else:
        output_csv = None
               
    return output_csv

#read the csv file containing the rainbow table
def read_csv(file_path):

    if file_path != None:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            my_dict = {}

            for row in reader:
                my_dict[row[0]] = row[1]
        file.close()
    else:
        my_dict = None

    return my_dict

#target_hash = 'df7f95cac5274f809efc754d9b748637'

def search(target_hash, rainbow_table):

    if rainbow_table != None and target_hash != None:
        for key, value in rainbow_table.items():
            if target_hash == value:
                print(f"the pwd has been cracked! and password is {key}!!\n")
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