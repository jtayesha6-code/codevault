# Error Handling Best Practices

## Overview
Robust error handling is critical for building reliable software. This guide covers try/catch patterns, custom exceptions, logging strategies, and retry logic across Python, JavaScript, and Java.

---

## 1. Try/Catch Fundamentals

#### Python
```python
import traceback

# Basic try/except/else/finally
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Caught: {e}")
except (TypeError, ValueError) as e:
    print(f"Type or value error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
    traceback.print_exc()
else:
    # Runs only if no exception was raised
    print(f"Success: {result}")
finally:
    # Always runs — cleanup goes here
    print("Cleanup complete")


# Context manager for resource safety
with open("data.txt", "r") as f:
    content = f.read()
# File is automatically closed, even if an exception occurs
```

#### JavaScript
```javascript
// Basic try/catch/finally
try {
  const data = JSON.parse('{"invalid json}');
} catch (error) {
  if (error instanceof SyntaxError) {
    console.error("JSON parse error:", error.message);
  } else if (error instanceof TypeError) {
    console.error("Type error:", error.message);
  } else {
    console.error("Unexpected error:", error);
  }
} finally {
  console.log("Cleanup complete");
}

// Async/await error handling
async function fetchData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Fetch failed:", error.message);
    throw error; // re-throw if caller should handle it
  }
}

// Promise .catch() pattern
fetch("/api/data")
  .then((res) => res.json())
  .then((data) => console.log(data))
  .catch((err) => console.error("Request failed:", err));
```

#### Java
```java
import java.io.*;

public class ErrorHandlingBasics {

    // Basic try/catch/finally
    public void readFile(String path) {
        BufferedReader reader = null;
        try {
            reader = new BufferedReader(new FileReader(path));
            String line = reader.readLine();
            System.out.println(line);
        } catch (FileNotFoundException e) {
            System.err.println("File not found: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("IO error: " + e.getMessage());
        } finally {
            try {
                if (reader != null) reader.close();
            } catch (IOException e) {
                System.err.println("Failed to close reader");
            }
        }
    }

    // Try-with-resources (Java 7+) — preferred approach
    public void readFileSafe(String path) {
        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }
    }

    // Multi-catch (Java 7+)
    public void multiCatch(String input) {
        try {
            int num = Integer.parseInt(input);
            int[] arr = new int[num];
            arr[num] = 42;
        } catch (NumberFormatException | ArrayIndexOutOfBoundsException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
```

---

## 2. Custom Exception Classes

#### Python
```python
class AppError(Exception):
    """Base exception for the application."""
    def __init__(self, message, code=None, details=None):
        super().__init__(message)
        self.code = code
        self.details = details or {}


class ValidationError(AppError):
    """Raised when input validation fails."""
    def __init__(self, field, message):
        super().__init__(
            message=f"Validation failed for '{field}': {message}",
            code="VALIDATION_ERROR",
            details={"field": field}
        )


class NotFoundError(AppError):
    """Raised when a resource is not found."""
    def __init__(self, resource, resource_id):
        super().__init__(
            message=f"{resource} with id '{resource_id}' not found",
            code="NOT_FOUND",
            details={"resource": resource, "id": resource_id}
        )


# Usage
def get_user(user_id):
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValidationError("user_id", "must be a positive integer")
    # Simulate lookup failure
    raise NotFoundError("User", user_id)


try:
    get_user(999)
except NotFoundError as e:
    print(f"[{e.code}] {e}")
    print(f"Details: {e.details}")
except AppError as e:
    print(f"App error [{e.code}]: {e}")
```

#### JavaScript
```javascript
class AppError extends Error {
  constructor(message, code = "UNKNOWN_ERROR", details = {}) {
    super(message);
    this.name = this.constructor.name;
    this.code = code;
    this.details = details;
    Error.captureStackTrace?.(this, this.constructor);
  }
}

class ValidationError extends AppError {
  constructor(field, message) {
    super(
      `Validation failed for '${field}': ${message}`,
      "VALIDATION_ERROR",
      { field }
    );
  }
}

class NotFoundError extends AppError {
  constructor(resource, id) {
    super(
      `${resource} with id '${id}' not found`,
      "NOT_FOUND",
      { resource, id }
    );
  }
}

// Usage
function getUser(userId) {
  if (typeof userId !== "number" || userId <= 0) {
    throw new ValidationError("userId", "must be a positive number");
  }
  throw new NotFoundError("User", userId);
}

try {
  getUser(999);
} catch (error) {
  if (error instanceof NotFoundError) {
    console.error(`[${error.code}] ${error.message}`);
    console.error("Details:", error.details);
  } else if (error instanceof AppError) {
    console.error(`App error [${error.code}]: ${error.message}`);
  } else {
    throw error; // re-throw unknown errors
  }
}
```

