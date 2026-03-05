# Two Sum Problem

## Problem Statement
- Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.
- Each input has exactly one solution, and you may not use the same element twice.

**Example inputs/outputs:**
- Input: `nums = [2, 7, 11, 15]`, `target = 9` → Output: `[0, 1]`
- Input: `nums = [3, 2, 4]`, `target = 6` → Output: `[1, 2]`
- Input: `nums = [3, 3]`, `target = 6` → Output: `[0, 1]`

**Edge cases:**
- Array with exactly two elements
- Negative numbers in the array
- Duplicate values that sum to target

## Solutions

### Solution 1: Brute Force
- **Time Complexity:** O(n²)
- **Space Complexity:** O(1)
- **Difficulty:** Easy

#### Python
```python
def two_sum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

#### JavaScript
```javascript
function twoSumBrute(nums, target) {
  for (let i = 0; i < nums.length; i++) {
    for (let j = i + 1; j < nums.length; j++) {
      if (nums[i] + nums[j] === target) {
        return [i, j];
      }
    }
  }
  return [];
}
```

#### Java
```java
public class TwoSum {
    public static int[] twoSumBrute(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target) {
                    return new int[]{i, j};
                }
            }
        }
        return new int[]{};
    }
}
```

**Explanation:** Check every pair of elements. For each element at index `i`, iterate through all subsequent elements at index `j` and check if their sum equals the target.

**When to use:** Acceptable for small input sizes or when space is extremely constrained. Simple to implement and easy to verify correctness.

### Solution 2: Hash Map
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)
- **Difficulty:** Easy

#### Python
```python
def two_sum_hashmap(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

#### JavaScript
```javascript
function twoSumHashMap(nums, target) {
  const seen = new Map();
  for (let i = 0; i < nums.length; i++) {
    const complement = target - nums[i];
    if (seen.has(complement)) {
      return [seen.get(complement), i];
    }
    seen.set(nums[i], i);
  }
  return [];
}
```

#### Java
```java
import java.util.HashMap;
import java.util.Map;

public class TwoSum {
    public static int[] twoSumHashMap(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (seen.containsKey(complement)) {
                return new int[]{seen.get(complement), i};
            }
            seen.put(nums[i], i);
        }
        return new int[]{};
    }
}
```

**Explanation:** Use a hash map to store each number and its index as we iterate. For each element, compute its complement (`target - num`) and check if it already exists in the map. If found, return both indices.

**When to use:** Preferred for large datasets. The single-pass approach is optimal for interview settings and production code where time complexity matters.

## Variations & Extensions
- **Three Sum:** Find all unique triplets that sum to zero
- **Two Sum II (Sorted Array):** Use two pointers when input is sorted
- **Two Sum with multiple pairs:** Return all pairs that sum to target

## Real-World Applications
- Financial reconciliation: matching transactions that balance to a specific amount
- Pair matching in recommendation systems
- Load balancing: distributing tasks across two servers to hit a resource target

## Tags
#algorithm #arrays #hash-map #easy
