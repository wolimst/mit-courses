from __future__ import annotations
from bst import BST, BSTNode


class AVL(BST):
    def __init__(self):
        super().__init__()

    def insert(self, node: AVLNode) -> AVL:
        """Insert a node into AVL tree.

        Complexity: O(lg n)
        """
        if self.root is None:
            self.root = node
        else:
            self.root.insert(node, tree=self)
        return self

    def insert_key(self, key) -> AVL:
        node = AVLNode(key)
        return self.insert(node)

    def delete_key(self, key) -> AVL:
        """Find and delete a node with key in the AVL tree.

        Complexity: O(lg n)
        """
        node = self.find_key(key)
        node.delete(tree=self)


class AVLNode(BSTNode):
    def __init__(self, key, parent: AVLNode = None):
        super().__init__(key, parent)
        self.height = 0

    def __repr__(self):
        parent = self.parent.key if self.parent else None
        left = self.left.key if self.left else None
        right = self.right.key if self.right else None
        return (
            f"Key: {self.key} / Parent: {parent} / Left: {left} / "
            + f"Right: {right} / Height Balance: {self.get_height_balance()}"
        )

    def update_height(self):
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        self.height = max(left_height, right_height) + 1

    def get_height_balance(self):
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        return right_height - left_height

    def rebalance(self, tree: AVLNode = None):
        """Rebalance the node when the height of children differ by 2.
        Update the tree root when the root is being rotated.

        Complexity: O(1)
        """
        self.update_height()
        if self.get_height_balance() == 2:  # self is right heavy
            # self.right is left heavy
            if self.right.get_height_balance() == -1:
                self.right.rotate_right(tree=tree)
            self.rotate_left(tree=tree)

        elif self.get_height_balance() == -2:  # left heavy
            # self.left is right heavy
            if self.left.get_height_balance() == 1:
                self.left.rotate_left(tree=tree)
            self.rotate_right(tree=tree)

    def rotate_left(self, tree: AVL = None) -> None:
        pivot = self.right
        if pivot is None:
            return

        self.right = pivot.left
        if pivot.left:
            pivot.left.parent = self

        pivot.left = self
        pivot.parent = self.parent
        self.parent = pivot
        if pivot.parent is None:
            tree.root = pivot
        elif pivot.parent.left is self:
            pivot.parent.left = pivot
        else:
            pivot.parent.right = pivot
        self.update_height()
        pivot.update_height()

    def rotate_right(self, tree: AVL = None) -> None:
        pivot = self.left
        if pivot is None:
            return

        self.left = pivot.right
        if pivot.right:
            pivot.right.parent = self

        pivot.right = self
        pivot.parent = self.parent
        self.parent = pivot
        if pivot.parent is None:
            tree.root = pivot
        elif pivot.parent.left is self:
            pivot.parent.left = pivot
        else:
            pivot.parent.right = pivot
        self.update_height()
        pivot.update_height()

    def insert(self, node: AVLNode, tree: AVL) -> None:
        """Insert the node into the tree and rebalance the tree.
        """
        if node.left or node.right:
            raise NotImplementedError(
                "Cannot insert another tree into the tree"
            )

        if self > node:
            if self.left is None:
                self.left = node
                node.parent = self
                node.update_height()
                self.update_height()
                return
            else:
                self.left.insert(node, tree=tree)
        elif self < node:
            if self.right is None:
                self.right = node
                node.parent = self
                node.update_height()
                self.update_height()
                return
            else:
                self.right.insert(node, tree=tree)
        else:
            raise NotImplementedError("Found same key values in the tree")
        self.rebalance(tree=tree)

    def delete(self, tree: AVL = None):
        """Delete the node and rebalance up to root.
        """
        parent = super().delete(tree=tree)
        node = parent
        while node:
            node.rebalance(tree=tree)
            node = node.parent
