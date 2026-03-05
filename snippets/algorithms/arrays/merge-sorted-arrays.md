# Merge Two Sorted Arrays

## Problem Statement
- Given two sorted arrays, merge them into one sorted array.
- The result should contain all elements from both arrays in sorted order.

**Example inputs/outputs:**
- Input: `[1, 3, 5]`, `[2, 4, 6]` → Output: `[1, 2, 3, 4, 5, 6]`
- Input: `[1, 2, 3]`, `[4, 5, 6]` → Output: `[1, 2, 3, 4, 5, 6]`
- Input: `[]`, `[1, 2, 3]` → Output: `[1, 2, 3]`

**Edge cases:**
- One or both arrays are empty
- Arrays of different lengths
- Arrays with duplicate values
- Arrays with negative numbers

## Solutions

### Solution 1: Two Pointers (New Array)
- **Time Complexity:** O(n + m)
- **Space Complexity:** O(n + m)
- **Difficulty:** Easy

#### Python
```python
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
```

#### JavaScript
```javascript
function mergeSorted(nums1, nums2) {
  const result = [];
  let i = 0;
  let j = 0;
  while (i < nums1.length && j < nums2.length) {
    if (nums1[i] <= nums2[j]) {
      result.push(nums1[i]);
      i++;
    } else {
      result.push(nums2[j]);
      j++;
    }
  }
  while (i < nums1.length) {
    result.push(nums1[i]);
    i++;
  }
  while (j < nums2.length) {
    result.push(nums2[j]);
    j++;
  }
  return result;
}
```

#### Java
```java
public class MergeSortedArrays {
    public static int[] mergeSorted(int[] nums1, int[] nums2) {
        int[] result = new int[nums1.length + nums2.length];
        int i = 0, j = 0, k = 0;
        while (i < nums1.length && j < nums2.length) {
            if (nums1[i] <= nums2[j]) {
                result[k++] = nums1[i++];
            } else {
                result[k++] = nums2[j++];
            }
        }
        while (i < nums1.length) {
            result[k++] = nums1[i++];
        }
        while (j < nums2.length) {
            result[k++] = nums2[j++];
        }
        return result;
    }
}
```

**Explanation:** Maintain two pointers, one for each array. Compare elements at both pointers, append the smaller one to the result, and advance that pointer. After one array is exhausted, append all remaining elements from the other array.

**When to use:** The standard approach for merging sorted sequences. This is the merge step in merge sort and is used whenever two sorted streams need to be combined.

### Solution 2: In-Place Merge (nums1 has extra space)
- **Time Complexity:** O(n + m)
- **Space Complexity:** O(1)
- **Difficulty:** Easy

#### Python
```python
def merge_in_place(nums1, m, nums2, n):
    p1 = m - 1
    p2 = n - 1
    write = m + n - 1
    while p1 >= 0 and p2 >= 0:
        if nums1[p1] >= nums2[p2]:
            nums1[write] = nums1[p1]
            p1 -= 1
        else:
            nums1[write] = nums2[p2]
            p2 -= 1
        write -= 1
    while p2 >= 0:
        nums1[write] = nums2[p2]
        p2 -= 1
        write -= 1
```

#### JavaScript
```javascript
function mergeInPlace(nums1, m, nums2, n) {
  let p1 = m - 1;
  let p2 = n - 1;
  let write = m + n - 1;
  while (p1 >= 0 && p2 >= 0) {
    if (nums1[p1] >= nums2[p2]) {
      nums1[write] = nums1[p1];
      p1--;
    } else {
      nums1[write] = nums2[p2];
      p2--;
    }
    write--;
  }
  while (p2 >= 0) {
    nums1[write] = nums2[p2];
    p2--;
    write--;
  }
}
```

#### Java
```java
public class MergeSortedArrays {
    public static void mergeInPlace(int[] nums1, int m, int[] nums2, int n) {
        int p1 = m - 1;
        int p2 = n - 1;
        int write = m + n - 1;
        while (p1 >= 0 && p2 >= 0) {
            if (nums1[p1] >= nums2[p2]) {
                nums1[write--] = nums1[p1--];
            } else {
                nums1[write--] = nums2[p2--];
            }
        }
        while (p2 >= 0) {
            nums1[write--] = nums2[p2--];
        }
    }
}
```

**Explanation:** When `nums1` has enough trailing space to hold `nums2`, merge from the back. Start writing at the last position and compare elements from the ends of both arrays, placing the larger one at the write pointer. This avoids overwriting unprocessed elements in `nums1`.

**When to use:** Classic LeetCode "Merge Sorted Array" variant. Use when one array already has allocated space at the end and you want to avoid extra memory allocation.

## Variations & Extensions
- **Merge k sorted arrays:** Generalize to merging k sorted arrays using a min-heap
- **Merge sorted linked lists:** Apply the same two-pointer logic to linked list nodes
- **Intersection of two sorted arrays:** Return only the common elements

## Real-World Applications
- Merge sort algorithm (the merge step)
- External sorting for large files that don't fit in memory
- Database merge joins for combining sorted result sets

## Tags
#algorithm #arrays #two-pointers #sorting #easy
