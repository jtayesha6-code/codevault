# Reverse a String

## Problem Statement
- Given a string (or array of characters), reverse it in-place.
- The function should modify the input directly without allocating extra space for another string.

**Example inputs/outputs:**
- Input: `["h", "e", "l", "l", "o"]` → Output: `["o", "l", "l", "e", "h"]`
- Input: `"hello"` → Output: `"olleh"`
- Input: `"a"` → Output: `"a"`

**Edge cases:**
- Empty string
- Single character
- String with spaces or special characters
- Palindrome string (remains unchanged)

## Solutions

### Solution 1: Two Pointers
- **Time Complexity:** O(n)
- **Space Complexity:** O(1)
- **Difficulty:** Easy

#### Python
```python
def reverse_string_two_pointers(s):
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    return s
```

#### JavaScript
```javascript
function reverseStringTwoPointers(s) {
  let left = 0;
  let right = s.length - 1;
  while (left < right) {
    [s[left], s[right]] = [s[right], s[left]];
    left++;
    right--;
  }
  return s;
}
```

#### Java
```java
public class ReverseString {
    public static void reverseStringTwoPointers(char[] s) {
        int left = 0;
        int right = s.length - 1;
        while (left < right) {
            char temp = s[left];
            s[left] = s[right];
            s[right] = temp;
            left++;
            right--;
        }
    }
}
```

**Explanation:** Place one pointer at the start and one at the end. Swap the characters at both pointers, then move them toward the center. Repeat until they meet.

**When to use:** Ideal when you need true in-place reversal with no extra memory. This is the canonical approach for character array reversal.

### Solution 2: Built-in / Slice
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)
- **Difficulty:** Easy

#### Python
```python
def reverse_string_slice(s):
    return s[::-1]
```

#### JavaScript
```javascript
function reverseStringBuiltin(s) {
  return s.split("").reverse().join("");
}
```

#### Java
```java
public class ReverseString {
    public static String reverseStringBuiltin(String s) {
        return new StringBuilder(s).reverse().toString();
    }
}
```

**Explanation:** Leverage language built-ins to reverse the string. Python uses slice notation `[::-1]`, JavaScript splits into an array, reverses, and joins, and Java uses `StringBuilder.reverse()`.

**When to use:** Best for production code when readability and brevity matter more than strict in-place constraints. Not suitable when the problem explicitly forbids extra space.

## Variations & Extensions
- **Reverse words in a string:** Reverse word order while keeping characters within each word intact
- **Reverse only vowels:** Swap only vowel characters in the string
- **Reverse in groups of k:** Reverse every k-character segment

## Real-World Applications
- Text processing and formatting tools
- Encoding/decoding algorithms (e.g., palindrome checks as a subroutine)
- UI rendering for right-to-left languages

## Tags
#algorithm #strings #two-pointers #easy
