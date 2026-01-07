from pydantic import BaseModel


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None


class RoleRequest(BaseModel):
    name: str
    description: str | None = None
