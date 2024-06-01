#imports
from itertools import product
import hashlib 
import csv

#CONSTANTS OR ALLOWED CHARS
SMALL = 'abcdefghijklmnopqrstuvwxyz'
CAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGITS = '1234567890'
SPECIAL_CHARS = '!@#$%^&*()_+'

# CHARACTER SET
CHAR_SET = SMALL + CAPS + DIGITS + SPECIAL_CHARS

# DEFINE THE MAX LENGTH OF THE PASSWORD
MAX_LEN = 3


#make it complatible with the rest of hashlib algos

#read the file
def read_store(file_path):

    wrd_list = []
    with open(file_path, 'r', encoding='iso-8859-1') as file:
        wrd_list = [line.strip() for line in file]


    return wrd_list

#all possible permutations
def perms():
    #store all the possible perms in the list 
    perms_list = []

    for i in range(1, MAX_LEN+1):
        perm_iter = product(CHAR_SET, repeat=i)

        for perm in perm_iter:
            password = ''.join(perm)
            perms_list.append(password)

    return perms_list

#determining which algorithm is being used
def switch(hash_name):

    if hash_name == 'md5' or hash_name == '1':
        result = 1
    elif hash_name == 'sha1' or hash_name == '2':
        result = 2
    elif hash_name == 'sha224' or hash_name == '3':
        result = 3
    elif hash_name == 'sha256' or hash_name == '4':
        result = 4
    elif hash_name == 'sha384' or hash_name == '5':
        result = 5
    elif hash_name == 'sha512' or hash_name == '6':
        result = 6
    else:
        result = 7

    return result               

#generates hashes of all the permuted passwords
def gen_perms_hashes(perms_list, hash_name):
    rainbow_table = {}

    if hash_name == 1:

        for perm in perms_list:
            wrd_hash = hashlib.md5()
            wrd_hash.update(perm.encode('iso-8859-1'))
            wrd_hash_hex = wrd_hash.hexdigest()
            rainbow_table[perm] = wrd_hash_hex

    elif hash_name == 2:
        for perm in perms_list:
            wrd_hash = hashlib.sha1()
            wrd_hash.update(perm.encode('iso-8859-1'))
            wrd_hash_hex = wrd_hash.hexdigest()
            rainbow_table[perm] = wrd_hash_hex

    elif hash_name == 3:
        for perm in perms_list:
            wrd_hash = hashlib.sha224()
            wrd_hash.update(perm.encode('iso-8859-1'))
            wrd_hash_hex = wrd_hash.hexdigest()
            rainbow_table[perm] = wrd_hash_hex

    elif hash_name == 4:
        for perm in perms_list:
            wrd_hash = hashlib.sha256()
            wrd_hash.update(perm.encode('iso-8859-1'))
            wrd_hash_hex = wrd_hash.hexdigest()
            rainbow_table[perm] = wrd_hash_hex
    
    elif hash_name == 5:
        for perm in perms_list:
            wrd_hash = hashlib.sha384()
            wrd_hash.update(perm.encode('iso-8859-1'))
            wrd_hash_hex = wrd_hash.hexdigest()
            rainbow_table[perm] = wrd_hash_hex
    
    elif hash_name == 6:
        for perm in perms_list:
            wrd_hash = hashlib.sha512()
            wrd_hash.update(perm.encode('iso-8859-1'))
            wrd_hash_hex = wrd_hash.hexdigest()
            rainbow_table[perm] = wrd_hash_hex

    else :
        print("selected algo is not supported by this program! OR it doesn't exist!\n")


    return rainbow_table

def save_to_csv(rainbow_table, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Input', 'Hash']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in rainbow_table.items():
            writer.writerow({'Input':key, 'Hash':value})
               
    return output_csv 



def main():
    #words_list = read_store('realhuman_phill.txt')
    permuts_list = perms()
    rainbow_table = gen_perms_hashes(permuts_list)
    save_to_csv(rainbow_table, 'output.csv')
    #print(rainbow_table)



if __name__ == '__main__':
    main()