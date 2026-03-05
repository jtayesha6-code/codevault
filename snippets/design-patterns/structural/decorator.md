# Decorator Pattern

## Problem Statement
- Attach **additional responsibilities to an object dynamically** without modifying its class.
- Provide a flexible alternative to subclassing for extending functionality.
- Allow behaviors to be **composed and stacked** — multiple decorators can wrap the same object.

**Example inputs/outputs:**
- `SimpleCoffee()` → "Simple Coffee", $1.00
- `MilkDecorator(SimpleCoffee())` → "Simple Coffee, Milk", $1.50
- `SugarDecorator(MilkDecorator(SimpleCoffee()))` → "Simple Coffee, Milk, Sugar", $1.70

**Edge cases:**
- Applying the same decorator multiple times (e.g., double shot of espresso)
- Order of decorator application affecting behavior
- Decorators that need to modify the return value vs. add side effects
- Removing a decorator from a chain at runtime

## Solutions

### Solution 1: Coffee Shop Example
- **Time Complexity:** O(d) where d is the number of decorators in the chain
- **Space Complexity:** O(d)
- **Difficulty:** Medium

#### Python
```python
from abc import ABC, abstractmethod


class Coffee(ABC):
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def cost(self) -> float:
        pass


class SimpleCoffee(Coffee):
    def description(self) -> str:
        return "Simple Coffee"

    def cost(self) -> float:
        return 1.00


class CoffeeDecorator(Coffee, ABC):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def description(self) -> str:
        return self._coffee.description()

    def cost(self) -> float:
        return self._coffee.cost()


class MilkDecorator(CoffeeDecorator):
    def description(self) -> str:
        return f"{self._coffee.description()}, Milk"

    def cost(self) -> float:
        return self._coffee.cost() + 0.50


class SugarDecorator(CoffeeDecorator):
    def description(self) -> str:
        return f"{self._coffee.description()}, Sugar"

    def cost(self) -> float:
        return self._coffee.cost() + 0.20


class WhipDecorator(CoffeeDecorator):
    def description(self) -> str:
        return f"{self._coffee.description()}, Whip"

    def cost(self) -> float:
        return self._coffee.cost() + 0.70


# Usage
coffee = SimpleCoffee()
print(f"{coffee.description()} = ${coffee.cost():.2f}")
# Simple Coffee = $1.00

coffee = MilkDecorator(coffee)
print(f"{coffee.description()} = ${coffee.cost():.2f}")
# Simple Coffee, Milk = $1.50

coffee = SugarDecorator(coffee)
print(f"{coffee.description()} = ${coffee.cost():.2f}")
# Simple Coffee, Milk, Sugar = $1.70

coffee = WhipDecorator(coffee)
print(f"{coffee.description()} = ${coffee.cost():.2f}")
# Simple Coffee, Milk, Sugar, Whip = $2.40

# Double milk
fancy = WhipDecorator(MilkDecorator(MilkDecorator(SimpleCoffee())))
print(f"{fancy.description()} = ${fancy.cost():.2f}")
# Simple Coffee, Milk, Milk, Whip = $2.70
```

#### JavaScript
```javascript
class SimpleCoffee {
  description() {
    return "Simple Coffee";
  }

  cost() {
    return 1.00;
  }
}

class MilkDecorator {
  constructor(coffee) {
    this.coffee = coffee;
  }

  description() {
    return `${this.coffee.description()}, Milk`;
  }

  cost() {
    return this.coffee.cost() + 0.50;
  }
}

class SugarDecorator {
  constructor(coffee) {
    this.coffee = coffee;
  }

  description() {
    return `${this.coffee.description()}, Sugar`;
  }

  cost() {
    return this.coffee.cost() + 0.20;
  }
}

class WhipDecorator {
  constructor(coffee) {
    this.coffee = coffee;
  }

  description() {
    return `${this.coffee.description()}, Whip`;
  }

  cost() {
    return this.coffee.cost() + 0.70;
  }
}

// Usage
let coffee = new SimpleCoffee();
console.log(`${coffee.description()} = $${coffee.cost().toFixed(2)}`);
// Simple Coffee = $1.00

coffee = new MilkDecorator(coffee);
console.log(`${coffee.description()} = $${coffee.cost().toFixed(2)}`);
// Simple Coffee, Milk = $1.50

coffee = new SugarDecorator(coffee);
console.log(`${coffee.description()} = $${coffee.cost().toFixed(2)}`);
// Simple Coffee, Milk, Sugar = $1.70

coffee = new WhipDecorator(coffee);
console.log(`${coffee.description()} = $${coffee.cost().toFixed(2)}`);
// Simple Coffee, Milk, Sugar, Whip = $2.40
```

