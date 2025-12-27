from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from models.user import User, UserRead, UserCreate
from db.session import AsyncSession, get_session
from sqlmodel import select
from config.security import create_access_token, password_hash, password_verify
from fastapi.security import OAuth2PasswordRequestForm
from config.settings import settings
from models.auth import TokenRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserRead)
async def create_user(
    payload: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    # Check if user exists
    existing = await session.exec(
        select(User).where(User.email == payload.email),
    )
    if existing.first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Handle New User Creation
    new_user = User(
        **payload.model_dump(exclude={"password"}),
        password_hash=password_hash(payload.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.post("/token")
async def get_access_token(
    form_payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
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

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes,
    )
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return TokenRead(
        access_token=access_token,
        token_type="bearer",
    )
