from model.models import userdata , changedata
from functools import wraps



# validate the user input in signup form
def validate_creds_structure(func):
    @wraps(func)
    def wrapper(User : userdata, *args , **kwargs):
        if not User.user_name or not User.password:
            raise ValueError("Username and password are required")
        if len(User.user_name) < 3 or len(User.user_name) > 15:
            raise ValueError("Username must be between 3 and 15 characters")
        if not User.user_name.isalnum():
            raise ValueError("Username must be alphanumeric no special characters allowed")

        if len(User.password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in User.password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in User.password):
            raise ValueError("Password must contain at least one lowercase letter")    
        if not any(char.isdigit() for char in User.password):
            raise ValueError("Password must contain at least one digit")
        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in User.password):
            raise ValueError("Password must contain at least one special character")  

        return func(User, *args , **kwargs)
    return wrapper