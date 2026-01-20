from typing import TypedDict

from pydantic import BaseModel

# === Detail response schema ===


class DetailResponse(BaseModel):
    detail: str


# === Error response schemas ===


class ErrorDetailDict(TypedDict):
    loc: list[str | int]
    msg: str
    type: str


class ErrorDetail(BaseModel):
    loc: list[str | int]
    msg: str
    type: str


class ErrorResponse(BaseModel):
    detail: list[ErrorDetail]
