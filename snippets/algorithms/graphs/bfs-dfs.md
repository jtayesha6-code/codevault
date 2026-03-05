# BFS & DFS Implementation

## Problem Statement
- Implement **Breadth-First Search (BFS)** and **Depth-First Search (DFS)** on an unweighted graph represented as an adjacency list.
- Given a starting node, traverse all reachable nodes and return the order in which they are visited.

**Example inputs/outputs:**
- Graph: `{0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}`
- BFS from node `0` → `[0, 1, 2, 3]`
- DFS from node `0` → `[0, 1, 3, 2]` (order may vary depending on neighbor iteration)

**Edge cases:**
- Disconnected graph (unreachable nodes)
- Graph with a single node
- Graph with cycles
- Self-loops

## Solutions

### Solution 1: Breadth-First Search (BFS)
- **Time Complexity:** O(V + E) where V = vertices, E = edges
- **Space Complexity:** O(V)
- **Difficulty:** Medium

#### Python
```python
from collections import deque

def bfs(graph, start):
    visited = set()
    order = []
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order
```

#### JavaScript
```javascript
function bfs(graph, start) {
  const visited = new Set();
  const order = [];
  const queue = [start];
  visited.add(start);

  while (queue.length > 0) {
    const node = queue.shift();
    order.push(node);
    for (const neighbor of graph.get(node) || []) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push(neighbor);
      }
    }
  }

  return order;
}

// Usage with Map-based adjacency list
const graph = new Map([
  [0, [1, 2]],
  [1, [0, 3]],
  [2, [0, 3]],
  [3, [1, 2]],
]);
console.log(bfs(graph, 0)); // [0, 1, 2, 3]
```

#### Java
```java
import java.util.*;

public class GraphTraversal {
    public static List<Integer> bfs(Map<Integer, List<Integer>> graph, int start) {
        Set<Integer> visited = new HashSet<>();
        List<Integer> order = new ArrayList<>();
        Queue<Integer> queue = new LinkedList<>();

        visited.add(start);
        queue.add(start);

        while (!queue.isEmpty()) {
            int node = queue.poll();
            order.add(node);
            for (int neighbor : graph.getOrDefault(node, Collections.emptyList())) {
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);
                    queue.add(neighbor);
                }
            }
        }

        return order;
    }
}
```

**Explanation:** BFS explores nodes level by level using a **queue** (FIFO). Start by enqueuing the source node and marking it as visited. At each step, dequeue a node, process it, and enqueue all unvisited neighbors. The `visited` set prevents revisiting nodes in cyclic graphs. Nodes are discovered in order of their distance from the source.

**When to use:** Finding the shortest path in unweighted graphs, level-order traversal in trees, finding all nodes within a given distance, web crawlers, and social network friend suggestions (degrees of separation).

### Solution 2: Depth-First Search (DFS) — Iterative
- **Time Complexity:** O(V + E)
- **Space Complexity:** O(V)
- **Difficulty:** Medium

#### Python
```python
def dfs_iterative(graph, start):
    visited = set()
    order = []
    stack = [start]

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        # Add neighbors in reverse to visit them in original order
        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                stack.append(neighbor)

    return order
```

#### JavaScript
```javascript
function dfsIterative(graph, start) {
  const visited = new Set();
  const order = [];
  const stack = [start];

  while (stack.length > 0) {
    const node = stack.pop();
    if (visited.has(node)) {
      continue;
    }
    visited.add(node);
    order.push(node);
    const neighbors = graph.get(node) || [];
    for (let i = neighbors.length - 1; i >= 0; i--) {
      if (!visited.has(neighbors[i])) {
        stack.push(neighbors[i]);
      }
    }
  }

  return order;
}
```

#### Java
```java
import java.util.*;

public class GraphTraversal {
    public static List<Integer> dfsIterative(Map<Integer, List<Integer>> graph, int start) {
        Set<Integer> visited = new HashSet<>();
        List<Integer> order = new ArrayList<>();
        Deque<Integer> stack = new ArrayDeque<>();

        stack.push(start);

        while (!stack.isEmpty()) {
            int node = stack.pop();
            if (visited.contains(node)) {
                continue;
            }
            visited.add(node);
            order.add(node);
            List<Integer> neighbors = graph.getOrDefault(node, Collections.emptyList());
            for (int i = neighbors.size() - 1; i >= 0; i--) {
                if (!visited.contains(neighbors.get(i))) {
                    stack.push(neighbors.get(i));
                }
            }
        }

        return order;
    }
}
```

**Explanation:** DFS explores as deep as possible along each branch before backtracking, using a **stack** (LIFO). Pop a node, mark it visited, process it, and push its unvisited neighbors. Neighbors are pushed in reverse order so the first neighbor in the adjacency list is visited first (matching the recursive version). The `visited` check after popping handles nodes that may be pushed multiple times.

**When to use:** When you need to explore all paths (e.g., maze solving), detect cycles, perform topological sorting, or when memory is a concern and the graph is deep but not wide.

### Solution 3: Depth-First Search (DFS) — Recursive
- **Time Complexity:** O(V + E)
- **Space Complexity:** O(V) — recursion stack
- **Difficulty:** Medium

#### Python
```python
def dfs_recursive(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    order = [start]

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            order.extend(dfs_recursive(graph, neighbor, visited))

    return order
```

#### JavaScript
```javascript
function dfsRecursive(graph, start, visited = new Set()) {
  visited.add(start);
  const order = [start];

  for (const neighbor of graph.get(start) || []) {
    if (!visited.has(neighbor)) {
      order.push(...dfsRecursive(graph, neighbor, visited));
    }
  }

  return order;
}
```

#### Java
```java
import java.util.*;

public class GraphTraversal {
    public static List<Integer> dfsRecursive(Map<Integer, List<Integer>> graph, int start) {
        List<Integer> order = new ArrayList<>();
        Set<Integer> visited = new HashSet<>();
        dfsHelper(graph, start, visited, order);
        return order;
    }

    private static void dfsHelper(Map<Integer, List<Integer>> graph, int node,
                                   Set<Integer> visited, List<Integer> order) {
        visited.add(node);
        order.add(node);
        for (int neighbor : graph.getOrDefault(node, Collections.emptyList())) {
            if (!visited.contains(neighbor)) {
                dfsHelper(graph, neighbor, visited, order);
            }
        }
    }
}
```

**Explanation:** The recursive DFS uses the call stack implicitly. Mark the current node as visited, process it, then recurse on each unvisited neighbor. The recursion naturally backtracks when all neighbors of a node have been explored. Cleaner to write but risks stack overflow on very deep graphs.

**When to use:** Preferred for tree-like structures (no risk of deep recursion) and when the algorithm naturally maps to recursion, such as finding connected components or solving backtracking problems.

## Variations & Extensions
- **Bidirectional BFS:** Search from both source and target simultaneously to find shortest path faster
- **DFS with timestamps:** Track discovery and finish times for topological sort and cycle detection
- **BFS on a grid/matrix:** Treat cells as nodes and adjacent cells as edges (common in pathfinding)
- **Dijkstra's Algorithm:** Extends BFS for weighted graphs using a priority queue

## Real-World Applications
- **BFS:** GPS and map navigation (shortest route), social network friend recommendations, web crawling, network broadcasting
- **DFS:** Solving mazes and puzzles, detecting cycles in dependency graphs, topological ordering of build tasks, garbage collection (mark-and-sweep)

## Tags
#algorithm #graphs #bfs #dfs #traversal #medium
