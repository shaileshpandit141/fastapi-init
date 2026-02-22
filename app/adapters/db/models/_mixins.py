import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel
from uuid6 import uuid7

from app.shared.time import get_utc_now

# =============================================================================
# Int ID Model Mixin.
# =============================================================================


class IntIDMixin(SQLModel, table=False):
    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"autoincrement": True},
    )


# =============================================================================
# UUID V7 Model Mixin.
# =============================================================================


class UUIDv7Mixin(SQLModel, table=False):
    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)


# =============================================================================
# Timestamp Model Mixin.
# =============================================================================


class TimestampMixin(SQLModel, table=False):
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )

    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )
