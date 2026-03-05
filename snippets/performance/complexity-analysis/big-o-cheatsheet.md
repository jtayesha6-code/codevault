# Big O Complexity Cheat Sheet

## Overview
Big O notation describes the upper bound of an algorithm's growth rate as input size increases. It focuses on the dominant term and ignores constants.

## Growth Rate Comparison

```
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)
```

| Complexity | Name | n=10 | n=100 | n=1,000 | n=10,000 | Practical? |
|:---|:---|:---|:---|:---|:---|:---|
| O(1) | Constant | 1 | 1 | 1 | 1 | ✅ Always |
| O(log n) | Logarithmic | 3 | 7 | 10 | 13 | ✅ Always |
| O(n) | Linear | 10 | 100 | 1,000 | 10,000 | ✅ Always |
| O(n log n) | Linearithmic | 30 | 664 | 9,966 | 132,877 | ✅ Usually |
| O(n²) | Quadratic | 100 | 10,000 | 1,000,000 | 100,000,000 | ⚠️ n < 10⁴ |
| O(n³) | Cubic | 1,000 | 1,000,000 | 10⁹ | 10¹² | ⚠️ n < 500 |
| O(2ⁿ) | Exponential | 1,024 | 10³⁰ | — | — | ❌ n < 25 |
| O(n!) | Factorial | 3,628,800 | — | — | — | ❌ n < 12 |

## Common Data Structure Operations

### Arrays / Lists

| Operation | Average | Worst |
|:---|:---|:---|
| Access by index | O(1) | O(1) |
| Search (unsorted) | O(n) | O(n) |
| Search (sorted) | O(log n) | O(log n) |
| Insert at end | O(1)* | O(n)* |
| Insert at index | O(n) | O(n) |
| Delete at end | O(1) | O(1) |
| Delete at index | O(n) | O(n) |

*Amortized O(1) for dynamic arrays; O(n) when resizing is triggered.

### Linked Lists

| Operation | Singly | Doubly |
|:---|:---|:---|
| Access by index | O(n) | O(n) |
| Search | O(n) | O(n) |
| Insert at head | O(1) | O(1) |
| Insert at tail | O(n) / O(1)* | O(1) |
| Delete head | O(1) | O(1) |
| Delete tail | O(n) | O(1) |
| Delete given node | O(n) | O(1) |

*O(1) if a tail pointer is maintained.

### Hash Tables

| Operation | Average | Worst |
|:---|:---|:---|
| Search | O(1) | O(n) |
| Insert | O(1) | O(n) |
| Delete | O(1) | O(n) |
| Space | O(n) | O(n) |

Worst case occurs with hash collisions. Good hash functions keep operations amortized O(1).

### Binary Search Tree (BST)

| Operation | Average (balanced) | Worst (skewed) |
|:---|:---|:---|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Min / Max | O(log n) | O(n) |

Self-balancing trees (AVL, Red-Black) guarantee O(log n) worst case.

### Heaps (Binary)

| Operation | Time |
|:---|:---|
| Find min/max | O(1) |
| Insert | O(log n) |
| Extract min/max | O(log n) |
| Build heap | O(n) |
| Heapify (sift down) | O(log n) |

### Stacks & Queues

| Operation | Time |
|:---|:---|
| Push / Enqueue | O(1) |
| Pop / Dequeue | O(1) |
| Peek | O(1) |
| Search | O(n) |

### Graphs (V = vertices, E = edges)

| Representation | Space | Add Edge | Has Edge | Iterate Neighbors |
|:---|:---|:---|:---|:---|
| Adjacency List | O(V + E) | O(1) | O(degree) | O(degree) |
| Adjacency Matrix | O(V²) | O(1) | O(1) | O(V) |

| Algorithm | Time | Space |
|:---|:---|:---|
| BFS | O(V + E) | O(V) |
| DFS | O(V + E) | O(V) |
| Dijkstra (min-heap) | O((V + E) log V) | O(V) |
| Bellman-Ford | O(V × E) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |
| Topological Sort | O(V + E) | O(V) |

## Sorting Algorithm Comparison

| Algorithm | Best | Average | Worst | Space | Stable? |
|:---|:---|:---|:---|:---|:---|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | ❌ |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ |
| Tim Sort | O(n) | O(n log n) | O(n log n) | O(n) | ✅ |
| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(k) | ✅ |
| Radix Sort | O(nk) | O(nk) | O(nk) | O(n + k) | ✅ |
| Bucket Sort | O(n + k) | O(n + k) | O(n²) | O(n) | ✅ |

*k = range of input values for counting/radix sort, number of buckets for bucket sort.*

## Quick Rules of Thumb

### Identifying Complexity from Code Patterns

```python
# O(1) — Constant
x = arr[5]

# O(log n) — Logarithmic (halving the problem)
while n > 0:
    n //= 2

# O(n) — Linear (single loop)
for i in range(n):
    process(i)

# O(n log n) — Linearithmic (sort then iterate)
arr.sort()
for item in arr:
    process(item)

# O(n²) — Quadratic (nested loops)
for i in range(n):
    for j in range(n):
        process(i, j)

# O(2ⁿ) — Exponential (branching recursion)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

### Amortized Analysis
Some operations are occasionally expensive but cheap on average:
- **Dynamic array resize**: Single insert is O(n) when resizing, but amortized O(1)
- **Hash table rehash**: O(n) when load factor exceeded, but amortized O(1) per insert

### Space Complexity Reminders
| Pattern | Space |
|:---|:---|
| Fixed variables | O(1) |
| Single array copy | O(n) |
| 2D matrix | O(n²) |
| Recursive call stack (depth d) | O(d) |
| Hash map of n entries | O(n) |
| Adjacency list | O(V + E) |

## Complexity Classes at a Glance

```
┌──────────┐
│   O(1)   │  Hash lookup, array index access
├──────────┤
│ O(log n) │  Binary search, balanced BST ops
├──────────┤
│   O(n)   │  Linear scan, single pass
├──────────┤
│O(n log n)│  Efficient sorting (merge, quick, heap)
├──────────┤
│  O(n²)   │  Brute-force pairs, simple DP on 2D grid
├──────────┤
│  O(2ⁿ)   │  Subset enumeration, naive recursion
├──────────┤
│  O(n!)   │  Permutation generation
└──────────┘
```

## Real-World Applications
- Choosing the right data structure based on operation frequency
- Estimating feasibility before coding a solution (will it TLE?)
- Comparing algorithm trade-offs in system design interviews
- Capacity planning and performance budgeting in production systems

## Tags
#complexity #performance #reference #big-o #cheatsheet
