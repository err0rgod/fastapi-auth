import jwt
from model.models import userdata 
from datetime import datetime , timedelta , timezone
import uuid
import logging

logger = logging.getLogger(__name__)
class jwtHandler:

    def __init__(self, SECRET_KEY: str, algorithm : str | None = "RS256") -> None:
        self.SECRET_KEY = SECRET_KEY
        self.algorithm = algorithm

    def createJwt(self,User : userdata, mins : int| None = 1440, *args , **kwargs) -> str:
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

        encoded = jwt.encode(data,self.SECRET_KEY, algorithms=[self.algorithm])
        return encoded
    def verifyJwt(self , token : str):
        try:
            decoded = jwt.decode(token , self.SECRET_KEY, algorithms=[self.algorithm])
            return decoded
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            raise ValueError("Token has Expired")
        except jwt.InvalidTokenError:
            logger.warning("Invalid Token")
            raise ValueError("Invalid Token")