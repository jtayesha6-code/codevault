# String Manipulation Toolkit

## Overview
A comprehensive reference for common string operations across Python, JavaScript, and Java. Covers everyday tasks like slicing, searching, transforming, and pattern matching.

---

## 1. Substring / Slicing

#### Python
```python
s = "Hello, World!"

s[0:5]          # "Hello"
s[7:]           # "World!"
s[-6:]          # "orld!"
s[::-1]         # "!dlroW ,olleH"  (reverse)
s[::2]          # "Hlo ol!"        (every 2nd char)
```

#### JavaScript
```javascript
const s = "Hello, World!";

s.substring(0, 5);   // "Hello"
s.slice(7);           // "World!"
s.slice(-6);          // "orld!"
s.split("").reverse().join("");  // "!dlroW ,olleH"
```

#### Java
```java
String s = "Hello, World!";

s.substring(0, 5);   // "Hello"
s.substring(7);      // "World!"
new StringBuilder(s).reverse().toString();  // "!dlroW ,olleH"
```

---

## 2. Split & Join

#### Python
```python
# Split
"a,b,c".split(",")           # ["a", "b", "c"]
"hello world".split()         # ["hello", "world"]  (splits on whitespace)
"a::b::c".split("::", 1)      # ["a", "b::c"]       (max 1 split)

# Join
",".join(["a", "b", "c"])     # "a,b,c"
" ".join(["hello", "world"])  # "hello world"
```

#### JavaScript
```javascript
// Split
"a,b,c".split(",");           // ["a", "b", "c"]
"hello world".split(" ");     // ["hello", "world"]
"a::b::c".split("::", 2);     // ["a", "b"]  (limit = max items returned)

// Join
["a", "b", "c"].join(",");    // "a,b,c"
["hello", "world"].join(" "); // "hello world"
```

#### Java
```java
// Split
"a,b,c".split(",");            // ["a", "b", "c"]
"hello world".split("\\s+");   // ["hello", "world"]
"a::b::c".split("::", 2);      // ["a", "b::c"]  (limit = max parts)

// Join
String.join(",", "a", "b", "c");               // "a,b,c"
String.join(" ", List.of("hello", "world"));   // "hello world"
```

---

## 3. Search & Find

#### Python
```python
s = "hello world hello"

s.find("world")        # 6       (first index, -1 if not found)
s.rfind("hello")       # 12      (last occurrence)
s.index("world")       # 6       (raises ValueError if not found)
s.count("hello")       # 2
"world" in s           # True
s.startswith("hello")  # True
s.endswith("hello")    # True
```

#### JavaScript
```javascript
const s = "hello world hello";

s.indexOf("world");       // 6    (-1 if not found)
s.lastIndexOf("hello");   // 12
s.includes("world");      // true
s.startsWith("hello");    // true
s.endsWith("hello");      // true
s.split("hello").length - 1;  // 2 (count occurrences)
```

#### Java
```java
String s = "hello world hello";

s.indexOf("world");        // 6    (-1 if not found)
s.lastIndexOf("hello");    // 12
s.contains("world");       // true
s.startsWith("hello");     // true
s.endsWith("hello");       // true
```

---

## 4. Replace & Transform

#### Python
```python
s = "Hello, World!"

s.replace("World", "Python")   # "Hello, Python!"
s.lower()                      # "hello, world!"
s.upper()                      # "HELLO, WORLD!"
s.title()                      # "Hello, World!"
s.swapcase()                   # "hELLO, wORLD!"
s.strip()                      # remove leading/trailing whitespace
s.lstrip("H")                  # "ello, World!"
s.center(20, "-")              # "---Hello, World!----"
s.zfill(20)                    # "0000000Hello, World!"
```

#### JavaScript
```javascript
const s = "Hello, World!";

s.replace("World", "JavaScript");      // "Hello, JavaScript!"
s.replaceAll("l", "L");                // "HeLLo, WorLd!"
s.toLowerCase();                        // "hello, world!"
s.toUpperCase();                        // "HELLO, WORLD!"
s.trim();                               // remove whitespace
s.trimStart();                          // left trim
s.trimEnd();                            // right trim
s.padStart(20, "-");                    // "-------Hello, World!"
s.padEnd(20, "-");                      // "Hello, World!-------"
```

#### Java
```java
String s = "Hello, World!";

s.replace("World", "Java");       // "Hello, Java!"
s.replaceAll("[aeiou]", "*");     // "H*ll*, W*rld!"  (regex)
s.toLowerCase();                   // "hello, world!"
s.toUpperCase();                   // "HELLO, WORLD!"
s.trim();                          // remove whitespace
s.strip();                         // Unicode-aware trim (Java 11+)
```

---

## 5. Character Frequency Counting

#### Python
```python
from collections import Counter

s = "abracadabra"

# Using Counter
freq = Counter(s)
# Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

freq.most_common(2)    # [('a', 5), ('b', 2)]

# Manual approach
freq = {}
for ch in s:
    freq[ch] = freq.get(ch, 0) + 1
```

#### JavaScript
```javascript
const s = "abracadabra";

// Using reduce
const freq = [...s].reduce((acc, ch) => {
  acc[ch] = (acc[ch] || 0) + 1;
  return acc;
}, {});
// { a: 5, b: 2, r: 2, c: 1, d: 1 }

// Using Map
const freqMap = new Map();
for (const ch of s) {
  freqMap.set(ch, (freqMap.get(ch) || 0) + 1);
}

// Sort by frequency
const sorted = Object.entries(freq).sort((a, b) => b[1] - a[1]);
```

