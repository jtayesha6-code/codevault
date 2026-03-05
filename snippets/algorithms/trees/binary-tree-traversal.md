# Binary Tree Traversal

## Problem Statement
- Traverse all nodes of a binary tree in a specific order and return the values
- Traversal orders: In-order (Left, Root, Right), Pre-order (Root, Left, Right), Post-order (Left, Right, Root), and Level-order (BFS)
- Example tree:
  ```
        1
       / \
      2   3
     / \
    4   5
  ```
  - In-order: `[4, 2, 5, 1, 3]`
  - Pre-order: `[1, 2, 4, 5, 3]`
  - Post-order: `[4, 5, 2, 3, 1]`
  - Level-order: `[1, 2, 3, 4, 5]`
- Edge cases: empty tree, single node, skewed tree (all left or all right children)

## Solutions

### Solution 1: Recursive Traversals
- **Time Complexity:** O(n) where n is the number of nodes
- **Space Complexity:** O(h) where h is the height of the tree (recursion stack)
- **Difficulty:** Medium

#### Python
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder(root):
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def preorder(root):
    if root is None:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def postorder(root):
    if root is None:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]
```

#### JavaScript
```javascript
class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

function inorder(root) {
  if (root === null) return [];
  return [...inorder(root.left), root.val, ...inorder(root.right)];
}

function preorder(root) {
  if (root === null) return [];
  return [root.val, ...preorder(root.left), ...preorder(root.right)];
}

function postorder(root) {
  if (root === null) return [];
  return [...postorder(root.left), ...postorder(root.right), root.val];
}
```

#### Java
```java
import java.util.ArrayList;
import java.util.List;

class TreeNode {
    int val;
    TreeNode left, right;
    TreeNode(int val) { this.val = val; }
}

public class RecursiveTraversal {
    public static List<Integer> inorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        inorderHelper(root, result);
        return result;
    }

    private static void inorderHelper(TreeNode node, List<Integer> result) {
        if (node == null) return;
        inorderHelper(node.left, result);
        result.add(node.val);
        inorderHelper(node.right, result);
    }

    public static List<Integer> preorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        preorderHelper(root, result);
        return result;
    }

    private static void preorderHelper(TreeNode node, List<Integer> result) {
        if (node == null) return;
        result.add(node.val);
        preorderHelper(node.left, result);
        preorderHelper(node.right, result);
    }

    public static List<Integer> postorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        postorderHelper(root, result);
        return result;
    }

    private static void postorderHelper(TreeNode node, List<Integer> result) {
        if (node == null) return;
        postorderHelper(node.left, result);
        postorderHelper(node.right, result);
        result.add(node.val);
    }
}
```

**Explanation:**
1. **In-order (Left, Root, Right):** Recursively visit the left subtree, process the current node, then visit the right subtree. For a BST, this produces sorted order.
2. **Pre-order (Root, Left, Right):** Process the current node first, then recursively visit left and right subtrees. Useful for creating a copy of the tree or serialization.
3. **Post-order (Left, Right, Root):** Recursively visit both subtrees before processing the current node. Useful for deleting a tree or evaluating expression trees.

**When to use:** When the tree depth is manageable and code simplicity is prioritized. Recursive solutions are clean and easy to reason about.

### Solution 2: Iterative Traversals Using a Stack
- **Time Complexity:** O(n)
- **Space Complexity:** O(h) where h is the height of the tree
- **Difficulty:** Medium

#### Python
```python
def inorder_iterative(root):
    result = []
    stack = []
    current = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.val)
        current = current.right
    return result

def preorder_iterative(root):
    if root is None:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result

def postorder_iterative(root):
    if root is None:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return result[::-1]
```

#### JavaScript
```javascript
function inorderIterative(root) {
  const result = [];
  const stack = [];
  let current = root;
  while (current !== null || stack.length > 0) {
    while (current !== null) {
      stack.push(current);
      current = current.left;
    }
    current = stack.pop();
    result.push(current.val);
    current = current.right;
  }
  return result;
}

function preorderIterative(root) {
  if (root === null) return [];
  const result = [];
  const stack = [root];
  while (stack.length > 0) {
    const node = stack.pop();
    result.push(node.val);
    if (node.right) stack.push(node.right);
    if (node.left) stack.push(node.left);
  }
  return result;
}

