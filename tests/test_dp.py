"""Tests for dynamic programming snippets."""

import pytest


# ---------------------------------------------------------------------------
# Fibonacci – Naive Recursion (from snippets/problem-solving/dynamic-programming/fibonacci.md)
# ---------------------------------------------------------------------------
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


# ---------------------------------------------------------------------------
# Fibonacci – Memoization (Top-Down DP)
# ---------------------------------------------------------------------------
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


# ---------------------------------------------------------------------------
# Fibonacci – Tabulation (Bottom-Up DP)
# ---------------------------------------------------------------------------
def fib_tabulation(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


# ---------------------------------------------------------------------------
# Fibonacci – Space-Optimized
# ---------------------------------------------------------------------------
def fib_optimized(n):
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1


# ============================== Fibonacci =================================

FIBONACCI_CASES = [
    (0, 0),
    (1, 1),
    (2, 1),
    (6, 8),
    (10, 55),
]


class TestFibonacciNaive:
    @pytest.mark.parametrize("n, expected", FIBONACCI_CASES)
    def test_values(self, n, expected):
        assert fib_naive(n) == expected


class TestFibonacciMemo:
    @pytest.mark.parametrize("n, expected", FIBONACCI_CASES)
    def test_values(self, n, expected):
        assert fib_memo(n) == expected


class TestFibonacciTabulation:
    @pytest.mark.parametrize("n, expected", FIBONACCI_CASES)
    def test_values(self, n, expected):
        assert fib_tabulation(n) == expected


class TestFibonacciOptimized:
    @pytest.mark.parametrize("n, expected", FIBONACCI_CASES)
    def test_values(self, n, expected):
        assert fib_optimized(n) == expected
