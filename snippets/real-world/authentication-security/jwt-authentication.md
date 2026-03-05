# JWT Authentication

## Problem Statement
- Implement JSON Web Token (JWT) based authentication for securing APIs
- Generate tokens upon successful login, validate tokens on protected routes, and handle token refresh
- Edge cases: expired tokens, tampered tokens, missing claims, clock skew

## Solutions

### Solution 1: Token Generation and Validation
- **Time Complexity:** O(1) for token creation/verification (cryptographic operations are constant relative to input)
- **Space Complexity:** O(1)
- **Difficulty:** Medium

#### Python
```python
import jwt
import datetime
from functools import wraps

SECRET_KEY = "your-256-bit-secret"  # In production, load from environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 15
REFRESH_TOKEN_EXPIRY_DAYS = 7


def generate_access_token(user_id: str, role: str) -> str:
    """Generate a short-lived access token."""
    payload = {
        "sub": user_id,
        "role": role,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES),
        "type": "access",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def generate_refresh_token(user_id: str, role: str) -> str:
    """Generate a long-lived refresh token."""
    payload = {
        "sub": user_id,
        "role": role,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
        "type": "refresh",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    """Verify and decode a JWT token. Raises on invalid/expired tokens."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {e}")


def refresh_access_token(refresh_token: str) -> str:
    """Use a valid refresh token to issue a new access token."""
    payload = verify_token(refresh_token)
    if payload.get("type") != "refresh":
        raise ValueError("Invalid token type: expected refresh token")
    return generate_access_token(payload["sub"], payload.get("role", "user"))


def require_auth(f):
    """Decorator that enforces JWT authentication on a route."""
    @wraps(f)
    def decorated(*args, **kwargs):
        from flask import request, jsonify

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or malformed token"}), 401
        token = auth_header.split(" ", 1)[1]
        try:
            payload = verify_token(token)
            if payload.get("type") != "access":
                return jsonify({"error": "Invalid token type"}), 401
            request.user = payload
        except ValueError as e:
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)
    return decorated


# --- Usage example ---
if __name__ == "__main__":
    access = generate_access_token("user123", "admin")
    refresh = generate_refresh_token("user123", "admin")
    print("Access token:", access)
    print("Refresh token:", refresh)

    decoded = verify_token(access)
    print("Decoded payload:", decoded)

    new_access = refresh_access_token(refresh)
    print("New access token:", new_access)
```

#### JavaScript
```javascript
const jwt = require("jsonwebtoken");

const SECRET_KEY = process.env.JWT_SECRET || "your-256-bit-secret";
const ACCESS_TOKEN_EXPIRY = "15m";
const REFRESH_TOKEN_EXPIRY = "7d";

/**
 * Generate a short-lived access token.
 */
function generateAccessToken(userId, role) {
  return jwt.sign({ sub: userId, role, type: "access" }, SECRET_KEY, {
    expiresIn: ACCESS_TOKEN_EXPIRY,
  });
}

/**
 * Generate a long-lived refresh token.
 */
function generateRefreshToken(userId, role) {
  return jwt.sign({ sub: userId, role, type: "refresh" }, SECRET_KEY, {
    expiresIn: REFRESH_TOKEN_EXPIRY,
  });
}

/**
 * Verify and decode a JWT token.
 * @returns {object} Decoded payload
 * @throws {Error} On invalid or expired tokens
 */
function verifyToken(token) {
  try {
    return jwt.verify(token, SECRET_KEY);
  } catch (err) {
    if (err.name === "TokenExpiredError") {
      throw new Error("Token has expired");
    }
    throw new Error(`Invalid token: ${err.message}`);
  }
}

/**
 * Issue a new access token using a valid refresh token.
 */
function refreshAccessToken(refreshToken) {
  const payload = verifyToken(refreshToken);
  if (payload.type !== "refresh") {
    throw new Error("Invalid token type: expected refresh token");
  }
    return generateAccessToken(payload.sub, payload.role || "user");
}

/**
 * Express middleware that enforces JWT authentication.
 */
function requireAuth(req, res, next) {
  const authHeader = req.headers.authorization || "";
  if (!authHeader.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Missing or malformed token" });
  }
  const token = authHeader.split(" ")[1];
  try {
    const payload = verifyToken(token);
    if (payload.type !== "access") {
      return res.status(401).json({ error: "Invalid token type" });
    }
    req.user = payload;
    next();
  } catch (err) {
    return res.status(401).json({ error: err.message });
  }
}

// --- Usage example ---
const access = generateAccessToken("user123", "admin");
const refresh = generateRefreshToken("user123", "admin");
console.log("Access token:", access);
console.log("Refresh token:", refresh);

const decoded = verifyToken(access);
console.log("Decoded payload:", decoded);

const newAccess = refreshAccessToken(refresh);
console.log("New access token:", newAccess);

module.exports = {
  generateAccessToken,
  generateRefreshToken,
  verifyToken,
  refreshAccessToken,
  requireAuth,
};
```

