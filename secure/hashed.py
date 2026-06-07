from argon2 import PasswordHasher
from model.models import userdata, refreshSession
from validations.structure import validate_creds_structure 
from datetime import datetime , timedelta , timezone
import logging
from sqlmodel import Session, select

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
    

def resetPassword(User : userdata,session : Session ,new_password : str, hash : str):
    is_valid = verifyPassword(User, hash)
    if not is_valid:
        raise ValueError("Invalid Credentials")
    else:
        hashed_new_password = ph.hash(new_password)
        statement = select(userdata).where(userdata.user_id == User.user_id)
        results = session.exec(statement).first()
        if results:
            results.password = hashed_new_password
            session.add(results)
            session.commit()
            token_statement = select(refreshSession).where((refreshSession.user_id == User.user_id) & (refreshSession.revoked == False))
            active_tokens = session.exec(token_statement).all()

            for token in active_tokens:
                token.revoked = True
                session.add(token)
            session.coomit()

            logger.info(f"Password changed and {len(active_tokens)} revoked for {User.user_id}")
            return True
        else:
            return False