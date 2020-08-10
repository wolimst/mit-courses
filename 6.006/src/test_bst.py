from __future__ import annotations
from typing import Union
import random
import math
import pytest
from bst import BST, BSTNode


class TestBST:
    def build_unique_random_number_list(
        self, size: int, lower_limit: int, upper_limit: int
    ) -> list:
        random_nums = []
        while len(random_nums) < size:
            number = random.randint(lower_limit, upper_limit)
            if number not in random_nums:
                random_nums.append(number)
        return random_nums

    def create_bst_with_key_list(self, li: list) -> BST:
        bst = BST()
        for item in li:
            bst.insert_key(item)
        assert self.check_representation_invarient(bst.root)
        return bst

    def check_representation_invarient(
        self,
        node: BSTNode,
        min_key: Union[int, float] = -math.inf,
        max_key: Union[int, float] = math.inf,
    ) -> bool:

        if node is None:
            return True

        if not (node.key > min_key and node.key < max_key):
            return False

        is_left_valid = self.check_representation_invarient(
            node.left, min_key, node.key
        )
        is_right_valid = self.check_representation_invarient(
            node.right, node.key, max_key
        )
        return is_left_valid and is_right_valid

    def test_check_representation_invarient(self):
        """
        This is not a valid BST and check_ri() should fail.
            10
        5        15
               2    20
              ```
        """
        bst = self.create_bst_with_key_list([10, 5, 15, 20])
        parent_node = bst.root.right
        misplaced_node = BSTNode(2, parent=parent_node)
        parent_node.left = misplaced_node
        assert self.check_representation_invarient(bst.root) is False

    def test_insert_balanced(self):
        bst = self.create_bst_with_key_list([10, 5, 20])
        assert bst.root.key == 10
        assert bst.root.left.key == 5
        assert bst.root.right.key == 20
        assert bst.root.left.parent is bst.root.right.parent is bst.root
        assert self.check_representation_invarient(bst.root)

    def test_insert_right_heavy(self):
        bst = self.create_bst_with_key_list([10, 20, 30])
        assert bst.root.key == 10
        assert bst.root.right.key == 20
        assert bst.root.right.right.key == 30
        assert bst.root.right.right.parent is bst.root.right
        assert bst.root.right.parent is bst.root
        assert self.check_representation_invarient(bst.root)

    def test_insert_zigzag(self):
        bst = self.create_bst_with_key_list([10, 30, 20])
        assert bst.root.right.key == 30
        assert bst.root.right.left.key == 20
        assert bst.root.right.left.parent is bst.root.right
        assert bst.root.right.parent is bst.root
        assert self.check_representation_invarient(bst.root)

    def test_insert_duplicated_key(self):
        with pytest.raises(NotImplementedError):
            self.create_bst_with_key_list([10, 20, 20])

    def test_find_key(self):
        bst = BST()
        node = BSTNode(20)
        bst.insert_key(10).insert_key(30).insert(node)
        node_found = bst.find_key(node.key)
        assert node_found is node

    def test_find_min(self):
        random_nums = self.build_unique_random_number_list(50, 0, 200)
        minimum = min(random_nums)

        bst = self.create_bst_with_key_list(random_nums)
        min_node = bst.find_min()
        assert minimum == min_node.key

    def test_find_max(self):
        random_nums = self.build_unique_random_number_list(50, 0, 200)
        maximum = max(random_nums)

        bst = self.create_bst_with_key_list(random_nums)
        max_node = bst.find_max()
        assert maximum == max_node.key

    def test_get_successor(self):
        num_node = 50
        random_nums = self.build_unique_random_number_list(num_node, 0, 200)

        sorted_random_nums = sorted(random_nums)
        target = sorted_random_nums[num_node // 2]
        sucessor_key = sorted_random_nums[num_node // 2 + 1]

        bst = self.create_bst_with_key_list(random_nums)
        sucessor = bst.find_key(target).get_successor()
        assert sucessor_key == sucessor.key

    def test_get_predecessor(self):
        num_node = 50
        random_nums = self.build_unique_random_number_list(num_node, 0, 200)

        sorted_random_nums = sorted(random_nums)
        target = sorted_random_nums[num_node // 2]
        predecessor_key = sorted_random_nums[num_node // 2 - 1]

        bst = self.create_bst_with_key_list(random_nums)
        predecessor = bst.find_key(target).get_predecessor()
        assert predecessor_key == predecessor.key

    def test_delete_random(self):
        num_node = 50
        random_nums = self.build_unique_random_number_list(num_node, 0, 200)
        bst = self.create_bst_with_key_list(random_nums)
        key = random_nums[num_node // 2]
        bst.delete_key(key)
        with pytest.raises(ValueError):
            bst.find_key(key)
        assert self.check_representation_invarient(bst.root)

    def test_delete_node_with_no_child(self):
        bst = self.create_bst_with_key_list([10, 5, 2, 7, 15])
        key = 2
        bst.delete_key(key)
        with pytest.raises(ValueError):
            bst.find_key(key)
        assert self.check_representation_invarient(bst.root)

    def test_delete_node_with_one_child(self):
        bst = self.create_bst_with_key_list([10, 5, 2, 7, 15, 12])
        key = 15
        bst.delete_key(key)
        with pytest.raises(ValueError):
            bst.find_key(key)
        assert self.check_representation_invarient(bst.root)

    def test_delete_node_with_two_child(self):
        bst = self.create_bst_with_key_list([10, 5, 2, 7, 15])
        key = 5
        bst.delete_key(key)
        with pytest.raises(ValueError):
            bst.find_key(key)
        assert self.check_representation_invarient(bst.root)

    def test_delete_root_with_no_child(self):
        bst = self.create_bst_with_key_list([10])
        bst.delete_key(bst.root.key)
        assert bst.root is None

    def test_delete_root_with_one_child(self):
        bst = self.create_bst_with_key_list([1, 6, 4, 2, 3, 5, 9, 7, 8, 10])
        assert bst.root.left is None
        bst.delete_key(bst.root.key)
        assert bst.root.key == 6
        assert bst.root.parent is None
        assert self.check_representation_invarient(bst.root)

    def test_delete_root_with_two_child(self):
        bst = self.create_bst_with_key_list([1, 0, 6, 4, 2, 3, 5, 9, 7, 8, 10])
        bst.delete_key(bst.root.key)
        assert bst.root.key == 2
        assert bst.root.parent is None
        assert bst.root.left.key == 0
        assert bst.root.right.key == 6
        assert bst.root.get_successor().key == 3
        assert bst.root.get_predecessor().key == 0
        assert self.check_representation_invarient(bst.root)
