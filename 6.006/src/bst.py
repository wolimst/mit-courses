from __future__ import annotations


class BST:
    def __init__(self):
        self.root = None

    def insert(self, node: BSTNode) -> BST:
        """
        Insert the node into tree.
        """
        if self.root is None:
            self.root = node
        else:
            self.root.insert(node)

        return self

    def insert_key(self, key) -> BST:
        """
        Create a node with key and insert it into tree.
        """
        node = BSTNode(key)
        return self.insert(node)

    def find_key(self, key) -> BSTNode:
        return self.root.find_key(key)

    def find_min(self) -> BSTNode:
        return self.root.find_min()

    def find_max(self) -> BSTNode:
        return self.root.find_max()


class BSTNode:
    def __init__(self, key, parent: BSTNode = None):
        self.key = key
        self.parent = parent
        self.left = self.right = None

    def __lt__(self, other: BSTNode) -> bool:
        return self.key < other.key

    def __gt__(self, other: BSTNode) -> bool:
        return self.key > other.key

    def insert(self, node: BSTNode) -> None:
        """
        Insert a node into subtree whose root is self.
        """
        if self > node:
            if self.left is None:
                self.left = node
                node.parent = self
            else:
                self.left.insert(node)

        elif self < node:
            if self.right is None:
                self.right = node
                node.parent = self
            else:
                self.right.insert(node)

        else:
            raise NotImplementedError("Found same key values in tree")

    def find_key(self, key) -> BSTNode:
        if key == self.key:
            return self

        elif key < self.key:
            if self.left is None:
                raise ValueError("Key not found in BST")
            return self.left.find_key(key)

        else:
            if self.right is None:
                raise ValueError("Key not found in BST")
            return self.right.find_key(key)

    def find_min(self) -> BSTNode:
        if self.left is None:
            return self
        return self.left.find_min()

    def find_max(self) -> BSTNode:
        if self.right is None:
            return self
        return self.right.find_max()

    def get_successor(self) -> BSTNode:
        """
        Find a node with next larger key.
        """
        if self.right is None:  # Go up until parent is on the right
            parent = self.parent
            child = self
            while parent is not None:
                if child < parent:
                    return parent
                else:
                    child = parent
                    parent = parent.parent
            else:
                raise ValueError("Successor not found in BST")

        return self.right.find_min()

    def get_predecessor(self) -> BSTNode:
        """
        Find a node with next smaller key.
        """
        if self.left is None:  # Go up until parent is on the left
            parent = self.parent
            child = self
            while parent is not None:
                if parent < child:
                    return parent
                else:
                    child = parent
                    parent = parent.parent
            else:
                raise ValueError("Predecessor not found in BST")

        return self.left.find_max()


if __name__ == "__main__":
    num_node = 10
    random_nums = [68, 64, 151, 110, 19, 77, 144, 127, 45, 62]
    sorted_random_nums = sorted(random_nums)
    target = sorted_random_nums[num_node // 2]
    predecessor_key = sorted_random_nums[num_node // 2 - 1]

    bst = BST()
    for item in random_nums:
        bst.insert_key(item)

    predecessor = bst.find_key(target).get_predecessor()
    print(predecessor_key, predecessor.key)
