from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from sqlmodel import SQLModel

# === OAuth2 Schemas ===


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
    description="Use email as the username field",
)


# === Jwt Schemas ===


class TokenRead(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str


class JwtTokenCreate(SQLModel):
    email: EmailStr
    password: str


class TokenRefresh(SQLModel):
    refresh_token: str


class TokenRevoked(SQLModel):
    access_token: str
    refresh_token: str
