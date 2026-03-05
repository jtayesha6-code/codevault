# REST API Client

## Problem Statement
- Make HTTP requests (GET, POST, PUT, DELETE) to REST APIs
- Handle errors, timeouts, and implement retry logic with exponential backoff
- Manage headers, authentication, and response parsing
- Edge cases: network failures, rate limiting (429), server errors (5xx), malformed responses

## Solutions

### Solution 1: Basic REST Client with Error Handling
- **Time Complexity:** O(1) per request (network-bound)
- **Space Complexity:** O(n) where n is the response size
- **Difficulty:** Medium

#### Python
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session(
    base_url: str = "",
    token: str = None,
    retries: int = 3,
    backoff_factor: float = 0.5,
    timeout: int = 30,
) -> requests.Session:
    """Create a configured requests session with retry logic."""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    if token:
        session.headers["Authorization"] = f"Bearer {token}"

    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "PUT", "DELETE", "HEAD", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Store config on session for use in helper methods
    session._base_url = base_url
    session._timeout = timeout
    return session


def get(session: requests.Session, path: str, params: dict = None) -> dict:
    """Send a GET request and return parsed JSON."""
    url = session._base_url + path
    response = session.get(url, params=params, timeout=session._timeout)
    response.raise_for_status()
    return response.json()


def post(session: requests.Session, path: str, data: dict = None) -> dict:
    """Send a POST request with JSON body."""
    url = session._base_url + path
    response = session.post(url, json=data, timeout=session._timeout)
    response.raise_for_status()
    return response.json() if response.content else {}


def put(session: requests.Session, path: str, data: dict = None) -> dict:
    """Send a PUT request with JSON body."""
    url = session._base_url + path
    response = session.put(url, json=data, timeout=session._timeout)
    response.raise_for_status()
    return response.json() if response.content else {}


def delete(session: requests.Session, path: str) -> bool:
    """Send a DELETE request. Returns True on success."""
    url = session._base_url + path
    response = session.delete(url, timeout=session._timeout)
    response.raise_for_status()
    return True


# --- Usage ---
if __name__ == "__main__":
    api = create_session(
        base_url="https://jsonplaceholder.typicode.com",
        timeout=10,
    )

    # GET
    posts = get(api, "/posts", params={"_limit": 5})
    print(f"Fetched {len(posts)} posts")

    # POST
    new_post = post(api, "/posts", data={
        "title": "Hello", "body": "World", "userId": 1,
    })
    print(f"Created post ID: {new_post.get('id')}")

    # PUT
    updated = put(api, "/posts/1", data={
        "title": "Updated Title", "body": "Updated Body", "userId": 1,
    })
    print(f"Updated post title: {updated.get('title')}")

    # DELETE
    deleted = delete(api, "/posts/1")
    print(f"Deleted: {deleted}")
```

#### JavaScript
```javascript
const https = require("https");
const http = require("http");

class RestClient {
  /**
   * @param {string} baseUrl - Base URL for all requests
   * @param {object} options - Configuration options
   * @param {string} options.token - Bearer token for authentication
   * @param {number} options.timeout - Request timeout in ms (default: 30000)
   * @param {number} options.retries - Max retry attempts (default: 3)
   */
  constructor(baseUrl, options = {}) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.token = options.token || null;
    this.timeout = options.timeout || 30000;
    this.retries = options.retries || 3;
    this.defaultHeaders = {
      "Content-Type": "application/json",
      Accept: "application/json",
    };
    if (this.token) {
      this.defaultHeaders["Authorization"] = `Bearer ${this.token}`;
    }
  }

  /**
   * Core request method with retry logic.
   */
  async request(method, path, { body, params, headers } = {}) {
    let url = `${this.baseUrl}${path}`;
    if (params) {
      const qs = new URLSearchParams(params).toString();
      url += `?${qs}`;
    }

    let lastError;
    for (let attempt = 0; attempt <= this.retries; attempt++) {
      if (attempt > 0) {
        const delay = Math.pow(2, attempt - 1) * 500;
        await new Promise((resolve) => setTimeout(resolve, delay));
      }

      try {
        const response = await this._fetch(method, url, {
          body,
          headers: { ...this.defaultHeaders, ...headers },
        });
        return response;
      } catch (err) {
        lastError = err;
        const retryable =
          err.statusCode >= 500 || err.statusCode === 429 || err.code === "ETIMEDOUT";
        if (!retryable || attempt === this.retries) throw err;
      }
    }
    throw lastError;
  }

  _fetch(method, url, { body, headers }) {
    return new Promise((resolve, reject) => {
      const parsed = new URL(url);
      const transport = parsed.protocol === "https:" ? https : http;
      const options = {
        method,
        hostname: parsed.hostname,
        port: parsed.port,
        path: parsed.pathname + parsed.search,
        headers,
        timeout: this.timeout,
      };

      const req = transport.request(options, (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          if (res.statusCode >= 400) {
            const err = new Error(`HTTP ${res.statusCode}: ${data}`);
            err.statusCode = res.statusCode;
            err.body = data;
            return reject(err);
          }
          try {
            resolve(data ? JSON.parse(data) : {});
          } catch {
            resolve(data);
          }
        });
      });

      req.on("timeout", () => {
        req.destroy();
        const err = new Error("Request timed out");
        err.code = "ETIMEDOUT";
        reject(err);
      });
      req.on("error", reject);

      if (body) req.write(JSON.stringify(body));
      req.end();
    });
  }

  async get(path, params) {
    return this.request("GET", path, { params });
  }
  async post(path, body) {
    return this.request("POST", path, { body });
  }
  async put(path, body) {
    return this.request("PUT", path, { body });
  }
  async delete(path) {
    return this.request("DELETE", path);
  }
}

