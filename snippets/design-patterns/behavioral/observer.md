# Observer Pattern

## Problem Statement
- Define a **one-to-many dependency** between objects so that when one object (the subject) changes state, **all its dependents (observers) are notified** and updated automatically.
- Decouple the subject from its observers — the subject should not need to know the concrete types of its observers.
- Allow observers to be added and removed dynamically at runtime.

**Example inputs/outputs:**
- `subject.subscribe(observer)` → observer is registered
- `subject.notify(data)` → all registered observers receive `data`
- `subject.unsubscribe(observer)` → observer stops receiving updates

**Edge cases:**
- Notifying when no observers are registered (should not error)
- An observer unsubscribing during notification
- Duplicate subscriptions of the same observer
- Observer throwing an exception during update
- Circular dependencies between subjects and observers

## Solutions

### Solution 1: Classic Observer
- **Time Complexity:** O(n) per notification, where n is the number of observers
- **Space Complexity:** O(n) for storing observer references
- **Difficulty:** Medium

#### Python
```python
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data: any) -> None:
        pass


class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list[Observer]] = {}

    def subscribe(self, event: str, observer: Observer) -> None:
        if event not in self._listeners:
            self._listeners[event] = []
        if observer not in self._listeners[event]:
            self._listeners[event].append(observer)

    def unsubscribe(self, event: str, observer: Observer) -> None:
        if event in self._listeners:
            self._listeners[event] = [
                o for o in self._listeners[event] if o is not observer
            ]

    def notify(self, event: str, data: any = None) -> None:
        for observer in list(self._listeners.get(event, [])):
            observer.update(event, data)


class Logger(Observer):
    def update(self, event: str, data: any) -> None:
        print(f"[LOG] {event}: {data}")


class Analytics(Observer):
    def __init__(self):
        self.events: list[dict] = []

    def update(self, event: str, data: any) -> None:
        self.events.append({"event": event, "data": data})


# Usage
emitter = EventEmitter()
logger = Logger()
analytics = Analytics()

emitter.subscribe("user:login", logger)
emitter.subscribe("user:login", analytics)

emitter.notify("user:login", {"user": "alice"})
# [LOG] user:login: {'user': 'alice'}

print(analytics.events)
# [{'event': 'user:login', 'data': {'user': 'alice'}}]

emitter.unsubscribe("user:login", logger)
emitter.notify("user:login", {"user": "bob"})
# Only analytics receives this event
print(len(analytics.events))  # 2
```

#### JavaScript
```javascript
class EventEmitter {
  #listeners = new Map();

  subscribe(event, observer) {
    if (!this.#listeners.has(event)) {
      this.#listeners.set(event, new Set());
    }
    this.#listeners.get(event).add(observer);
  }

  unsubscribe(event, observer) {
    const observers = this.#listeners.get(event);
    if (observers) {
      observers.delete(observer);
    }
  }

  notify(event, data) {
    const observers = this.#listeners.get(event);
    if (observers) {
      for (const observer of [...observers]) {
        observer.update(event, data);
      }
    }
  }
}

class Logger {
  update(event, data) {
    console.log(`[LOG] ${event}:`, data);
  }
}

class Analytics {
  constructor() {
    this.events = [];
  }

  update(event, data) {
    this.events.push({ event, data });
  }
}

// Usage
const emitter = new EventEmitter();
const logger = new Logger();
const analytics = new Analytics();

emitter.subscribe("user:login", logger);
emitter.subscribe("user:login", analytics);

emitter.notify("user:login", { user: "alice" });
// [LOG] user:login: { user: 'alice' }

console.log(analytics.events);
// [{ event: 'user:login', data: { user: 'alice' } }]

emitter.unsubscribe("user:login", logger);
emitter.notify("user:login", { user: "bob" });
console.log(analytics.events.length); // 2
```

#### Java
```java
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

// Observer.java
public interface Observer {
    void update(String event, Object data);
}

// EventEmitter.java
public class EventEmitter {
    private final Map<String, List<Observer>> listeners =
        new ConcurrentHashMap<>();

    public void subscribe(String event, Observer observer) {
        listeners.computeIfAbsent(event, k -> new CopyOnWriteArrayList<>())
                 .add(observer);
    }

    public void unsubscribe(String event, Observer observer) {
        List<Observer> observers = listeners.get(event);
        if (observers != null) {
            observers.remove(observer);
        }
    }

    public void notify(String event, Object data) {
        List<Observer> observers = listeners.get(event);
        if (observers != null) {
            for (Observer observer : observers) {
                observer.update(event, data);
            }
        }
    }
}

// Logger.java
public class Logger implements Observer {
    @Override
    public void update(String event, Object data) {
        System.out.println("[LOG] " + event + ": " + data);
    }
}

// Analytics.java
public class Analytics implements Observer {
    private final List<Map<String, Object>> events = new ArrayList<>();

    @Override
    public void update(String event, Object data) {
        events.add(Map.of("event", event, "data", data));
    }

    public List<Map<String, Object>> getEvents() {
        return Collections.unmodifiableList(events);
    }
}

// Usage
// EventEmitter emitter = new EventEmitter();
// Logger logger = new Logger();
// Analytics analytics = new Analytics();
// emitter.subscribe("user:login", logger);
// emitter.subscribe("user:login", analytics);
// emitter.notify("user:login", Map.of("user", "alice"));
// Output: [LOG] user:login: {user=alice}
```

**Explanation:** The classic observer uses a subject (EventEmitter) that maintains a map of event names to lists of observers. When `notify` is called, the subject iterates over all registered observers for that event and calls their `update` method. The iteration uses a copy of the observer list (Python's `list()`, JavaScript's spread, Java's `CopyOnWriteArrayList`) to safely handle observers that unsubscribe during notification. Using a `Set` (JavaScript) or checking for duplicates (Python) prevents the same observer from being notified twice.

**When to use:** Event-driven architectures, GUI frameworks, real-time notification systems, and any scenario where multiple components need to react to state changes without tight coupling.

### Solution 2: Callback-Based Observer (Pub/Sub)
- **Time Complexity:** O(n) per notification
- **Space Complexity:** O(n) for storing callbacks
- **Difficulty:** Medium

#### Python
```python
from typing import Callable


class PubSub:
    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = {}

    def subscribe(self, event: str, callback: Callable) -> Callable:
        if event not in self._subscribers:
            self._subscribers[event] = []
        self._subscribers[event].append(callback)

        def unsubscribe():
            self._subscribers[event].remove(callback)
        return unsubscribe

    def publish(self, event: str, *args, **kwargs) -> None:
        for callback in list(self._subscribers.get(event, [])):
            callback(*args, **kwargs)


# Usage
bus = PubSub()

messages = []
unsub = bus.subscribe("chat:message", lambda msg: messages.append(msg))

bus.publish("chat:message", "Hello!")
bus.publish("chat:message", "World!")
print(messages)  # ['Hello!', 'World!']

unsub()
bus.publish("chat:message", "Ignored")
print(messages)  # ['Hello!', 'World!']
```

#### JavaScript
```javascript
class PubSub {
  #subscribers = new Map();

  subscribe(event, callback) {
    if (!this.#subscribers.has(event)) {
      this.#subscribers.set(event, []);
    }
    this.#subscribers.get(event).push(callback);

    return () => {
      const callbacks = this.#subscribers.get(event);
      const index = callbacks.indexOf(callback);
      if (index !== -1) callbacks.splice(index, 1);
    };
  }

  publish(event, ...args) {
    const callbacks = this.#subscribers.get(event);
    if (callbacks) {
      for (const callback of [...callbacks]) {
        callback(...args);
      }
    }
  }
}

// Usage
const bus = new PubSub();
const messages = [];

const unsub = bus.subscribe("chat:message", (msg) => messages.push(msg));

bus.publish("chat:message", "Hello!");
bus.publish("chat:message", "World!");
console.log(messages); // ['Hello!', 'World!']

unsub();
bus.publish("chat:message", "Ignored");
console.log(messages); // ['Hello!', 'World!']
```

#### Java
```java
import java.util.*;
import java.util.function.Consumer;

public class PubSub {
    private final Map<String, List<Consumer<Object>>> subscribers =
        new HashMap<>();

    public Runnable subscribe(String event, Consumer<Object> callback) {
        subscribers.computeIfAbsent(event, k -> new ArrayList<>())
                   .add(callback);
        return () -> {
            List<Consumer<Object>> callbacks = subscribers.get(event);
            if (callbacks != null) {
                callbacks.remove(callback);
            }
        };
    }

    public void publish(String event, Object data) {
        List<Consumer<Object>> callbacks = subscribers.get(event);
        if (callbacks != null) {
            for (Consumer<Object> callback : new ArrayList<>(callbacks)) {
                callback.accept(data);
            }
        }
    }
}

// Usage
// PubSub bus = new PubSub();
// List<String> messages = new ArrayList<>();
//
// Runnable unsub = bus.subscribe("chat:message",
//     data -> messages.add((String) data));
//
// bus.publish("chat:message", "Hello!");
// bus.publish("chat:message", "World!");
// System.out.println(messages); // [Hello!, World!]
//
// unsub.run();
// bus.publish("chat:message", "Ignored");
// System.out.println(messages); // [Hello!, World!]
```

**Explanation:** The callback-based variant (Pub/Sub) uses functions/lambdas instead of observer objects. The `subscribe` method returns an unsubscribe function, making cleanup simple and eliminating the need to hold a reference to the observer. This is the dominant pattern in JavaScript (DOM events, Node.js EventEmitter, React state management) and is increasingly common in other languages. It's more lightweight than the class-based approach and fits well with functional programming styles.

**When to use:** When observers are simple and don't need their own state. Ideal for event buses, message brokers, and reactive UI frameworks where callbacks are the natural abstraction.

## Variations & Extensions
- **Async Observer:** Observers return promises/futures, and the subject waits for all to resolve before proceeding
- **Weak Reference Observer:** Use weak references to prevent memory leaks from forgotten subscriptions
- **Filtered Observer:** Observers subscribe with a predicate and only receive matching events
- **Replay Subject:** New observers receive the last N events upon subscribing (as in RxJS `ReplaySubject`)
- **Mediator Pattern:** A centralized mediator replaces direct subject–observer links, reducing coupling further

## Real-World Applications
- DOM event listeners (`addEventListener` / `removeEventListener`)
- Node.js `EventEmitter` class
- React/Vue/Angular change detection and state management (Redux, Vuex)
- Message queues and pub/sub systems (Redis Pub/Sub, Apache Kafka consumers)
- Model-View-Controller (MVC) — the model notifies views of state changes
- Stock ticker and real-time data feeds

## Tags
#design-pattern #behavioral #observer #pub-sub #event-driven #medium
