from __future__ import annotations
import math
import random
from heap import MaxHeap


class TestMaxHeap:
    def check_representation_invarient(self, heap: MaxHeap) -> bool:
        max_non_leaf_index = len(heap) // 2 - 1

        i = 0
        while i <= max_non_leaf_index:
            node = heap.get_key(i)

            left_child_index = heap.get_left_child_index(i)
            left_child = heap.get_key(left_child_index)
            try:
                right_child_index = heap.get_right_child_index(i)
                right_child = heap.get_key(right_child_index)
            except IndexError:
                right_child = -math.inf

            if node < left_child or node < right_child:
                break
            i += 1
        else:
            return True

        return False

    def test_build_max_heap(self):
        test_sets = [
            [9, 7, 8, 4, 5, 6, 3, 2, 1, 0],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 1, 1, 1, 3, 3, 5, 5, 5, 5],
            [random.randint(-10, 10) for i in range(50)],
            [],
        ]
        for test_set in test_sets:
            heap = MaxHeap(test_set)
            assert self.check_representation_invarient(heap)

    def test_insert(self):
        heap = MaxHeap([])
        for i in range(50):
            random_number = random.randint(0, 10)
            heap.insert(random_number)
            assert self.check_representation_invarient(heap)

    def test_sort(self):
        random_numbers = [random.randint(0, 10) for i in range(50)]
        heap = MaxHeap(random_numbers)
        assert heap.sort() == sorted(random_numbers, reverse=True)
