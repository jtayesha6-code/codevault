# Median of Two Sorted Arrays

## Problem Statement
- Given two sorted arrays `nums1` and `nums2`, return the median of the combined sorted array
- The overall run time complexity should be O(log(min(n, m)))
- The median is the middle value if the total length is odd, or the average of the two middle values if even

**Example:**
```
Input:  nums1 = [1, 3], nums2 = [2]
Output: 2.0

Input:  nums1 = [1, 2], nums2 = [3, 4]
Output: 2.5  → (2 + 3) / 2

Input:  nums1 = [], nums2 = [1]
Output: 1.0
```

**Edge Cases:**
- One or both arrays are empty
- Arrays of very different lengths
- All elements in one array are smaller than all elements in the other
- Arrays with duplicate values

## Solutions

### Solution 1: Merge Approach
- **Time Complexity:** O(n + m)
- **Space Complexity:** O(n + m)
- **Difficulty:** Medium

#### Python
```python
def find_median_merge(nums1, nums2):
    """Find median by merging two sorted arrays."""
    merged = []
    i = j = 0

    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1

    merged.extend(nums1[i:])
    merged.extend(nums2[j:])

    n = len(merged)
    if n % 2 == 1:
        return float(merged[n // 2])
    return (merged[n // 2 - 1] + merged[n // 2]) / 2.0


# Examples
print(find_median_merge([1, 3], [2]))        # 2.0
print(find_median_merge([1, 2], [3, 4]))     # 2.5
print(find_median_merge([], [1]))            # 1.0
```

#### JavaScript
```javascript
function findMedianMerge(nums1, nums2) {
  const merged = [];
  let i = 0, j = 0;

  while (i < nums1.length && j < nums2.length) {
    if (nums1[i] <= nums2[j]) {
      merged.push(nums1[i++]);
    } else {
      merged.push(nums2[j++]);
    }
  }

  while (i < nums1.length) merged.push(nums1[i++]);
  while (j < nums2.length) merged.push(nums2[j++]);

  const n = merged.length;
  if (n % 2 === 1) return merged[Math.floor(n / 2)];
  return (merged[Math.floor(n / 2) - 1] + merged[Math.floor(n / 2)]) / 2;
}

// Examples
console.log(findMedianMerge([1, 3], [2]));     // 2
console.log(findMedianMerge([1, 2], [3, 4]));  // 2.5
console.log(findMedianMerge([], [1]));          // 1
```

#### Java
```java
public class MedianTwoSortedArrays {

    public static double findMedianMerge(int[] nums1, int[] nums2) {
        int[] merged = new int[nums1.length + nums2.length];
        int i = 0, j = 0, k = 0;

        while (i < nums1.length && j < nums2.length) {
            if (nums1[i] <= nums2[j]) {
                merged[k++] = nums1[i++];
            } else {
                merged[k++] = nums2[j++];
            }
        }
        while (i < nums1.length) merged[k++] = nums1[i++];
        while (j < nums2.length) merged[k++] = nums2[j++];

        int n = merged.length;
        if (n % 2 == 1) return merged[n / 2];
        return (merged[n / 2 - 1] + merged[n / 2]) / 2.0;
    }

    public static void main(String[] args) {
        System.out.println(findMedianMerge(new int[]{1, 3}, new int[]{2}));     // 2.0
        System.out.println(findMedianMerge(new int[]{1, 2}, new int[]{3, 4})); // 2.5
        System.out.println(findMedianMerge(new int[]{}, new int[]{1}));         // 1.0
    }
}
```

**Explanation:**
1. Use two pointers to merge both sorted arrays into one sorted array
2. Pick the smaller element at each step to maintain sort order
3. After merging, find the median from the middle element(s)

**When to use:** When simplicity is preferred over optimal performance, or when the arrays are small enough that O(n + m) is acceptable.

### Solution 2: Binary Search (Optimal)
- **Time Complexity:** O(log(min(n, m)))
- **Space Complexity:** O(1)
- **Difficulty:** Hard

#### Python
```python
def find_median_binary_search(nums1, nums2):
    """Find median using binary search on the shorter array."""
    # Ensure nums1 is the shorter array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    lo, hi = 0, m
    half = (m + n + 1) // 2

    while lo <= hi:
        i = (lo + hi) // 2        # partition index in nums1
        j = half - i               # partition index in nums2

        left1 = nums1[i - 1] if i > 0 else float("-inf")
        right1 = nums1[i] if i < m else float("inf")
        left2 = nums2[j - 1] if j > 0 else float("-inf")
        right2 = nums2[j] if j < n else float("inf")

        if left1 <= right2 and left2 <= right1:
            # Correct partition found
            if (m + n) % 2 == 1:
                return float(max(left1, left2))
            return (max(left1, left2) + min(right1, right2)) / 2.0
        elif left1 > right2:
            hi = i - 1  # move partition left in nums1
        else:
            lo = i + 1  # move partition right in nums1

    raise ValueError("Input arrays are not sorted")


# Examples
print(find_median_binary_search([1, 3], [2]))        # 2.0
print(find_median_binary_search([1, 2], [3, 4]))     # 2.5
print(find_median_binary_search([], [1]))             # 1.0
print(find_median_binary_search([2], []))             # 2.0
print(find_median_binary_search([1, 3, 5], [2, 4, 6]))  # 3.5
```

#### JavaScript
```javascript
function findMedianBinarySearch(nums1, nums2) {
  // Ensure nums1 is the shorter array
  if (nums1.length > nums2.length) {
    [nums1, nums2] = [nums2, nums1];
  }

  const m = nums1.length;
  const n = nums2.length;
  let lo = 0, hi = m;
  const half = Math.floor((m + n + 1) / 2);

  while (lo <= hi) {
    const i = Math.floor((lo + hi) / 2);
    const j = half - i;

    const left1 = i > 0 ? nums1[i - 1] : -Infinity;
    const right1 = i < m ? nums1[i] : Infinity;
    const left2 = j > 0 ? nums2[j - 1] : -Infinity;
    const right2 = j < n ? nums2[j] : Infinity;

    if (left1 <= right2 && left2 <= right1) {
      if ((m + n) % 2 === 1) return Math.max(left1, left2);
      return (Math.max(left1, left2) + Math.min(right1, right2)) / 2;
    } else if (left1 > right2) {
      hi = i - 1;
    } else {
      lo = i + 1;
    }
  }

  throw new Error("Input arrays are not sorted");
}

// Examples
console.log(findMedianBinarySearch([1, 3], [2]));           // 2
console.log(findMedianBinarySearch([1, 2], [3, 4]));        // 2.5
console.log(findMedianBinarySearch([], [1]));                // 1
console.log(findMedianBinarySearch([1, 3, 5], [2, 4, 6]));  // 3.5
```

#### Java
```java
public class MedianTwoSortedArraysBinarySearch {

    public static double findMedian(int[] nums1, int[] nums2) {
        // Ensure nums1 is the shorter array
        if (nums1.length > nums2.length) {
            int[] temp = nums1;
            nums1 = nums2;
            nums2 = temp;
        }

        int m = nums1.length, n = nums2.length;
        int lo = 0, hi = m;
        int half = (m + n + 1) / 2;

        while (lo <= hi) {
            int i = (lo + hi) / 2;
            int j = half - i;

            int left1 = (i > 0) ? nums1[i - 1] : Integer.MIN_VALUE;
            int right1 = (i < m) ? nums1[i] : Integer.MAX_VALUE;
            int left2 = (j > 0) ? nums2[j - 1] : Integer.MIN_VALUE;
            int right2 = (j < n) ? nums2[j] : Integer.MAX_VALUE;

            if (left1 <= right2 && left2 <= right1) {
                if ((m + n) % 2 == 1) {
                    return Math.max(left1, left2);
                }
                return (Math.max(left1, left2) + Math.min(right1, right2)) / 2.0;
            } else if (left1 > right2) {
                hi = i - 1;
            } else {
                lo = i + 1;
            }
        }

        throw new IllegalArgumentException("Input arrays are not sorted");
    }

    public static void main(String[] args) {
        System.out.println(findMedian(new int[]{1, 3}, new int[]{2}));          // 2.0
        System.out.println(findMedian(new int[]{1, 2}, new int[]{3, 4}));      // 2.5
        System.out.println(findMedian(new int[]{}, new int[]{1}));              // 1.0
        System.out.println(findMedian(new int[]{1, 3, 5}, new int[]{2, 4, 6})); // 3.5
    }
}
```

**Explanation:**
1. Always binary search on the shorter array to minimize iterations
2. Partition both arrays such that the left half contains exactly `(m + n + 1) / 2` elements
3. The partition is valid when the largest element on the left side of each array is ≤ the smallest element on the right side of the other array
4. If `left1 > right2`, the partition in nums1 is too far right → move left
5. If `left2 > right1`, the partition in nums1 is too far left → move right
6. Once the correct partition is found, the median is computed from the boundary elements

**When to use:** When optimal O(log(min(n, m))) time is required, especially for large arrays. This is a classic interview question testing binary search mastery.

## Variations & Extensions
- **Kth smallest element** in two sorted arrays (generalization)
- **Median of K sorted arrays** using a min-heap
- **Median in a data stream** using two heaps
- **Weighted median** where elements have associated weights

## Real-World Applications
- Database query optimization for merging sorted indexes
- Statistical analysis on partitioned data sets
- Real-time median computation in streaming systems
- Load balancing across sorted server response times

## Tags
#binary-search #arrays #hard #divide-and-conquer #two-pointers
