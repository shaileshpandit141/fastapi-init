from pydantic import BaseModel
from sqlmodel import SQLModel


class TokenRead(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenCreate(SQLModel):
    refresh_token: str


class RevokedTokenCreate(BaseModel):
    access_token: str
    refresh_token: str
