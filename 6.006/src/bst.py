from __future__ import annotations


class BST:
    def __init__(self):
        self.root = None

    def insert(self, node: BSTNode) -> BST:
        """
        Insert the node into tree.

        Complexity: O(h)
                    where h is the height of the tree.
                    h = lg(n) when the tree is balanced.
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
        """
        Find a node with the key.

        Complexity: O(h)
        """
        return self.root.find_key(key)

    def find_min(self) -> BSTNode:
        return self.root.find_min()

    def find_max(self) -> BSTNode:
        return self.root.find_max()

    def delete_key(self, key) -> BST:
        """
        Find and delete a node with the key.

        Complexity: O(h)
        """
        node = self.find_key(key)
        if self.root == node:
            node.delete(bst=self)
        else:
            node.delete()
        return self


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
        Insert the node into subtree whose root is self.
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

        Complexity: O(h)
        """
        if self.right is None:  # Go up until the parent is on the right
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

        Complexity: O(h)
        """
        if self.left is None:  # Go up until the parent is on the left
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

    def delete(self, bst: BST = None) -> None:
        # The node has no child
        if self.left is None and self.right is None:
            self.__update_parent_child_link(child_node=None, bst=bst)

        # The node has one child
        elif self.left is None:
            self.__update_parent_child_link(child_node=self.right, bst=bst)
        elif self.right is None:
            self.__update_parent_child_link(child_node=self.left, bst=bst)

        # The node has two child
        else:
            successor = self.get_successor()
            self.key = successor.key
            successor.delete()

    def __update_parent_child_link(
        self, child_node=None, bst: BST = None
    ) -> None:
        if self.parent is None:
            bst.root = child_node
        elif self == self.parent.left:
            self.parent.left = child_node
        else:
            self.parent.right = child_node

        if child_node:
            child_node.parent = self.parent
