import uuid
from datetime import datetime, timezone

from sqlalchemy import text
from sqlmodel import Field, SQLModel
from uuid6 import uuid7


class UUIDMixin(SQLModel):
    id: uuid.UUID = Field(
        default_factory=uuid7,
        primary_key=True,
        sa_column_kwargs={"server_default": text("uuid_generate_v7()")},
    )


class TimestampMixin:
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
