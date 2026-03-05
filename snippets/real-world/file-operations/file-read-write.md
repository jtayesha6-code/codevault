# File Read/Write Operations

## Problem Statement
- Read and write text files, JSON files, and CSV files in Python, JavaScript, and Java
- Handle errors gracefully (missing files, permission denied, malformed data)
- Edge cases: empty files, large files, encoding issues, concurrent access

## Solutions

### Solution 1: Text File Read/Write
- **Time Complexity:** O(n) where n is the file size
- **Space Complexity:** O(n)
- **Difficulty:** Easy

#### Python
```python
from pathlib import Path


def read_text_file(filepath: str) -> str:
    """Read an entire text file and return its contents."""
    try:
        return Path(filepath).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {filepath}")


def write_text_file(filepath: str, content: str, append: bool = False) -> None:
    """Write or append text to a file, creating parent directories if needed."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    with open(path, mode, encoding="utf-8") as f:
        f.write(content)


def read_lines(filepath: str) -> list[str]:
    """Read a file and return a list of stripped lines."""
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f]


# --- Usage ---
if __name__ == "__main__":
    write_text_file("output/example.txt", "Hello, World!\n")
    write_text_file("output/example.txt", "Second line\n", append=True)
    content = read_text_file("output/example.txt")
    print(content)
    lines = read_lines("output/example.txt")
    print(lines)
```

#### JavaScript
```javascript
const fs = require("fs");
const path = require("path");

/**
 * Read an entire text file and return its contents.
 */
function readTextFile(filepath) {
  try {
    return fs.readFileSync(filepath, "utf-8");
  } catch (err) {
    if (err.code === "ENOENT") throw new Error(`File not found: ${filepath}`);
    if (err.code === "EACCES") throw new Error(`Permission denied: ${filepath}`);
    throw err;
  }
}

/**
 * Write or append text to a file, creating parent directories if needed.
 */
function writeTextFile(filepath, content, append = false) {
  const dir = path.dirname(filepath);
  fs.mkdirSync(dir, { recursive: true });
  if (append) {
    fs.appendFileSync(filepath, content, "utf-8");
  } else {
    fs.writeFileSync(filepath, content, "utf-8");
  }
}

/**
 * Read a file and return an array of trimmed lines.
 */
function readLines(filepath) {
  const content = readTextFile(filepath);
  return content.split("\n").filter((line) => line.length > 0);
}

// --- Async versions ---

async function readTextFileAsync(filepath) {
  const fsPromises = require("fs").promises;
  try {
    return await fsPromises.readFile(filepath, "utf-8");
  } catch (err) {
    if (err.code === "ENOENT") throw new Error(`File not found: ${filepath}`);
    if (err.code === "EACCES") throw new Error(`Permission denied: ${filepath}`);
    throw err;
  }
}

async function writeTextFileAsync(filepath, content) {
  const fsPromises = require("fs").promises;
  const dir = path.dirname(filepath);
  await fsPromises.mkdir(dir, { recursive: true });
  await fsPromises.writeFile(filepath, content, "utf-8");
}

// --- Usage ---
writeTextFile("output/example.txt", "Hello, World!\n");
writeTextFile("output/example.txt", "Second line\n", true);
console.log(readTextFile("output/example.txt"));
console.log(readLines("output/example.txt"));

module.exports = {
  readTextFile,
  writeTextFile,
  readLines,
  readTextFileAsync,
  writeTextFileAsync,
};
```

#### Java
```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;

public class TextFileOperations {

    /** Read an entire text file and return its contents. */
    public static String readTextFile(String filepath) throws IOException {
        try {
            return Files.readString(Path.of(filepath), StandardCharsets.UTF_8);
        } catch (NoSuchFileException e) {
            throw new IOException("File not found: " + filepath, e);
        } catch (AccessDeniedException e) {
            throw new IOException("Permission denied: " + filepath, e);
        }
    }

    /** Write text to a file, creating parent directories if needed. */
    public static void writeTextFile(String filepath, String content, boolean append)
            throws IOException {
        Path path = Path.of(filepath);
        if (path.getParent() != null) {
            Files.createDirectories(path.getParent());
        }
        if (append) {
            Files.writeString(path, content, StandardCharsets.UTF_8,
                    StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        } else {
            Files.writeString(path, content, StandardCharsets.UTF_8);
        }
    }

    /** Read a file and return a list of lines. */
    public static List<String> readLines(String filepath) throws IOException {
        return Files.readAllLines(Path.of(filepath), StandardCharsets.UTF_8);
    }

    public static void main(String[] args) throws IOException {
        writeTextFile("output/example.txt", "Hello, World!\n", false);
        writeTextFile("output/example.txt", "Second line\n", true);
        System.out.println(readTextFile("output/example.txt"));
        System.out.println(readLines("output/example.txt"));
    }
}
```