#### Java
```java
// Coffee.java
public interface Coffee {
    String description();
    double cost();
}

// SimpleCoffee.java
public class SimpleCoffee implements Coffee {
    @Override
    public String description() {
        return "Simple Coffee";
    }

    @Override
    public double cost() {
        return 1.00;
    }
}

// CoffeeDecorator.java
public abstract class CoffeeDecorator implements Coffee {
    protected final Coffee coffee;

    public CoffeeDecorator(Coffee coffee) {
        this.coffee = coffee;
    }

    @Override
    public String description() {
        return coffee.description();
    }

    @Override
    public double cost() {
        return coffee.cost();
    }
}

// MilkDecorator.java
public class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String description() {
        return coffee.description() + ", Milk";
    }

    @Override
    public double cost() {
        return coffee.cost() + 0.50;
    }
}

// SugarDecorator.java
public class SugarDecorator extends CoffeeDecorator {
    public SugarDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String description() {
        return coffee.description() + ", Sugar";
    }

    @Override
    public double cost() {
        return coffee.cost() + 0.20;
    }
}

// WhipDecorator.java
public class WhipDecorator extends CoffeeDecorator {
    public WhipDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String description() {
        return coffee.description() + ", Whip";
    }

    @Override
    public double cost() {
        return coffee.cost() + 0.70;
    }
}

// Usage
// Coffee coffee = new SimpleCoffee();
// coffee = new MilkDecorator(coffee);
// coffee = new SugarDecorator(coffee);
// coffee = new WhipDecorator(coffee);
// System.out.println(coffee.description() + " = $" +
//     String.format("%.2f", coffee.cost()));
// Output: Simple Coffee, Milk, Sugar, Whip = $2.40
```

**Explanation:** Each decorator wraps a `Coffee` object and delegates to it while adding its own behavior. `MilkDecorator` adds ", Milk" to the description and $0.50 to the cost. Because every decorator implements the same `Coffee` interface, decorators can be stacked in any combination and any order. The key insight is that `MilkDecorator(SugarDecorator(SimpleCoffee()))` is still a `Coffee` — the client doesn't need to know how many layers of decoration exist. This avoids a combinatorial explosion of subclasses (MilkCoffee, SugarMilkCoffee, WhipSugarMilkCoffee, etc.).

**When to use:** When you need to add responsibilities to individual objects dynamically without affecting other objects of the same class. Perfect for pricing systems, UI component styling, and any scenario with combinatorial feature sets.

