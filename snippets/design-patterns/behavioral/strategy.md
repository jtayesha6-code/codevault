# Strategy Pattern

## Problem Statement
- Define a **family of algorithms**, encapsulate each one, and make them **interchangeable** at runtime.
- Let the algorithm vary independently from the clients that use it.
- Eliminate complex conditional logic (`if/else` or `switch`) that selects behavior based on type.

**Example inputs/outputs:**
- `payment.process(100, credit_card_strategy)` → processes $100 via credit card
- `payment.process(100, paypal_strategy)` → processes $100 via PayPal
- `sorter.sort(data, quicksort_strategy)` → sorts data using quicksort

**Edge cases:**
- Strategy is `null` or not set before use
- Switching strategies mid-operation
- Strategies requiring different configuration or dependencies
- Ensuring all strategies conform to the same interface contract

## Solutions

### Solution 1: Payment Processing Strategies
- **Time Complexity:** O(1) for strategy selection; varies per strategy execution
- **Space Complexity:** O(1)
- **Difficulty:** Medium

#### Python
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def pay(self, amount: float) -> str:
        masked = self.card_number[-4:]
        return f"Paid ${amount:.2f} with credit card ending in {masked}"


class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} via PayPal ({self.email})"


class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def pay(self, amount: float) -> str:
        short_addr = self.wallet_address[:8] + "..."
        return f"Paid ${amount:.2f} with crypto wallet {short_addr}"


@dataclass
class ShoppingCart:
    items: list[tuple[str, float]]

    def total(self) -> float:
        return sum(price for _, price in self.items)

    def checkout(self, strategy: PaymentStrategy) -> str:
        amount = self.total()
        if amount <= 0:
            return "Cart is empty"
        return strategy.pay(amount)


# Usage
cart = ShoppingCart(items=[("Book", 12.99), ("Pen", 1.50)])

print(cart.checkout(CreditCardPayment("4111111111111234")))
# Paid $14.49 with credit card ending in 1234

print(cart.checkout(PayPalPayment("user@example.com")))
# Paid $14.49 via PayPal (user@example.com)

print(cart.checkout(CryptoPayment("0xABCDEF1234567890")))
# Paid $14.49 with crypto wallet 0xABCDEF...
```

#### JavaScript
```javascript
class CreditCardPayment {
  constructor(cardNumber) {
    this.cardNumber = cardNumber;
  }

  pay(amount) {
    const masked = this.cardNumber.slice(-4);
    return `Paid $${amount.toFixed(2)} with credit card ending in ${masked}`;
  }
}

class PayPalPayment {
  constructor(email) {
    this.email = email;
  }

  pay(amount) {
    return `Paid $${amount.toFixed(2)} via PayPal (${this.email})`;
  }
}

class CryptoPayment {
  constructor(walletAddress) {
    this.walletAddress = walletAddress;
  }

  pay(amount) {
    const shortAddr = this.walletAddress.slice(0, 8) + "...";
    return `Paid $${amount.toFixed(2)} with crypto wallet ${shortAddr}`;
  }
}

class ShoppingCart {
  constructor() {
    this.items = [];
  }

  addItem(name, price) {
    this.items.push({ name, price });
  }

  total() {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }

  checkout(strategy) {
    const amount = this.total();
    if (amount <= 0) return "Cart is empty";
    return strategy.pay(amount);
  }
}

// Usage
const cart = new ShoppingCart();
cart.addItem("Book", 12.99);
cart.addItem("Pen", 1.50);

console.log(cart.checkout(new CreditCardPayment("4111111111111234")));
// Paid $14.49 with credit card ending in 1234

console.log(cart.checkout(new PayPalPayment("user@example.com")));
// Paid $14.49 via PayPal (user@example.com)

console.log(cart.checkout(new CryptoPayment("0xABCDEF1234567890")));
// Paid $14.49 with crypto wallet 0xABCDEF...
```

#### Java
```java
// PaymentStrategy.java
public interface PaymentStrategy {
    String pay(double amount);
}

// CreditCardPayment.java
public class CreditCardPayment implements PaymentStrategy {
    private final String cardNumber;

    public CreditCardPayment(String cardNumber) {
        this.cardNumber = cardNumber;
    }