**Explanation:**
1. **Encoding** — Always specify UTF-8 explicitly to avoid platform-dependent encoding issues.
2. **Directory creation** — Automatically create parent directories before writing so callers don't need to worry about path existence.
3. **Error handling** — Catch and re-throw specific exceptions (file not found, permission denied) with clear messages.

**When to use:** Configuration files, log processing, report generation, data import/export scripts.

### Solution 2: JSON File Operations
- **Time Complexity:** O(n) for parsing/serializing
- **Space Complexity:** O(n)
- **Difficulty:** Easy

#### Python
```python
import json
from pathlib import Path


def read_json(filepath: str) -> dict | list:
    """Read and parse a JSON file."""
    try:
        text = Path(filepath).read_text(encoding="utf-8")
        return json.loads(text)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {filepath}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {filepath}: {e}")


def write_json(filepath: str, data: dict | list, pretty: bool = True) -> None:
    """Write data to a JSON file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2 if pretty else None, ensure_ascii=False)
        f.write("\n")


def update_json(filepath: str, updates: dict) -> dict:
    """Read a JSON object, merge updates, and write it back."""
    data = read_json(filepath)
    if not isinstance(data, dict):
        raise TypeError("Can only update JSON objects, not arrays")
    data.update(updates)
    write_json(filepath, data)
    return data


# --- Usage ---
if __name__ == "__main__":
    config = {"host": "localhost", "port": 8080, "debug": True}
    write_json("output/config.json", config)

    loaded = read_json("output/config.json")
    print("Loaded:", loaded)

    updated = update_json("output/config.json", {"port": 9090})
    print("Updated:", updated)
```

#### JavaScript
```javascript
const fs = require("fs");
const path = require("path");

/**
 * Read and parse a JSON file.
 */
function readJson(filepath) {
  try {
    const text = fs.readFileSync(filepath, "utf-8");
    return JSON.parse(text);
  } catch (err) {
    if (err.code === "ENOENT") throw new Error(`JSON file not found: ${filepath}`);
    if (err instanceof SyntaxError)
      throw new Error(`Invalid JSON in ${filepath}: ${err.message}`);
    throw err;
  }
}

/**
 * Write data to a JSON file.
 */
function writeJson(filepath, data, pretty = true) {
  const dir = path.dirname(filepath);
  fs.mkdirSync(dir, { recursive: true });
  const content = JSON.stringify(data, null, pretty ? 2 : undefined) + "\n";
  fs.writeFileSync(filepath, content, "utf-8");
}

/**
 * Read a JSON object, merge updates, and write it back.
 */
function updateJson(filepath, updates) {
  const data = readJson(filepath);
  if (typeof data !== "object" || Array.isArray(data)) {
    throw new Error("Can only update JSON objects, not arrays");
  }
  const updated = { ...data, ...updates };
  writeJson(filepath, updated);
  return updated;
}

// --- Usage ---
const config = { host: "localhost", port: 8080, debug: true };
writeJson("output/config.json", config);
console.log("Loaded:", readJson("output/config.json"));
console.log("Updated:", updateJson("output/config.json", { port: 9090 }));

module.exports = { readJson, writeJson, updateJson };
```

