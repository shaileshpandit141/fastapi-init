from sqlmodel import SQLModel


class TokenRead(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenRefresh(SQLModel):
    refresh_token: str


class TokenRevoked(SQLModel):
    access_token: str
    refresh_token: str