    @Override
    public String pay(double amount) {
        String masked = cardNumber.substring(cardNumber.length() - 4);
        return String.format("Paid $%.2f with credit card ending in %s",
            amount, masked);
    }
}

// PayPalPayment.java
public class PayPalPayment implements PaymentStrategy {
    private final String email;

    public PayPalPayment(String email) {
        this.email = email;
    }

    @Override
    public String pay(double amount) {
        return String.format("Paid $%.2f via PayPal (%s)", amount, email);
    }
}

// CryptoPayment.java
public class CryptoPayment implements PaymentStrategy {
    private final String walletAddress;

    public CryptoPayment(String walletAddress) {
        this.walletAddress = walletAddress;
    }

    @Override
    public String pay(double amount) {
        String shortAddr = walletAddress.substring(0, 8) + "...";
        return String.format("Paid $%.2f with crypto wallet %s",
            amount, shortAddr);
    }
}

// ShoppingCart.java
import java.util.ArrayList;
import java.util.List;

public class ShoppingCart {
    private final List<double[]> items = new ArrayList<>();

    public void addItem(String name, double price) {
        items.add(new double[]{price});
    }

    public double total() {
        return items.stream().mapToDouble(item -> item[0]).sum();
    }

    public String checkout(PaymentStrategy strategy) {
        double amount = total();
        if (amount <= 0) return "Cart is empty";
        return strategy.pay(amount);
    }
}

// Usage
// ShoppingCart cart = new ShoppingCart();
// cart.addItem("Book", 12.99);
// cart.addItem("Pen", 1.50);
// System.out.println(cart.checkout(new CreditCardPayment("4111111111111234")));
// Output: Paid $14.49 with credit card ending in 1234
```

**Explanation:** The context (`ShoppingCart`) delegates the payment behavior to a strategy object passed at checkout time. Each strategy (CreditCard, PayPal, Crypto) implements the same `pay` interface but with different internal logic. The cart doesn't need to know how payment works — it just calls `strategy.pay(amount)`. This eliminates the need for conditional branches and makes it trivial to add new payment methods: create a new class implementing `PaymentStrategy`, and pass it to `checkout`.

**When to use:** When you have multiple algorithms or behaviors for the same task and want to switch between them at runtime. Ideal for payment processing, tax calculation, shipping cost computation, and any domain with pluggable business rules.

### Solution 2: Sorting Strategies
- **Time Complexity:** Varies per strategy (O(n²) for bubble sort, O(n log n) for merge sort)
- **Space Complexity:** Varies per strategy
- **Difficulty:** Medium

#### Python
```python
from abc import ABC, abstractmethod


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class BubbleSort(SortStrategy):
    @property
    def name(self) -> str:
        return "Bubble Sort"

    def sort(self, data: list[int]) -> list[int]:
        arr = data[:]
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class MergeSort(SortStrategy):
    @property
    def name(self) -> str:
        return "Merge Sort"

    def sort(self, data: list[int]) -> list[int]:
        if len(data) <= 1:
            return data[:]
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self._merge(left, right)

    def _merge(self, left: list[int], right: list[int]) -> list[int]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result


class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    @property
    def strategy(self) -> SortStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def sort(self, data: list[int]) -> list[int]:
        print(f"Sorting with {self._strategy.name}")
        return self._strategy.sort(data)


# Usage
data = [38, 27, 43, 3, 9, 82, 10]

sorter = Sorter(BubbleSort())
print(sorter.sort(data))  # [3, 9, 10, 27, 38, 43, 82]

sorter.strategy = MergeSort()
print(sorter.sort(data))  # [3, 9, 10, 27, 38, 43, 82]
```

#### JavaScript
```javascript
class BubbleSort {
  get name() {
    return "Bubble Sort";
  }

  sort(data) {
    const arr = [...data];
    const n = arr.length;
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n - i - 1; j++) {
        if (arr[j] > arr[j + 1]) {
          [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        }
      }
    }
    return arr;
  }
}

class MergeSort {
  get name() {
    return "Merge Sort";
  }

  sort(data) {
    if (data.length <= 1) return [...data];
    const mid = Math.floor(data.length / 2);
    const left = this.sort(data.slice(0, mid));
    const right = this.sort(data.slice(mid));
    return this.#merge(left, right);
  }