// --- Usage ---
(async () => {
  const api = new RestClient("https://jsonplaceholder.typicode.com", {
    timeout: 10000,
  });

  const posts = await api.get("/posts", { _limit: "5" });
  console.log(`Fetched ${posts.length} posts`);

  const newPost = await api.post("/posts", {
    title: "Hello",
    body: "World",
    userId: 1,
  });
  console.log(`Created post ID: ${newPost.id}`);

  const updated = await api.put("/posts/1", {
    title: "Updated Title",
    body: "Updated Body",
    userId: 1,
  });
  console.log(`Updated post title: ${updated.title}`);

  await api.delete("/posts/1");
  console.log("Deleted successfully");
})();

module.exports = RestClient;
```

#### Java
```java
import java.io.*;
import java.net.*;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.time.Duration;
import java.util.Map;

public class RestClient {

    private final String baseUrl;
    private final HttpClient client;
    private final String token;
    private final int maxRetries;

    public RestClient(String baseUrl, String token, int timeoutSeconds, int maxRetries) {
        this.baseUrl = baseUrl.replaceAll("/$", "");
        this.token = token;
        this.maxRetries = maxRetries;
        this.client = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(timeoutSeconds))
                .build();
    }

    public RestClient(String baseUrl) {
        this(baseUrl, null, 30, 3);
    }

    /** Send a GET request and return the response body. */
    public String get(String path) throws IOException, InterruptedException {
        HttpRequest request = buildRequest("GET", path, null);
        return executeWithRetry(request);
    }

    /** Send a POST request with a JSON body. */
    public String post(String path, String jsonBody) throws IOException, InterruptedException {
        HttpRequest request = buildRequest("POST", path, jsonBody);
        return executeWithRetry(request);
    }

    /** Send a PUT request with a JSON body. */
    public String put(String path, String jsonBody) throws IOException, InterruptedException {
        HttpRequest request = buildRequest("PUT", path, jsonBody);
        return executeWithRetry(request);
    }

    /** Send a DELETE request. */
    public String delete(String path) throws IOException, InterruptedException {
        HttpRequest request = buildRequest("DELETE", path, null);
        return executeWithRetry(request);
    }

    private HttpRequest buildRequest(String method, String path, String body) {
        HttpRequest.Builder builder = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + path))
                .header("Content-Type", "application/json")
                .header("Accept", "application/json")
                .timeout(Duration.ofSeconds(30));

        if (token != null && !token.isEmpty()) {
            builder.header("Authorization", "Bearer " + token);
        }

        if (body != null) {
            builder.method(method, BodyPublishers.ofString(body));
        } else {
            builder.method(method, BodyPublishers.noBody());
        }

        return builder.build();
    }

    private String executeWithRetry(HttpRequest request)
            throws IOException, InterruptedException {
        IOException lastException = null;

        for (int attempt = 0; attempt <= maxRetries; attempt++) {
            if (attempt > 0) {
                long delay = (long) Math.pow(2, attempt - 1) * 500;
                Thread.sleep(delay);
            }

            try {
                HttpResponse<String> response =
                        client.send(request, BodyHandlers.ofString());
                int status = response.statusCode();

                if (status >= 200 && status < 300) {
                    return response.body();
                }

                boolean retryable = status == 429 || status >= 500;
                if (!retryable || attempt == maxRetries) {
                    throw new IOException(
                            "HTTP " + status + ": " + response.body());
                }
            } catch (HttpTimeoutException e) {
                lastException = new IOException("Request timed out", e);
                if (attempt == maxRetries) throw lastException;
            }
        }
        throw lastException != null ? lastException : new IOException("Request failed");
    }

    public static void main(String[] args) throws Exception {
        RestClient api = new RestClient("https://jsonplaceholder.typicode.com");

        // GET
        String posts = api.get("/posts?_limit=5");
        System.out.println("Posts: " + posts.substring(0, Math.min(100, posts.length())) + "...");

        // POST
        String created = api.post("/posts",
                "{\"title\":\"Hello\",\"body\":\"World\",\"userId\":1}");
        System.out.println("Created: " + created);

        // PUT
        String updated = api.put("/posts/1",
                "{\"title\":\"Updated\",\"body\":\"Body\",\"userId\":1}");
        System.out.println("Updated: " + updated);

        // DELETE
        api.delete("/posts/1");
        System.out.println("Deleted successfully");
    }
}
```

**Explanation:**
1. **Session/client reuse** — Reuse a single HTTP client (session) across requests to benefit from connection pooling and shared configuration (headers, timeouts).
2. **Retry with exponential backoff** — Automatically retry on transient failures (5xx, 429, timeouts) with increasing delays (500ms, 1s, 2s, ...) to avoid overwhelming the server.
3. **Status code handling** — Raise exceptions for 4xx/5xx responses so callers can use try/catch for error handling.
4. **Parameterized URLs** — Query parameters are built safely using URL encoding utilities, not string concatenation.

**When to use:** Any application that consumes third-party APIs — payment gateways, social media integrations, microservice communication.

### Solution 2: Advanced Patterns (Rate Limiting, Pagination)
- **Difficulty:** Medium

#### Python
```python
import time
import requests


