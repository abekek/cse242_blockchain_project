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