# from jwt_handler import jwtHandler
from sqlmodel import Session , select
from model.models import jwt_blacklist
from datetime import datetime , timedelta
from functools import wraps

class handleJwtBlacklist:
    def __init__(self, session : Session) -> None:
        self.session = session

    def debarJwt(self,jti : str, user_name : str, expired_at: datetime):
        blacklist = jwt_blacklist(
            jti = jti,
            user_name=user_name,
            expired_at=expired_at
        )

        self.session.add(blacklist)
        self.session.commit()

    def is_token_blacklisted(self, jti : str):
        statement = select(jwt_blacklist).where(jwt_blacklist.jti == jti)
        result = self.session.exec(statement).first()
        return result is not None