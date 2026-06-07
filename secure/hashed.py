from argon2 import PasswordHasher
from model.models import userdata
from validations.structure import validate_creds_structure 
from datetime import datetime , timedelta , timezone


ph = PasswordHasher()

@validate_creds_structure
def hash_password(User : userdata):
    hash = ph.hash(User.password)
    User.password =  hash
    return User


def verifyPassword(User : userdata , hash : str):
    now = datetime.now(timezone.utc)
    if User.locked_untill and now < User.locked_untill:
        raise  ValueError("Account Locked Try again Later.")
    try:
        valid =  ph.verify(hash, User.password)
        if valid:
            User.failed_attempts = 0
            User.locked_untill = None
            return True
    except Exception:
        User.failed_attempts+=1
        if User.failed_attempts >= 5:
            User.locked_untill = now + timedelta(minutes=15)
        return False
    