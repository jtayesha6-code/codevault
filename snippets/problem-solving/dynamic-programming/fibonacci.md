# Fibonacci Sequence (Dynamic Programming)

## Problem Statement
- Compute the **nth Fibonacci number**, where the sequence is defined as:
  - `F(0) = 0`, `F(1) = 1`
  - `F(n) = F(n-1) + F(n-2)` for `n ≥ 2`
- This problem is a classic introduction to dynamic programming, illustrating how overlapping subproblems and optimal substructure can be exploited.

**Example inputs/outputs:**
- Input: `n = 0` → Output: `0`
- Input: `n = 1` → Output: `1`
- Input: `n = 6` → Output: `8` (sequence: 0, 1, 1, 2, 3, 5, 8)
- Input: `n = 10` → Output: `55`

**Edge cases:**
- `n = 0` and `n = 1` (base cases)
- Large values of `n` (performance and overflow concerns)
- Negative input (undefined in the classic formulation)

## Solutions

### Solution 1: Naive Recursion
- **Time Complexity:** O(2^n)
- **Space Complexity:** O(n) — recursion stack depth
- **Difficulty:** Medium

#### Python
```python
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)
```

#### JavaScript
```javascript
function fibNaive(n) {
  if (n <= 1) {
    return n;
  }
  return fibNaive(n - 1) + fibNaive(n - 2);
}
```

#### Java
```java
public class Fibonacci {
    public static long fibNaive(int n) {
        if (n <= 1) {
            return n;
        }
        return fibNaive(n - 1) + fibNaive(n - 2);
    }
}
```

**Explanation:** Directly implements the mathematical definition. Each call branches into two recursive calls, creating an exponential call tree. For example, `fib(5)` computes `fib(3)` twice and `fib(2)` three times. This redundant computation makes it impractical for `n > 35`.

**When to use:** Only useful for understanding the problem or as a starting point to motivate dynamic programming. Never use in production due to exponential time.

### Solution 2: Memoization (Top-Down DP)
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)
- **Difficulty:** Medium

#### Python
```python
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

#### JavaScript
```javascript
function fibMemo(n, memo = new Map()) {
  if (n <= 1) {
    return n;
  }
  if (memo.has(n)) {
    return memo.get(n);
  }
  const result = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
  memo.set(n, result);
  return result;
}
```

#### Java
```java
import java.util.HashMap;
import java.util.Map;

public class Fibonacci {
    public static long fibMemo(int n) {
        return fibMemoHelper(n, new HashMap<>());
    }

    private static long fibMemoHelper(int n, Map<Integer, Long> memo) {
        if (n <= 1) {
            return n;
        }
        if (memo.containsKey(n)) {
            return memo.get(n);
        }
        long result = fibMemoHelper(n - 1, memo) + fibMemoHelper(n - 2, memo);
        memo.put(n, result);
        return result;
    }
}
```

**Explanation:** Enhances naive recursion by caching results in a hash map. Before computing `fib(n)`, check if it's already been computed. Each subproblem is solved exactly once, reducing the time from O(2^n) to O(n). The recursion tree collapses into a linear chain of lookups and computations.

**When to use:** When you want to keep the recursive structure (top-down thinking) while achieving linear performance. Good for problems where only a subset of subproblems are needed, as it avoids computing unnecessary states.

### Solution 3: Tabulation (Bottom-Up DP)
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)
- **Difficulty:** Medium

#### Python
```python
def fib_tabulation(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

#### JavaScript
```javascript
function fibTabulation(n) {
  if (n <= 1) {
    return n;
  }
  const dp = new Array(n + 1).fill(0);
  dp[1] = 1;
  for (let i = 2; i <= n; i++) {
    dp[i] = dp[i - 1] + dp[i - 2];
  }
  return dp[n];
}
```

#### Java
```java
public class Fibonacci {
    public static long fibTabulation(int n) {
        if (n <= 1) {
            return n;
        }
        long[] dp = new long[n + 1];
        dp[1] = 1;
        for (int i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        return dp[n];
    }
}
```

**Explanation:** Build the solution from the bottom up. Start with the base cases `dp[0] = 0` and `dp[1] = 1`, then iteratively fill the table up to `dp[n]`. Each entry only depends on the previous two, so we compute them in order. No recursion overhead and no risk of stack overflow.

**When to use:** Preferred in most production settings. Eliminates recursion overhead, avoids stack overflow on large inputs, and is straightforward to implement. Use when all subproblems need to be computed.

### Solution 4: Space-Optimized (Iterative)
- **Time Complexity:** O(n)
- **Space Complexity:** O(1)
- **Difficulty:** Medium

#### Python
```python
def fib_optimized(n):
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1
```

#### JavaScript
```javascript
function fibOptimized(n) {
  if (n <= 1) {
    return n;
  }
  let prev2 = 0;
  let prev1 = 1;
  for (let i = 2; i <= n; i++) {
    const curr = prev1 + prev2;
    prev2 = prev1;
    prev1 = curr;
  }
  return prev1;
}
```

#### Java
```java
public class Fibonacci {
    public static long fibOptimized(int n) {
        if (n <= 1) {
            return n;
        }
        long prev2 = 0;
        long prev1 = 1;
        for (int i = 2; i <= n; i++) {
            long curr = prev1 + prev2;
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }
}
```

**Explanation:** Since `F(n)` only depends on `F(n-1)` and `F(n-2)`, we only need two variables instead of an entire array. At each step, compute the current value, then shift the two variables forward. This reduces space from O(n) to O(1) while maintaining O(n) time.

**When to use:** The optimal solution for computing a single Fibonacci number. Use in production or competitive programming when space efficiency matters. Note that if you need all Fibonacci numbers up to `n`, tabulation is better since it stores all results.

## Variations & Extensions
- **Matrix Exponentiation:** Compute `F(n)` in O(log n) time using matrix power of `[[1,1],[1,0]]`
- **Fibonacci in modular arithmetic:** Compute `F(n) % M` for large `n` (common in competitive programming)
- **Generalized Fibonacci (Tribonacci):** Each term is the sum of the three preceding terms
- **Climbing Stairs Problem:** Count ways to reach the top where you can climb 1 or 2 steps at a time (same recurrence as Fibonacci)

## Real-World Applications
- Fibonacci heaps in graph algorithms (Dijkstra, Prim)
- Financial modeling and trading algorithms using Fibonacci retracement levels
- Nature-inspired algorithms: phyllotaxis (leaf arrangement), spiral growth patterns
- Agile estimation using Fibonacci-based story points (1, 2, 3, 5, 8, 13…)

## Tags
#algorithm #dynamic-programming #recursion #memoization #fibonacci #medium