  #merge(left, right) {
    const result = [];
    let i = 0, j = 0;
    while (i < left.length && j < right.length) {
      if (left[i] <= right[j]) {
        result.push(left[i++]);
      } else {
        result.push(right[j++]);
      }
    }
    return result.concat(left.slice(i), right.slice(j));
  }
}

class Sorter {
  constructor(strategy) {
    this.strategy = strategy;
  }

  sort(data) {
    console.log(`Sorting with ${this.strategy.name}`);
    return this.strategy.sort(data);
  }
}

// Usage
const data = [38, 27, 43, 3, 9, 82, 10];

const sorter = new Sorter(new BubbleSort());
console.log(sorter.sort(data)); // [3, 9, 10, 27, 38, 43, 82]

sorter.strategy = new MergeSort();
console.log(sorter.sort(data)); // [3, 9, 10, 27, 38, 43, 82]
```

#### Java
```java
import java.util.Arrays;

// SortStrategy.java
public interface SortStrategy {
    int[] sort(int[] data);
    String getName();
}

// BubbleSort.java
public class BubbleSort implements SortStrategy {
    @Override
    public String getName() {
        return "Bubble Sort";
    }

    @Override
    public int[] sort(int[] data) {
        int[] arr = data.clone();
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
        return arr;
    }
}

// MergeSort.java
public class MergeSort implements SortStrategy {
    @Override
    public String getName() {
        return "Merge Sort";
    }

    @Override
    public int[] sort(int[] data) {
        if (data.length <= 1) return data.clone();
        int mid = data.length / 2;
        int[] left = sort(Arrays.copyOfRange(data, 0, mid));
        int[] right = sort(Arrays.copyOfRange(data, mid, data.length));
        return merge(left, right);
    }

    private int[] merge(int[] left, int[] right) {
        int[] result = new int[left.length + right.length];
        int i = 0, j = 0, k = 0;
        while (i < left.length && j < right.length) {
            result[k++] = (left[i] <= right[j]) ? left[i++] : right[j++];
        }
        while (i < left.length) result[k++] = left[i++];
        while (j < right.length) result[k++] = right[j++];
        return result;
    }
}

// Sorter.java
public class Sorter {
    private SortStrategy strategy;

    public Sorter(SortStrategy strategy) {
        this.strategy = strategy;
    }

    public void setStrategy(SortStrategy strategy) {
        this.strategy = strategy;
    }

    public int[] sort(int[] data) {
        System.out.println("Sorting with " + strategy.getName());
        return strategy.sort(data);
    }
}

// Usage
// int[] data = {38, 27, 43, 3, 9, 82, 10};
// Sorter sorter = new Sorter(new BubbleSort());
// System.out.println(Arrays.toString(sorter.sort(data)));
// Output: [3, 9, 10, 27, 38, 43, 82]
//
// sorter.setStrategy(new MergeSort());
// System.out.println(Arrays.toString(sorter.sort(data)));
// Output: [3, 9, 10, 27, 38, 43, 82]
```

**Explanation:** The Sorter context holds a reference to a `SortStrategy` and delegates the sorting work to it. Strategies can be swapped at runtime via a setter, allowing the same `Sorter` instance to use different algorithms depending on the data characteristics (e.g., use bubble sort for nearly-sorted small arrays, merge sort for large datasets). Each strategy is self-contained and independently testable.

**When to use:** When you need to select an algorithm at runtime based on data characteristics, user preferences, or performance requirements. Common in sorting, compression, routing, and any domain with multiple interchangeable algorithms.

## Variations & Extensions
- **Function-based Strategy:** In languages with first-class functions, pass a function/lambda instead of a strategy object — simpler for one-method strategies
- **Strategy with Context Data:** Pass the context itself to the strategy, allowing strategies to access richer information
- **Composite Strategy:** Combine multiple strategies (e.g., sort by multiple criteria using a chain of comparators)
- **Strategy Registry:** Map string keys to strategy instances for configuration-driven selection

## Real-World Applications
- Payment gateways — selecting between Stripe, PayPal, or bank transfer at checkout
- Compression libraries — choosing between gzip, brotli, or zstd based on content type
- Authentication — switching between OAuth, JWT, or API key validation
- Routing algorithms — selecting shortest path vs. fastest route vs. least fuel
- Tax calculation — applying different tax rules per region or product category

## Tags
#design-pattern #behavioral #strategy #polymorphism #medium
