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
import random
import string
import hashlib

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
print("1. Input folder name (all files in folder will be used)")
print("2. Zip file")

user_input = input("Enter 1 or 2: ")

if user_input == "1":
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
elif user_input == "2":
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
    output_access = 'output'
    if user_input == "1":
        output_access = '../output'
        
    with open(f'{output_access}/{filenames[i][:-4]}.block.out', 'w') as f:
        f.write(blocks[i].print(True))

# validation of the blockchain
num_bad_entities = 100
validation = Validate(blocks, num_bad_entities)

choosen_address = "de0acd701ed59eb60ccbf38de33a2f5f91e6cde0"
print(f"\nValidating chosen address = {choosen_address} ...")
val_res = validation.balance(choosen_address)
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
        
    def inorder_traverse_tree(self, only_leaves = True):
        l = []
        self.inorder_traverse_tree_helper(self.root, l, only_leaves)
        return l
    
    def inorder_traverse_tree_helper(self, node, l, only_leaves):
        if node == None:
            return
        self.inorder_traverse_tree_helper(node.left, l, only_leaves)
        if only_leaves:
            if node.balance != None:
                l.append(node)
        else:
            l.append(node)
        self.inorder_traverse_tree_helper(node.right, l, only_leaves)

    def postorder_traverse_tree(self, only_leaves = True):
        l = []
        self.postorder_traverse_tree_helper(self.root, l, only_leaves)
        return l

    def postorder_traverse_tree_helper(self, node, l, only_leaves):
        if node == None:
            return
        if only_leaves:
            if node.balance != None:
                l.append(node)
        else:
            l.append(node)
        self.postorder_traverse_tree_helper(node.left, l, only_leaves)
        self.postorder_traverse_tree_helper(node.right, l, only_leaves)

    def proof_of_membership(self, address):
        solution_path = []
        solutions = []
        path = []
        path.append(self.root)
        self.proof_of_membership_helper(self.root, solutions, path)
        for solution in solutions:
            if solution[-1].address == address or solution[-2].address == address:
                for s in reversed(solution):
                    solution_path.append(s.hash_value)
                break
        return solution_path
    
    def proof_of_membership_helper(self, node, solutions, current_path):
        if node == None or (node.left == None and node.right == None):
            return
        current_path_copy = list(current_path)
        if node.left != None and node.right != None:
            current_path_copy.append(node.right)
            current_path_copy.append(node.left)
            solutions.append(current_path_copy)
            self.proof_of_membership_helper(node.right, solutions, current_path_copy)
            self.proof_of_membership_helper(node.left, solutions, current_path_copy)
        elif node.left != None:
            current_path_copy.append(node.left)
            solutions.append(current_path_copy)
            self.proof_of_membership_helper(node.left, solutions, current_path_copy)
        elif node.right != None:
            current_path_copy.append(node.right)
            solutions.append(current_path_copy)
            self.proof_of_membership_helper(node.right, solutions, current_path_copy)

    def getStr(self, node):
        if node.address != None:
            return str(node.address) + " " + str(node.balance) + "\n"
        else:
            return ""


from MerkleTree import MerkleTree
from Block import Block
import random
import string
import re
import copy
import hashlib

