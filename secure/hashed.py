from argon2 import PasswordHasher
from model.models import userdata
from validations.structure import validate_creds_structure 
from datetime import datetime , timedelta , timezone
import logging

ph = PasswordHasher()
logger = logging.getLogger(__name__)

@validate_creds_structure
def hash_password(User : userdata):
    logger.info(f"Password Hashed of {User.user_id}")
    hash = ph.hash(User.password)
    User.password =  hash
    return User


def verifyPassword(User : userdata , hash : str):
    now = datetime.now(timezone.utc)
    if User.locked_untill and now < User.locked_untill:
        logger.warning(f"accout locked of user {User.user_id}")
        raise  ValueError("Account Locked Try again Later.")
    try:
        valid =  ph.verify(hash, User.password)
        if valid:
            logger.info("JWT token verified")
            User.failed_attempts = 0
            User.locked_untill = None
            return True
    except Exception:
        logger.warning(f"Invalid hash by {User.user_id} bruteforce protection initiated")
        User.failed_attempts+=1
        if User.failed_attempts >= 5:
            User.locked_untill = now + timedelta(minutes=15)
        return False
    