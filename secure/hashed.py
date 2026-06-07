from argon2 import PasswordHasher
from model.models import userdata
from validations.structure import validate_creds_structure 

ph = PasswordHasher()

@validate_creds_structure
def hash_password(User : userdata):
    hash = ph.hash(User.password)
    User.password =  hash
    return User


def verifyPassword(User : userdata , hash : str):
    try:
        return ph.verify(hash , User.password)
    except:
        return False
    