### Solution 2: Logging Decorator
- **Time Complexity:** O(1) per decorator layer (plus the wrapped function's time)
- **Space Complexity:** O(1)
- **Difficulty:** Medium

#### Python
```python
import functools
import time


def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[CALL] {func.__name__}(args={args}, kwargs={kwargs})")
        result = func(*args, **kwargs)
        print(f"[RETURN] {func.__name__} -> {result}")
        return result
    return wrapper


def timing(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMING] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def retry(max_attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[RETRY] {func.__name__} attempt {attempt} "
                          f"failed: {e}")
                    if attempt == max_attempts:
                        raise
        return wrapper
    return decorator


# Usage — decorators stack from bottom to top
@timing
@log_calls
def add(a: int, b: int) -> int:
    return a + b


result = add(3, 5)
# [CALL] add(args=(3, 5), kwargs={})
# [RETURN] add -> 8
# [TIMING] add took 0.0001s
print(result)  # 8


@retry(max_attempts=3)
@log_calls
def unreliable_fetch(url: str) -> str:
    return f"Data from {url}"


print(unreliable_fetch("https://api.example.com"))
# [CALL] unreliable_fetch(args=('https://api.example.com',), kwargs={})
# [RETURN] unreliable_fetch -> Data from https://api.example.com
# Data from https://api.example.com
```

#### JavaScript
```javascript
function logCalls(fn) {
  return function (...args) {
    console.log(`[CALL] ${fn.name}(${args.map(a => JSON.stringify(a)).join(", ")})`);
    const result = fn.apply(this, args);
    console.log(`[RETURN] ${fn.name} ->`, result);
    return result;
  };
}

function timing(fn) {
  return function (...args) {
    const start = performance.now();
    const result = fn.apply(this, args);
    const elapsed = (performance.now() - start).toFixed(4);
    console.log(`[TIMING] ${fn.name} took ${elapsed}ms`);
    return result;
  };
}

function retry(maxAttempts = 3) {
  return function (fn) {
    return function (...args) {
      for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
          return fn.apply(this, args);
        } catch (e) {
          console.log(`[RETRY] ${fn.name} attempt ${attempt} failed: ${e.message}`);
          if (attempt === maxAttempts) throw e;
        }
      }
    };
  };
}

// Usage
function add(a, b) {
  return a + b;
}

const decoratedAdd = timing(logCalls(add));

console.log(decoratedAdd(3, 5));
// [CALL] add(3, 5)
// [RETURN] add -> 8
// [TIMING] add took 0.0100ms
// 8

const decoratedFetch = retry(3)(logCalls(function fetchData(url) {
  return `Data from ${url}`;
}));

console.log(decoratedFetch("https://api.example.com"));
// [CALL] fetchData("https://api.example.com")
// [RETURN] fetchData -> Data from https://api.example.com
// Data from https://api.example.com
```

#### Java
```java
import java.util.function.Function;

// FunctionDecorator.java — composable function decorators
public class FunctionDecorators {

    public static <T, R> Function<T, R> logCalls(
            String name, Function<T, R> fn) {
        return input -> {
            System.out.println("[CALL] " + name + "(" + input + ")");
            R result = fn.apply(input);
            System.out.println("[RETURN] " + name + " -> " + result);
            return result;
        };
    }

    public static <T, R> Function<T, R> timing(
            String name, Function<T, R> fn) {
        return input -> {
            long start = System.nanoTime();
            R result = fn.apply(input);
            double elapsed = (System.nanoTime() - start) / 1_000_000.0;
            System.out.printf("[TIMING] %s took %.4fms%n", name, elapsed);
            return result;
        };
    }

    public static <T, R> Function<T, R> retry(
            String name, int maxAttempts, Function<T, R> fn) {
        return input -> {
            for (int attempt = 1; attempt <= maxAttempts; attempt++) {
                try {
                    return fn.apply(input);
                } catch (Exception e) {
                    System.out.printf("[RETRY] %s attempt %d failed: %s%n",
                        name, attempt, e.getMessage());
                    if (attempt == maxAttempts) throw e;
                }
            }
            throw new IllegalStateException("Unreachable");
        };
    }
}

// Usage
// Function<Integer, Integer> doubleIt = x -> x * 2;
//
// Function<Integer, Integer> decorated =
//     FunctionDecorators.timing("doubleIt",
//         FunctionDecorators.logCalls("doubleIt", doubleIt));
//
// System.out.println(decorated.apply(5));
// [CALL] doubleIt(5)
// [RETURN] doubleIt -> 10
// [TIMING] doubleIt took 0.1234ms
// 10
```

**Explanation:** The function-based decorator pattern wraps functions with additional behavior. In Python, the `@decorator` syntax is native language support for this pattern. Each decorator takes a function, returns a new function that adds behavior (logging, timing, retrying) around the original call. Decorators compose naturally — `@timing @log_calls` first logs, then times. This is the most Pythonic application of the Decorator pattern and is widely used in frameworks (Flask routes, Django views, pytest fixtures).

**When to use:** When you need to add cross-cutting concerns (logging, caching, authentication, rate limiting) to functions or methods without modifying their core logic. The function-based approach is simpler than the class-based approach when you only need to wrap a single method.

## Variations & Extensions
- **Transparent Decorator:** The decorator is indistinguishable from the original object (important for `isinstance` checks and type systems)
- **Conditional Decorator:** Only applies decoration when a condition is met (e.g., log only in debug mode)
- **Decorator with State:** The decorator maintains its own state (e.g., call count, cache)
- **Decorator vs. Proxy:** A proxy controls access; a decorator adds behavior — they share the same wrapping structure
- **Python `functools.wraps`:** Preserves the original function's metadata (`__name__`, `__doc__`) when using function decorators

## Real-World Applications
- Java I/O streams — `BufferedReader(InputStreamReader(FileInputStream(...)))` stacks behaviors
- Python decorators — `@app.route`, `@login_required`, `@lru_cache`
- Express.js / Koa middleware — each middleware wraps the next handler with additional behavior
- React Higher-Order Components (HOCs) — `withAuth(withLogging(Component))`
- Logging and monitoring — adding instrumentation without modifying business logic

## Tags
#design-pattern #structural #decorator #wrapper #composition #medium
