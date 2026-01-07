from pydantic import BaseModel, Field


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None


class RoleRequest(BaseModel):
    name: str
    description: str | None = None


class PermissionRequest(BaseModel):
    code: str
    description: str | None = Field(default=None, max_length=255)