#### Java
```java
import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.util.Map;

public class JwtAuthenticator {

    // In production, load from environment or a secrets manager
    private static final String SECRET = "your-256-bit-secret-key-at-least-32chars!!";
    private static final SecretKey KEY =
            Keys.hmacShaKeyFor(SECRET.getBytes(StandardCharsets.UTF_8));
    private static final long ACCESS_TOKEN_EXPIRY_MS = 15 * 60 * 1000;   // 15 minutes
    private static final long REFRESH_TOKEN_EXPIRY_MS = 7 * 24 * 60 * 60 * 1000; // 7 days

    /** Generate a short-lived access token. */
    public static String generateAccessToken(String userId, String role) {
        Date now = new Date();
        return Jwts.builder()
                .subject(userId)
                .claim("role", role)
                .claim("type", "access")
                .issuedAt(now)
                .expiration(new Date(now.getTime() + ACCESS_TOKEN_EXPIRY_MS))
                .signWith(KEY)
                .compact();
    }

    /** Generate a long-lived refresh token. */
    public static String generateRefreshToken(String userId, String role) {
        Date now = new Date();
        return Jwts.builder()
                .subject(userId)
                .claim("role", role)
                .claim("type", "refresh")
                .issuedAt(now)
                .expiration(new Date(now.getTime() + REFRESH_TOKEN_EXPIRY_MS))
                .signWith(KEY)
                .compact();
    }

    /** Verify and decode a JWT token. Throws on invalid/expired tokens. */
    public static Claims verifyToken(String token) {
        try {
            return Jwts.parser()
                    .verifyWith(KEY)
                    .build()
                    .parseSignedClaims(token)
                    .getPayload();
        } catch (ExpiredJwtException e) {
            throw new RuntimeException("Token has expired", e);
        } catch (JwtException e) {
            throw new RuntimeException("Invalid token: " + e.getMessage(), e);
        }
    }

    /** Use a valid refresh token to issue a new access token. */
    public static String refreshAccessToken(String refreshToken) {
        Claims claims = verifyToken(refreshToken);
        if (!"refresh".equals(claims.get("type", String.class))) {
            throw new RuntimeException("Invalid token type: expected refresh token");
        }
        String role = claims.get("role", String.class);
        return generateAccessToken(claims.getSubject(), role != null ? role : "user");
    }

    public static void main(String[] args) {
        String access = generateAccessToken("user123", "admin");
        String refresh = generateRefreshToken("user123", "admin");
        System.out.println("Access token: " + access);
        System.out.println("Refresh token: " + refresh);

        Claims decoded = verifyToken(access);
        System.out.println("Subject: " + decoded.getSubject());
        System.out.println("Role: " + decoded.get("role"));

        String newAccess = refreshAccessToken(refresh);
        System.out.println("New access token: " + newAccess);
    }
}
```

**Explanation:**
1. **Token generation** — Create a JWT with claims (`sub`, `role`, `type`, `exp`, `iat`) and sign it with a secret key using HMAC-SHA256.
2. **Token verification** — Parse the token, verify the signature and expiration, and return the decoded claims. Distinct error handling for expired vs. tampered tokens.
3. **Refresh flow** — Accept a refresh token, verify it is the correct type, and issue a new short-lived access token without re-authenticating.
4. **Middleware/decorator** — Extract the Bearer token from the `Authorization` header, verify it, attach user info to the request, and reject unauthorized requests with 401.

**When to use:** Any API or web application that requires stateless authentication — microservices, single-page applications, mobile app backends.

### Solution 2: Security Best Practices
- **Difficulty:** Medium

#### Python
```python
import os
import secrets
import hashlib

# 1. Always load secrets from environment variables
SECRET_KEY = os.environ["JWT_SECRET_KEY"]

# 2. Use a token blocklist for logout / revocation
token_blocklist: set[str] = set()


def revoke_token(token: str) -> None:
    """Add a token's fingerprint to the blocklist (e.g., on logout)."""
    fingerprint = hashlib.sha256(token.encode()).hexdigest()
    token_blocklist.add(fingerprint)


def is_token_revoked(token: str) -> bool:
    """Check if a token has been revoked."""
    fingerprint = hashlib.sha256(token.encode()).hexdigest()
    return fingerprint in token_blocklist


# 3. Bind tokens to a fingerprint cookie to prevent token theft
def generate_fingerprint() -> tuple[str, str]:
    """Generate a random fingerprint and its hash for token binding."""
    raw = secrets.token_hex(32)
    hashed = hashlib.sha256(raw.encode()).hexdigest()
    return raw, hashed  # raw goes in cookie, hashed goes in JWT claim


# 4. Rate-limit login attempts (pseudocode with a dict; use Redis in production)
login_attempts: dict[str, list[float]] = {}
MAX_ATTEMPTS = 5
WINDOW_SECONDS = 300


def check_rate_limit(ip: str) -> bool:
    """Return True if the IP is within rate limits."""
    import time

    now = time.time()
    attempts = login_attempts.get(ip, [])
    attempts = [t for t in attempts if now - t < WINDOW_SECONDS]
    login_attempts[ip] = attempts
    return len(attempts) < MAX_ATTEMPTS
```

