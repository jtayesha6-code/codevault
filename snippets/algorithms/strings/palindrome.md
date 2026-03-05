# Check Palindrome

## Problem Statement
- Given a string, determine if it is a palindrome (reads the same forwards and backwards).
- Consider only alphanumeric characters and ignore case for the classic variant.

**Example inputs/outputs:**
- Input: `"racecar"` → Output: `true`
- Input: `"A man, a plan, a canal: Panama"` → Output: `true`
- Input: `"hello"` → Output: `false`

**Edge cases:**
- Empty string (considered a palindrome)
- Single character (always a palindrome)
- String with only non-alphanumeric characters
- Mixed case input

## Solutions

### Solution 1: Two Pointers
- **Time Complexity:** O(n)
- **Space Complexity:** O(1)
- **Difficulty:** Easy

#### Python
```python
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
```

#### JavaScript
```javascript
function isPalindromeTwoPointers(s) {
  let left = 0;
  let right = s.length - 1;
  while (left < right) {
    while (left < right && !isAlphanumeric(s[left])) left++;
    while (left < right && !isAlphanumeric(s[right])) right--;
    if (s[left].toLowerCase() !== s[right].toLowerCase()) {
      return false;
    }
    left++;
    right--;
  }
  return true;
}

function isAlphanumeric(ch) {
  return /^[a-z0-9]$/i.test(ch);
}
```

#### Java
```java
public class Palindrome {
    public static boolean isPalindromeTwoPointers(String s) {
        int left = 0;
        int right = s.length() - 1;
        while (left < right) {
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) {
                left++;
            }
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) {
                right--;
            }
            if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
}
```

**Explanation:** Use two pointers starting from both ends of the string. Skip non-alphanumeric characters, compare characters (case-insensitive), and move inward. If all compared pairs match, the string is a palindrome.

**When to use:** Preferred when you need O(1) space and the input may contain non-alphanumeric characters that should be ignored.

### Solution 2: Reverse Comparison
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)
- **Difficulty:** Easy

#### Python
```python
def is_palindrome_reverse(s):
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]
```

#### JavaScript
```javascript
function isPalindromeReverse(s) {
  const cleaned = s.replace(/[^a-z0-9]/gi, "").toLowerCase();
  const reversed = cleaned.split("").reverse().join("");
  return cleaned === reversed;
}
```

#### Java
```java
public class Palindrome {
    public static boolean isPalindromeReverse(String s) {
        String cleaned = s.replaceAll("[^a-zA-Z0-9]", "").toLowerCase();
        String reversed = new StringBuilder(cleaned).reverse().toString();
        return cleaned.equals(reversed);
    }
}
```

**Explanation:** First, strip all non-alphanumeric characters and convert to lowercase. Then, reverse the cleaned string and compare it to the original cleaned string. If they are equal, the input is a palindrome.

**When to use:** Great for readability and quick implementation. Ideal in scripting or when clarity is more important than memory optimization.

## Variations & Extensions
- **Palindrome number:** Check if an integer is a palindrome without converting to string
- **Longest palindromic substring:** Find the longest substring that is a palindrome
- **Valid palindrome II:** Check if a string can become a palindrome by removing at most one character

## Real-World Applications
- DNA sequence analysis (detecting palindromic sequences in genetics)
- Data validation and input sanitization
- Natural language processing for wordplay detection

## Tags
#algorithm #strings #two-pointers #easy
