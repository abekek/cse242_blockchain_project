import os
import sys

from MerkleTree import MerkleTree

# get all files in root directory
files = os.listdir(os.getcwd())

# Switch current directory to /code/ in the case that text files are in that directory (that's how we tested)
os.chdir(os.getcwd() + '/code')

# now search in the /code/ directory
files.extend(os.listdir(os.getcwd()))

# get all files with .txt extension
txt_files = [file for file in files if file.endswith('.txt')]

# prompt user for file name
file_name = input('Enter file name: ')

if file_name in txt_files:
    # open file
    with open(file_name, 'r') as f:
        # read file
        file_content = f.read()
        #if file_content is empty
        if not file_content:
            print('File is empty')
            sys.exit()
        file_content = [line.split() for line in file_content.splitlines()]
        merkle_tree = MerkleTree(file_content)
        print(f'Merkle Tree root hash: {merkle_tree.get_root()}')


