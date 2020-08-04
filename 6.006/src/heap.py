from __future__ import annotations
import math


class MaxHeap:
    def __init__(self, heap):
        self.heap = list(heap)
        self.build_max_heap()

    def __str__(self):
        return str(self.heap)

    def __len__(self):
        return len(self.heap)

    def get_key(self, index: int):
        return self.heap[index]

    def insert(self, key) -> MaxHeap:
        """
        Insert a key into the max heap.

        Complexity: O(lg(n))
        """
        i = len(self.heap)
        self.heap.append(key)
        while i > 0:
            parent_index = (i + 1) // 2 - 1
            if self.heap[i] > self.heap[parent_index]:
                self.heap[i], self.heap[parent_index] = (
                    self.heap[parent_index],
                    self.heap[i],
                )
                i = parent_index
            else:
                break
        return self

    def build_max_heap(self) -> None:
        """
        Produces a max heap from an unordered array.

        Complexity: O(n) where n is the size of heap
                    because there are 2^m nodes on level m and the complexity
                    of max_heapify() of a node on level m is O(lg(n) - m).
        """
        max_non_leaf_index = len(self.heap) // 2 - 1
        for i in range(max_non_leaf_index, -1, -1):
            self.max_heapify(i)

    def max_heapify(self, i: int) -> None:
        """
        Correct a single violation of the heap property in a subtree's root.

        Complexity: O(lg(n))
                    where n is the size of the partial heap whose root index
                    is i.
        """
        try:
            left_child_index = self.get_left_child_index(i)
            left_child = self.heap[left_child_index]
        except IndexError:
            left_child = -math.inf

        try:
            right_child_index = self.get_right_child_index(i)
            right_child = self.heap[right_child_index]
        except IndexError:
            right_child = -math.inf

        if left_child == -math.inf and right_child == -math.inf:
            return

        if left_child >= right_child:
            j = left_child_index
        else:
            j = right_child_index

        if self.heap[i] < self.heap[j]:
            self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

        self.max_heapify(j)

    def get_left_child_index(self, index: int) -> int:
        child_index = index * 2 + 1
        if not self.index_exists(child_index):
            raise IndexError(f"Index {index} is out of range.")
        return child_index

    def get_right_child_index(self, index: int) -> int:
        child_index = index * 2 + 2
        if not self.index_exists(child_index):
            raise IndexError(f"Index {index} is out of range.")
        return child_index

    def index_exists(self, i: int) -> bool:
        if i < len(self.heap):
            return True
        else:
            return False

    def sort(self) -> list:
        """
        Complexity: O(n lg(n))
        """
        heap_copy = self.heap.copy()

        desc_sorted_list = []
        while len(self.heap):
            self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
            desc_sorted_list.append(self.heap.pop())
            self.max_heapify(0)

        self.heap = heap_copy
        return desc_sorted_list
