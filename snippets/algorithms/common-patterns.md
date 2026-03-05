# Common Algorithm Patterns

## Overview
Recognizing patterns is the fastest way to solve coding problems. This guide covers the most frequently encountered algorithmic patterns with templates, examples, and guidance on when to apply each one.

---

## 1. Two Pointers

### When to Use
- Sorted array or linked list
- Finding pairs/triplets that satisfy a condition
- Comparing elements from both ends
- Removing duplicates in-place

### Template

#### Python
```python
def two_pointer_opposite(arr, target):
    """Two pointers moving inward from both ends (sorted array)."""
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []


def two_pointer_same_direction(arr):
    """Two pointers moving in the same direction (e.g., remove duplicates)."""
    if not arr:
        return 0
    slow = 0
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
    return slow + 1
```

#### JavaScript
```javascript
function twoPointerOpposite(arr, target) {
  let left = 0, right = arr.length - 1;
  while (left < right) {
    const sum = arr[left] + arr[right];
    if (sum === target) return [left, right];
    else if (sum < target) left++;
    else right--;
  }
  return [];
}

function twoPointerSameDirection(arr) {
  if (arr.length === 0) return 0;
  let slow = 0;
  for (let fast = 1; fast < arr.length; fast++) {
    if (arr[fast] !== arr[slow]) {
      slow++;
      arr[slow] = arr[fast];
    }
  }
  return slow + 1;
}
```

### Classic Problems
- Two Sum (sorted array)
- 3Sum / 4Sum
- Container With Most Water
- Remove Duplicates from Sorted Array
- Trapping Rain Water

---

## 2. Sliding Window

### When to Use
- Contiguous subarray/substring problems
- Finding max/min/target sum in a window
- String permutation or anagram matching
- Fixed-size or variable-size window

### Template

#### Python
```python
def sliding_window_fixed(arr, k):
    """Fixed-size window of length k."""
    window_sum = sum(arr[:k])
    max_sum = window_sum

    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)

    return max_sum


def sliding_window_variable(s, target):
    """Variable-size window — smallest subarray with sum >= target."""
    left = 0
    current_sum = 0
    min_len = float("inf")

    for right in range(len(s)):
        current_sum += s[right]
        while current_sum >= target:
            min_len = min(min_len, right - left + 1)
            current_sum -= s[left]
            left += 1

    return min_len if min_len != float("inf") else 0
```

#### JavaScript
```javascript
function slidingWindowFixed(arr, k) {
  let windowSum = arr.slice(0, k).reduce((a, b) => a + b, 0);
  let maxSum = windowSum;

  for (let i = k; i < arr.length; i++) {
    windowSum += arr[i] - arr[i - k];
    maxSum = Math.max(maxSum, windowSum);
  }
  return maxSum;
}

function slidingWindowVariable(arr, target) {
  let left = 0, currentSum = 0, minLen = Infinity;

  for (let right = 0; right < arr.length; right++) {
    currentSum += arr[right];
    while (currentSum >= target) {
      minLen = Math.min(minLen, right - left + 1);
      currentSum -= arr[left++];
    }
  }
  return minLen === Infinity ? 0 : minLen;
}
```

### Classic Problems
- Maximum Sum Subarray of Size K
- Longest Substring Without Repeating Characters
- Minimum Window Substring
- Fruit Into Baskets
- Permutation in String

---

## 3. Fast & Slow Pointers (Floyd's Tortoise & Hare)

### When to Use
- Detecting cycles in a linked list or array
- Finding the middle of a linked list
- Finding the start of a cycle
- Determining if a number is a happy number

### Template

#### Python
```python
def has_cycle(head):
    """Detect cycle in a linked list."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False


def find_cycle_start(head):
    """Find where the cycle begins."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Reset one pointer to head
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None


def find_middle(head):
    """Find the middle node of a linked list."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

#### JavaScript
```javascript
function hasCycle(head) {
  let slow = head, fast = head;
  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow === fast) return true;
  }
  return false;
}

function findCycleStart(head) {
  let slow = head, fast = head;
  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow === fast) {
      slow = head;
      while (slow !== fast) {
        slow = slow.next;
        fast = fast.next;
      }
      return slow;
    }
  }
  return null;
}

function findMiddle(head) {
  let slow = head, fast = head;
  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
  }
  return slow;
}
```

### Classic Problems
- Linked List Cycle / Cycle II
- Happy Number
- Find the Duplicate Number
- Middle of the Linked List
- Palindrome Linked List

---

## 4. Merge Intervals

### When to Use
- Problems involving overlapping intervals
- Merging or inserting intervals
- Scheduling / meeting room problems
- Finding free time slots

### Template

#### Python
```python
def merge_intervals(intervals):
    """Merge overlapping intervals."""
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged


def insert_interval(intervals, new):
    """Insert a new interval and merge if necessary."""
    result = []
    i = 0

    # Add all intervals ending before new starts
    while i < len(intervals) and intervals[i][1] < new[0]:
        result.append(intervals[i])
        i += 1

    # Merge overlapping intervals
    while i < len(intervals) and intervals[i][0] <= new[1]:
        new[0] = min(new[0], intervals[i][0])
        new[1] = max(new[1], intervals[i][1])
        i += 1
    result.append(new)

    # Add remaining intervals
    result.extend(intervals[i:])
    return result
```

#### JavaScript
```javascript
function mergeIntervals(intervals) {
  intervals.sort((a, b) => a[0] - b[0]);
  const merged = [intervals[0]];

  for (let i = 1; i < intervals.length; i++) {
    const last = merged[merged.length - 1];
    if (intervals[i][0] <= last[1]) {
      last[1] = Math.max(last[1], intervals[i][1]);
    } else {
      merged.push(intervals[i]);
    }
  }
  return merged;
}
```

### Classic Problems
- Merge Intervals
- Insert Interval
- Meeting Rooms I & II
- Non-overlapping Intervals
- Employee Free Time

---

## 5. Cyclic Sort

### When to Use
- Array contains numbers in range [1, n] or [0, n]
- Finding missing/duplicate numbers
- Input is a permutation (or close to one)

### Template

#### Python
```python
def cyclic_sort(nums):
    """Sort numbers in range [1, n] in O(n) time, O(1) space."""
    i = 0
    while i < len(nums):
        correct = nums[i] - 1  # where nums[i] should be
        if nums[i] != nums[correct]:
            nums[i], nums[correct] = nums[correct], nums[i]
        else:
            i += 1
    return nums


def find_missing_number(nums):
    """Find the missing number in [0, n]."""
    i = 0
    n = len(nums)
    while i < n:
        if nums[i] < n and nums[i] != i:
            nums[nums[i]], nums[i] = nums[i], nums[nums[i]]
        else:
            i += 1

    for i in range(n):
        if nums[i] != i:
            return i
    return n


def find_duplicate(nums):
    """Find the duplicate in [1, n] where len = n + 1."""
    i = 0
    while i < len(nums):
        correct = nums[i] - 1
        if nums[i] != nums[correct]:
            nums[i], nums[correct] = nums[correct], nums[i]
        else:
            i += 1

    for i in range(len(nums)):
        if nums[i] != i + 1:
            return nums[i]
    return -1
```

#### JavaScript
```javascript
function cyclicSort(nums) {
  let i = 0;
  while (i < nums.length) {
    const correct = nums[i] - 1;
    if (nums[i] !== nums[correct]) {
      [nums[i], nums[correct]] = [nums[correct], nums[i]];
    } else {
      i++;
    }
  }
  return nums;
}

function findMissingNumber(nums) {
  let i = 0;
  const n = nums.length;
  while (i < n) {
    if (nums[i] < n && nums[i] !== i) {
      [nums[nums[i]], nums[i]] = [nums[i], nums[nums[i]]];
    } else {
      i++;
    }
  }
  for (let i = 0; i < n; i++) {
    if (nums[i] !== i) return i;
  }
  return n;
}
```

### Classic Problems
- Find the Missing Number
- Find All Missing Numbers
- Find the Duplicate Number
- Find All Duplicates
- Find the Corrupt Pair

---

## 6. BFS (Breadth-First Search)

### When to Use
- Shortest path in unweighted graphs
- Level-order traversal of trees
- Finding connected components
- Problems asking for minimum steps/moves

### Template

#### Python
```python
from collections import deque

def bfs_graph(graph, start):
    """BFS traversal of a graph."""
    visited = {start}
    queue = deque([start])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result


def bfs_level_order(root):
    """Level-order traversal of a binary tree."""
    if not root:
        return []
    result = []
    queue = deque([root])

    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)

    return result
```

#### JavaScript
```javascript
function bfsGraph(graph, start) {
  const visited = new Set([start]);
  const queue = [start];
  const result = [];

  while (queue.length > 0) {
    const node = queue.shift();
    result.push(node);

    for (const neighbor of graph[node]) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push(neighbor);
      }
    }
  }
  return result;
}
```

### Classic Problems
- Binary Tree Level Order Traversal
- Shortest Path in Binary Matrix
- Rotting Oranges
- Word Ladder
- Number of Islands (BFS variant)

---

## 7. DFS (Depth-First Search)

### When to Use
- Exploring all paths or checking connectivity
- Detecting cycles in graphs
- Topological sorting
- Solving puzzles (mazes, permutations)
- Tree traversal (preorder, inorder, postorder)

### Template

#### Python
```python
def dfs_recursive(graph, node, visited=None):
    """DFS traversal — recursive."""
    if visited is None:
        visited = set()
    visited.add(node)
    result = [node]

    for neighbor in graph[node]:
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))

    return result


def dfs_iterative(graph, start):
    """DFS traversal — iterative with stack."""
    visited = set()
    stack = [start]
    result = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)

    return result
```

#### JavaScript
```javascript
function dfsRecursive(graph, node, visited = new Set()) {
  visited.add(node);
  const result = [node];

  for (const neighbor of graph[node]) {
    if (!visited.has(neighbor)) {
      result.push(...dfsRecursive(graph, neighbor, visited));
    }
  }
  return result;
}

function dfsIterative(graph, start) {
  const visited = new Set();
  const stack = [start];
  const result = [];

  while (stack.length > 0) {
    const node = stack.pop();
    if (visited.has(node)) continue;
    visited.add(node);
    result.push(node);

    for (const neighbor of graph[node]) {
      if (!visited.has(neighbor)) stack.push(neighbor);
    }
  }
  return result;
}
```

### Classic Problems
- Number of Islands
- Clone Graph
- Course Schedule (cycle detection)
- Path Sum I / II / III
- All Paths From Source to Target

---

## Pattern Selection Guide

| Problem Characteristics | Pattern |
|:---|:---|
| Sorted array, find pair with condition | Two Pointers |
| Contiguous subarray/substring optimization | Sliding Window |
| Linked list cycle or middle element | Fast & Slow Pointers |
| Overlapping intervals or scheduling | Merge Intervals |
| Numbers in range [1, n], find missing/duplicate | Cyclic Sort |
| Shortest path, level-by-level processing | BFS |
| Explore all paths, connectivity, tree traversal | DFS |

## Tags
#algorithms #patterns #reference #two-pointers #sliding-window #bfs #dfs
