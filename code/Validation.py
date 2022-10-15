from MerkleTree import MerkleTree
from Block import Block
import hashlib
import random
import string

class Validate:
    def __init__(self, blocks, num_bad_entities):
        self.addresses = {}
        self.blocks = blocks
        self.num_bad_entities = num_bad_entities
        self.bad_blocks = self.generate_bad_blocks()

    # HW 5: 2.3
    def generate_bad_blocks(self):
        bad_blocks = self.blocks.copy()
        for _ in range(self.num_bad_entities):
            # choose a random block to make bad
            rnd_block_idx = random.randint(0, len(bad_blocks) - 1)
            rnd_block = bad_blocks[rnd_block_idx]
            # choose a random bad action
            rnd_action = random.randint(0, 2)
            if rnd_action == 0:
                # put the random hash in the block hash
                rnd_block.hash_header = ''.join(random.choices(string.hexdigits, k=40)).lower()
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
            leaves = block.header.hash_root.traverse_tree()
            for leaf in leaves:
                addresses[leaf.address] = i
        return addresses

    def balance(self):
        pass

    # HW5: 2.2
    def validate_block(self, block):
        block_content = block.print(True)
        start = 'BEGIN BLOCK\n'
        end = 'END HEADER\n'
        transaction = "".join(block_content[len(start):-len(end)])
        file_content = [line.split() for line in transaction.splitlines()]
        merkle_tree = MerkleTree(file_content)
        ## Check that transactions in the block make the merkle tree passed in the block
        if merkle_tree.get_root() != block.header.hash_root.get_root():
            return False
        hash_of_block_header = hashlib.sha256((str(block.hash_prev) + str(merkle_tree.get_root())) + str(block.timestamp) + str(block.target) + 
                    str(block.nonce)).encode('utf-8').hexdigest()
        ## Check hash of the block header is correct
        if hash_of_block_header != block.hash_header:
            return False
        return True
        
    def validate_recursively(self, block):
        if block.hash_prev == None:
            return self.validate_block(block)
        # else:
        #     return validate_block(block) and 

    def validate_blockchain(self):
        return self.validate_recursively(self.blocks[-1])