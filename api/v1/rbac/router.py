from typing import Sequence

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from dependencies.roles import AdminUserDep
from dependencies.session import SessionDep
from models.user import Role
from schemas.role import RoleRequest, RoleResponse

router = APIRouter(prefix="/rbac", tags=["rbac"])


@router.get("/roles", response_model=list[RoleResponse])
async def list_roles(admin: AdminUserDep, session: SessionDep) -> Sequence[Role]:
    result = await session.exec(select(Role))
    return result.all()


@router.post("/roles", response_model=Role, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_in: RoleRequest, admin: AdminUserDep, session: SessionDep
) -> RoleRequest:
    existing = await session.exec(select(Role).where(Role.name == role_in.name))
    if existing.first():
        raise HTTPException(status_code=400, detail="Role already exists")

    session.add(role_in)

    await session.commit()
    await session.refresh(role_in)

    return role_in
