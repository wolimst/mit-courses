import math


class Heap:
    def __init__(self, heap):
        self.heap = list(heap)

    def __str__(self):
        return str(self.heap)

    def __len__(self):
        return len(self.heap)

    def build_max_heap(self):
        """
        Produces a max heap from an unordered array.

        Complexity: O(n) where n is the size of heap
                    because level m has 2^m nodes and the complexity of
                    max_heapify() of a node on level m is O(lg(n) - m)
        """
        max_non_leaf_index = len(self.heap) // 2 - 1
        for i in range(max_non_leaf_index, -1, -1):
            self.max_heapify(i)

    def max_heapify(self, i: int):
        """
        Correct a single violation of the heap property in a subtree's root.

        Complexity: O(lg(n))
                    where n is the size of the partial heap whose root index
                    is i.
        """
        try:
            left_heap_index = self.get_left_heap_index_of(i)
            left_child = self.heap[left_heap_index]
        except IndexError:
            left_child = -math.inf

        try:
            right_heap_index = self.get_right_heap_index_of(i)
            right_child = self.heap[right_heap_index]
        except IndexError:
            right_child = -math.inf

        if left_child == -math.inf and right_child == -math.inf:
            return

        if left_child >= right_child:
            j = left_heap_index
        else:
            j = right_heap_index

        if self.heap[i] < self.heap[j]:
            self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

        self.max_heapify(j)

    def get_left_heap_index_of(self, i: int) -> int:
        """
        Complexity: O(1)
        """
        child_index = i * 2 + 1
        if not self.index_exists(child_index):
            raise IndexError(f"Index {i} is a leaf.")
        return child_index

    def get_right_heap_index_of(self, i: int) -> int:
        """
        Complexity: O(1)
        """
        child_index = i * 2 + 2
        if not self.index_exists(child_index):
            raise IndexError(f"Index {i} is a leaf.")
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

        self.build_max_heap()
        heap_copy = self.heap.copy()

        sorted_desc = []
        while len(self.heap):
            self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
            sorted_desc.append(self.heap.pop())
            self.max_heapify(0)

        self.heap = heap_copy
        return sorted_desc


if __name__ == "__main__":
    heap = Heap([1, 2, 3, 4, 5, 6, 7, 8, 9])
    print(heap)

    heap.build_max_heap()
    print(heap)

    sorted = heap.sort()
    print(sorted)
