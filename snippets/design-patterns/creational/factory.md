# Factory Pattern

## Problem Statement
- Create objects **without specifying the exact class** to instantiate.
- Delegate the instantiation logic to a factory method or class, decoupling the client from concrete implementations.
- Allow new types to be added without modifying existing client code (Open/Closed Principle).

**Example inputs/outputs:**
- `factory.create("button")` → returns a `Button` instance
- `factory.create("checkbox")` → returns a `Checkbox` instance
- `factory.create("unknown")` → raises an error or returns a default

**Edge cases:**
- Requesting an unregistered or unknown type
- Passing invalid configuration to the factory
- Thread-safe factory registration in concurrent environments
- Circular dependencies between created objects

## Solutions

### Solution 1: Simple Factory
- **Time Complexity:** O(1) for object creation
- **Space Complexity:** O(1)
- **Difficulty:** Medium

#### Python
```python
from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass


class EmailNotification(Notification):
    def send(self, message: str) -> str:
        return f"Email: {message}"


class SMSNotification(Notification):
    def send(self, message: str) -> str:
        return f"SMS: {message}"


class PushNotification(Notification):
    def send(self, message: str) -> str:
        return f"Push: {message}"


class NotificationFactory:
    _creators = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }

    @staticmethod
    def create(channel: str) -> Notification:
        creator = NotificationFactory._creators.get(channel)
        if creator is None:
            raise ValueError(f"Unknown notification channel: {channel}")
        return creator()


# Usage
notification = NotificationFactory.create("email")
print(notification.send("Hello!"))  # Email: Hello!

notification = NotificationFactory.create("sms")
print(notification.send("Hello!"))  # SMS: Hello!
```

#### JavaScript
```javascript
class EmailNotification {
  send(message) {
    return `Email: ${message}`;
  }
}

class SMSNotification {
  send(message) {
    return `SMS: ${message}`;
  }
}

class PushNotification {
  send(message) {
    return `Push: ${message}`;
  }
}

class NotificationFactory {
  static #creators = {
    email: EmailNotification,
    sms: SMSNotification,
    push: PushNotification,
  };

  static create(channel) {
    const Creator = NotificationFactory.#creators[channel];
    if (!Creator) {
      throw new Error(`Unknown notification channel: ${channel}`);
    }
    return new Creator();
  }
}

// Usage
const notification = NotificationFactory.create("email");
console.log(notification.send("Hello!")); // Email: Hello!

const sms = NotificationFactory.create("sms");
console.log(sms.send("Hello!")); // SMS: Hello!
```

#### Java
```java
// Notification.java
public interface Notification {
    String send(String message);
}

// EmailNotification.java
public class EmailNotification implements Notification {
    @Override
    public String send(String message) {
        return "Email: " + message;
    }
}

// SMSNotification.java
public class SMSNotification implements Notification {
    @Override
    public String send(String message) {
        return "SMS: " + message;
    }
}

// PushNotification.java
public class PushNotification implements Notification {
    @Override
    public String send(String message) {
        return "Push: " + message;
    }
}

// NotificationFactory.java
public class NotificationFactory {
    public static Notification create(String channel) {
        return switch (channel) {
            case "email" -> new EmailNotification();
            case "sms" -> new SMSNotification();
            case "push" -> new PushNotification();
            default -> throw new IllegalArgumentException(
                "Unknown notification channel: " + channel
            );
        };
    }
}

// Usage
// Notification n = NotificationFactory.create("email");
// System.out.println(n.send("Hello!")); // Email: Hello!
```

**Explanation:** The Simple Factory centralizes object creation in a single static method. The client passes a type identifier, and the factory returns the appropriate concrete instance. The client depends only on the `Notification` interface, never on concrete classes. Adding a new notification channel requires only adding a new class and registering it in the factory — no client code changes.

**When to use:** When you have a small, relatively stable set of related types and want to centralize creation logic. Common in configuration-driven systems where the type is determined at runtime (e.g., from a config file or user input).

### Solution 2: Factory Method
- **Time Complexity:** O(1) for object creation
- **Space Complexity:** O(1)
- **Difficulty:** Medium

