# Sudoku Solver

## Problem Statement
- Solve a 9×9 Sudoku puzzle by filling empty cells (represented as `'.'` or `0`)
- Each row must contain digits 1–9 with no repetition
- Each column must contain digits 1–9 with no repetition
- Each of the nine 3×3 sub-boxes must contain digits 1–9 with no repetition
- The input board is guaranteed to have a single valid solution

**Example:**
```
Input:                    Output:
5 3 . | . 7 . | . . .    5 3 4 | 6 7 8 | 9 1 2
6 . . | 1 9 5 | . . .    6 7 2 | 1 9 5 | 3 4 8
. 9 8 | . . . | . 6 .    1 9 8 | 3 4 2 | 5 6 7
------+-------+------    ------+-------+------
8 . . | . 6 . | . . 3    8 5 9 | 7 6 1 | 4 2 3
4 . . | 8 . 3 | . . 1    4 2 6 | 8 5 3 | 7 9 1
7 . . | . 2 . | . . 6    7 1 3 | 9 2 4 | 8 5 6
------+-------+------    ------+-------+------
. 6 . | . . . | 2 8 .    9 6 1 | 5 3 7 | 2 8 4
. . . | 4 1 9 | . . 5    2 8 7 | 4 1 9 | 6 3 5
. . . | . 8 . | . 7 9    3 4 5 | 2 8 6 | 1 7 9
```

**Edge Cases:**
- Board is already complete → return as-is
- Board with many empty cells → still solvable but slower

## Solutions

### Solution 1: Backtracking with Constraint Sets
- **Time Complexity:** O(9^(n*n)) worst case, much faster in practice due to pruning
- **Space Complexity:** O(n*n) for the board and constraint sets
- **Difficulty:** Hard

#### Python
```python
def solve_sudoku(board):
    """
    Solve Sudoku in-place using backtracking with constraint sets.
    board: list of 9 lists, each containing 9 characters ('1'-'9' or '.').
    """
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []

    # Initialize constraint sets from pre-filled cells
    for r in range(9):
        for c in range(9):
            if board[r][c] != ".":
                num = board[r][c]
                rows[r].add(num)
                cols[c].add(num)
                boxes[(r // 3) * 3 + c // 3].add(num)
            else:
                empty.append((r, c))

    def backtrack(idx):
        if idx == len(empty):
            return True

        r, c = empty[idx]
        box_id = (r // 3) * 3 + c // 3

        for num in "123456789":
            if num in rows[r] or num in cols[c] or num in boxes[box_id]:
                continue

            board[r][c] = num
            rows[r].add(num)
            cols[c].add(num)
            boxes[box_id].add(num)

            if backtrack(idx + 1):
                return True

            board[r][c] = "."
            rows[r].remove(num)
            cols[c].remove(num)
            boxes[box_id].remove(num)

        return False

    backtrack(0)


def print_sudoku(board):
    """Pretty-print a Sudoku board."""
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("------+-------+------")
        line = ""
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                line += "| "
            line += val + " "
        print(line.strip())


# Example
board = [
    ["5","3",".",".","7",".",".",".","."],
    ["6",".",".","1","9","5",".",".","."],
    [".","9","8",".",".",".",".","6","."],
    ["8",".",".",".","6",".",".",".","3"],
    ["4",".",".","8",".","3",".",".","1"],
    ["7",".",".",".","2",".",".",".","6"],
    [".","6",".",".",".",".","2","8","."],
    [".",".",".","4","1","9",".",".","5"],
    [".",".",".",".","8",".",".","7","9"],
]

print("Before:")
print_sudoku(board)
solve_sudoku(board)
print("\nAfter:")
print_sudoku(board)
```

#### JavaScript
```javascript
function solveSudoku(board) {
  const rows = Array.from({ length: 9 }, () => new Set());
  const cols = Array.from({ length: 9 }, () => new Set());
  const boxes = Array.from({ length: 9 }, () => new Set());
  const empty = [];

  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      if (board[r][c] !== ".") {
        const num = board[r][c];
        rows[r].add(num);
        cols[c].add(num);
        boxes[Math.floor(r / 3) * 3 + Math.floor(c / 3)].add(num);
      } else {
        empty.push([r, c]);
      }
    }
  }

  function backtrack(idx) {
    if (idx === empty.length) return true;

    const [r, c] = empty[idx];
    const boxId = Math.floor(r / 3) * 3 + Math.floor(c / 3);

    for (let d = 1; d <= 9; d++) {
      const num = String(d);
      if (rows[r].has(num) || cols[c].has(num) || boxes[boxId].has(num)) {
        continue;
      }

      board[r][c] = num;
      rows[r].add(num);
      cols[c].add(num);
      boxes[boxId].add(num);

      if (backtrack(idx + 1)) return true;

      board[r][c] = ".";
      rows[r].delete(num);
      cols[c].delete(num);
      boxes[boxId].delete(num);
    }

    return false;
  }

  backtrack(0);
}

function printSudoku(board) {
  for (let i = 0; i < 9; i++) {
    if (i % 3 === 0 && i !== 0) console.log("------+-------+------");
    let line = "";
    for (let j = 0; j < 9; j++) {
      if (j % 3 === 0 && j !== 0) line += "| ";
      line += board[i][j] + " ";
    }
    console.log(line.trimEnd());
  }
}

// Example
const board = [
  ["5","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"],
];

console.log("Before:");
printSudoku(board);
solveSudoku(board);
console.log("\nAfter:");
printSudoku(board);
```

