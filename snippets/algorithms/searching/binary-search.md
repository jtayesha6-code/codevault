# Binary Search Implementation

## Problem Statement
- Given a sorted array of integers `nums` and an integer `target`, find the index of `target` in the array. Return `-1` if it is not found.
- The array is sorted in ascending order and contains no duplicates.

**Example inputs/outputs:**
- Input: `nums = [1, 3, 5, 7, 9, 11]`, `target = 7` → Output: `3`
- Input: `nums = [2, 4, 6, 8, 10]`, `target = 5` → Output: `-1`
- Input: `nums = [1]`, `target = 1` → Output: `0`

**Edge cases:**
- Empty array
- Single-element array
- Target smaller than all elements
- Target larger than all elements
- Target at the first or last position

## Solutions

### Solution 1: Iterative Binary Search
- **Time Complexity:** O(log n)
- **Space Complexity:** O(1)
- **Difficulty:** Medium

#### Python
```python
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
```

#### JavaScript
```javascript
function binarySearchIterative(nums, target) {
  let left = 0;
  let right = nums.length - 1;
  while (left <= right) {
    const mid = left + Math.floor((right - left) / 2);
    if (nums[mid] === target) {
      return mid;
    } else if (nums[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }
  return -1;
}
```

#### Java
```java
public class BinarySearch {
    public static int binarySearchIterative(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) {
                return mid;
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }
}
```

**Explanation:** Maintain two pointers `left` and `right` defining the search range. Compute the midpoint using `left + (right - left) / 2` to avoid integer overflow. Compare the middle element with the target: if equal, return the index; if the target is larger, search the right half; otherwise, search the left half. Repeat until the range is exhausted.

**When to use:** Preferred in production code due to constant space usage and no risk of stack overflow. Ideal for searching in large sorted datasets such as database indices, dictionaries, or sorted log files.

### Solution 2: Recursive Binary Search
- **Time Complexity:** O(log n)
- **Space Complexity:** O(log n) — due to recursion stack
- **Difficulty:** Medium

#### Python
```python
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
```

#### JavaScript
```javascript
function binarySearchRecursive(nums, target, left = 0, right = nums.length - 1) {
  if (left > right) {
    return -1;
  }
  const mid = left + Math.floor((right - left) / 2);
  if (nums[mid] === target) {
    return mid;
  } else if (nums[mid] < target) {
    return binarySearchRecursive(nums, target, mid + 1, right);
  } else {
    return binarySearchRecursive(nums, target, left, mid - 1);
  }
}
```

#### Java
```java
public class BinarySearch {
    public static int binarySearchRecursive(int[] nums, int target) {
        return binarySearchHelper(nums, target, 0, nums.length - 1);
    }

    private static int binarySearchHelper(int[] nums, int target, int left, int right) {
        if (left > right) {
            return -1;
        }
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) {
            return mid;
        } else if (nums[mid] < target) {
            return binarySearchHelper(nums, target, mid + 1, right);
        } else {
            return binarySearchHelper(nums, target, left, mid - 1);
        }
    }
}
```

**Explanation:** The logic mirrors the iterative version but uses the call stack to track the current search range. Each recursive call narrows the range by half. The base case `left > right` terminates the search when the target is not found.

**When to use:** Useful when a recursive style fits naturally into the broader algorithm (e.g., divide-and-conquer problems). Cleaner to read for some developers, but avoid on very large arrays due to stack depth limits.

## Variations & Extensions
- **Lower Bound / Upper Bound:** Find the first or last occurrence of a target in a sorted array with duplicates
- **Search in Rotated Sorted Array:** Apply binary search when the array has been rotated at an unknown pivot
- **Search Insert Position:** Return the index where the target would be inserted to keep the array sorted
- **Peak Element:** Find a peak element in an array where neighbors are not equal

## Real-World Applications
- Searching sorted database indices and B-trees
- Autocomplete and dictionary lookup systems
- Version bisecting in Git (`git bisect`) to find the commit that introduced a bug
- Finding insertion points in sorted collections for maintaining order

## Tags
#algorithm #searching #binary-search #divide-and-conquer #medium
