# https://stackoverflow.com/questions/72411835/how-to-correctly-do-a-double-sha256-hashing
# https://github.com/howCodeORG/Simple-Python-Blockchain/blob/master/blockchain.py

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
            self.hash_header = hashlib.sha256((
                str(self.hash_prev) + 
                str(self.hash_root) +
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
            print(tries)

        def get_nonce(self):
            return self.nonce

    # function to print the block
    def print(self, printLedger):
        print("BEGIN BLOCK")
        print("BEGIN HEADER")
        print(self.header.hash_prev)
        print(self.header.hash_root)
        print(self.header.timestamp)
        print(self.header.target)
        print(self.header.nonce)
        print("END HEADER")
        if printLedger:
            self.hash_root.print()
        print("END BLOCK")
        print("")
    