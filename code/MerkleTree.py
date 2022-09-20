import hashlib

# hashed_string = hashlib.sha256(input_string.encode('utf-8')).hexdigest()
# hexdigest() which is used to convert our data into hexadecimal format

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
            print("idx: " + str(idx)  + " " + leaf[0] + " " + leaf[1])
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