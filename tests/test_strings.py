"""Tests for string algorithm snippets."""

import pytest


# ---------------------------------------------------------------------------
# Reverse String – Two Pointers (from snippets/algorithms/strings/reverse-string.md)
# ---------------------------------------------------------------------------
def reverse_string_two_pointers(s):
    chars = list(s)
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    return "".join(chars)


# ---------------------------------------------------------------------------
# Reverse String – Slice (from snippets/algorithms/strings/reverse-string.md)
# ---------------------------------------------------------------------------
def reverse_string_slice(s):
    return s[::-1]


# ---------------------------------------------------------------------------
# Palindrome – Two Pointers (from snippets/algorithms/strings/palindrome.md)
# ---------------------------------------------------------------------------
def is_palindrome_two_pointers(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


# ---------------------------------------------------------------------------
# Palindrome – Reverse Comparison (from snippets/algorithms/strings/palindrome.md)
# ---------------------------------------------------------------------------
def is_palindrome_reverse(s):
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]


# =========================== Reverse String ===============================


class TestReverseString:
    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("hello", "olleh"),
            ("a", "a"),
            ("", ""),
            ("racecar", "racecar"),
            ("ab", "ba"),
        ],
    )
    def test_two_pointers(self, input_str, expected):
        assert reverse_string_two_pointers(input_str) == expected

    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("hello", "olleh"),
            ("a", "a"),
            ("", ""),
            ("racecar", "racecar"),
            ("ab", "ba"),
        ],
    )
    def test_slice(self, input_str, expected):
        assert reverse_string_slice(input_str) == expected


# ============================= Palindrome =================================


class TestPalindrome:
    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("racecar", True),
            ("hello", False),
            ("A man, a plan, a canal: Panama", True),
            ("", True),
            ("a", True),
        ],
    )
    def test_two_pointers(self, input_str, expected):
        assert is_palindrome_two_pointers(input_str) == expected

    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("racecar", True),
            ("hello", False),
            ("A man, a plan, a canal: Panama", True),
            ("", True),
            ("a", True),
        ],
    )
    def test_reverse(self, input_str, expected):
        assert is_palindrome_reverse(input_str) == expected
