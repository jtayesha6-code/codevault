# Linked List Cycle Detection

## Problem Statement
- Determine whether a singly linked list contains a cycle (a node's `next` pointer points back to a previously visited node)
- If a cycle exists, find the node where the cycle begins
- Example: `1 → 2 → 3 → 4 → 5 → 3` (cycle starts at node 3) → Output: cycle detected, start = node 3
- Example: `1 → 2 → 3 → None` → Output: no cycle
- Edge cases: empty list, single node with self-loop, single node without cycle, cycle at the head

## Solutions

### Solution 1: Floyd's Tortoise and Hare — Cycle Detection
- **Time Complexity:** O(n)
- **Space Complexity:** O(1)
- **Difficulty:** Medium

#### Python
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def has_cycle(head):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

#### JavaScript
```javascript
class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

function hasCycle(head) {
  let slow = head;
  let fast = head;
  while (fast !== null && fast.next !== null) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow === fast) return true;
  }
  return false;
}
```

#### Java
```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

public class CycleDetection {
    public static boolean hasCycle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }
}
```

**Explanation:**
1. Initialize two pointers, `slow` and `fast`, both starting at the head
2. Move `slow` one step at a time and `fast` two steps at a time
3. If there is a cycle, `fast` will eventually meet `slow` inside the cycle
4. If `fast` reaches `null`, there is no cycle
5. This works because in a cycle, the fast pointer closes the gap by one node per iteration

**When to use:** When you need to detect cycles in constant space without modifying the list.

### Solution 2: Floyd's Algorithm — Find Cycle Start
- **Time Complexity:** O(n)
- **Space Complexity:** O(1)
- **Difficulty:** Medium

#### Python
```python
def detect_cycle_start(head):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Cycle found — find the entry point
            entry = head
            while entry != slow:
                entry = entry.next
                slow = slow.next
            return entry
    return None
```

#### JavaScript
```javascript
function detectCycleStart(head) {
  let slow = head;
  let fast = head;
  while (fast !== null && fast.next !== null) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow === fast) {
      let entry = head;
      while (entry !== slow) {
        entry = entry.next;
        slow = slow.next;
      }
      return entry;
    }
  }
  return null;
}
```

#### Java
```java
public class CycleDetection {
    public static ListNode detectCycleStart(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                ListNode entry = head;
                while (entry != slow) {
                    entry = entry.next;
                    slow = slow.next;
                }
                return entry;
            }
        }
        return null;
    }
}
```

**Explanation:**
1. First, detect the cycle using slow and fast pointers (same as Solution 1)
2. Once they meet, initialize a new pointer `entry` at the head
3. Move both `entry` and `slow` one step at a time; they will meet at the cycle's start
4. **Why this works:** Let `d` = distance from head to cycle start, and `k` = distance from cycle start to meeting point. At the meeting point, slow has traveled `d + k` and fast has traveled `2(d + k)`. The difference `d + k` is a multiple of the cycle length, so moving `d` more steps from the meeting point lands at the cycle start — the same distance as from the head.

**When to use:** When you need to identify exactly where a cycle begins, such as in memory leak detection or circular buffer analysis.

## Variations & Extensions
- **Find the length of the cycle:** After detecting the meeting point, keep one pointer fixed and move the other until they meet again, counting steps
- **Remove the cycle:** Find the cycle start, then traverse to the node whose `next` is the cycle start and set its `next` to `null`
- **Detect cycle using hashing:** Use a HashSet to store visited nodes (O(n) space, simpler logic)
- **Doubly linked list cycle detection:** Adapt for lists with both `next` and `prev` pointers

## Real-World Applications
- Detecting infinite loops in state machines or workflow engines
- Memory leak detection in garbage collectors (reference cycles)
- Detecting circular dependencies in build systems and package managers
- Network routing loop detection
- Validating linked data structures in database internals

## Tags
#algorithm #linked-list #two-pointers #cycle-detection #medium
