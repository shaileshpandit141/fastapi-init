from pydantic import BaseModel

# =============================================================================
# Detail Response Schema.
# =============================================================================


class DetailResponse(BaseModel):
    detail: str


# =============================================================================
# Error Response Schema.
# =============================================================================


class ErrorDetail(BaseModel):
    loc: list[str | int]
    msg: str
    type: str


class ErrorResponse(BaseModel):
    detail: list[ErrorDetail]
