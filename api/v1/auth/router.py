from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from core.security.jwt.create import create_access_token
from core.security.jwt.exceptions import JWTError
from core.security.jwt.revocation import revoke_token
from core.security.jwt.verify import verify_refresh_token
from core.security.password import hash_password, verify_password
from dependencies.oauth2 import OAuth2PasswordFormDep
from dependencies.redis import RedisDep
from dependencies.session import SessionDep
from models.user import User
from schemas.auth import RevokedTokenRequest, TokenResponse
from schemas.message import MessageResponse
from schemas.user import UserCreateRequest, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


# --- Handle user sign up action ---


@router.post("/signup", response_model=UserResponse)
async def create_user(payload: UserCreateRequest, session: SessionDep) -> User:
    # Check if user exists
    existing = await session.exec(
        select(User).where(User.email == payload.email),
    )
    if existing.first():
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    # Handle New User Creation
    new_user = User(
        **payload.model_dump(exclude={"password"}),
        password_hash=hash_password(payload.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


# --- Handle access token ---


@router.post("/token")
async def get_access_token(
    form_payload: OAuth2PasswordFormDep, session: SessionDep
) -> TokenResponse:
    user = await session.exec(
        select(User).where(User.email == form_payload.username),
    )
    user = user.first()
    if not user or not verify_password(form_payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return TokenResponse(
        access_token=create_access_token({"id": user.id}),
        refresh_token=create_access_token({"id": user.id}),
        token_type="bearer",
    )


# --- Handle refresh token ---


@router.post("/refresh")
async def refresh_access_token(refresh_token: str, redis: RedisDep) -> TokenResponse:
    try:
        claims = await verify_refresh_token(redis=redis, token=refresh_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expire refresh token")

    return TokenResponse(
        access_token=create_access_token({"id": claims["id"]}),
        refresh_token=refresh_token,
        token_type="bearer",
    )


# --- Handle refresh token revoke ---


@router.post("/signout")
async def signout(payload: RevokedTokenRequest, redis: RedisDep) -> MessageResponse:
    try:
        claims = await verify_refresh_token(redis=redis, token=payload.refresh_token)
    except JWTError:
        raise HTTPException(status_code=200, detail="Sign out successfull")

    await revoke_token(redis=redis, jti=claims["jti"], exp=claims["exp"])

    return MessageResponse(detail="Sign out successfull")
