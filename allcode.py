# https://stackoverflow.com/questions/72411835/how-to-correctly-do-a-double-sha256-hashing

from datetime import datetime
import hashlib
import random

class Block:

    def __init__(self, hash_prev, hash_root):
        self.hash_header = None
        self.header = self.Header(hash_prev, hash_root)

    def get_hash(self):
        return self.hash_header

    class Header:
        def __init__(self, hash_prev, hash_root):
            self.hash_prev = hash_prev
            self.hash_root = hash_root
            self.timestamp = datetime.now()
            self.target = 2**256 >> 1
            self.nonce = 0

        def hash(self):
            return hashlib.sha256((
                str(self.hash_prev) + 
                str(self.hash_root.get_root()) +
                str(self.timestamp) + 
                str(self.target) + 
                str(self.nonce)).encode('utf-8')).hexdigest()

        def set_nonce(self):
            curr_nonce = random.randint(0, 2**64)
            tries = 0
            while True:
                tries += 1
                if int(hashlib.sha256((hex(curr_nonce) + self.hash_root.get_root()).encode('utf-8')).hexdigest(), 16) < self.target:
                    self.nonce = curr_nonce
                    break
                else:
                    curr_nonce = random.randint(0, 2**64)
            # print(tries)

        def get_nonce(self):
            return self.nonce

    # function to print the block
    def print(self, printLedger):
        res = ""
        res+="BEGIN BLOCK\n"
        res+="BEGIN HEADER\n"
        res+= 'Hash of the previous block: {}\n'.format(self.header.hash_prev)
        res+= 'Merkle Tree root: {}\n'.format(self.header.hash_root.get_root())
        res+= 'Timestamp: {}\n'.format(self.header.timestamp)
        res+= 'Target: {}\n'.format(self.header.target)
        res+= 'Nonce: {}\n'.format(self.header.nonce)
        res+= "END HEADER\n"
        if printLedger:
            res += self.header.hash_root.print()
        res+= "END BLOCK\n\n"
        return res
    


import random
import string

# number of total blocks
num_blocks = 30

for num_block in range(num_blocks):
    data = []
    num_addresses = random.randint(50, 100)
    for row_num in range(num_addresses):
        # get string of length 40 generated randomly with from the hexadecimal alphabet
        row = ''.join(random.choices(string.hexdigits, k=40)).lower()
        balance = random.randint(0, 1000000)
        data.append((row, balance))

    # put the data into a txt file
    with open(f'code/datagen_{num_block}.txt', 'w+') as f:
        for row, balance in data:
            f.write(f'{row} {balance}\n')


import os
import sys
import zipfile
import glob

from MerkleTree import MerkleTree
from Block import Block

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


import hashlib

class MerkleTree:

    class Node:
        # constructor
        def __init__(self):
            self.left = None
            self.right = None
            self.address = None
            self.balance = None
            self.hash_value = None

        # function to hash data
        def hash(self, hash1, hash2):
            return hashlib.sha256((hash1 + hash2).encode('utf-8')).hexdigest()

    # function to create a node
    def __init__(self, leaves):
        self.root = self.build_tree(leaves)

    # function to build the tree
    def build_tree(self, leaves):
        # get a list of leaves
        leaf_nodes = []
        for idx, leaf in enumerate(leaves):
            node = self.Node()
            node.left = None
            node.right = None
            node.address = leaf[0]
            node.balance = leaf[1]
            node.hash_value = node.hash(node.address, node.balance)
            leaf_nodes.append(node)
        return self.build_tree_helper(leaf_nodes)
        
    # function to build the tree
    def build_tree_helper(self, leaf_nodes):
        if len(leaf_nodes) == 1:
            return leaf_nodes[0]
        else:
            new_nodes = []
            for i in range(0, len(leaf_nodes) - 1, 2):
                node = self.Node()
                node.left = leaf_nodes[i]
                node.right = leaf_nodes[i + 1]
                node.hash_value = node.hash(node.left.hash_value, node.right.hash_value)
                new_nodes.append(node)
            if len(leaf_nodes) % 2 == 1:
                node = self.Node()
                node.left = leaf_nodes[-1]
                node.right = None
                node.hash_value = node.hash(leaf_nodes[-1].hash_value, "")
                new_nodes.append(node)
            return self.build_tree_helper(new_nodes)
            
    # function to get the root
    def get_root(self):
        return self.root.hash_value

    # function to print the contents of the tree
    def print(self):
        return self.print_helper(self.root, 0, "")
    
    # helper print function
    def print_helper(self, node, level, res):
        if node == None:
            return ""
        return self.print_helper(node.right, level + 1, res) + self.getStr(node) + self.print_helper(node.left, level + 1, res)
        
    
    def getStr(self, node):
        if node.address != None:
            return str(node.address) + " " + str(node.balance) + "\n"
        else:
            return ""