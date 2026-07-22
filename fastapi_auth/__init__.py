from fastapi_auth.crypto.passwords import (
    hash_password,
    verifyPassword,
    resetPassword,
)
from fastapi_auth.tokens.jwt import jwtHandler
from fastapi_auth.tokens.refresh import RefreshManager
from fastapi_auth.middleware.auth import require_auth
from fastapi_auth.middleware.ratelimit import RateLimiter
from fastapi_auth.validators.credentials import validate_creds_structure

# Clean API Aliases
Security = {
    "hash": hash_password,
    "verify": verifyPassword,
    "reset": resetPassword,
}

# Standardized Naming Aliases
TokenHandler = jwtHandler
SessionManager = RefreshManager

__version__ = "1.0.0"
__all__ = [
    "hash_password",
    "verifyPassword",
    "resetPassword",
    "jwtHandler",
    "RefreshManager",
    "RateLimiter",
    "require_auth",
    "validate_creds_structure",
    "Security",
    "TokenHandler",
    "SessionManager",
]
