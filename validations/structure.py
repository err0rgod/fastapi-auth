from model.models import userdata , changedata
from functools import wraps



# validate the user input in signup form
def validate_creds_structure(func):
    @wraps(func)
    async def wrapper(User : userdata, *args , **kwargs):
        if User.userName == "" or User.password == "":
            return "Username and password are required"
        if len(User.userName) < 3 or len(User.userName) > 15:
            return "Username must be between 3 and 15 characters"
        for char in User.userName:
            if not char.isalnum():
                return "Username must be alphanumeric no special characters allowed"
        if len(User.password) < 8:
            return "Password must be at least 8 characters long"
        elif not any(char.isupper() for char in User.password):
            return "Password must contain at least one uppercase letter"
        elif not any(char.islower() for char in User.password):
            return "Password must contain at least one lowercase letter"    
        elif not any(char.isdigit() for char in User.password):
            return "Password must contain at least one digit"
        elif not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in User.password):
            return "Password must contain at least one special character"  
        return await func(User,*args , **kwargs)
    return wrapper