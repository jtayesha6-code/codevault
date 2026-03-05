"""Tests for array algorithm snippets."""

import pytest


# ---------------------------------------------------------------------------
# Two Sum – Brute Force (from snippets/algorithms/arrays/two-sum.md)
# ---------------------------------------------------------------------------
def two_sum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


# ---------------------------------------------------------------------------
# Two Sum – Hash Map (from snippets/algorithms/arrays/two-sum.md)
# ---------------------------------------------------------------------------
def two_sum_hashmap(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


# ---------------------------------------------------------------------------
# Find Duplicate – Hash Set (from snippets/algorithms/arrays/find-duplicates.md)
# ---------------------------------------------------------------------------
def find_duplicate_hashset(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)
    return -1


# ---------------------------------------------------------------------------
# Find Duplicate – Floyd's Cycle Detection
# ---------------------------------------------------------------------------
def find_duplicate_floyd(nums):
    slow = nums[0]
    fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow


# ---------------------------------------------------------------------------
# Merge Sorted Arrays (from snippets/algorithms/arrays/merge-sorted-arrays.md)
# ---------------------------------------------------------------------------
def merge_sorted(nums1, nums2):
    result = []
    i, j = 0, 0
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            result.append(nums1[i])
            i += 1
        else:
            result.append(nums2[j])
            j += 1
    result.extend(nums1[i:])
    result.extend(nums2[j:])
    return result


# ============================= Two Sum Tests ==============================


class TestTwoSumBruteForce:
    def test_basic(self):
        assert two_sum_brute([2, 7, 11, 15], 9) == [0, 1]

    def test_middle_pair(self):
        assert two_sum_brute([3, 2, 4], 6) == [1, 2]

    def test_duplicates(self):
        assert two_sum_brute([3, 3], 6) == [0, 1]

    def test_no_solution(self):
        assert two_sum_brute([1, 2, 3], 100) == []


class TestTwoSumHashMap:
    def test_basic(self):
        assert two_sum_hashmap([2, 7, 11, 15], 9) == [0, 1]

    def test_middle_pair(self):
        assert two_sum_hashmap([3, 2, 4], 6) == [1, 2]

    def test_duplicates(self):
        assert two_sum_hashmap([3, 3], 6) == [0, 1]

    def test_no_solution(self):
        assert two_sum_hashmap([1, 2, 3], 100) == []


# ========================= Find Duplicate Tests ===========================


class TestFindDuplicate:
    @pytest.mark.parametrize(
        "nums, expected",
        [
            ([1, 3, 4, 2, 2], 2),
            ([3, 1, 3, 4, 2], 3),
            ([1, 1], 1),
        ],
    )
    def test_hashset(self, nums, expected):
        assert find_duplicate_hashset(nums) == expected

    @pytest.mark.parametrize(
        "nums, expected",
        [
            ([1, 3, 4, 2, 2], 2),
            ([3, 1, 3, 4, 2], 3),
            ([1, 1], 1),
        ],
    )
    def test_floyd(self, nums, expected):
        assert find_duplicate_floyd(nums) == expected


# ====================== Merge Sorted Arrays Tests ========================


class TestMergeSortedArrays:
    def test_basic(self):
        assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]

    def test_non_overlapping(self):
        assert merge_sorted([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6]

    def test_empty_first(self):
        assert merge_sorted([], [1, 2, 3]) == [1, 2, 3]

    def test_empty_second(self):
        assert merge_sorted([1, 2, 3], []) == [1, 2, 3]

    def test_both_empty(self):
        assert merge_sorted([], []) == []
