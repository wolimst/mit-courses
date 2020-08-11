from typing import Iterable
import math
from counting_sort import counting_sort


def radix_sort(iterable: Iterable[int], max_key: int = None) -> Iterable[int]:
    """Sort the iterable using radix sort algorithm.

    Items of the iterable should be positive interger. Sorting iterable whose
    item is other than positive integer is not implemented.

    Complexity: O(n)
                when k < n^O(1) where k is the maximum key in iterable and
                n is the size of the iterable.
    """
    if len(iterable) < 2:
        return iterable

    if max_key is None:
        max_key = max(iterable)

    n = len(iterable)
    num_digits = int(math.log(max_key, n)) + 1

    for i in range(num_digits):
        iterable = counting_sort(
            iterable, get_key=lambda x, n=n, i=i: (x // (n ** i)) % n
        )  # Key is (i+1)th digit of the integer in base n.
    return iterable
