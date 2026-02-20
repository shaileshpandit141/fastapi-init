from pydantic import EmailStr
from sqlmodel import SQLModel

# =============================================================================
# Jwt Token Schemas.
# =============================================================================


class JwtTokenRead(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str


class JwtTokenCreate(SQLModel):
    email: EmailStr
    password: str


class JwtTokenRefresh(SQLModel):
    refresh_token: str


class JwtTokenRevoked(SQLModel):
    access_token: str
    refresh_token: str
