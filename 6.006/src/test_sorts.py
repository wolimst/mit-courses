import pytest
import numpy as np
from counting_sort import counting_sort
from radix_sort import radix_sort


class TestCountingSort:
    def test_sort_integers(self):
        array = [0, 1, 5, 3, 2, 2, 1]
        sorted_array = counting_sort(array)
        assert sorted_array == sorted(array)

    def test_negative_keys_should_raise_error(self):
        array = [-1, -2, 0, 1, 5, 3, 2, 2, 1]
        with pytest.raises(ValueError):
            counting_sort(array)

    def test_non_integer_keys_should_raise_error(self):
        array = [0, "a", 5.5, 3, 2, 2, 1]
        with pytest.raises(ValueError):
            counting_sort(array)

    def test_stable_sort(self):
        # Stable sort maintains relative order of items with same keys.
        keys = [0, 1, 5, 3, 2, 2, 1, 2]
        position = list(range(len(keys)))

        array = []
        for i in range(len(keys)):
            array.append({"key": keys[i], "position": position[i]})
        sorted_array = counting_sort(array, get_key=lambda x: x["key"])

        tuples = [(a["key"], a["position"]) for a in array]
        sorted_tuples = [(a["key"], a["position"]) for a in sorted_array]
        assert sorted_tuples == sorted(tuples)


class TestRadixSort:
    def test_sort_base10(self):
        array = [12, 10, 13, 19, 20, 102, 78, 34, 25, 140]
        sorted_array = radix_sort(array)
        assert sorted_array == sorted(array)

    def test_sort_base13(self):
        array = [12, 10, 13, 19, 20, 102, 78, 34, 25, 140, 0, 4, 382]
        sorted_array = radix_sort(array)
        assert sorted_array == sorted(array)

    def test_sort_random_array(self):
        n = np.random.randint(50)
        array = np.random.randint(0, 5 * n, size=n)
        sorted_array = radix_sort(array)
        assert list(sorted_array) == sorted(array)
