# Contributing to CodeVault

Thank you for your interest in contributing! This guide explains how to add new snippets, maintain quality, and get your changes merged.

## How to Add New Snippets

1. **Pick a topic** — Choose an algorithm, data structure, or coding problem not yet covered in the `snippets/` directory.
2. **Use the template** — Copy `TEMPLATE.md` into the appropriate subdirectory under `snippets/` and rename it to match your topic (e.g., `snippets/sorting/merge_sort.md`).
3. **Fill in every section** — Problem statement, at least one solution with complexity analysis, explanations, and tags are all required.
4. **Add tests** — Write Python tests for your algorithm (see [Testing Requirements](#testing-requirements)).
5. **Open a PR** — Submit your changes following the [PR Process](#pr-process).

## Code Style Guidelines

### General
- Write clean, readable code with meaningful variable names.
- Keep solutions self-contained — each snippet should run independently.
- Only add comments where the logic is non-obvious; avoid redundant comments.

### Python
- Follow [PEP 8](https://peps.python.org/pep-0008/) conventions.
- Use type hints for function signatures.
- Use `snake_case` for functions and variables.

### JavaScript
- Use `const`/`let` (never `var`).
- Use camelCase for functions and variables.
- Prefer arrow functions for short callbacks.

### Java
- Follow standard Java naming conventions (camelCase for methods, PascalCase for classes).
- Include the class wrapper so the snippet compiles standalone.

### Markdown
- Use fenced code blocks with the language identifier (` ```python `, ` ```javascript `, ` ```java `).
- Keep line length reasonable (≤ 120 characters where practical).
- Use ATX-style headings (`#`, `##`, `###`).

## Testing Requirements

Every algorithm snippet must include corresponding Python tests.

- Place test files in the `tests/` directory, mirroring the `snippets/` structure (e.g., `tests/sorting/test_merge_sort.py`).
- Name test files with a `test_` prefix.
- Use Python's built-in `unittest` or `pytest` framework.
- Cover at minimum:
  - A basic / happy-path case
  - Edge cases (empty input, single element, duplicates, large input)
  - Expected time/space complexity class (where feasible)

Example:

```python
import pytest

def test_merge_sort_basic():
    assert merge_sort([3, 1, 2]) == [1, 2, 3]

def test_merge_sort_empty():
    assert merge_sort([]) == []

def test_merge_sort_single():
    assert merge_sort([1]) == [1]
```

Run all tests from the repository root:

```bash
pytest tests/
```

## PR Process

1. **Fork the repository** and create a feature branch from `main`.
2. **Make your changes** following the template and style guidelines.
3. **Run tests locally** — ensure all existing and new tests pass with `pytest tests/`.
4. **Commit with a clear message** — e.g., `Add merge sort snippet with Python/JS/Java solutions`.
5. **Open a pull request** against `main` with:
   - A descriptive title.
   - A summary of what the snippet covers.
   - Confirmation that tests pass.
6. **Address review feedback** promptly.

## Snippet Quality Checklist

Before submitting, verify your snippet meets these criteria:

- [ ] **Template followed** — All required sections from `TEMPLATE.md` are present.
- [ ] **Problem statement is clear** — Includes description, example inputs/outputs, and edge cases.
- [ ] **At least one complete solution** — With code in Python, JavaScript, and Java.
- [ ] **Complexity analysis** — Time and space complexity listed for every solution.
- [ ] **Difficulty rated** — Easy, Medium, or Hard.
- [ ] **Explanation provided** — Step-by-step walkthrough of the approach.
- [ ] **Real-world applications** — At least one practical use case described.
- [ ] **Tags added** — Relevant algorithm/category/difficulty tags at the bottom.
- [ ] **Tests written** — Python tests covering basic and edge cases exist in `tests/`.
- [ ] **Tests pass** — `pytest tests/` completes with no failures.
- [ ] **Code style** — Follows the style guidelines for each language.
- [ ] **No duplicates** — The topic is not already covered by an existing snippet.
