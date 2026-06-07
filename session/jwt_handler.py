from jwt import encode
from functools import wraps
from model.models import userdata 
from datetime import datetime , timedelta , timezone
import uuid


class jwtHandler:

    def __init__(self, SECRET_KEY: str) -> None:
        self.SECRET_KEY = SECRET_KEY

    def wrappper(self,User : userdata, mins : int| None = 1440,  algorithm : str | None = "HS256",*args , **kwargs) -> str:
        # for using the UTC globally
        now = datetime.now(timezone.utc)
        # jwt structure
        exp = timedelta(minutes=mins)
        jti = str(uuid.uuid4())
        data = {
            "sub": User.user_id,
            "jti" : jti,
            "user_name" : User.user_name,
            "iat" : now,
            "exp" : now + exp
        }

        encoded = encode(data,self.SECRET_KEY, algorithm=algorithm)
        return encoded