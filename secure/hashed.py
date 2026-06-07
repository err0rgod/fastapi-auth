from argon2 import PasswordHasher
from model.models import userdata
from validations.structure import validate_creds_structure 

ph = PasswordHasher()

@validate_creds_structure
async def hash_password(User : userdata):
    hash = ph.hash(User.password)
    User.password =  hash
    return User