class RateLimitedClient:
    """REST client with built-in rate limiting and pagination support."""

    def __init__(self, base_url: str, requests_per_second: float = 10, token: str = None):
        self.base_url = base_url.rstrip("/")
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0.0
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def _throttle(self):
        """Enforce rate limiting between requests."""
        elapsed = time.monotonic() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.monotonic()

    def get(self, path: str, params: dict = None, timeout: int = 30) -> dict:
        self._throttle()
        response = self.session.get(
            self.base_url + path, params=params, timeout=timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_all_pages(self, path: str, params: dict = None,
                      page_param: str = "page", per_page: int = 100,
                      max_pages: int = 100) -> list:
        """Fetch all pages of a paginated endpoint."""
        params = dict(params or {})
        params["per_page"] = per_page
        all_items = []

        for page in range(1, max_pages + 1):
            params[page_param] = page
            data = self.get(path, params=params)

            if isinstance(data, list):
                if not data:
                    break
                all_items.extend(data)
                if len(data) < per_page:
                    break
            else:
                all_items.append(data)
                break

        return all_items

    def get_cursor_pages(self, path: str, params: dict = None,
                         cursor_field: str = "next_cursor",
                         data_field: str = "data") -> list:
        """Fetch all pages using cursor-based pagination."""
        params = dict(params or {})
        all_items = []

        while True:
            response = self.get(path, params=params)
            items = response.get(data_field, [])
            all_items.extend(items)

            cursor = response.get(cursor_field)
            if not cursor:
                break
            params["cursor"] = cursor

        return all_items


# --- Usage ---
if __name__ == "__main__":
    client = RateLimitedClient(
        "https://jsonplaceholder.typicode.com",
        requests_per_second=5,
    )
    all_posts = client.get_all_pages("/posts", per_page=10, max_pages=5)
    print(f"Fetched {len(all_posts)} posts across multiple pages")
```

#### JavaScript
```javascript
class RateLimitedClient {
  /**
   * @param {string} baseUrl
   * @param {object} options
   * @param {number} options.requestsPerSecond - Max requests per second
   * @param {string} options.token - Bearer token
   */
  constructor(baseUrl, options = {}) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.minInterval = 1000 / (options.requestsPerSecond || 10);
    this.lastRequestTime = 0;
    this.token = options.token || null;
  }

  async _throttle() {
    const elapsed = Date.now() - this.lastRequestTime;
    if (elapsed < this.minInterval) {
      await new Promise((r) => setTimeout(r, this.minInterval - elapsed));
    }
    this.lastRequestTime = Date.now();
  }

  async get(path, params) {
    await this._throttle();
    let url = `${this.baseUrl}${path}`;
    if (params) url += `?${new URLSearchParams(params)}`;

    const headers = { Accept: "application/json" };
    if (this.token) headers["Authorization"] = `Bearer ${this.token}`;

    const response = await fetch(url, { headers });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }

  /**
   * Fetch all pages of a paginated endpoint.
   */
  async getAllPages(path, { pageParam = "page", perPage = 100, maxPages = 100 } = {}) {
    const allItems = [];

    for (let page = 1; page <= maxPages; page++) {
      const data = await this.get(path, {
        [pageParam]: page,
        per_page: perPage,
      });

      if (Array.isArray(data)) {
        if (data.length === 0) break;
        allItems.push(...data);
        if (data.length < perPage) break;
      } else {
        allItems.push(data);
        break;
      }
    }

    return allItems;
  }

  /**
   * Fetch all pages using cursor-based pagination.
   */
  async getCursorPages(path, { cursorField = "next_cursor", dataField = "data" } = {}) {
    const allItems = [];
    let cursor = null;

    while (true) {
      const params = cursor ? { cursor } : {};
      const response = await this.get(path, params);
      const items = response[dataField] || [];
      allItems.push(...items);

      cursor = response[cursorField];
      if (!cursor) break;
    }

    return allItems;
  }
}

