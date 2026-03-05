# Database CRUD Operations

## Problem Statement
- Implement Create, Read, Update, and Delete operations against a relational database
- Use parameterized queries to prevent SQL injection
- Handle connection pooling for efficient resource usage
- Edge cases: duplicate keys, missing records, connection failures, transaction rollbacks

## Solutions

### Solution 1: Basic CRUD with Parameterized Queries
- **Time Complexity:** O(1) per single-row operation (database-dependent for scans)
- **Space Complexity:** O(n) where n is the result set size
- **Difficulty:** Easy

#### Python
```python
import sqlite3
from contextlib import contextmanager


@contextmanager
def get_connection(db_path: str = "app.db"):
    """Context manager for safe connection handling."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def create_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER CHECK(age > 0)
        )
    """)


def create_user(conn: sqlite3.Connection, name: str, email: str, age: int) -> int:
    """Insert a new user. Returns the new row ID."""
    cursor = conn.execute(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        (name, email, age),
    )
    return cursor.lastrowid


def get_user_by_id(conn: sqlite3.Connection, user_id: int) -> dict | None:
    """Fetch a single user by ID."""
    cursor = conn.execute(
        "SELECT id, name, email, age FROM users WHERE id = ?",
        (user_id,),
    )
    row = cursor.fetchone()
    return dict(row) if row else None


def get_all_users(conn: sqlite3.Connection, limit: int = 100, offset: int = 0) -> list[dict]:
    """Fetch users with pagination."""
    cursor = conn.execute(
        "SELECT id, name, email, age FROM users ORDER BY id LIMIT ? OFFSET ?",
        (limit, offset),
    )
    return [dict(row) for row in cursor.fetchall()]


def update_user(conn: sqlite3.Connection, user_id: int, name: str = None,
                email: str = None, age: int = None) -> bool:
    """Update user fields. Returns True if a row was modified."""
    fields, values = [], []
    if name is not None:
        fields.append("name = ?")
        values.append(name)
    if email is not None:
        fields.append("email = ?")
        values.append(email)
    if age is not None:
        fields.append("age = ?")
        values.append(age)
    if not fields:
        return False
    values.append(user_id)
    cursor = conn.execute(
        f"UPDATE users SET {', '.join(fields)} WHERE id = ?",
        tuple(values),
    )
    return cursor.rowcount > 0


def delete_user(conn: sqlite3.Connection, user_id: int) -> bool:
    """Delete a user by ID. Returns True if a row was deleted."""
    cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    return cursor.rowcount > 0


# --- Usage example ---
if __name__ == "__main__":
    with get_connection(":memory:") as conn:
        create_table(conn)

        uid = create_user(conn, "Alice", "alice@example.com", 30)
        print("Created user ID:", uid)

        user = get_user_by_id(conn, uid)
        print("Fetched user:", user)

        update_user(conn, uid, name="Alice Smith", age=31)
        print("Updated user:", get_user_by_id(conn, uid))

        deleted = delete_user(conn, uid)
        print("Deleted:", deleted)
        print("After delete:", get_user_by_id(conn, uid))
```

