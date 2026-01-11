import uuid
from datetime import datetime, timezone
from typing import Self

from pydantic import model_validator
from sqlalchemy import Column, DateTime, func, text
from sqlmodel import Field, SQLModel  # type: ignore
from uuid6 import uuid7


class BaseIntIDModel(SQLModel):
    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"autoincrement": True},
    )


class BaseUUIDModel(SQLModel):
    id: uuid.UUID = Field(
        default_factory=uuid7,
        primary_key=True,
        sa_column_kwargs={"server_default": text("uuid_generate_v7()")},
    )


class BaseTimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
    )


class NonEmptyUpdateModel(SQLModel):
    @model_validator(mode="after")
    def check_not_empty(self) -> Self:
        if not any(self.model_dump(exclude_unset=True).values()):
            raise ValueError("At least one field must be provided")
        return self