#### Java
```java
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonSyntaxException;
import com.google.gson.reflect.TypeToken;

import java.io.IOException;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Map;

public class JsonFileOperations {

    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();

    /** Read and parse a JSON file into a Map. */
    public static Map<String, Object> readJson(String filepath) throws IOException {
        try {
            String text = Files.readString(Path.of(filepath), StandardCharsets.UTF_8);
            Type type = new TypeToken<Map<String, Object>>() {}.getType();
            Map<String, Object> result = GSON.fromJson(text, type);
            if (result == null) throw new IOException("Empty JSON file: " + filepath);
            return result;
        } catch (NoSuchFileException e) {
            throw new IOException("JSON file not found: " + filepath, e);
        } catch (JsonSyntaxException e) {
            throw new IOException("Invalid JSON in " + filepath + ": " + e.getMessage(), e);
        }
    }

    /** Write a Map to a JSON file. */
    public static void writeJson(String filepath, Map<String, Object> data) throws IOException {
        Path path = Path.of(filepath);
        if (path.getParent() != null) {
            Files.createDirectories(path.getParent());
        }
        String json = GSON.toJson(data) + "\n";
        Files.writeString(path, json, StandardCharsets.UTF_8);
    }

    /** Read a JSON file as a typed object. */
    public static <T> T readJsonAs(String filepath, Class<T> clazz) throws IOException {
        String text = Files.readString(Path.of(filepath), StandardCharsets.UTF_8);
        return GSON.fromJson(text, clazz);
    }

    /** Write any object to a JSON file. */
    public static void writeJsonObject(String filepath, Object data) throws IOException {
        Path path = Path.of(filepath);
        if (path.getParent() != null) {
            Files.createDirectories(path.getParent());
        }
        String json = GSON.toJson(data) + "\n";
        Files.writeString(path, json, StandardCharsets.UTF_8);
    }

    public static void main(String[] args) throws IOException {
        Map<String, Object> config = Map.of("host", "localhost", "port", 8080, "debug", true);
        writeJson("output/config.json", config);

        Map<String, Object> loaded = readJson("output/config.json");
        System.out.println("Loaded: " + loaded);
    }
}
```

**Explanation:**
1. **Parse errors** — Distinguish between "file not found" and "malformed JSON" to give callers actionable error messages.
2. **Pretty printing** — Default to indented output for human readability; allow compact mode for storage/network efficiency.
3. **Update pattern** — Read → merge → write-back is a common pattern for configuration files and settings.

**When to use:** Application configuration, API response caching, data serialization between services.

### Solution 3: CSV File Operations
- **Time Complexity:** O(n) where n is the number of rows
- **Space Complexity:** O(n)
- **Difficulty:** Easy

#### Python
```python
import csv
from pathlib import Path


def read_csv(filepath: str) -> list[dict]:
    """Read a CSV file and return a list of dictionaries (one per row)."""
    try:
        with open(filepath, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {filepath}")


def write_csv(filepath: str, data: list[dict], fieldnames: list[str] = None) -> None:
    """Write a list of dictionaries to a CSV file."""
    if not data:
        return
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(data[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def filter_csv(filepath: str, predicate) -> list[dict]:
    """Read a CSV and return only rows matching the predicate."""
    rows = read_csv(filepath)
    return [row for row in rows if predicate(row)]


# --- Usage ---
if __name__ == "__main__":
    employees = [
        {"name": "Alice", "department": "Engineering", "salary": "95000"},
        {"name": "Bob", "department": "Marketing", "salary": "72000"},
        {"name": "Carol", "department": "Engineering", "salary": "105000"},
    ]
    write_csv("output/employees.csv", employees)

    loaded = read_csv("output/employees.csv")
    print("All employees:", loaded)

    engineers = filter_csv(
        "output/employees.csv",
        lambda row: row["department"] == "Engineering",
    )
    print("Engineers:", engineers)
```

#### JavaScript
```javascript
const fs = require("fs");
const path = require("path");

/**
 * Parse CSV text into an array of objects using the header row as keys.
 */
function parseCsv(text) {
  const lines = text.trim().split("\n");
  if (lines.length === 0) return [];
  const headers = lines[0].split(",").map((h) => h.trim());
  return lines.slice(1).map((line) => {
    const values = line.split(",").map((v) => v.trim());
    const row = {};
    headers.forEach((header, i) => {
      row[header] = values[i] || "";
    });
    return row;
  });
}

/**
 * Read a CSV file and return an array of objects.
 */
function readCsv(filepath) {
  try {
    const text = fs.readFileSync(filepath, "utf-8");
    return parseCsv(text);
  } catch (err) {
    if (err.code === "ENOENT") throw new Error(`CSV file not found: ${filepath}`);
    throw err;
  }
}

/**
 * Write an array of objects to a CSV file.
 */
function writeCsv(filepath, data) {
  if (!data || data.length === 0) return;
  const dir = path.dirname(filepath);
  fs.mkdirSync(dir, { recursive: true });

  const headers = Object.keys(data[0]);
  const lines = [headers.join(",")];
  for (const row of data) {
    lines.push(headers.map((h) => String(row[h] ?? "")).join(","));
  }
  fs.writeFileSync(filepath, lines.join("\n") + "\n", "utf-8");
}

/**
 * Read a CSV and return only rows matching the predicate.
 */
function filterCsv(filepath, predicate) {
  return readCsv(filepath).filter(predicate);
}

// --- Usage ---
const employees = [
  { name: "Alice", department: "Engineering", salary: "95000" },
  { name: "Bob", department: "Marketing", salary: "72000" },
  { name: "Carol", department: "Engineering", salary: "105000" },
];
writeCsv("output/employees.csv", employees);
console.log("All:", readCsv("output/employees.csv"));
console.log(
  "Engineers:",
  filterCsv("output/employees.csv", (r) => r.department === "Engineering")
);

module.exports = { readCsv, writeCsv, parseCsv, filterCsv };
```