#### Java
```java
import java.util.*;

public class SudokuSolver {

    public void solveSudoku(char[][] board) {
        Set<Character>[] rows = new HashSet[9];
        Set<Character>[] cols = new HashSet[9];
        Set<Character>[] boxes = new HashSet[9];
        List<int[]> empty = new ArrayList<>();

        for (int i = 0; i < 9; i++) {
            rows[i] = new HashSet<>();
            cols[i] = new HashSet<>();
            boxes[i] = new HashSet<>();
        }

        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                if (board[r][c] != '.') {
                    char num = board[r][c];
                    rows[r].add(num);
                    cols[c].add(num);
                    boxes[(r / 3) * 3 + c / 3].add(num);
                } else {
                    empty.add(new int[]{r, c});
                }
            }
        }

        backtrack(0, board, rows, cols, boxes, empty);
    }

    private boolean backtrack(int idx, char[][] board,
                              Set<Character>[] rows, Set<Character>[] cols,
                              Set<Character>[] boxes, List<int[]> empty) {
        if (idx == empty.size()) return true;

        int r = empty.get(idx)[0];
        int c = empty.get(idx)[1];
        int boxId = (r / 3) * 3 + c / 3;

        for (char num = '1'; num <= '9'; num++) {
            if (rows[r].contains(num) || cols[c].contains(num)
                    || boxes[boxId].contains(num)) {
                continue;
            }

            board[r][c] = num;
            rows[r].add(num);
            cols[c].add(num);
            boxes[boxId].add(num);

            if (backtrack(idx + 1, board, rows, cols, boxes, empty)) return true;

            board[r][c] = '.';
            rows[r].remove(num);
            cols[c].remove(num);
            boxes[boxId].remove(num);
        }

        return false;
    }

    public static void printBoard(char[][] board) {
        for (int i = 0; i < 9; i++) {
            if (i % 3 == 0 && i != 0)
                System.out.println("------+-------+------");
            StringBuilder sb = new StringBuilder();
            for (int j = 0; j < 9; j++) {
                if (j % 3 == 0 && j != 0) sb.append("| ");
                sb.append(board[i][j]).append(" ");
            }
            System.out.println(sb.toString().stripTrailing());
        }
    }

    public static void main(String[] args) {
        char[][] board = {
            {'5','3','.','.','7','.','.','.','.'},
            {'6','.','.','1','9','5','.','.','.'},
            {'.','9','8','.','.','.','.','6','.'},
            {'8','.','.','.','6','.','.','.','3'},
            {'4','.','.','8','.','3','.','.','1'},
            {'7','.','.','.','2','.','.','.','6'},
            {'.','6','.','.','.','.','2','8','.'},
            {'.','.','.','4','1','9','.','.','5'},
            {'.','.','.','.','8','.','.','7','9'}
        };

        System.out.println("Before:");
        printBoard(board);

        new SudokuSolver().solveSudoku(board);

        System.out.println("\nAfter:");
        printBoard(board);
    }
}
```

**Explanation:**
1. Pre-process the board: populate constraint sets for each row, column, and 3×3 box with existing numbers, and collect all empty cell coordinates
2. Recursively try digits 1–9 in the first empty cell
3. Before placing a digit, check it doesn't conflict with the row, column, or box constraints
4. If a digit is valid, add it to the constraint sets and recurse to the next empty cell
5. If no digit works, backtrack: reset the cell and remove the digit from the constraint sets
6. The board is solved when all empty cells are filled

**When to use:** Constraint satisfaction problems, puzzle generation/validation, and any problem where you need to fill a grid under mutual exclusion rules.

## Variations & Extensions
- **Sudoku validator:** Only check whether a completed board is valid
- **Sudoku generator:** Generate a random valid puzzle with a unique solution
- **16×16 Sudoku:** Extend to larger grids with hex digits
- **Diagonal Sudoku:** Add constraint that main diagonals also contain 1–9
- **Optimized solver:** Use Algorithm X / Dancing Links for faster solving

## Real-World Applications
- Puzzle game development and mobile apps
- Constraint propagation in AI systems
- Test case generation for software testing
- Combinatorial optimization research

## Tags
#backtracking #recursion #hard #constraint-satisfaction #matrix
