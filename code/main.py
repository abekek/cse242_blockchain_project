import os
import sys
import zipfile
import glob
import random
import string

from MerkleTree import MerkleTree
from Block import Block
from Validation import Validate

txt_files = []
files = []
blocks = []
filenames = []

files = glob.glob('/output/*')
for f in files:
    os.remove(f)

def handle_filecontent(file_content):
    if not file_content:
        print('File is empty')
        sys.exit()
    file_content = [line.split() for line in file_content.splitlines()]
    merkle_tree = MerkleTree(file_content)
    if len(blocks) == 0:
        block = Block(0, merkle_tree)
        block.header.set_nonce()
        block.hash_header = block.header.hash()
        blocks.append(block)
    else:
        block = Block(blocks[-1].hash_header, merkle_tree)
        block.header.set_nonce()
        block.hash_header = block.header.hash()
        blocks.append(block)

print("Choose an option:")
print("1. Input file names")
print("2. Input folder name (all files in folder will be used)")
print("3. Zip file")

user_input = input("Enter 1, 2 or 3: ")

if user_input == "1":
    # get all files in root directory
    files = os.listdir(os.getcwd())

    # Switch current directory to /code/ in the case that text files are in that directory (that's how we tested)
    os.chdir(os.getcwd() + '/code')

    # now search in the /code/ directory
    files.extend(os.listdir(os.getcwd()))

    # prompt user for file name
    file_name = input('Enter file names separated by space (example: file1.txt file2.txt): ')
    files_inputed = file_name.split(' ')
    # get all files with .txt extension
    txt_files = [file for file in files if file.endswith('.txt')]
elif user_input == "2":
    # prompt user for folder name
    folder_name = input('Enter folder name: ')
    try:
        os.chdir(os.getcwd() + '/' + folder_name)
    except:
        print('Error: Folder does not exist')
        sys.exit()
    # os.chdir(os.getcwd() + '/' + folder_name)
    files = os.listdir(os.getcwd())
    files_inputed = files
    # get all files with .txt extension
    txt_files = [file for file in files if file.endswith('.txt')]
elif user_input == "3":
    # handle zip file
    zipfile_name = input("Enter Zip file name (example: file.zip): ")
    file = zipfile.ZipFile(zipfile_name, "r")
    for name in file.namelist():
        if(name.endswith(".txt")):
            data = file.read(name)
            handle_filecontent(data.decode('utf-8'))
            filenames.append(name)
else:
    sys.exit(0)

for fa in txt_files:
    if fa in files_inputed:
        # open file
        with open(fa, 'r') as f:
            # read file
            file_content = f.read()
            #if file_content is empty
            handle_filecontent(file_content)
            # append file name
            filenames.append(fa)
    else:
        print(f'File {fa} was not found')

# Change back to parent 
os.chdir(os.getcwd())

for i in range(len(blocks)):
    # write to file 
    with open(f'output/{filenames[i][:-4]}.block.out', 'w') as f:
        f.write(blocks[i].print(True))

# validation of the blockchain
num_bad_entities = 100
validation = Validate(blocks, num_bad_entities)

existing_address = "de0acd701ed59eb60ccbf38de33a2f5f91e6cde0"
print(f"Validating existing address = {existing_address} ...")
val_res = validation.balance(existing_address)
print(f"Exists = {val_res[1]}, balance of existing address = {val_res[0]} ")
print("Validation complete\n")

random_address = ''.join(random.choices(string.hexdigits, k=40)).lower()
print(f"Validating random address = {random_address} ...")
val_res = validation.balance(random_address)
print(f"Exists = {val_res[1]}, balance of random address = {val_res[0]} ")
print("Validation complete\n")

print("Validating initially created blockchain...")
print('Initially created blockchain is valid? ' + str(validation.validate_blockchain(blocks)))
print("Validation complete\n")

print("Validating generated bad blockchain...")
bad_blocks = validation.bad_blocks
print('Generated bad blockchain is valid? ' + str(validation.validate_blockchain(bad_blocks)))
print("Validation complete\n")
