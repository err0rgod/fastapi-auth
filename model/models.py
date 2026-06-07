from pydantic import BaseModel 
from sqlmodel import SQLModel , Field
from datetime import datetime
from typing import Optional

class userdata(SQLModel, table=True):
    user_id : str = Field( primary_key= True, nullable= False, unique=True)
    user_name : str = Field(unique= True, nullable= False)
    password : str = Field(nullable=False)
    failed_attempts : int = Field(default=0)
    locked_untill : Optional[datetime] = Field(default=None)

class jwt_blacklist(SQLModel, table=True):
    user_name : str = Field(nullable= False)
    jti : str = Field(primary_key=True, nullable=False)
    expired_at : datetime = Field(nullable=False)

class changedata(BaseModel):
    user_name : str 
    old_password : str
    new_password : str

class refreshSession(SQLModel, table = True):
    session_id : str = Field(primary_key=True, nullable=False)
    user_id : str = Field(nullable=False, foreign_key="userdata.user_id")
    token_hash : str =  Field(nullable=False)
    expires_at : datetime = Field(nullable=False)
    revoked : bool = Field(nullable=False, default=False)