#### Java
```java
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class CsvFileOperations {

    /** Read a CSV file and return a list of maps (header -> value). */
    public static List<Map<String, String>> readCsv(String filepath) throws IOException {
        List<Map<String, String>> rows = new ArrayList<>();
        try (BufferedReader reader = Files.newBufferedReader(
                Path.of(filepath), StandardCharsets.UTF_8)) {
            String headerLine = reader.readLine();
            if (headerLine == null) return rows;
            String[] headers = headerLine.split(",", -1);
            for (int i = 0; i < headers.length; i++) headers[i] = headers[i].trim();

            String line;
            while ((line = reader.readLine()) != null) {
                String[] values = line.split(",", -1);
                Map<String, String> row = new LinkedHashMap<>();
                for (int i = 0; i < headers.length; i++) {
                    row.put(headers[i], i < values.length ? values[i].trim() : "");
                }
                rows.add(row);
            }
        }
        return rows;
    }

    /** Write a list of maps to a CSV file. */
    public static void writeCsv(String filepath, List<Map<String, String>> data)
            throws IOException {
        if (data == null || data.isEmpty()) return;
        Path path = Path.of(filepath);
        if (path.getParent() != null) {
            Files.createDirectories(path.getParent());
        }

        List<String> headers = new ArrayList<>(data.get(0).keySet());
        try (BufferedWriter writer = Files.newBufferedWriter(
                path, StandardCharsets.UTF_8)) {
            writer.write(String.join(",", headers));
            writer.newLine();
            for (Map<String, String> row : data) {
                List<String> values = new ArrayList<>();
                for (String header : headers) {
                    values.add(row.getOrDefault(header, ""));
                }
                writer.write(String.join(",", values));
                writer.newLine();
            }
        }
    }

    public static void main(String[] args) throws IOException {
        List<Map<String, String>> employees = List.of(
                new LinkedHashMap<>(Map.of("name", "Alice", "department", "Engineering", "salary", "95000")),
                new LinkedHashMap<>(Map.of("name", "Bob", "department", "Marketing", "salary", "72000")),
                new LinkedHashMap<>(Map.of("name", "Carol", "department", "Engineering", "salary", "105000"))
        );
        writeCsv("output/employees.csv", employees);

        List<Map<String, String>> loaded = readCsv("output/employees.csv");
        System.out.println("All employees: " + loaded);

        loaded.stream()
                .filter(row -> "Engineering".equals(row.get("department")))
                .forEach(row -> System.out.println("Engineer: " + row));
    }
}
```

**Explanation:**
1. **Header-based access** — Use the first row as column headers so data is accessed by name, not index, making code self-documenting.
2. **DictReader/DictWriter (Python)** — The standard library handles quoting, escaping, and newline normalization automatically.
3. **Simple parser (JS/Java)** — A basic comma-split parser works for clean data; for production use with embedded commas or quotes, use a library like `csv-parse` (Node.js) or Apache Commons CSV (Java).

**When to use:** Data import/export, report generation, ETL pipelines, spreadsheet processing.

## Variations & Extensions
- Stream large files line-by-line instead of loading entirely into memory
- Handle different encodings (Latin-1, UTF-16) with explicit codec parameters
- Implement file locking for concurrent access in multi-process environments
- Add YAML and TOML file support for configuration management

## Real-World Applications
- Reading application configuration files on startup
- Exporting database query results to CSV for business users
- Processing log files for analysis and monitoring
- Caching API responses as JSON files to reduce network calls

## Tags
#file-io #text #json #csv #error-handling #easy