#### Python
```python
from abc import ABC, abstractmethod


class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class HTMLButton(Button):
    def render(self) -> str:
        return "<button>HTML Button</button>"


class WindowsButton(Button):
    def render(self) -> str:
        return "[Windows Button]"


class Dialog(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        """Factory method — subclasses decide which Button to create."""
        pass

    def render(self) -> str:
        button = self.create_button()
        return f"Dialog with {button.render()}"


class WebDialog(Dialog):
    def create_button(self) -> Button:
        return HTMLButton()


class WindowsDialog(Dialog):
    def create_button(self) -> Button:
        return WindowsButton()


# Usage
def get_dialog(platform: str) -> Dialog:
    if platform == "web":
        return WebDialog()
    elif platform == "windows":
        return WindowsDialog()
    raise ValueError(f"Unknown platform: {platform}")


dialog = get_dialog("web")
print(dialog.render())  # Dialog with <button>HTML Button</button>
```

#### JavaScript
```javascript
class HTMLButton {
  render() {
    return "<button>HTML Button</button>";
  }
}

class WindowsButton {
  render() {
    return "[Windows Button]";
  }
}

class Dialog {
  createButton() {
    throw new Error("Subclasses must implement createButton()");
  }

  render() {
    const button = this.createButton();
    return `Dialog with ${button.render()}`;
  }
}

class WebDialog extends Dialog {
  createButton() {
    return new HTMLButton();
  }
}

class WindowsDialog extends Dialog {
  createButton() {
    return new WindowsButton();
  }
}

// Usage
function getDialog(platform) {
  if (platform === "web") return new WebDialog();
  if (platform === "windows") return new WindowsDialog();
  throw new Error(`Unknown platform: ${platform}`);
}

const dialog = getDialog("web");
console.log(dialog.render()); // Dialog with <button>HTML Button</button>
```

#### Java
```java
// Button.java
public interface Button {
    String render();
}

// HTMLButton.java
public class HTMLButton implements Button {
    @Override
    public String render() {
        return "<button>HTML Button</button>";
    }
}

// WindowsButton.java
public class WindowsButton implements Button {
    @Override
    public String render() {
        return "[Windows Button]";
    }
}

// Dialog.java
public abstract class Dialog {
    public abstract Button createButton();

    public String render() {
        Button button = createButton();
        return "Dialog with " + button.render();
    }
}

// WebDialog.java
public class WebDialog extends Dialog {
    @Override
    public Button createButton() {
        return new HTMLButton();
    }
}

// WindowsDialog.java
public class WindowsDialog extends Dialog {
    @Override
    public Button createButton() {
        return new WindowsButton();
    }
}

// Usage
// Dialog dialog = new WebDialog();
// System.out.println(dialog.render());
// Output: Dialog with <button>HTML Button</button>
```

**Explanation:** The Factory Method pattern defines an interface for creating objects but lets subclasses decide which class to instantiate. The base `Dialog` class defines a `render` workflow that depends on a `Button`, but it delegates the actual button creation to subclasses via `createButton()`. Each subclass (`WebDialog`, `WindowsDialog`) returns the appropriate button type. This follows the Open/Closed Principle — adding a new platform requires a new `Dialog` subclass without modifying existing code.

**When to use:** When a class cannot anticipate which objects it needs to create, or when you want subclasses to specify the objects they create. Ideal for frameworks and libraries where users extend base classes with their own implementations.

## Variations & Extensions
- **Abstract Factory:** Creates families of related objects (e.g., buttons + checkboxes + text fields for a given platform) without specifying concrete classes
- **Parameterized Factory with Registry:** Use a dictionary/map to register creator functions dynamically at runtime, enabling plugin architectures
- **Factory with Dependency Injection:** Combine factories with DI containers for more flexible object graphs
- **Prototype-based Factory:** Instead of instantiating new objects, clone a prototype instance

## Real-World Applications
- UI frameworks creating platform-specific components (React Native, Flutter)
- Database drivers — `DriverManager.getConnection()` in JDBC returns the correct driver implementation
- Logging frameworks — `LoggerFactory.getLogger()` in SLF4J
- Payment processing — creating the right payment handler based on payment method
- Document parsers — creating the right parser based on file extension (JSON, XML, CSV)

## Tags
#design-pattern #creational #factory #factory-method #medium
