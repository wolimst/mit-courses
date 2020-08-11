from typing import NewType, Iterable, Any, Callable
import math
import numpy as np

PositiveInt = NewType("PositiveInt", int)


def __get_min_max(
    iterable: Iterable[Any], get_key: Callable[..., PositiveInt]
):
    min_key, max_key = math.inf, -math.inf
    for item in iterable:
        key = get_key(item)
        if not isinstance(key, (int, np.integer)):
            raise ValueError("The iterable has non-integer key values.")
        if key > max_key:
            max_key = key
        if key < min_key:
            min_key = key
    return min_key, max_key


def counting_sort(
    iterable: Iterable[Any], get_key: Callable[..., PositiveInt] = lambda x: x
) -> Iterable[Any]:
    """Sort an iterable whose keys are positive integers.

    iterable -- An iterable to be sorted.
    get_key -- A function that returns the key value from an item in the
                iterable.

    Complexity: O(n + k)
                where n is the size of iterable and k is the maximum value of
                keys in the iterable.
    """

    if len(iterable) == 0:
        return iterable

    min_key, max_key = __get_min_max(iterable, get_key)
    if min_key < 0:
        raise ValueError("The iterable has non-positive key values.")

    position = [0] * (max_key + 1)
    for item in iterable:
        position[get_key(item)] += 1

    total = 0
    for i in range(len(position)):
        position[i], total = total, total + position[i]

    output = [None] * len(iterable)
    for item in iterable:
        key = get_key(item)
        output[position[key]] = item
        position[key] += 1

    return output
