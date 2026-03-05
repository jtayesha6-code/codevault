# N-Queens Problem

## Problem Statement
- Place N queens on an N×N chessboard so that no two queens threaten each other
- No two queens may share the same row, column, or diagonal
- Return all distinct solutions

**Example:**
```
Input: n = 4
Output: [
  [".Q..",    ["..Q.",
   "...Q",    "Q...",
   "Q...",    "...Q",
   "..Q."],   ".Q.."]
]
```

**Edge Cases:**
- n = 1 → single queen on a 1×1 board
- n = 2 or n = 3 → no valid solutions exist

## Solutions

### Solution 1: Backtracking
- **Time Complexity:** O(N!)
- **Space Complexity:** O(N²)
- **Difficulty:** Hard

#### Python
```python
def solve_n_queens(n):
    """
    Solve the N-Queens problem using backtracking.
    Returns all valid board configurations.
    """
    results = []
    board = [["." for _ in range(n)] for _ in range(n)]

    # Track which columns and diagonals are under attack
    cols = set()
    diag1 = set()  # row - col (top-left to bottom-right)
    diag2 = set()  # row + col (top-right to bottom-left)

    def backtrack(row):
        if row == n:
            results.append(["".join(r) for r in board])
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            board[row][col] = "Q"
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            backtrack(row + 1)

            board[row][col] = "."
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return results


def print_board(solution):
    """Visualize a single board configuration."""
    n = len(solution)
    print("+" + "---+" * n)
    for row in solution:
        print("|", end="")
        for ch in row:
            print(f" {ch} |", end="")
        print()
        print("+" + "---+" * n)


# Example
solutions = solve_n_queens(4)
print(f"Found {len(solutions)} solutions for 4-Queens:\n")
for i, sol in enumerate(solutions):
    print(f"Solution {i + 1}:")
    print_board(sol)
    print()
```

#### JavaScript
```javascript
function solveNQueens(n) {
  const results = [];
  const board = Array.from({ length: n }, () => Array(n).fill("."));
  const cols = new Set();
  const diag1 = new Set(); // row - col
  const diag2 = new Set(); // row + col

  function backtrack(row) {
    if (row === n) {
      results.push(board.map((r) => r.join("")));
      return;
    }

    for (let col = 0; col < n; col++) {
      if (cols.has(col) || diag1.has(row - col) || diag2.has(row + col)) {
        continue;
      }

      board[row][col] = "Q";
      cols.add(col);
      diag1.add(row - col);
      diag2.add(row + col);

      backtrack(row + 1);

      board[row][col] = ".";
      cols.delete(col);
      diag1.delete(row - col);
      diag2.delete(row + col);
    }
  }

  backtrack(0);
  return results;
}

function printBoard(solution) {
  const n = solution.length;
  const border = "+" + "---+".repeat(n);
  for (const row of solution) {
    console.log(border);
    console.log("|" + [...row].map((ch) => ` ${ch} |`).join(""));
  }
  console.log(border);
}

// Example
const solutions = solveNQueens(4);
console.log(`Found ${solutions.length} solutions for 4-Queens:\n`);
solutions.forEach((sol, i) => {
  console.log(`Solution ${i + 1}:`);
  printBoard(sol);
  console.log();
});
```

#### Java
```java
import java.util.*;

public class NQueens {

    public List<List<String>> solveNQueens(int n) {
        List<List<String>> results = new ArrayList<>();
        char[][] board = new char[n][n];
        for (char[] row : board) Arrays.fill(row, '.');

        Set<Integer> cols = new HashSet<>();
        Set<Integer> diag1 = new HashSet<>(); // row - col
        Set<Integer> diag2 = new HashSet<>(); // row + col

        backtrack(0, n, board, cols, diag1, diag2, results);
        return results;
    }

    private void backtrack(int row, int n, char[][] board,
                           Set<Integer> cols, Set<Integer> diag1,
                           Set<Integer> diag2, List<List<String>> results) {
        if (row == n) {
            List<String> snapshot = new ArrayList<>();
            for (char[] r : board) snapshot.add(new String(r));
            results.add(snapshot);
            return;
        }

        for (int col = 0; col < n; col++) {
            if (cols.contains(col) || diag1.contains(row - col)
                    || diag2.contains(row + col)) {
                continue;
            }

            board[row][col] = 'Q';
            cols.add(col);
            diag1.add(row - col);
            diag2.add(row + col);

            backtrack(row + 1, n, board, cols, diag1, diag2, results);

            board[row][col] = '.';
            cols.remove(col);
            diag1.remove(row - col);
            diag2.remove(row + col);
        }
    }

    public static void printBoard(List<String> solution) {
        int n = solution.size();
        String border = "+" + "---+".repeat(n);
        for (String row : solution) {
            System.out.println(border);
            StringBuilder sb = new StringBuilder("|");
            for (char ch : row.toCharArray()) {
                sb.append(" ").append(ch).append(" |");
            }
            System.out.println(sb);
        }
        System.out.println(border);
    }

    public static void main(String[] args) {
        NQueens solver = new NQueens();
        List<List<String>> solutions = solver.solveNQueens(4);
        System.out.printf("Found %d solutions for 4-Queens:%n%n", solutions.size());
        for (int i = 0; i < solutions.size(); i++) {
            System.out.printf("Solution %d:%n", i + 1);
            printBoard(solutions.get(i));
            System.out.println();
        }
    }
}
```

**Explanation:**
1. Place queens row by row from top to bottom
2. For each row, try every column position
3. Check if placing a queen is safe using three sets: columns, main diagonals (row − col), and anti-diagonals (row + col)
4. If safe, place the queen and recurse to the next row
5. If the recursion fails to find a valid placement, backtrack by removing the queen and restoring the sets
6. When all N rows are filled, record the board as a valid solution

**Board Visualization (n=4, Solution 1):**
```
+---+---+---+---+
| . | Q | . | . |
+---+---+---+---+
| . | . | . | Q |
+---+---+---+---+
| Q | . | . | . |
+---+---+---+---+
| . | . | Q | . |
+---+---+---+---+
```

**When to use:** Problems requiring exhaustive search with constraint satisfaction, combinatorial puzzles, and scheduling problems with mutual exclusion constraints.

## Variations & Extensions
- **N-Queens II:** Return only the count of distinct solutions
- **N-Queens with obstacles:** Some cells are blocked and cannot hold a queen
- **N-Rooks:** Place N rooks so none attack each other (simpler — only row/column constraints)
- **Iterative approach:** Use an explicit stack instead of recursion

## Real-World Applications
- Constraint satisfaction problems in AI (CSP solvers)
- VLSI circuit design for non-attacking component placement
- Parallel memory storage schemes
- Task scheduling where resources conflict

## Tags
#backtracking #recursion #hard #constraint-satisfaction #combinatorics
