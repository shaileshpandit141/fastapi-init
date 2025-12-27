from fastapi import APIRouter, HTTPException, status
from models.user import User
from schemas.user import UserRead, UserCreate
from dependencies.session import SessionDep
from sqlmodel import select
from core.security.auth import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)
from core.security.password import password_hash, password_verify
from schemas.auth import TokenRead
from dependencies.oauth2 import OAuth2PasswordFormDep


router = APIRouter(prefix="/auth", tags=["auth"])


# --- Handle user sign up action ---


@router.post("/signup", response_model=UserRead)
async def create_user(payload: UserCreate, session: SessionDep) -> User:
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
        password_hash=password_hash(payload.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


# --- Handle access token ---


@router.post("/token")
async def get_access_token(
    form_payload: OAuth2PasswordFormDep,
    session: SessionDep,
) -> TokenRead:
    user = await session.exec(
        select(User).where(User.email == form_payload.username),
    )
    user = user.first()
    if not user or not password_verify(
        form_payload.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
    )

    return TokenRead(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


# --- Handle refresh token ---


@router.post("/refresh")
async def get_refresh_token(
    refresh_token: str,
    session: SessionDep,
) -> TokenRead:
    # Verify token signature
    uuid = verify_refresh_token(token=refresh_token)

    # Check token against DB / blacklist here (for rotation / logout).
    access_token = create_access_token(
        data={"sub": str(uuid)},
    )

    return TokenRead(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )
