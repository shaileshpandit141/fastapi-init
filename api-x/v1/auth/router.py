from collections.abc import Awaitable, Callable
from typing import Any, Mapping

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from core.security.jwt.create import create_access_token, create_refresh_token
from core.security.jwt.exceptions import JWTError
from core.security.jwt.revocation import revoke_token
from core.security.jwt.verify import verify_access_token, verify_refresh_token
from core.security.password import hash_password, verify_password
from dependencies.auth.oauth2 import OAuth2PasswordFormDep
from dependencies.cache.redis import RedisDep
from dependencies.connections.sessions import AsyncSessionDep
from models.user import User, UserStatus
from schemas.auth import RefreshTokenCreate, RevokedTokenCreate, TokenRead
from schemas.message import MessageRead
from schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


# --- Handle user sign up action ---


@router.post("/signup", response_model=UserRead)
async def create_user(payload: UserCreate, session: AsyncSessionDep) -> User:
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
    form_payload: OAuth2PasswordFormDep, session: AsyncSessionDep
) -> TokenRead:
    user = await session.exec(
        select(User).where(User.email == form_payload.username),
    )
    user = user.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    if user.status == UserStatus.INACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is inactive",
        )

    if not verify_password(form_payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return TokenRead(
        access_token=create_access_token({"id": user.id}),
        refresh_token=create_refresh_token({"id": user.id}),
        token_type="bearer",
    )


# --- Handle refresh token ---


@router.post("/refresh")
async def refresh_access_token(
    payload: RefreshTokenCreate, redis: RedisDep
) -> TokenRead:
    try:
        claims = await verify_refresh_token(redis=redis, token=payload.refresh_token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expire refresh token",
        )

    return TokenRead(
        access_token=create_access_token({"id": claims["id"]}),
        refresh_token=payload.refresh_token,
        token_type="bearer",
    )


# --- Handle refresh token revoke ---


VerifyFn = Callable[..., Awaitable[Mapping[str, Any]]]


@router.post("/signout")
async def signout(payload: RevokedTokenCreate, redis: RedisDep) -> MessageRead:

    async def _revoke_if_valid(verify_fn: VerifyFn, token: str) -> None:
        try:
            claims = await verify_fn(redis=redis, token=token)
            await revoke_token(redis=redis, jti=claims["jti"], exp=claims["exp"])
        except JWTError:
            pass

    await _revoke_if_valid(verify_access_token, payload.access_token)
    await _revoke_if_valid(verify_refresh_token, payload.refresh_token)

    return MessageRead(detail="Sign out successful")
