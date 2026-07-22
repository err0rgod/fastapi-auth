"""
Module for handling JSON Web Token (JWT) generation and verification.
Provides functionality for creating access tokens and refresh session objects.
"""

from typing import Optional
import jwt
from datetime import datetime, timedelta, timezone
import uuid
import logging
import secrets

logger = logging.getLogger(__name__)


class jwtHandler:
    """
    Handles JWT operations including creation and verification.

    Attributes:
        SECRET_KEY (str): The secret key used for signing and verifying tokens.
        algorithm (str): The algorithm used for JWT encoding/decoding (default: "RS256").
    """

    def __init__(self, SECRET_KEY: str, algorithm: Optional[str] = "HS256") -> None:
        """
        Initializes the jwtHandler with security credentials.

        Args:
            SECRET_KEY (str): Secret key for JWT.
            algorithm (str, optional): JWT signing algorithm. Defaults to "RS256".
        """
        self.SECRET_KEY = SECRET_KEY
        self.algorithm = algorithm

    def createJwt(
        self,
        sub: str,
        jwt_mins: Optional[int] = 15,
        refresh_days: Optional[int] = 7,
        *args,
        **kwargs,
    ) -> dict:
        """
        Generates access and refresh tokens.

        Args:
            sub (str): Unique identifier for the user.
            jwt_mins (int, optional): Access token validity in minutes.
            refresh_days (int, optional): Refresh token validity in days.

        Returns:
            dict: Contains 'access_token' and 'refresh_token' and 'refresh_day'.
        """
        # Using UTC for global consistency
        now = datetime.now(timezone.utc)

        # JWT Payload structure
        exp = timedelta(minutes=jwt_mins)
        jti = str(uuid.uuid4())
        data = {
            "sub": sub,
            "jti": jti,
            "iat": now,
            "exp": now + exp,
        }

        # Encode Access Token
        access_token = jwt.encode(data, self.SECRET_KEY, algorithm=self.algorithm)

        # Generate Refresh Token
        raw_refresh_token = secrets.token_urlsafe(64)

        return {
            "access_token": access_token,
            "refresh_token": raw_refresh_token,
            "refresh_days": refresh_days
        }

    def verifyJwt(self, token: str) -> dict:
        """
        Verifies and decodes a JWT access token.

        Args:
            token (str): The encoded JWT token string.

        Returns:
            dict: The decoded token payload.

        Raises:
            ValueError: If the token has expired or is invalid.
        """
        try:
            decoded = jwt.decode(token, self.SECRET_KEY, algorithms=[self.algorithm])
            return decoded
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            raise ValueError("Token has Expired")
        except jwt.InvalidTokenError:
            logger.warning("Invalid Token")
            raise ValueError("Invalid Token")