#### Java
```java
String s = "abracadabra";

// Using HashMap
Map<Character, Integer> freq = new HashMap<>();
for (char ch : s.toCharArray()) {
    freq.merge(ch, 1, Integer::sum);
}
// {a=5, b=2, r=2, c=1, d=1}

// Using int array (for lowercase letters only)
int[] count = new int[26];
for (char ch : s.toCharArray()) {
    count[ch - 'a']++;
}

// Sort by frequency
freq.entrySet().stream()
    .sorted(Map.Entry.<Character, Integer>comparingByValue().reversed())
    .forEach(e -> System.out.println(e.getKey() + ": " + e.getValue()));
```

---

## 6. String Comparison

#### Python
```python
# Equality
"abc" == "abc"       # True
"abc" != "def"       # True

# Lexicographic
"apple" < "banana"   # True
"abc" > "abb"        # True

# Case-insensitive
"Hello".lower() == "hello".lower()  # True
```

#### JavaScript
```javascript
// Equality
"abc" === "abc";                  // true

// Lexicographic
"apple".localeCompare("banana");  // -1 (a < b)
"apple" < "banana";              // true

// Case-insensitive
"Hello".toLowerCase() === "hello".toLowerCase();  // true
```

#### Java
```java
// Equality — always use .equals(), never ==
"abc".equals("abc");                  // true

// Lexicographic
"apple".compareTo("banana");          // negative (a < b)

// Case-insensitive
"Hello".equalsIgnoreCase("hello");    // true
"Hello".compareToIgnoreCase("hello"); // 0
```

---

## 7. Regex Basics

#### Python
```python
import re

text = "Contact: alice@example.com or bob@test.org"

# Search
match = re.search(r"\b\w+@\w+\.\w+\b", text)
if match:
    print(match.group())           # "alice@example.com"

# Find all
emails = re.findall(r"\b\w+@\w+\.\w+\b", text)
# ["alice@example.com", "bob@test.org"]

# Replace
cleaned = re.sub(r"\b\w+@\w+\.\w+\b", "[REDACTED]", text)
# "Contact: [REDACTED] or [REDACTED]"

# Split
parts = re.split(r"[,;\s]+", "a, b; c d")
# ["a", "b", "c", "d"]

# Validate pattern
is_email = bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", "user@example.com"))
```

#### JavaScript
```javascript
const text = "Contact: alice@example.com or bob@test.org";

// Search
const match = text.match(/\b\w+@\w+\.\w+\b/);
// match[0] = "alice@example.com"

// Find all
const emails = text.match(/\b\w+@\w+\.\w+\b/g);
// ["alice@example.com", "bob@test.org"]

// Replace
const cleaned = text.replace(/\b\w+@\w+\.\w+\b/g, "[REDACTED]");

// Split
"a, b; c d".split(/[,;\s]+/);
// ["a", "b", "c", "d"]

// Test
/^[^@]+@[^@]+\.[^@]+$/.test("user@example.com");  // true
```

#### Java
```java
import java.util.regex.*;

String text = "Contact: alice@example.com or bob@test.org";

// Search
Matcher m = Pattern.compile("\\b\\w+@\\w+\\.\\w+\\b").matcher(text);
if (m.find()) {
    System.out.println(m.group());  // "alice@example.com"
}

// Find all
while (m.find()) {
    System.out.println(m.group());
}

// Replace
String cleaned = text.replaceAll("\\b\\w+@\\w+\\.\\w+\\b", "[REDACTED]");

// Split
String[] parts = "a, b; c d".split("[,;\\s]+");
// ["a", "b", "c", "d"]

// Validate
boolean valid = "user@example.com".matches("[^@]+@[^@]+\\.[^@]+");
```

---

## 8. Type Conversion

#### Python
```python
# Char ↔ ASCII
ord("A")           # 65
chr(65)            # "A"

# String ↔ Number
str(42)            # "42"
int("42")          # 42
float("3.14")      # 3.14

# String ↔ List of chars
list("hello")      # ['h', 'e', 'l', 'l', 'o']
"".join(['h', 'e', 'l', 'l', 'o'])  # "hello"
```

#### JavaScript
```javascript
// Char ↔ Code
"A".charCodeAt(0);            // 65
String.fromCharCode(65);      // "A"

// String ↔ Number
String(42);                   // "42"
Number("42");                 // 42
parseInt("42", 10);           // 42
parseFloat("3.14");           // 3.14

// String ↔ Array of chars
[..."hello"];                 // ['h', 'e', 'l', 'l', 'o']
['h', 'e', 'l', 'l', 'o'].join("");  // "hello"
```

#### Java
```java
// Char ↔ ASCII
(int) 'A';                           // 65
(char) 65;                           // 'A'

// String ↔ Number
String.valueOf(42);                  // "42"
Integer.parseInt("42");              // 42
Double.parseDouble("3.14");          // 3.14

// String ↔ char array
"hello".toCharArray();               // ['h', 'e', 'l', 'l', 'o']
new String(new char[]{'h', 'e', 'l', 'l', 'o'});  // "hello"
```

---

## Real-World Applications
- Input parsing and data cleaning in ETL pipelines
- Log file analysis and pattern extraction
- User input validation and sanitization
- Search engine tokenization and indexing

## Tags
#strings #reference #toolkit #regex #python #javascript #java
