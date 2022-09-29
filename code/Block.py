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
    