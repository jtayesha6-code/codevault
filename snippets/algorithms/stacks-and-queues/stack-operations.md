# Stack Operations

## Problem Statement
- Implement a stack data structure supporting core operations: Push, Pop, Peek, and isEmpty
- A stack follows the Last-In-First-Out (LIFO) principle
- Example operations: `push(1)`, `push(2)`, `peek()` → `2`, `pop()` → `2`, `pop()` → `1`, `isEmpty()` → `true`
- Edge cases: popping from an empty stack, peeking at an empty stack, stack overflow (fixed-size)

## Solutions

### Solution 1: Array-Based Stack
- **Time Complexity:** O(1) for all operations (amortized for dynamic arrays)
- **Space Complexity:** O(n) where n is the number of elements
- **Difficulty:** Easy

#### Python
```python
class ArrayStack:
    def __init__(self):
        self._data = []

    def push(self, value):
        self._data.append(value)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek at empty stack")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)
```

#### JavaScript
```javascript
class ArrayStack {
  constructor() {
    this.data = [];
  }

  push(value) {
    this.data.push(value);
  }

  pop() {
    if (this.isEmpty()) throw new Error("Pop from empty stack");
    return this.data.pop();
  }

  peek() {
    if (this.isEmpty()) throw new Error("Peek at empty stack");
    return this.data[this.data.length - 1];
  }

  isEmpty() {
    return this.data.length === 0;
  }

  size() {
    return this.data.length;
  }
}
```

#### Java
```java
import java.util.ArrayList;

public class ArrayStack<T> {
    private final ArrayList<T> data = new ArrayList<>();

    public void push(T value) {
        data.add(value);
    }

    public T pop() {
        if (isEmpty()) throw new RuntimeException("Pop from empty stack");
        return data.remove(data.size() - 1);
    }

    public T peek() {
        if (isEmpty()) throw new RuntimeException("Peek at empty stack");
        return data.get(data.size() - 1);
    }

    public boolean isEmpty() {
        return data.isEmpty();
    }

    public int size() {
        return data.size();
    }
}
```

**Explanation:**
1. Use a dynamic array (list) as the underlying storage
2. `push` appends to the end of the array — O(1) amortized
3. `pop` removes and returns the last element — O(1)
4. `peek` returns the last element without removing it — O(1)
5. `isEmpty` checks whether the array has zero elements

**When to use:** The simplest and most cache-friendly implementation. Ideal for most use cases where the stack size is predictable or dynamic resizing is acceptable.

### Solution 2: Linked-List-Based Stack
- **Time Complexity:** O(1) for all operations
- **Space Complexity:** O(n) where n is the number of elements
- **Difficulty:** Easy

#### Python
```python
class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

class LinkedListStack:
    def __init__(self):
        self._top = None
        self._size = 0

    def push(self, value):
        self._top = Node(value, self._top)
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        value = self._top.value
        self._top = self._top.next
        self._size -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek at empty stack")
        return self._top.value

    def is_empty(self):
        return self._top is None

    def size(self):
        return self._size
```

#### JavaScript
```javascript
class Node {
  constructor(value, next = null) {
    this.value = value;
    this.next = next;
  }
}

class LinkedListStack {
  constructor() {
    this.top = null;
    this._size = 0;
  }

  push(value) {
    this.top = new Node(value, this.top);
    this._size++;
  }

  pop() {
    if (this.isEmpty()) throw new Error("Pop from empty stack");
    const value = this.top.value;
    this.top = this.top.next;
    this._size--;
    return value;
  }

  peek() {
    if (this.isEmpty()) throw new Error("Peek at empty stack");
    return this.top.value;
  }

  isEmpty() {
    return this.top === null;
  }

  size() {
    return this._size;
  }
}
```

#### Java
```java
public class LinkedListStack<T> {
    private static class Node<T> {
        T value;
        Node<T> next;
        Node(T value, Node<T> next) {
            this.value = value;
            this.next = next;
        }
    }

    private Node<T> top = null;
    private int size = 0;

    public void push(T value) {
        top = new Node<>(value, top);
        size++;
    }

    public T pop() {
        if (isEmpty()) throw new RuntimeException("Pop from empty stack");
        T value = top.value;
        top = top.next;
        size--;
        return value;
    }

    public T peek() {
        if (isEmpty()) throw new RuntimeException("Peek at empty stack");
        return top.value;
    }

    public boolean isEmpty() {
        return top == null;
    }

    public int size() {
        return size;
    }
}
```

**Explanation:**
1. Each element is wrapped in a `Node` that holds a value and a pointer to the next node
2. `push` creates a new node pointing to the current top, then updates the top — O(1)
3. `pop` saves the top value, advances the top pointer to the next node, and returns the saved value — O(1)
4. No resizing is needed since each node is independently allocated

**When to use:** When you need guaranteed O(1) operations without amortized resizing, or when memory is fragmented and contiguous allocation is expensive.

### Solution 3: Application — Balanced Parentheses Checker
- **Time Complexity:** O(n) where n is the length of the string
- **Space Complexity:** O(n) in the worst case
- **Difficulty:** Easy

#### Python
```python
def is_balanced(expression):
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}
    for char in expression:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack or stack[-1] != matching[char]:
                return False
            stack.pop()
    return len(stack) == 0
```

#### JavaScript
```javascript
function isBalanced(expression) {
  const stack = [];
  const matching = { ')': '(', ']': '[', '}': '{' };
  for (const char of expression) {
    if ('([{'.includes(char)) {
      stack.push(char);
    } else if (')]}'.includes(char)) {
      if (stack.length === 0 || stack[stack.length - 1] !== matching[char]) {
        return false;
      }
      stack.pop();
    }
  }
  return stack.length === 0;
}
```

#### Java
```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Map;

public class BalancedParentheses {
    public static boolean isBalanced(String expression) {
        Deque<Character> stack = new ArrayDeque<>();
        Map<Character, Character> matching = Map.of(')', '(', ']', '[', '}', '{');
        for (char c : expression.toCharArray()) {
            if (c == '(' || c == '[' || c == '{') {
                stack.push(c);
            } else if (matching.containsKey(c)) {
                if (stack.isEmpty() || stack.peek() != matching.get(c)) {
                    return false;
                }
                stack.pop();
            }
        }
        return stack.isEmpty();
    }
}
```

**Explanation:**
1. Iterate through each character in the expression
2. Push opening brackets onto the stack
3. For each closing bracket, check that the stack is not empty and the top matches the expected opening bracket
4. If any mismatch is found, return `false`
5. After processing all characters, the stack must be empty for the expression to be balanced

**When to use:** Validating expressions in compilers, IDEs, and code linters; checking well-formed HTML/XML tags; validating mathematical expressions.

## Variations & Extensions
- **Min Stack:** Track the minimum element at each level so `getMin()` is O(1)
- **Max Stack:** Same concept but tracking the maximum
- **Stack using two queues:** Implement a stack interface using only queue operations
- **Postfix expression evaluation:** Evaluate expressions like `3 4 + 2 *` using a stack
- **Undo/Redo mechanism:** Two stacks to support undo and redo operations

## Real-World Applications
- Function call management (call stack) in programming language runtimes
- Undo/redo functionality in text editors and design tools
- Browser back/forward navigation history
- Expression parsing and evaluation in compilers and calculators
- Depth-first search (DFS) traversal of graphs and trees
- Syntax validation in IDEs and linters

## Tags
#data-structure #stack #array #linked-list #easy