#### Java
```java
// Base application exception
public class AppException extends RuntimeException {
    private final String code;
    private final Map<String, Object> details;

    public AppException(String message, String code, Map<String, Object> details) {
        super(message);
        this.code = code;
        this.details = details != null ? details : Map.of();
    }

    public String getCode() { return code; }
    public Map<String, Object> getDetails() { return details; }
}

// Specific exceptions
public class ValidationException extends AppException {
    public ValidationException(String field, String message) {
        super(
            String.format("Validation failed for '%s': %s", field, message),
            "VALIDATION_ERROR",
            Map.of("field", field)
        );
    }
}

public class NotFoundException extends AppException {
    public NotFoundException(String resource, Object id) {
        super(
            String.format("%s with id '%s' not found", resource, id),
            "NOT_FOUND",
            Map.of("resource", resource, "id", id)
        );
    }
}

// Usage
public class UserService {
    public User getUser(int userId) {
        if (userId <= 0) {
            throw new ValidationException("userId", "must be a positive integer");
        }
        // Simulate lookup failure
        throw new NotFoundException("User", userId);
    }

    public static void main(String[] args) {
        try {
            new UserService().getUser(999);
        } catch (NotFoundException e) {
            System.err.printf("[%s] %s%n", e.getCode(), e.getMessage());
            System.err.println("Details: " + e.getDetails());
        } catch (AppException e) {
            System.err.printf("App error [%s]: %s%n", e.getCode(), e.getMessage());
        }
    }
}
```

---

## 3. Error Logging Patterns

#### Python
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def process_order(order_id):
    logger.info("Processing order %s", order_id)
    try:
        # Simulate processing
        if order_id < 0:
            raise ValueError("Invalid order ID")
        logger.info("Order %s processed successfully", order_id)
    except ValueError as e:
        logger.warning("Validation error for order %s: %s", order_id, e)
        raise
    except Exception as e:
        logger.error("Failed to process order %s: %s", order_id, e, exc_info=True)
        raise
```

#### JavaScript
```javascript
// Structured logging helper
const LogLevel = { DEBUG: 0, INFO: 1, WARN: 2, ERROR: 3 };

function createLogger(name, minLevel = LogLevel.INFO) {
  function log(level, levelName, message, context = {}) {
    if (level < minLevel) return;
    const entry = {
      timestamp: new Date().toISOString(),
      level: levelName,
      logger: name,
      message,
      ...context,
    };
    const output = level >= LogLevel.ERROR ? console.error : console.log;
    output(JSON.stringify(entry));
  }

  return {
    debug: (msg, ctx) => log(LogLevel.DEBUG, "DEBUG", msg, ctx),
    info: (msg, ctx) => log(LogLevel.INFO, "INFO", msg, ctx),
    warn: (msg, ctx) => log(LogLevel.WARN, "WARN", msg, ctx),
    error: (msg, ctx) => log(LogLevel.ERROR, "ERROR", msg, ctx),
  };
}

// Usage
const logger = createLogger("OrderService");

function processOrder(orderId) {
  logger.info("Processing order", { orderId });
  try {
    if (orderId < 0) throw new Error("Invalid order ID");
    logger.info("Order processed successfully", { orderId });
  } catch (error) {
    logger.error("Failed to process order", {
      orderId,
      error: error.message,
      stack: error.stack,
    });
    throw error;
  }
}
```

#### Java
```java
import java.util.logging.*;

public class OrderService {
    private static final Logger logger = Logger.getLogger(OrderService.class.getName());

    public void processOrder(int orderId) {
        logger.info(() -> "Processing order " + orderId);
        try {
            if (orderId < 0) {
                throw new IllegalArgumentException("Invalid order ID");
            }
            logger.info(() -> "Order " + orderId + " processed successfully");
        } catch (IllegalArgumentException e) {
            logger.warning(() -> "Validation error for order " + orderId + ": " + e.getMessage());
            throw e;
        } catch (Exception e) {
            logger.log(Level.SEVERE, "Failed to process order " + orderId, e);
            throw e;
        }
    }
}
```

---

## 4. Retry Logic with Exponential Backoff

#### Python
```python
import time
import random
import logging

logger = logging.getLogger(__name__)


def retry_with_backoff(func, max_retries=3, base_delay=1.0,
                       max_delay=60.0, retryable_exceptions=(Exception,)):
    """
    Retry a function with exponential backoff and jitter.
    """
    for attempt in range(max_retries + 1):
        try:
            return func()
        except retryable_exceptions as e:
            if attempt == max_retries:
                logger.error("All %d retries exhausted: %s", max_retries, e)
                raise

            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, delay * 0.1)
            wait = delay + jitter

            logger.warning(
                "Attempt %d/%d failed: %s. Retrying in %.1fs",
                attempt + 1, max_retries, e, wait
            )
            time.sleep(wait)


# Decorator version
def retryable(max_retries=3, base_delay=1.0, exceptions=(Exception,)):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return retry_with_backoff(
                lambda: func(*args, **kwargs),
                max_retries=max_retries,
                base_delay=base_delay,
                retryable_exceptions=exceptions,
            )
        return wrapper
    return decorator