#### JavaScript
```javascript
const crypto = require("crypto");

// 1. Always load secrets from environment variables
const SECRET_KEY = process.env.JWT_SECRET_KEY;
if (!SECRET_KEY) {
  throw new Error("JWT_SECRET_KEY environment variable is required");
}

// 2. Token blocklist for logout / revocation
const tokenBlocklist = new Set();

function revokeToken(token) {
  const fingerprint = crypto.createHash("sha256").update(token).digest("hex");
  tokenBlocklist.add(fingerprint);
}

function isTokenRevoked(token) {
  const fingerprint = crypto.createHash("sha256").update(token).digest("hex");
  return tokenBlocklist.has(fingerprint);
}

// 3. Bind tokens to a fingerprint cookie
function generateFingerprint() {
  const raw = crypto.randomBytes(32).toString("hex");
  const hashed = crypto.createHash("sha256").update(raw).digest("hex");
  return { raw, hashed }; // raw -> HttpOnly cookie, hashed -> JWT claim
}

// 4. Rate-limit login attempts
const loginAttempts = new Map();
const MAX_ATTEMPTS = 5;
const WINDOW_MS = 5 * 60 * 1000;

function checkRateLimit(ip) {
  const now = Date.now();
  const attempts = (loginAttempts.get(ip) || []).filter(
    (t) => now - t < WINDOW_MS
  );
  loginAttempts.set(ip, attempts);
  return attempts.length < MAX_ATTEMPTS;
}

module.exports = {
  revokeToken,
  isTokenRevoked,
  generateFingerprint,
  checkRateLimit,
};
```

#### Java
```java
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Collections;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class JwtSecurityUtils {

    // 1. Always load secrets from environment variables
    private static final String SECRET_KEY = System.getenv("JWT_SECRET_KEY");

    static {
        if (SECRET_KEY == null || SECRET_KEY.isEmpty()) {
            throw new RuntimeException("JWT_SECRET_KEY environment variable is required");
        }
    }

    // 2. Token blocklist for revocation (use Redis/database in production)
    private static final Set<String> TOKEN_BLOCKLIST =
            Collections.newSetFromMap(new ConcurrentHashMap<>());

    public static void revokeToken(String token) throws NoSuchAlgorithmException {
        TOKEN_BLOCKLIST.add(sha256(token));
    }

    public static boolean isTokenRevoked(String token) throws NoSuchAlgorithmException {
        return TOKEN_BLOCKLIST.contains(sha256(token));
    }

    // 3. Fingerprint binding
    public static String[] generateFingerprint() throws NoSuchAlgorithmException {
        SecureRandom random = new SecureRandom();
        byte[] bytes = new byte[32];
        random.nextBytes(bytes);
        String raw = bytesToHex(bytes);
        String hashed = sha256(raw);
        return new String[]{raw, hashed}; // raw -> cookie, hashed -> JWT claim
    }

    private static String sha256(String input) throws NoSuchAlgorithmException {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = digest.digest(input.getBytes(StandardCharsets.UTF_8));
        return bytesToHex(hash);
    }

    private static String bytesToHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder(bytes.length * 2);
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
```

**Explanation:**
1. **Environment-based secrets** — Never hard-code secrets; load them from environment variables or a secrets manager.
2. **Token revocation** — Maintain a blocklist (backed by Redis or a database in production) to invalidate tokens on logout.
3. **Fingerprint binding** — Pair each token with a random fingerprint stored in an HttpOnly cookie. The hash of the fingerprint is embedded in the JWT, preventing stolen tokens from being reused without the cookie.
4. **Rate limiting** — Throttle login attempts per IP to mitigate brute-force attacks.

**When to use:** Production systems that need defense-in-depth beyond basic JWT signing — banking, healthcare, or any app handling sensitive data.

## Variations & Extensions
- Use asymmetric keys (RS256) instead of symmetric (HS256) for distributed systems where only the auth server needs to sign tokens
- Add audience (`aud`) and issuer (`iss`) claims for multi-tenant systems
- Implement sliding-window token refresh where tokens are renewed on each request
- Store refresh tokens in a database to allow per-device revocation

## Real-World Applications
- Single-page application (SPA) authentication with a REST API
- Microservice-to-microservice authentication
- Mobile app backends with token-based sessions
- OAuth 2.0 resource server token validation

## Tags
#jwt #authentication #security #middleware #medium
