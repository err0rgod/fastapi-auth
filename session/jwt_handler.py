import jwt
from model.models import userdata , refreshSession
from datetime import datetime , timedelta , timezone
import uuid
import logging
import secrets


logger = logging.getLogger(__name__)
class jwtHandler:

    def __init__(self, SECRET_KEY: str, algorithm : str | None = "RS256") -> None:
        self.SECRET_KEY = SECRET_KEY
        self.algorithm = algorithm

    def createJwt(self,User : userdata, jwt_mins : int| None = 15,refresh_days : int |None = 7, *args , **kwargs) -> str:
        # for using the UTC globally
        now = datetime.now(timezone.utc)
        # jwt structure
        exp = timedelta(minutes=jwt_mins)
        jti = str(uuid.uuid4())
        data = {
            "sub": User.user_id,
            "jti" : jti,
            "user_name" : User.user_name,
            "iat" : now,
            "exp" : now + exp
        }
        refresh_token = secrets.token_urlsafe(64)

        encoded = jwt.encode(data,self.SECRET_KEY, algorithms=[self.algorithm])
        return [encoded,refreshSession]
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