class Validate:
    def __init__(self, blocks, num_bad_entities):
        self.blocks = blocks
        self.num_bad_entities = num_bad_entities
        self.bad_blocks = self.generate_bad_blocks()
        self.addresses = self.save_addresses()
        self.membership_proof_arr = []

    # HW 5: 2.3
    def generate_bad_blocks(self):
        bad_blocks = []

        for i in range(len(self.blocks)):
            bad_blocks.append(copy.deepcopy(self.blocks[i]))
        
        for _ in range(self.num_bad_entities):
            # choose a random block to make bad
            rnd_block_idx = random.randint(0, len(bad_blocks) - 1)
            rnd_block = bad_blocks[rnd_block_idx]
            # choose a random bad action
            rnd_action = random.randint(0, 2)
            if rnd_action == 0:
                # put the random hash in the block hash
                rnd_block.hash_header = ''.join(random.choices(string.hexdigits, k=64)).lower()
            elif rnd_action == 1:
                # change the timestamp of a header in a block
                rnd_block.header.timestamp = random.randint(0, 100000000)
            elif rnd_action == 2:
                # choose whether to change the address or the balance
                address_or_balance = random.randint(0, 1)
                if address_or_balance == 0:
                    # change the balance of a leaf node
                    self.change_node(rnd_block.header.hash_root.root, random.randint(0, 100000000))
                else:
                    # change the address of a leaf node
                    self.change_node(rnd_block.header.hash_root.root, ''.join(random.choices(string.hexdigits, k=40)).lower())

        return bad_blocks

    # HW 5: 2.3
    def change_node(self, node, val_new):
        if node.left == None or node.right == None:
            if type(val_new) == int:
                node.balance = val_new
            else:
                node.address = val_new
        else:
            left_or_right = random.randint(0, 1)
            if left_or_right == 0:
                self.change_node(node.left, val_new)
            else:
                self.change_node(node.right, val_new)

    def save_addresses(self):
        addresses = {}
        # traverse the blockchain and save all the addresses
        for i, block in enumerate(self.blocks):
            leaves = block.header.hash_root.inorder_traverse_tree()
            for leaf in leaves:
                addresses[leaf.address] = (i, int(leaf.balance))
        return addresses

    def balance(self, key_address):
        if key_address in self.addresses:
            return self.addresses[key_address][1], True, self.membership_proof(key_address)
        return -1, False, None

    # HW5: 2.2
    def __validate_block(self, block, index, blocks):
        ## Check for hash of block before
        if index != 0:
            if block.header.hash_prev != blocks[index-1].hash_header:
                print("Invalid block: "+str(index+1))
                return False
        block_content = block.print(True)
        start = 'END HEADER\n'
        end = 'END BLOCK\n\n'
        transaction = (block_content.split(start))[1].split(end)[0]
        file_content = [line.split() for line in transaction.splitlines()]
        file_content.reverse()
        ## Rebuild the tree
        merkle_tree = MerkleTree(file_content)
        ## Check that transactions in the block make the merkle tree passed in the block
        if merkle_tree.get_root() != block.header.hash_root.get_root():
            print("Invalid block: "+str(index+1))
            return False
        hash_of_block_header = block.header.hash()
        ## Check hash of the block header is correct
        if hash_of_block_header != block.hash_header:
            print("Invalid block: "+str(index+1))
            return False
        return True
        
    def __validate_recursively(self, blocks, index):
        if index == -1:
            return False
        if index == 0:
            return self.__validate_block(blocks[index], index, blocks)
        else:
            return self.__validate_block(blocks[index], index, blocks) and self.__validate_recursively(self.blocks, index-1)

    def validate_blockchain(self, blocks):
        return self.__validate_recursively(blocks, len(blocks)-1)

    # HW5: 2.5
    def membership_proof(self, key_address):
        block = self.blocks[self.addresses[key_address][0]]
    
        self.membership_proof_postorder(block.header.hash_root.root, [block.header.hash_root.root.hash_value], key_address)
        self.membership_proof_arr.reverse()    
        
        print('\nProof of membership:')
        
        self.membership_proof_arr = self.proof_of_membership(key_address)
        print("Path from data to the merkle tree root: " + str(self.membership_proof_arr))

        res = ""
        res+="BLOCK HEADER\n"
        res+= 'Hash of the previous block: {}\n'.format(block.header.hash_prev)
        res+= 'Merkle Tree root: {}\n'.format(block.header.hash_root.get_root())
        res+= 'Timestamp: {}\n'.format(block.header.timestamp)
        res+= 'Target: {}\n'.format(block.header.target)
        res+= 'Nonce: {}\n'.format(block.header.nonce)
        res+= "END HEADER\n"
        print(res)

        to_recent = []
        for i in range(self.addresses[key_address][0], len(self.blocks)):
            to_recent.append(self.blocks[i].hash_header)

        print("Path from the current block to the recent block: " + str(to_recent))
        
        path_len = len(self.membership_proof_arr)
        if path_len % 2 == 0: # the number of nodes in the path is even aka only one leaf node
            if hashlib.sha256((self.membership_proof_arr[0]).encode('utf-8')).hexdigest() == self.membership_proof_arr[1]:
                for i in range(1, len(self.membership_proof_arr) - 2, 2):
                    if(hashlib.sha256((self.membership_proof_arr[i] + self.membership_proof_arr[i+1]).encode('utf-8')).hexdigest() == self.membership_proof_arr[i+2]):
                        pass
                    elif(hashlib.sha256((self.membership_proof_arr[i] + self.membership_proof_arr[i+1]).encode('utf-8')).hexdigest() == self.membership_proof_arr[i+3]):
                        pass
                    else: # failed
                        print("Membership proof failed")
                        break
            if(hashlib.sha256((self.membership_proof_arr[path_len - 3] + self.membership_proof_arr[path_len - 2]).encode('utf-8')).hexdigest() == self.membership_proof_arr[path_len - 1]):
                print('Membership proof is valid')
            else:
                print("Membership proof failed")
        else: 
            for i in range(0,len(self.membership_proof_arr) - 2, 2):
                if(hashlib.sha256((self.membership_proof_arr[i] + self.membership_proof_arr[i+1]).encode('utf-8')).hexdigest() == self.membership_proof_arr[i+2]):
                    # print("True")
                    pass
                elif(hashlib.sha256((self.membership_proof_arr[i] + self.membership_proof_arr[i+1]).encode('utf-8')).hexdigest() == self.membership_proof_arr[i+3]):
                    # print("True")
                    pass
                else: # failed
                    print("Membership proof failed")
                    break
            if(hashlib.sha256((self.membership_proof_arr[path_len - 3] + self.membership_proof_arr[path_len - 2]).encode('utf-8')).hexdigest() == self.membership_proof_arr[path_len - 1]):
                print('Membership proof is valid')
            else: 
                print("Membership proof failed")
    
    # root is a parent node
    # path is the array that contains the path to the root node
    def membership_proof_postorder(self, root, path, key_address):
        if root == None:
            return
        else: 
            if root.address == key_address:
                self.membership_proof_arr = path
                return path # None
            newPath = path.copy()
            # add left and right children to the array if they exist
            if root.left != None:
                newPath.append(root.left.hash_value)
            if root.right != None:
                newPath.append(root.right.hash_value)
            # call the function recursively on the left and right children
            self.membership_proof_postorder(root.left, newPath, key_address)
            self.membership_proof_postorder(root.right, newPath, key_address)

    def proof_of_membership(self, key_address):
        if key_address in self.addresses:
            block = self.blocks[self.addresses[key_address][0]]
            path = block.header.hash_root.proof_of_membership(key_address)
            return path
        else:
            return []
        

    