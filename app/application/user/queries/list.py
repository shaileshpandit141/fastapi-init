from dataclasses import dataclass


@dataclass(slots=True)
class ListUserQuery:
    limit: int
    offset: int
