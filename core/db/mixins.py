import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, func, text
from sqlmodel import Field, SQLModel  # type: ignore
from uuid6 import uuid7

from core.utils.time import time


class IntIDMixin(SQLModel, table=False):
    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={
            "autoincrement": True,
        },
    )


class UUIDv7Mixin(SQLModel, table=False):
    id: uuid.UUID = Field(
        default_factory=uuid7,
        primary_key=True,
        sa_column_kwargs={
            "server_default": text("uuid_generate_v7()"),
        },
    )


class TimestampMixin(SQLModel, table=False):
    created_at: datetime = Field(
        default_factory=time.utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )
    updated_at: datetime = Field(
        default_factory=time.utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )
