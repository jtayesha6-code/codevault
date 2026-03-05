# Merge Sort

## Problem Statement
- Sort an array of elements in ascending order using the Merge Sort algorithm
- Merge Sort is a stable, divide and conquer algorithm that splits the array in half, recursively sorts each half, and merges the sorted halves
- Example input: `[38, 27, 43, 3, 9, 82, 10]` → Output: `[3, 9, 10, 27, 38, 43, 82]`
- Edge cases: empty array, single element, already sorted, reverse sorted, all duplicate elements

## Solutions

### Solution 1: Top-Down Merge Sort (Recursive)
- **Time Complexity:** O(n log n) in all cases
- **Space Complexity:** O(n) for the temporary arrays
- **Difficulty:** Medium

#### Python
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

#### JavaScript
```javascript
function mergeSort(arr) {
  if (arr.length <= 1) return arr;
  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid));
  const right = mergeSort(arr.slice(mid));
  return merge(left, right);
}

function merge(left, right) {
  const result = [];
  let i = 0, j = 0;
  while (i < left.length && j < right.length) {
    if (left[i] <= right[j]) {
      result.push(left[i++]);
    } else {
      result.push(right[j++]);
    }
  }
  return result.concat(left.slice(i), right.slice(j));
}
```

#### Java
```java
import java.util.Arrays;

public class MergeSort {
    public static int[] mergeSort(int[] arr) {
        if (arr.length <= 1) return arr;
        int mid = arr.length / 2;
        int[] left = mergeSort(Arrays.copyOfRange(arr, 0, mid));
        int[] right = mergeSort(Arrays.copyOfRange(arr, mid, arr.length));
        return merge(left, right);
    }

    private static int[] merge(int[] left, int[] right) {
        int[] result = new int[left.length + right.length];
        int i = 0, j = 0, k = 0;
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                result[k++] = left[i++];
            } else {
                result[k++] = right[j++];
            }
        }
        while (i < left.length) result[k++] = left[i++];
        while (j < right.length) result[k++] = right[j++];
        return result;
    }

    public static void main(String[] args) {
        int[] arr = {38, 27, 43, 3, 9, 82, 10};
        int[] sorted = mergeSort(arr);
        System.out.println(Arrays.toString(sorted));
    }
}
```

**Explanation:**
1. Divide the array into two halves at the midpoint
2. Recursively sort each half until sub-arrays have one or zero elements
3. Merge two sorted halves by comparing elements one by one and placing the smaller element first
4. Append any remaining elements from either half
5. The `<=` comparison ensures stability (equal elements maintain their original order)

**When to use:** When stable sorting is required, or when worst-case O(n log n) performance is needed regardless of input order.

### Solution 2: In-Place Merge Sort
- **Time Complexity:** O(n log n)
- **Space Complexity:** O(n) for the temporary buffer during merge
- **Difficulty:** Medium

#### Python
```python
def merge_sort_inplace(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left < right:
        mid = left + (right - left) // 2
        merge_sort_inplace(arr, left, mid)
        merge_sort_inplace(arr, mid + 1, right)
        merge_inplace(arr, left, mid, right)
    return arr

def merge_inplace(arr, left, mid, right):
    temp = arr[left:right + 1]
    i = 0
    j = mid - left + 1
    k = left
    length = right - left + 1
    while i <= mid - left and j < length:
        if temp[i] <= temp[j]:
            arr[k] = temp[i]
            i += 1
        else:
            arr[k] = temp[j]
            j += 1
        k += 1
    while i <= mid - left:
        arr[k] = temp[i]
        i += 1
        k += 1
    while j < length:
        arr[k] = temp[j]
        j += 1
        k += 1
```

#### JavaScript
```javascript
function mergeSortInPlace(arr, left = 0, right = arr.length - 1) {
  if (left < right) {
    const mid = left + Math.floor((right - left) / 2);
    mergeSortInPlace(arr, left, mid);
    mergeSortInPlace(arr, mid + 1, right);
    mergeInPlace(arr, left, mid, right);
  }
  return arr;
}

function mergeInPlace(arr, left, mid, right) {
  const temp = arr.slice(left, right + 1);
  let i = 0;
  let j = mid - left + 1;
  let k = left;
  const length = right - left + 1;
  while (i <= mid - left && j < length) {
    if (temp[i] <= temp[j]) {
      arr[k++] = temp[i++];
    } else {
      arr[k++] = temp[j++];
    }
  }
  while (i <= mid - left) arr[k++] = temp[i++];
  while (j < length) arr[k++] = temp[j++];
}
```

#### Java
```java
import java.util.Arrays;

public class MergeSortInPlace {
    public static void mergeSort(int[] arr, int left, int right) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            mergeSort(arr, left, mid);
            mergeSort(arr, mid + 1, right);
            merge(arr, left, mid, right);
        }
    }

    private static void merge(int[] arr, int left, int mid, int right) {
        int[] temp = Arrays.copyOfRange(arr, left, right + 1);
        int i = 0;
        int j = mid - left + 1;
        int k = left;
        int length = right - left + 1;
        while (i <= mid - left && j < length) {
            if (temp[i] <= temp[j]) {
                arr[k++] = temp[i++];
            } else {
                arr[k++] = temp[j++];
            }
        }
        while (i <= mid - left) arr[k++] = temp[i++];
        while (j < length) arr[k++] = temp[j++];
    }

    public static void main(String[] args) {
        int[] arr = {38, 27, 43, 3, 9, 82, 10};
        mergeSort(arr, 0, arr.length - 1);
        System.out.println(Arrays.toString(arr));
    }
}
```

**Explanation:**
1. Divide the array by computing the midpoint index
2. Recursively sort the left half `[left..mid]` and the right half `[mid+1..right]`
3. Copy the segment to a temporary buffer, then merge back into the original array
4. This modifies the original array rather than returning a new one

**When to use:** When you want to sort in place and avoid creating new array objects at each recursive call, while still using a temporary buffer for merging.

## Variations & Extensions
- **Bottom-Up Merge Sort:** Iterative approach that merges sub-arrays of increasing size (1, 2, 4, 8, ...)
- **Natural Merge Sort:** Takes advantage of existing sorted runs in the input
- **Linked List Merge Sort:** Particularly efficient for linked lists since merging doesn't require extra space
- **External Merge Sort:** Used when data doesn't fit in memory (e.g., sorting large files)

## Real-World Applications
- Python's `sorted()` and `list.sort()` use Timsort, a hybrid of Merge Sort and Insertion Sort
- External sorting for large datasets that exceed available RAM
- Sorting linked lists where random access is expensive
- Counting inversions in an array (modified merge sort)
- Stable sorting requirement in database engines

## Tags
#algorithm #sorting #divide-and-conquer #stable-sort #medium
