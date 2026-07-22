# FastAPI-Auth

FastAPI-Auth is a professional-grade, database-agnostic authentication and session management utility library for Python. It provides high-level security primitives without enforcing any specific database ORM or model structure, giving you total flexibility.

## Core Features

- **Crypto Utilities:** Argon2id password hashing and verification with brute-force protection logic.
- **Token Management:** JWT creation and verification.
- **Session Utilities:** Secure refresh token hashing for rotation strategies.
- **Middleware:** Storage-agnostic rate limiting and authentication decorators.
- **Validation:** Strict structural validation for usernames and passwords.
- **Lightweight:** No dependency on SQLModel, Pydantic, or any specific database driver.

## Installation

```bash
pip install fastapi-auth
```

## Quick Start

### 1. Password Hashing

```python
from fastapi_auth import Security

# Hash a password
hashed = Security["hash"]("my_secure_password")

# Verify a password
is_valid = Security["verify"]("my_secure_password", hashed)

# Reset logic (Verify old -> Hash new)
new_hash = Security["reset"](hashed, "old_password", "new_password")
```

### 2. JWT & Tokens

```python
from fastapi_auth import TokenHandler, SessionManager

handler = TokenHandler(SECRET_KEY="your_secret_key")

# Create Access & Refresh tokens
tokens = handler.createJwt(sub="user_id_123")
# Returns: {"access_token": "...", "refresh_token": "...", "refresh_days": 7}

# Hash refresh token for secure storage
session_util = SessionManager()
storage_hash = session_util.hash_refresh_token(tokens["refresh_token"])
```

### 3. Middleware & Protection

```python
from fastapi_auth import require_auth, TokenHandler

handler = TokenHandler(SECRET_KEY="your_secret_key")

@require_auth(jwt_handler=handler)
def protected_route(payload):
    return f"Hello {payload['sub']}"
```

## Architecture: Why "Database Agnostic"?

Unlike other libraries that force you to use a specific ORM (like SQLAlchemy or SQLModel), FastAPI-Auth acts as a **security toolkit**. 

- **You** control the database (PostgreSQL, MongoDB, Redis, etc.).
- **You** control the models.
- **FastAPI-Auth** handles the heavy lifting of hashing, signing, and security logic.

## Testing

```bash
pytest
```

## License

MIT License.