function postorderIterative(root) {
  if (root === null) return [];
  const result = [];
  const stack = [root];
  while (stack.length > 0) {
    const node = stack.pop();
    result.push(node.val);
    if (node.left) stack.push(node.left);
    if (node.right) stack.push(node.right);
  }
  return result.reverse();
}
```

#### Java
```java
import java.util.*;

public class IterativeTraversal {
    public static List<Integer> inorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode current = root;
        while (current != null || !stack.isEmpty()) {
            while (current != null) {
                stack.push(current);
                current = current.left;
            }
            current = stack.pop();
            result.add(current.val);
            current = current.right;
        }
        return result;
    }

    public static List<Integer> preorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        Deque<TreeNode> stack = new ArrayDeque<>();
        stack.push(root);
        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            result.add(node.val);
            if (node.right != null) stack.push(node.right);
            if (node.left != null) stack.push(node.left);
        }
        return result;
    }

    public static List<Integer> postorder(TreeNode root) {
        LinkedList<Integer> result = new LinkedList<>();
        if (root == null) return result;
        Deque<TreeNode> stack = new ArrayDeque<>();
        stack.push(root);
        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            result.addFirst(node.val);
            if (node.left != null) stack.push(node.left);
            if (node.right != null) stack.push(node.right);
        }
        return result;
    }
}
```

**Explanation:**
1. **Iterative In-order:** Push all left children onto the stack, then pop a node, record its value, and move to its right child. Repeat until the stack is empty and no current node exists.
2. **Iterative Pre-order:** Push root to the stack. Pop a node, record it, then push its right child followed by its left child (so left is processed first).
3. **Iterative Post-order:** Similar to pre-order but push left before right, then reverse the result. Alternatively, use `addFirst` to build the result in reverse.

**When to use:** When recursion depth might cause a stack overflow (very deep or skewed trees), or in environments where explicit stack control is preferred.

### Solution 3: Level-Order Traversal (BFS)
- **Time Complexity:** O(n)
- **Space Complexity:** O(w) where w is the maximum width of the tree
- **Difficulty:** Medium

#### Python
```python
from collections import deque

def level_order(root):
    if root is None:
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
function levelOrder(root) {
  if (root === null) return [];
  const result = [];
  const queue = [root];
  while (queue.length > 0) {
    const level = [];
    const size = queue.length;
    for (let i = 0; i < size; i++) {
      const node = queue.shift();
      level.push(node.val);
      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }
    result.push(level);
  }
  return result;
}
```

#### Java
```java
import java.util.*;

public class LevelOrderTraversal {
    public static List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> level = new ArrayList<>();
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                level.add(node.val);
                if (node.left != null) queue.offer(node.left);
                if (node.right != null) queue.offer(node.right);
            }
            result.add(level);
        }
        return result;
    }
}
```

**Explanation:**
1. Use a queue (FIFO) initialized with the root node
2. Process all nodes at the current level before moving to the next level
3. For each node, record its value and enqueue its left and right children
4. Each iteration of the outer loop processes one complete level
5. The result is a list of lists, where each inner list contains values at that depth

**When to use:** When you need to process or display a tree level by level, find the minimum depth, or perform breadth-first operations like shortest path in an unweighted tree.

## Variations & Extensions
- **Morris Traversal:** In-order traversal with O(1) space by temporarily modifying tree pointers
- **Zigzag Level-Order:** Alternate left-to-right and right-to-left at each level
- **Vertical Order Traversal:** Group nodes by their horizontal distance from the root
- **Boundary Traversal:** Visit left boundary, leaves, and right boundary
- **Reverse Level-Order:** Process levels from bottom to top

## Real-World Applications
- In-order traversal of BSTs for sorted data retrieval in databases
- Pre-order traversal for serializing/deserializing tree structures (e.g., JSON, XML)
- Post-order traversal for calculating directory sizes in file systems
- Level-order traversal for printing organizational hierarchies and network topologies
- Expression tree evaluation in compilers and calculators

## Tags
#algorithm #tree #binary-tree #traversal #bfs #dfs #medium
