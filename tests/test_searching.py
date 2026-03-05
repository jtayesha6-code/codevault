"""Tests for searching algorithm snippets."""

import pytest


# ---------------------------------------------------------------------------
# Binary Search – Iterative (from snippets/algorithms/searching/binary-search.md)
# ---------------------------------------------------------------------------
def binary_search_iterative(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


# ---------------------------------------------------------------------------
# Binary Search – Recursive (from snippets/algorithms/searching/binary-search.md)
# ---------------------------------------------------------------------------
def binary_search_recursive(nums, target, left=0, right=None):
    if right is None:
        right = len(nums) - 1
    if left > right:
        return -1
    mid = left + (right - left) // 2
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        return binary_search_recursive(nums, target, mid + 1, right)
    else:
        return binary_search_recursive(nums, target, left, mid - 1)


# =========================== Binary Search ================================


class TestBinarySearchIterative:
    def test_found(self):
        assert binary_search_iterative([1, 3, 5, 7, 9, 11], 7) == 3

    def test_not_found(self):
        assert binary_search_iterative([2, 4, 6, 8, 10], 5) == -1

    def test_single_element_found(self):
        assert binary_search_iterative([1], 1) == 0

    def test_single_element_not_found(self):
        assert binary_search_iterative([1], 2) == -1

    def test_empty_array(self):
        assert binary_search_iterative([], 1) == -1

    def test_first_element(self):
        assert binary_search_iterative([1, 3, 5, 7], 1) == 0

    def test_last_element(self):
        assert binary_search_iterative([1, 3, 5, 7], 7) == 3


class TestBinarySearchRecursive:
    def test_found(self):
        assert binary_search_recursive([1, 3, 5, 7, 9, 11], 7) == 3

    def test_not_found(self):
        assert binary_search_recursive([2, 4, 6, 8, 10], 5) == -1

    def test_single_element_found(self):
        assert binary_search_recursive([1], 1) == 0

    def test_single_element_not_found(self):
        assert binary_search_recursive([1], 2) == -1

    def test_empty_array(self):
        assert binary_search_recursive([], 1) == -1

    def test_first_element(self):
        assert binary_search_recursive([1, 3, 5, 7], 1) == 0

    def test_last_element(self):
        assert binary_search_recursive([1, 3, 5, 7], 7) == 3
