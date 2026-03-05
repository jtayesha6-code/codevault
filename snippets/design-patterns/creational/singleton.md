# Singleton Pattern

## Problem Statement
- Ensure a class has **only one instance** and provide a **global point of access** to it.
- The instance should be created lazily (on first use) or eagerly (at load time), depending on the use case.
- In multithreaded environments, the implementation must be **thread-safe** to prevent multiple instances from being created.

**Example inputs/outputs:**
- `getInstance()` called multiple times → always returns the same object reference
- `instance1 = Singleton.getInstance()`, `instance2 = Singleton.getInstance()` → `instance1 is instance2` is `true`

**Edge cases:**
- Concurrent access from multiple threads
- Serialization and deserialization creating a new instance (Java)
- Subclassing a singleton class
- Module reloading in dynamic languages

## Solutions

### Solution 1: Simple Singleton
- **Time Complexity:** O(1) for `getInstance`
- **Space Complexity:** O(1)
- **Difficulty:** Medium

#### Python
```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Guard against re-initialization
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.value = None

# Usage
s1 = Singleton()
s2 = Singleton()
assert s1 is s2
```

#### JavaScript
```javascript
class Singleton {
  constructor() {
    if (Singleton.instance) {
      return Singleton.instance;
    }
    this.value = null;
    Singleton.instance = this;
  }

  static getInstance() {
    if (!Singleton.instance) {
      Singleton.instance = new Singleton();
    }
    return Singleton.instance;
  }
}

// Usage
const s1 = Singleton.getInstance();
const s2 = Singleton.getInstance();
console.log(s1 === s2); // true
```

#### Java
```java
public class Singleton {
    private static Singleton instance;
    private Object value;

    private Singleton() {
        this.value = null;
    }

    public static Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }

    public Object getValue() {
        return value;
    }

    public void setValue(Object value) {
        this.value = value;
    }
}
```

**Explanation:** The simplest singleton implementation. A private constructor prevents direct instantiation. A static method checks if an instance exists; if not, it creates one and stores it in a class-level field. All subsequent calls return the same instance. This version is **not thread-safe** in Java — see Solution 2 for a thread-safe variant.

**When to use:** Suitable for single-threaded applications, scripts, or environments where concurrency is not a concern (e.g., simple CLI tools, configuration loaders in single-threaded contexts).

### Solution 2: Thread-Safe Singleton
- **Time Complexity:** O(1) for `getInstance`
- **Space Complexity:** O(1)
- **Difficulty:** Medium

#### Python
```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                # Double-check after acquiring the lock
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.value = None

# Usage
s1 = Singleton()
s2 = Singleton()
assert s1 is s2
```

#### JavaScript
```javascript
// JavaScript is single-threaded in the main event loop, so the simple
// version is inherently thread-safe. The module pattern is the idiomatic
// approach for singletons in JavaScript/Node.js:

// logger.js — the module itself acts as a singleton
class Logger {
  constructor() {
    this.logs = [];
  }

  log(message) {
    const entry = `[${new Date().toISOString()}] ${message}`;
    this.logs.push(entry);
    console.log(entry);
  }

  getHistory() {
    return [...this.logs];
  }
}

// Module-level instance: Node.js caches modules after first require/import
const instance = new Logger();
Object.freeze(instance);

export default instance;

// Usage (in another file):
// import logger from './logger.js';
// logger.log('Application started');
```

#### Java
```java
public class Singleton {
    // volatile ensures visibility across threads
    private static volatile Singleton instance;
    private Object value;

    private Singleton() {
        this.value = null;
    }

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }

    public Object getValue() {
        return value;
    }

    public void setValue(Object value) {
        this.value = value;
    }
}
```

**Explanation:** Uses the **double-checked locking** pattern. The first `null` check avoids the overhead of acquiring a lock on every call. The second check inside the synchronized block ensures only one thread creates the instance. In Java, the `volatile` keyword prevents instruction reordering that could expose a partially constructed object. In Python, `threading.Lock` serves the same purpose. JavaScript's single-threaded event loop makes this unnecessary — the module pattern is the idiomatic singleton.

**When to use:** Required in any multithreaded application — web servers, background workers, and concurrent systems. This is the standard production-ready singleton approach.

### When to Use Singletons
- **Configuration managers** — a single source of truth for app settings
- **Connection pools** — reuse database or HTTP connections
- **Logging services** — centralized log management
- **Caches** — shared in-memory cache across the application
- **Hardware interface access** — printer spoolers, device drivers

### When NOT to Use Singletons
- **Unit testing** — singletons carry state between tests, making isolation difficult. Prefer dependency injection.
- **When multiple instances may be needed later** — singletons make this refactor painful.
- **As a replacement for global variables** — if you just need shared data, consider passing dependencies explicitly.
- **In highly concurrent systems with mutable state** — a singleton with mutable shared state becomes a bottleneck and a source of race conditions. Use thread-local storage or immutable shared state instead.

## Variations & Extensions
- **Enum Singleton (Java):** `enum Singleton { INSTANCE; }` — the simplest and most bulletproof Java singleton, immune to serialization and reflection attacks
- **Borg / Monostate Pattern:** Multiple instances share the same state instead of enforcing a single instance
- **Multiton Pattern:** A map of named instances, extending the singleton concept to a fixed set of instances
- **Dependency Injection:** An alternative to singletons where a framework manages object lifecycles

## Real-World Applications
- Database connection pools (e.g., HikariCP, SQLAlchemy engine)
- Application configuration and settings management
- Logging frameworks (e.g., Python's `logging` module, Log4j)
- Thread pools and executor services
- GUI application instances (e.g., ensuring only one main window)

## Tags
#design-pattern #creational #singleton #thread-safety #medium