#### JavaScript
```javascript
const sqlite3 = require("better-sqlite3");

class UserRepository {
  constructor(dbPath = "app.db") {
    this.db = sqlite3(dbPath);
    this.db.pragma("journal_mode = WAL");
    this.db.pragma("foreign_keys = ON");
    this._createTable();
  }

  _createTable() {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER CHECK(age > 0)
      )
    `);
  }

  /** Insert a new user. Returns the new row. */
  createUser(name, email, age) {
    const stmt = this.db.prepare(
      "INSERT INTO users (name, email, age) VALUES (?, ?, ?)"
    );
    const result = stmt.run(name, email, age);
    return { id: result.lastInsertRowid, name, email, age };
  }

  /** Fetch a single user by ID. */
  getUserById(id) {
    const stmt = this.db.prepare(
      "SELECT id, name, email, age FROM users WHERE id = ?"
    );
    return stmt.get(id) || null;
  }

  /** Fetch users with pagination. */
  getAllUsers(limit = 100, offset = 0) {
    const stmt = this.db.prepare(
      "SELECT id, name, email, age FROM users ORDER BY id LIMIT ? OFFSET ?"
    );
    return stmt.all(limit, offset);
  }

  /** Update user fields. Returns true if a row was modified. */
  updateUser(id, updates) {
    const fields = [];
    const values = [];
    for (const [key, value] of Object.entries(updates)) {
      if (["name", "email", "age"].includes(key) && value !== undefined) {
        fields.push(`${key} = ?`);
        values.push(value);
      }
    }
    if (fields.length === 0) return false;
    values.push(id);
    const stmt = this.db.prepare(
      `UPDATE users SET ${fields.join(", ")} WHERE id = ?`
    );
    return stmt.run(...values).changes > 0;
  }

  /** Delete a user by ID. Returns true if a row was deleted. */
  deleteUser(id) {
    const stmt = this.db.prepare("DELETE FROM users WHERE id = ?");
    return stmt.run(id).changes > 0;
  }

  close() {
    this.db.close();
  }
}

// --- Usage example ---
const repo = new UserRepository(":memory:");

const user = repo.createUser("Alice", "alice@example.com", 30);
console.log("Created:", user);

console.log("Fetched:", repo.getUserById(user.id));

repo.updateUser(user.id, { name: "Alice Smith", age: 31 });
console.log("Updated:", repo.getUserById(user.id));

console.log("Deleted:", repo.deleteUser(user.id));
console.log("After delete:", repo.getUserById(user.id));

repo.close();