# Usage
@retryable(max_retries=3, base_delay=0.5, exceptions=(ConnectionError, TimeoutError))
def call_external_api():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Connection refused")
    return {"status": "ok"}


try:
    result = call_external_api()
    print(f"Success: {result}")
except ConnectionError:
    print("Failed after all retries")
```

#### JavaScript
```javascript
async function retryWithBackoff(fn, {
  maxRetries = 3,
  baseDelay = 1000,
  maxDelay = 60000,
  retryableErrors = [Error],
} = {}) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      const isRetryable = retryableErrors.some((cls) => error instanceof cls);
      if (!isRetryable || attempt === maxRetries) {
        throw error;
      }

      const delay = Math.min(baseDelay * 2 ** attempt, maxDelay);
      const jitter = Math.random() * delay * 0.1;
      const wait = delay + jitter;

      console.warn(
        `Attempt ${attempt + 1}/${maxRetries} failed: ${error.message}. ` +
        `Retrying in ${(wait / 1000).toFixed(1)}s`
      );
      await new Promise((resolve) => setTimeout(resolve, wait));
    }
  }
}

// Usage
async function callExternalAPI() {
  if (Math.random() < 0.7) {
    throw new Error("Connection refused");
  }
  return { status: "ok" };
}

(async () => {
  try {
    const result = await retryWithBackoff(callExternalAPI, {
      maxRetries: 3,
      baseDelay: 500,
    });
    console.log("Success:", result);
  } catch (error) {
    console.error("Failed after all retries:", error.message);
  }
})();
```

#### Java
```java
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;
import java.util.logging.Logger;

public class RetryWithBackoff {
    private static final Logger logger = Logger.getLogger(RetryWithBackoff.class.getName());

    public static <T> T execute(Supplier<T> task, int maxRetries,
                                long baseDelayMs, long maxDelayMs,
                                Class<? extends Exception>... retryableExceptions) throws Exception {
        for (int attempt = 0; attempt <= maxRetries; attempt++) {
            try {
                return task.get();
            } catch (Exception e) {
                boolean isRetryable = false;
                for (Class<? extends Exception> cls : retryableExceptions) {
                    if (cls.isInstance(e)) {
                        isRetryable = true;
                        break;
                    }
                }

                if (!isRetryable || attempt == maxRetries) {
                    throw e;
                }

                long delay = Math.min(baseDelayMs * (1L << attempt), maxDelayMs);
                long jitter = (long) (Math.random() * delay * 0.1);
                long wait = delay + jitter;

                logger.warning(String.format(
                    "Attempt %d/%d failed: %s. Retrying in %dms",
                    attempt + 1, maxRetries, e.getMessage(), wait
                ));
                TimeUnit.MILLISECONDS.sleep(wait);
            }
        }
        throw new RuntimeException("Retry logic error");
    }

    // Usage
    public static void main(String[] args) {
        try {
            String result = execute(
                () -> {
                    if (Math.random() < 0.7) {
                        throw new RuntimeException("Connection refused");
                    }
                    return "ok";
                },
                3, 500, 60000, RuntimeException.class
            );
            System.out.println("Success: " + result);
        } catch (Exception e) {
            System.err.println("Failed after all retries: " + e.getMessage());
        }
    }
}
```

**Explanation:**
1. Start with a base delay (e.g., 500ms)
2. On each retry, double the delay: 500ms → 1s → 2s → 4s
3. Add random jitter (±10%) to prevent thundering herd
4. Cap the delay at a maximum to avoid unreasonable waits
5. Only retry on specified exception types — don't retry on programming errors

---

## 5. Error Handling Anti-Patterns

```python
# ❌ DON'T: Catch and silence errors
try:
    risky_operation()
except Exception:
    pass

# ✅ DO: Log or handle meaningfully
try:
    risky_operation()
except SpecificError as e:
    logger.error("Operation failed: %s", e)
    raise


# ❌ DON'T: Catch overly broad exceptions at low level
try:
    value = int(user_input)
except Exception:
    value = 0

# ✅ DO: Catch specific exceptions
try:
    value = int(user_input)
except ValueError:
    value = 0


# ❌ DON'T: Use exceptions for flow control
try:
    item = my_dict[key]
except KeyError:
    item = default_value

# ✅ DO: Use language features
item = my_dict.get(key, default_value)
```

---

## Variations & Extensions
- **Circuit breaker pattern:** Stop retrying after repeated failures and fail fast
- **Dead letter queues:** Route failed messages for later analysis
- **Global error handlers:** Express error middleware, Python sys.excepthook
- **Structured error responses:** Standardized JSON error format for APIs

## Real-World Applications
- API gateway retry logic for microservice communication
- Payment processing with idempotent retries
- Database connection recovery in connection pools
- File upload retry logic in cloud storage SDKs

## Tags
#error-handling #best-practices #retry #logging #exceptions #python #javascript #java
