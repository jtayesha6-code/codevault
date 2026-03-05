# Quick Sort

## Problem Statement
- Sort an array of elements in ascending order using the Quick Sort algorithm
- Quick Sort is a divide and conquer algorithm that selects a "pivot" element, partitions the array around the pivot, and recursively sorts the sub-arrays
- Example input: `[10, 7, 8, 9, 1, 5]` → Output: `[1, 5, 7, 8, 9, 10]`
- Edge cases: empty array, single element, already sorted, reverse sorted, all duplicate elements

## Solutions

### Solution 1: Lomuto Partition Scheme
- **Time Complexity:** O(n log n) average, O(n²) worst case
- **Space Complexity:** O(log n) due to recursion stack
- **Difficulty:** Medium

#### Python
```python
def quick_sort_lomuto(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_index = lomuto_partition(arr, low, high)
        quick_sort_lomuto(arr, low, pivot_index - 1)
        quick_sort_lomuto(arr, pivot_index + 1, high)
    return arr

def lomuto_partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

#### JavaScript
```javascript
function quickSortLomuto(arr, low = 0, high = arr.length - 1) {
  if (low < high) {
    const pivotIndex = lomutoPartition(arr, low, high);
    quickSortLomuto(arr, low, pivotIndex - 1);
    quickSortLomuto(arr, pivotIndex + 1, high);
  }
  return arr;
}

function lomutoPartition(arr, low, high) {
  const pivot = arr[high];
  let i = low - 1;
  for (let j = low; j < high; j++) {
    if (arr[j] <= pivot) {
      i++;
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
  }
  [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
  return i + 1;
}
```

#### Java
```java
public class QuickSortLomuto {
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = lomutoPartition(arr, low, high);
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }

    private static int lomutoPartition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;
        return i + 1;
    }

    public static void main(String[] args) {
        int[] arr = {10, 7, 8, 9, 1, 5};
        quickSort(arr, 0, arr.length - 1);
        for (int val : arr) System.out.print(val + " ");
    }
}
```

**Explanation:**
1. Choose the last element as the pivot
2. Maintain a pointer `i` for the boundary of elements less than or equal to the pivot
3. Iterate through the array with pointer `j`; when `arr[j] <= pivot`, increment `i` and swap `arr[i]` with `arr[j]`
4. After the loop, place the pivot in its correct position at `i + 1`
5. Recursively sort the left and right sub-arrays

**When to use:** Simple to implement and understand; good default choice for in-place sorting when average-case performance matters.

### Solution 2: Hoare Partition Scheme
- **Time Complexity:** O(n log n) average, O(n²) worst case
- **Space Complexity:** O(log n) due to recursion stack
- **Difficulty:** Medium

#### Python
```python
def quick_sort_hoare(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_index = hoare_partition(arr, low, high)
        quick_sort_hoare(arr, low, pivot_index)
        quick_sort_hoare(arr, pivot_index + 1, high)
    return arr

def hoare_partition(arr, low, high):
    pivot = arr[low + (high - low) // 2]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        j -= 1
        while arr[j] > pivot:
            j -= 1
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]
```

#### JavaScript
```javascript
function quickSortHoare(arr, low = 0, high = arr.length - 1) {
  if (low < high) {
    const pivotIndex = hoarePartition(arr, low, high);
    quickSortHoare(arr, low, pivotIndex);
    quickSortHoare(arr, pivotIndex + 1, high);
  }
  return arr;
}

function hoarePartition(arr, low, high) {
  const pivot = arr[low + Math.floor((high - low) / 2)];
  let i = low - 1;
  let j = high + 1;
  while (true) {
    do { i++; } while (arr[i] < pivot);
    do { j--; } while (arr[j] > pivot);
    if (i >= j) return j;
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
}
```

#### Java
```java
public class QuickSortHoare {
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = hoarePartition(arr, low, high);
            quickSort(arr, low, pivotIndex);
            quickSort(arr, pivotIndex + 1, high);
        }
    }

    private static int hoarePartition(int[] arr, int low, int high) {
        int pivot = arr[low + (high - low) / 2];
        int i = low - 1;
        int j = high + 1;
        while (true) {
            do { i++; } while (arr[i] < pivot);
            do { j--; } while (arr[j] > pivot);
            if (i >= j) return j;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }

    public static void main(String[] args) {
        int[] arr = {10, 7, 8, 9, 1, 5};
        quickSort(arr, 0, arr.length - 1);
        for (int val : arr) System.out.print(val + " ");
    }
}
```

**Explanation:**
1. Select the middle element as the pivot to reduce worst-case likelihood
2. Use two pointers `i` and `j` starting from opposite ends
3. Move `i` forward until an element >= pivot is found; move `j` backward until an element <= pivot is found
4. Swap elements at `i` and `j` if they haven't crossed
5. Return `j` as the partition point when pointers cross

**When to use:** Hoare's scheme performs fewer swaps on average than Lomuto's. Preferred in performance-critical applications.

## Variations & Extensions
- **Randomized Quick Sort:** Choose a random pivot to avoid worst-case on sorted input
- **Three-way partitioning (Dutch National Flag):** Efficient when there are many duplicate elements
- **Iterative Quick Sort:** Use an explicit stack to eliminate recursion overhead
- **Introsort:** Hybrid of Quick Sort, Heap Sort, and Insertion Sort used in many standard libraries

## Real-World Applications
- Default sorting algorithm in many standard libraries (e.g., C `qsort`, Java `Arrays.sort` for primitives)
- Database query engines for sorting result sets
- File system directory listing
- Numerical computing and scientific simulations

## Tags
#algorithm #sorting #divide-and-conquer #medium
