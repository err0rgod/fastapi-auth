from datetime import datetime, timezone
from model.models import refreshSession, userdata
from sqlmodel import select, Session
import hashlib


class RefreshManager:
    def __init__(self, db_session : Session) -> None:
        self.session = db_session

    def validate_and_rotate(self, raw_refresh_token : str):
        now = datetime.now(timezone.utc)

        token_hash = hashlib.sha256(raw_refresh_token.encode().hexdigest())

        statement= select(refreshSession).where(refreshSession.token_hash == token_hash)
        db_token = self.session.exec(statement).first()

        if not db_token:
            raise ValueError("Inavlid refresh token.")
        if db_token.revoked:
            raise ValueError("DB token has been revoked. possible theft.")
        if now > db_token.expires_at:
            raise ValueError("The token has been expired.")
        db_token.revoked = True
        self.session.add(db_token)

        self.session.commit()
        return db_token.user_id         