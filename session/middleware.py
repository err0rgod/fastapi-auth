from functools import wraps
from session.jwt_handler import jwtHandler
from session.blacklist import handleJwtBlacklist
from sqlmodel import Session
import logging

logger = logging.getLogger(__name__)

def require_auth(jwt_handler : jwtHandler , blacklist_manager : handleJwtBlacklist = None):
    def decorator(func):
        @wraps(func)
        def wrapper(token : str, *args , **kwargs):
            logger.info("Initiated authenctication check")
            if not token:
                logger.warning("Authentication token missing")
                raise ValueError("Authenticatioin token is missing")
            # verify and decode jwt
            payload = jwt_handler.verifyJwt(token)

            # check db for blacklist
            if blacklist_manager and blacklist_manager.is_token_blacklisted(payload.get("jti")):
                logger.warning("Token was revoked.")
                raise ValueError("Token has been revoked")
            
            return func(payload, *args , **kwargs)
        return wrapper
    return decorator