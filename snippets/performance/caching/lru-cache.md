# LRU Cache Design

## Problem Statement
- Design a data structure that follows the constraints of a **Least Recently Used (LRU) Cache**.
- Implement `get(key)` and `put(key, value)` operations, both in **O(1)** average time complexity.
- The cache has a fixed capacity. When inserting a new key and the cache is full, evict the least recently used item before inserting the new one.
- Any `get` or `put` on an existing key marks it as recently used.

**Example inputs/outputs:**
- `LRUCache(2)` → create cache with capacity 2
- `put(1, 1)` → cache: `{1=1}`
- `put(2, 2)` → cache: `{1=1, 2=2}`
- `get(1)` → returns `1`, cache: `{2=2, 1=1}`
- `put(3, 3)` → evicts key `2`, cache: `{1=1, 3=3}`
- `get(2)` → returns `-1` (not found)

**Edge cases:**
- Cache capacity of 1
- Updating an existing key with `put`
- Getting a non-existent key
- Multiple puts followed by gets in varying order

## Solutions

### Solution 1: OrderedDict / LinkedHashMap
- **Time Complexity:** O(1) for both `get` and `put`
- **Space Complexity:** O(capacity)
- **Difficulty:** Medium

#### Python
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

#### JavaScript
```javascript
class LRUCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.cache = new Map();
  }

  get(key) {
    if (!this.cache.has(key)) {
      return -1;
    }
    const value = this.cache.get(key);
    // Move to end by re-inserting (Map maintains insertion order)
    this.cache.delete(key);
    this.cache.set(key, value);
    return value;
  }

  put(key, value) {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    }
    this.cache.set(key, value);
    if (this.cache.size > this.capacity) {
      // Evict the least recently used (first inserted) key
      const lruKey = this.cache.keys().next().value;
      this.cache.delete(lruKey);
    }
  }
}
```

#### Java
```java
import java.util.LinkedHashMap;
import java.util.Map;

public class LRUCache {
    private final int capacity;
    private final LinkedHashMap<Integer, Integer> cache;

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new LinkedHashMap<>(capacity, 0.75f, true) {
            @Override
            protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
                return size() > LRUCache.this.capacity;
            }
        };
    }

    public int get(int key) {
        return cache.getOrDefault(key, -1);
    }

    public void put(int key, int value) {
        cache.put(key, value);
    }
}
```

**Explanation:** Python's `OrderedDict`, JavaScript's `Map`, and Java's `LinkedHashMap` all maintain insertion order internally. On `get`, we move the accessed key to the end (most recent). On `put`, we insert or update and evict the front element (least recent) if the capacity is exceeded. Java's `LinkedHashMap` with `accessOrder=true` (the third constructor argument) automatically reorders on access, and `removeEldestEntry` handles eviction.

**When to use:** Ideal for interview settings and most production scenarios. Leverages well-tested standard library implementations that are both correct and performant.

### Solution 2: HashMap + Doubly Linked List (From Scratch)
- **Time Complexity:** O(1) for both `get` and `put`
- **Space Complexity:** O(capacity)
- **Difficulty:** Medium

#### Python
```python
class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        # Sentinel nodes to avoid null checks
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_end(self, node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_end(node)
        return node.value

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self._add_to_end(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]
```

#### JavaScript
```javascript
class Node {
  constructor(key = 0, value = 0) {
    this.key = key;
    this.value = value;
    this.prev = null;
    this.next = null;
  }
}

class LRUCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.cache = new Map();
    this.head = new Node();
    this.tail = new Node();
    this.head.next = this.tail;
    this.tail.prev = this.head;
  }

  _remove(node) {
    node.prev.next = node.next;
    node.next.prev = node.prev;
  }

  _addToEnd(node) {
    node.prev = this.tail.prev;
    node.next = this.tail;
    this.tail.prev.next = node;
    this.tail.prev = node;
  }

  get(key) {
    if (!this.cache.has(key)) {
      return -1;
    }
    const node = this.cache.get(key);
    this._remove(node);
    this._addToEnd(node);
    return node.value;
  }

  put(key, value) {
    if (this.cache.has(key)) {
      this._remove(this.cache.get(key));
    }
    const node = new Node(key, value);
    this._addToEnd(node);
    this.cache.set(key, node);
    if (this.cache.size > this.capacity) {
      const lru = this.head.next;
      this._remove(lru);
      this.cache.delete(lru.key);
    }
  }
}
```

#### Java
```java
import java.util.HashMap;
import java.util.Map;

public class LRUCache {
    private static class Node {
        int key, value;
        Node prev, next;

        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }

    private final int capacity;
    private final Map<Integer, Node> cache;
    private final Node head;
    private final Node tail;

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new HashMap<>();
        this.head = new Node(0, 0);
        this.tail = new Node(0, 0);
        head.next = tail;
        tail.prev = head;
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void addToEnd(Node node) {
        node.prev = tail.prev;
        node.next = tail;
        tail.prev.next = node;
        tail.prev = node;
    }

    public int get(int key) {
        if (!cache.containsKey(key)) {
            return -1;
        }
        Node node = cache.get(key);
        remove(node);
        addToEnd(node);
        return node.value;
    }

    public void put(int key, int value) {
        if (cache.containsKey(key)) {
            remove(cache.get(key));
        }
        Node node = new Node(key, value);
        addToEnd(node);
        cache.put(key, node);
        if (cache.size() > capacity) {
            Node lru = head.next;
            remove(lru);
            cache.remove(lru.key);
        }
    }
}
```

**Explanation:** A HashMap provides O(1) key lookup, while a doubly linked list maintains access order. Sentinel `head` and `tail` nodes simplify edge-case handling. On `get`, the node is moved to the tail (most recent). On `put`, a new node is added at the tail, and if capacity is exceeded, the node after `head` (least recent) is evicted. Storing the key in each node allows us to remove it from the HashMap during eviction.

**When to use:** Use this approach when you need to understand the internals for interviews, or when your language doesn't provide an ordered dictionary. Also preferred when you need custom eviction callbacks or more control over the data structure.

## Variations & Extensions
- **LFU Cache (Least Frequently Used):** Evict the item with the lowest access count
- **TTL Cache:** Add expiration times to cache entries
- **Thread-safe LRU Cache:** Add locking or use concurrent data structures
- **Bounded LRU with size-based eviction:** Evict based on memory usage instead of item count

## Real-World Applications
- Web browser caching of recently visited pages
- Database query result caching (e.g., MySQL query cache)
- CDN edge caching for frequently accessed content
- Operating system page replacement algorithms

## Tags
#data-structure #caching #design #hash-map #linked-list #medium