// --- Usage ---
(async () => {
  const client = new RateLimitedClient(
    "https://jsonplaceholder.typicode.com",
    { requestsPerSecond: 5 }
  );
  const posts = await client.getAllPages("/posts", { perPage: 10, maxPages: 5 });
  console.log(`Fetched ${posts.length} posts across multiple pages`);
})();

module.exports = RateLimitedClient;
```

#### Java
```java
import java.io.IOException;
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpResponse.BodyHandlers;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

public class RateLimitedClient {

    private final String baseUrl;
    private final HttpClient client;
    private final long minIntervalMs;
    private final String token;
    private long lastRequestTime = 0;

    public RateLimitedClient(String baseUrl, double requestsPerSecond, String token) {
        this.baseUrl = baseUrl.replaceAll("/$", "");
        this.minIntervalMs = (long) (1000.0 / requestsPerSecond);
        this.token = token;
        this.client = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(30))
                .build();
    }

    private synchronized void throttle() throws InterruptedException {
        long elapsed = System.currentTimeMillis() - lastRequestTime;
        if (elapsed < minIntervalMs) {
            Thread.sleep(minIntervalMs - elapsed);
        }
        lastRequestTime = System.currentTimeMillis();
    }

    public String get(String path) throws IOException, InterruptedException {
        throttle();
        HttpRequest.Builder builder = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + path))
                .header("Accept", "application/json")
                .GET()
                .timeout(Duration.ofSeconds(30));

        if (token != null) {
            builder.header("Authorization", "Bearer " + token);
        }

        HttpResponse<String> response = client.send(builder.build(), BodyHandlers.ofString());
        if (response.statusCode() >= 400) {
            throw new IOException("HTTP " + response.statusCode() + ": " + response.body());
        }
        return response.body();
    }

    /**
     * Fetch multiple pages from a paginated endpoint.
     * Returns a list of raw JSON response strings (one per page).
     */
    public List<String> getAllPages(String basePath, int perPage, int maxPages)
            throws IOException, InterruptedException {
        List<String> pages = new ArrayList<>();
        String separator = basePath.contains("?") ? "&" : "?";

        for (int page = 1; page <= maxPages; page++) {
            String path = basePath + separator + "page=" + page + "&per_page=" + perPage;
            String data = get(path);

            pages.add(data);
            // Stop if we got fewer items than requested (simple heuristic)
            if (data.equals("[]") || !data.startsWith("[")) break;
        }

        return pages;
    }

    public static void main(String[] args) throws Exception {
        RateLimitedClient client = new RateLimitedClient(
                "https://jsonplaceholder.typicode.com", 5.0, null);

        List<String> pages = client.getAllPages("/posts", 10, 5);
        System.out.println("Fetched " + pages.size() + " pages of posts");
    }
}
```

**Explanation:**
1. **Rate limiting** — Track the timestamp of the last request and sleep if the minimum interval hasn't elapsed, preventing 429 (Too Many Requests) responses.
2. **Offset pagination** — Increment the `page` parameter until the server returns an empty list or fewer items than the page size.
3. **Cursor pagination** — Use a cursor/token from each response to fetch the next page, which is more efficient for large datasets and avoids issues with concurrent inserts.

**When to use:** Integrating with APIs that have rate limits (GitHub, Stripe, Slack) or endpoints that return large datasets across many pages.

## Variations & Extensions
- Add request/response logging and metrics collection
- Implement circuit breaker pattern to stop calling failing services
- Add response caching with TTL to reduce redundant API calls
- Support file upload with multipart form data
- Add OAuth 2.0 client credentials flow for service-to-service auth

## Real-World Applications
- Payment gateway integration (Stripe, PayPal)
- Social media API consumption (Twitter, GitHub)
- Microservice-to-microservice communication
- Third-party data aggregation and ETL pipelines

## Tags
#rest-api #http #retry #rate-limiting #pagination #medium
