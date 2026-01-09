from typing import Self

from pydantic import model_validator
from sqlmodel import SQLModel


class NonEmptyUpdateModel(SQLModel):
    @model_validator(mode="after")
    def check_not_empty(self) -> Self:
        if not any(self.model_dump(exclude_unset=True).values()):
            raise ValueError("At least one field must be provided")
        return self
