# Find Duplicate in Array

## Problem Statement
- Given an array of `n + 1` integers where each integer is in the range `[1, n]`, find the one duplicate number.
- There is exactly one duplicate number, but it may appear more than twice.

**Example inputs/outputs:**
- Input: `[1, 3, 4, 2, 2]` → Output: `2`
- Input: `[3, 1, 3, 4, 2]` → Output: `3`
- Input: `[1, 1]` → Output: `1`

**Edge cases:**
- Minimum array size of 2 (e.g., `[1, 1]`)
- Duplicate appears more than twice
- Duplicate is the largest or smallest value in the range

## Solutions

### Solution 1: Hash Set
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)
- **Difficulty:** Easy

#### Python
```python
def find_duplicate_hashset(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)
    return -1
```

#### JavaScript
```javascript
function findDuplicateHashSet(nums) {
  const seen = new Set();
  for (const num of nums) {
    if (seen.has(num)) {
      return num;
    }
    seen.add(num);
  }
  return -1;
}
```

#### Java
```java
import java.util.HashSet;
import java.util.Set;

public class FindDuplicate {
    public static int findDuplicateHashSet(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int num : nums) {
            if (seen.contains(num)) {
                return num;
            }
            seen.add(num);
        }
        return -1;
    }
}
```

**Explanation:** Iterate through the array, adding each element to a hash set. Before adding, check if the element is already in the set. The first element found in the set is the duplicate.

**When to use:** Simple and intuitive. Use when extra O(n) space is acceptable and you want straightforward, readable code.

### Solution 2: Floyd's Cycle Detection (Tortoise and Hare)
- **Time Complexity:** O(n)
- **Space Complexity:** O(1)
- **Difficulty:** Easy

#### Python
```python
def find_duplicate_floyd(nums):
    slow = nums[0]
    fast = nums[0]

    # Phase 1: detect cycle
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: find cycle entrance (the duplicate)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow
```

#### JavaScript
```javascript
function findDuplicateFloyd(nums) {
  let slow = nums[0];
  let fast = nums[0];

  // Phase 1: detect cycle
  do {
    slow = nums[slow];
    fast = nums[nums[fast]];
  } while (slow !== fast);

  // Phase 2: find cycle entrance (the duplicate)
  slow = nums[0];
  while (slow !== fast) {
    slow = nums[slow];
    fast = nums[fast];
  }

  return slow;
}
```

#### Java
```java
public class FindDuplicate {
    public static int findDuplicateFloyd(int[] nums) {
        int slow = nums[0];
        int fast = nums[0];

        // Phase 1: detect cycle
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);

        // Phase 2: find cycle entrance (the duplicate)
        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }

        return slow;
    }
}
```

**Explanation:** Treat the array as a linked list where `nums[i]` points to the next node. Since there is a duplicate, a cycle must exist. Use Floyd's algorithm: move a slow pointer one step and a fast pointer two steps until they meet (cycle detected). Then reset slow to the start and advance both one step at a time — they meet at the cycle entrance, which is the duplicate value.

**When to use:** Optimal when you cannot modify the array and need O(1) space. A classic technique for linked list cycle problems adapted to arrays.

## Variations & Extensions
- **Find all duplicates:** Return all elements that appear twice in an array of `[1, n]`
- **Missing number:** Find the missing number in `[0, n]` with one number absent
- **Find duplicate and missing:** Identify both the duplicate and the missing number

## Real-World Applications
- Data integrity checks: detecting duplicate records in databases
- Network packet deduplication
- File system consistency checks for duplicate inodes

## Tags
#algorithm #arrays #hash-set #cycle-detection #easy
