from __future__ import annotations
from bst import BST, BSTNode


class AVL(BST):
    def __init__(self):
        super().__init__()

    def insert(self, node: AVLNode) -> AVL:
        if self.root is None:
            self.root = node
        else:
            self.root.insert(node, avl=self)
        return self

    def insert_key(self, key) -> AVL:
        node = AVLNode(key)
        return self.insert(node)

    def delete_key(self):
        pass


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

    def insert(self, node: AVLNode, avl: AVL) -> None:
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
                self.left.insert(node, avl=avl)

        elif self < node:
            if self.right is None:
                self.right = node
                node.parent = self
                node.update_height()
                self.update_height()
                return
            else:
                self.right.insert(node, avl=avl)

        else:
            raise NotImplementedError("Found same key values in the tree")

        self.update_height()

        # Balance the tree
        if self.get_height_balance() == 2:  # self is right heavy
            # self.right is left heavy
            if self.right.get_height_balance() == -1:
                self.right.rotate_right(avl=avl)
            self.rotate_left(avl=avl)

        elif self.get_height_balance() == -2:  # left heavy
            # self.left is right heavy
            if self.left.get_height_balance() == 1:
                self.left.rotate_left(avl=avl)
            self.rotate_right(avl=avl)

    def rotate_left(self, avl: AVL = None) -> None:
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
            avl.root = pivot
        elif pivot.parent.left is self:
            pivot.parent.left = pivot
        else:
            pivot.parent.right = pivot
        self.update_height()
        pivot.update_height()
        return

    def rotate_right(self, avl: AVL = None) -> None:
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
            avl.root = pivot
        elif pivot.parent.left is self:
            pivot.parent.left = pivot
        else:
            pivot.parent.right = pivot

        self.update_height()
        pivot.update_height()
        return

    def delete(self):
        pass
