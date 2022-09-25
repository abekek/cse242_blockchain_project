import os
import sys

from MerkleTree import MerkleTree
from Block import Block

txt_files = []
files = []

print("Choose an option:")
print("1. Input file names")
print("2. Input folder name (all files in folder will be used)")

user_input = input("Enter 1 or 2: ")

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
elif user_input == "2":
    # prompt user for folder name
    folder_name = input('Enter folder name: ')
    files = os.listdir(os.getcwd() + '/' + folder_name)
    files_inputed = files
else:
    sys.exit(0)

# get all files with .txt extension
txt_files = [file for file in files if file.endswith('.txt')]

blocks = []

for fa in txt_files:
    if fa in files_inputed:
        # open file
        with open(fa, 'r') as f:
            # read file
            file_content = f.read()
            #if file_content is empty
            if not file_content:
                print('File is empty')
                sys.exit()
            file_content = [line.split() for line in file_content.splitlines()]
            merkle_tree = MerkleTree(file_content)
            if len(blocks) == 0:
                blocks.append(Block(0, merkle_tree))
            else:
                blocks.append(Block(blocks[-1].get_hash(), merkle_tree))
            blocks[-1].header.set_nonce()
    else:
        print(f'File {fa} was not found')  

for block in blocks:
    block.print(True)