module.exports = UserRepository;
```

#### Java
```java
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class UserRepository {

    private final String url;

    public UserRepository(String url) {
        this.url = url;
        createTable();
    }

    private Connection getConnection() throws SQLException {
        return DriverManager.getConnection(url);
    }

    private void createTable() {
        String sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER CHECK(age > 0)
            )
            """;
        try (Connection conn = getConnection();
             Statement stmt = conn.createStatement()) {
            stmt.execute(sql);
        } catch (SQLException e) {
            throw new RuntimeException("Failed to create table", e);
        }
    }

    /** Insert a new user. Returns the generated ID. */
    public long createUser(String name, String email, int age) {
        String sql = "INSERT INTO users (name, email, age) VALUES (?, ?, ?)";
        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, name);
            ps.setString(2, email);
            ps.setInt(3, age);
            ps.executeUpdate();
            try (ResultSet rs = ps.getGeneratedKeys()) {
                if (rs.next()) return rs.getLong(1);
                throw new RuntimeException("No ID returned");
            }
        } catch (SQLException e) {
            throw new RuntimeException("Failed to create user", e);
        }
    }

    /** Fetch a single user by ID. */
    public Optional<User> getUserById(long id) {
        String sql = "SELECT id, name, email, age FROM users WHERE id = ?";
        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) return Optional.of(mapRow(rs));
                return Optional.empty();
            }
        } catch (SQLException e) {
            throw new RuntimeException("Failed to fetch user", e);
        }
    }

    /** Fetch users with pagination. */
    public List<User> getAllUsers(int limit, int offset) {
        String sql = "SELECT id, name, email, age FROM users ORDER BY id LIMIT ? OFFSET ?";
        List<User> users = new ArrayList<>();
        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, limit);
            ps.setInt(2, offset);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) users.add(mapRow(rs));
            }
        } catch (SQLException e) {
            throw new RuntimeException("Failed to fetch users", e);
        }
        return users;
    }

    /** Update a user's name. Returns true if a row was modified. */
    public boolean updateUser(long id, String name, String email, Integer age) {
        List<String> fields = new ArrayList<>();
        List<Object> values = new ArrayList<>();
        if (name != null) { fields.add("name = ?"); values.add(name); }
        if (email != null) { fields.add("email = ?"); values.add(email); }
        if (age != null) { fields.add("age = ?"); values.add(age); }
        if (fields.isEmpty()) return false;

        values.add(id);
        String sql = "UPDATE users SET " + String.join(", ", fields) + " WHERE id = ?";
        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            for (int i = 0; i < values.size(); i++) {
                ps.setObject(i + 1, values.get(i));
            }
            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            throw new RuntimeException("Failed to update user", e);
        }
    }

    /** Delete a user by ID. Returns true if a row was deleted. */
    public boolean deleteUser(long id) {
        String sql = "DELETE FROM users WHERE id = ?";
        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, id);
            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            throw new RuntimeException("Failed to delete user", e);
        }
    }

    private User mapRow(ResultSet rs) throws SQLException {
        return new User(
            rs.getLong("id"), rs.getString("name"),
            rs.getString("email"), rs.getInt("age")
        );
    }

    public record User(long id, String name, String email, int age) {}

    public static void main(String[] args) {
        UserRepository repo = new UserRepository("jdbc:sqlite::memory:");

        long id = repo.createUser("Alice", "alice@example.com", 30);
        System.out.println("Created ID: " + id);

        System.out.println("Fetched: " + repo.getUserById(id));

        repo.updateUser(id, "Alice Smith", null, 31);
        System.out.println("Updated: " + repo.getUserById(id));

        System.out.println("Deleted: " + repo.deleteUser(id));
        System.out.println("After delete: " + repo.getUserById(id));
    }
}
```

**Explanation:**
1. **Parameterized queries** — All SQL values are passed via placeholders (`?`), never concatenated into the query string, preventing SQL injection.
2. **Connection management** — Python uses a context manager, JavaScript uses a class with explicit `close()`, and Java uses try-with-resources to guarantee connections are released.
3. **Return values** — Create returns the new ID, Read returns the entity or `null`/`Optional.empty()`, Update/Delete return a boolean indicating whether any row was affected.
4. **Pagination** — The `getAllUsers` method accepts `limit` and `offset` parameters to avoid loading entire tables into memory.

**When to use:** Any application backed by a relational database — web apps, internal tools, data pipelines.

### Solution 2: Connection Pooling
- **Time Complexity:** O(1) per connection acquire/release
- **Space Complexity:** O(pool_size) for maintained connections
- **Difficulty:** Easy

#### Python
```python
from psycopg2 import pool

# Create a connection pool (min 2 connections, max 10)
connection_pool = pool.ThreadedConnectionPool(
    minconn=2,
    maxconn=10,
    host="localhost",
    port=5432,
    dbname="myapp",
    user="app_user",
    password="secret",  # In production, load from environment
)


def execute_query(sql: str, params: tuple = ()) -> list[dict]:
    """Execute a query using a pooled connection."""
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            if cur.description:
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]
            conn.commit()
            return []
    except Exception:
        conn.rollback()
        raise
    finally:
        connection_pool.putconn(conn)


# --- Usage ---
# users = execute_query("SELECT * FROM users WHERE age > %s", (18,))
# execute_query("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
#               ("Bob", "bob@example.com", 25))
```

#### JavaScript
```javascript
const { Pool } = require("pg");

// Create a connection pool
const pool = new Pool({
  host: "localhost",
  port: 5432,
  database: "myapp",
  user: "app_user",
  password: process.env.DB_PASSWORD,
  max: 10, // max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

pool.on("error", (err) => {
  console.error("Unexpected pool error:", err);
});

/**
 * Execute a query using a pooled connection.
 */
async function executeQuery(sql, params = []) {
  const client = await pool.connect();
  try {
    const result = await client.query(sql, params);
    return result.rows;
  } finally {
    client.release();
  }
}

/**
 * Execute multiple statements in a transaction.
 */
async function executeTransaction(queries) {
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    const results = [];
    for (const { sql, params } of queries) {
      results.push(await client.query(sql, params));
    }
    await client.query("COMMIT");
    return results;
  } catch (err) {
    await client.query("ROLLBACK");
    throw err;
  } finally {
    client.release();
  }
}

// --- Usage ---
// const users = await executeQuery("SELECT * FROM users WHERE age > $1", [18]);
// await executeTransaction([
//   { sql: "INSERT INTO users (name, email) VALUES ($1, $2)", params: ["Bob", "bob@ex.com"] },
//   { sql: "INSERT INTO audit_log (action) VALUES ($1)", params: ["user_created"] },
// ]);

module.exports = { executeQuery, executeTransaction, pool };
```

#### Java
```java
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

import java.sql.*;
import java.util.*;

public class ConnectionPoolExample {

    private final HikariDataSource dataSource;

    public ConnectionPoolExample() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:postgresql://localhost:5432/myapp");
        config.setUsername("app_user");
        config.setPassword(System.getenv("DB_PASSWORD"));
        config.setMaximumPoolSize(10);
        config.setMinimumIdle(2);
        config.setIdleTimeout(30000);
        config.setConnectionTimeout(2000);
        this.dataSource = new HikariDataSource(config);
    }

    /** Execute a query and return results as a list of maps. */
    public List<Map<String, Object>> executeQuery(String sql, Object... params)
            throws SQLException {
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            for (int i = 0; i < params.length; i++) {
                ps.setObject(i + 1, params[i]);
            }
            if (ps.execute()) {
                return resultSetToList(ps.getResultSet());
            }
            return Collections.emptyList();
        }
    }

    /** Execute multiple statements in a transaction. */
    public void executeTransaction(List<String> sqls, List<Object[]> paramsList)
            throws SQLException {
        try (Connection conn = dataSource.getConnection()) {
            conn.setAutoCommit(false);
            try {
                for (int i = 0; i < sqls.size(); i++) {
                    try (PreparedStatement ps = conn.prepareStatement(sqls.get(i))) {
                        Object[] params = paramsList.get(i);
                        for (int j = 0; j < params.length; j++) {
                            ps.setObject(j + 1, params[j]);
                        }
                        ps.executeUpdate();
                    }
                }
                conn.commit();
            } catch (SQLException e) {
                conn.rollback();
                throw e;
            }
        }
    }

    private List<Map<String, Object>> resultSetToList(ResultSet rs) throws SQLException {
        List<Map<String, Object>> results = new ArrayList<>();
        ResultSetMetaData meta = rs.getMetaData();
        int columnCount = meta.getColumnCount();
        while (rs.next()) {
            Map<String, Object> row = new LinkedHashMap<>();
            for (int i = 1; i <= columnCount; i++) {
                row.put(meta.getColumnLabel(i), rs.getObject(i));
            }
            results.add(row);
        }
        return results;
    }

    public void close() {
        dataSource.close();
    }
}
```

**Explanation:**
1. **Connection pooling** — Reuses database connections instead of opening/closing them per query, dramatically reducing latency and resource consumption under load.
2. **Pool configuration** — `max` (pool size), `idleTimeout`, and `connectionTimeout` control resource usage and fail-fast behavior.
3. **Transaction support** — Multiple statements are wrapped in `BEGIN`/`COMMIT` with `ROLLBACK` on failure, ensuring atomicity.

**When to use:** Any application that makes frequent database calls — web servers, background job processors, data-intensive services.

## Variations & Extensions
- Add soft deletes (set a `deleted_at` timestamp instead of removing the row)
- Implement optimistic locking with a `version` column for concurrent updates
- Add full-text search using database-specific features (PostgreSQL `tsvector`, MySQL `FULLTEXT`)
- Implement batch inserts for bulk data loading

## Real-World Applications
- Web application backends (user management, product catalogs)
- Content management systems
- E-commerce order processing
- Internal business tools and dashboards

## Tags
#database #crud #sql #parameterized-queries #connection-pooling #easy
