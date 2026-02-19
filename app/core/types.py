from typing import TypedDict

# =============================================================================
# Error Response Dict.
# =============================================================================


class ErrorDetailDict(TypedDict):
    loc: list[str | int]
    msg: str
    type: str
