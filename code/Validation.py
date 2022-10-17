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
        

    