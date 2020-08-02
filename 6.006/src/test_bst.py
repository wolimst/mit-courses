from __future__ import annotations
import pytest
import random
from bst import BST, BSTNode


class TestBST:
    def check_representation_invarient(self, bst: BSTNode) -> bool:
        pass

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
        return bst

    def test_insert_balanced(self):
        bst = BST()
        bst.insert_key(10).insert_key(5).insert_key(20)
        assert bst.root.key == 10
        assert bst.root.left.key == 5
        assert bst.root.right.key == 20
        assert bst.root.left.parent == bst.root.right.parent == bst.root

    def test_insert_right_heavy(self):
        bst = BST()
        bst.insert_key(10).insert_key(20).insert_key(30)
        assert bst.root.key == 10
        assert bst.root.right.key == 20
        assert bst.root.right.right.key == 30
        assert bst.root.right.right.parent == bst.root.right
        assert bst.root.right.parent == bst.root

    def test_insert_zigzag(self):
        bst = BST()
        bst.insert_key(10).insert_key(30).insert_key(20)
        assert bst.root.right.key == 30
        assert bst.root.right.left.key == 20
        assert bst.root.right.left.parent == bst.root.right
        assert bst.root.right.parent == bst.root

    def test_insert_duplicated_key(self):
        bst = BST()
        with pytest.raises(NotImplementedError):
            bst.insert_key(10).insert_key(20).insert_key(20)

    def test_find_key(self):
        bst = BST()
        node = BSTNode(20)
        bst.insert_key(10).insert_key(30).insert(node)
        node_found = bst.find_key(node.key)
        print(node_found.key)
        assert node_found == node

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

        print(target)
        print(random_nums)
        print(sorted_random_nums)

        bst = self.create_bst_with_key_list(random_nums)
        sucessor = bst.find_key(target).get_successor()
        assert sucessor_key == sucessor.key

    def test_get_predecessor(self):
        num_node = 50
        random_nums = self.build_unique_random_number_list(num_node, 0, 200)

        sorted_random_nums = sorted(random_nums)
        target = sorted_random_nums[num_node // 2]
        predecessor_key = sorted_random_nums[num_node // 2 - 1]

        print(target)
        print(random_nums)
        print(sorted_random_nums)

        bst = self.create_bst_with_key_list(random_nums)
        predecessor = bst.find_key(target).get_predecessor()
        assert predecessor_key == predecessor.key
