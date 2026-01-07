from typing import Sequence

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from dependencies.authorization.roles import AdminUserDep
from dependencies.connections.session import SessionDep
from models.user import Permission, Role
from schemas.rbac import RoleRequest, RoleResponse

router = APIRouter(prefix="/rbac", tags=["rbac"])


@router.get("/roles", response_model=list[RoleResponse])
async def list_roles(admin: AdminUserDep, session: SessionDep) -> Sequence[Role]:
    result = await session.exec(select(Role))
    return result.all()


@router.post("/roles", response_model=Role, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_in: RoleRequest, admin: AdminUserDep, session: SessionDep
) -> Role:
    role = Role.model_validate(role_in)
    session.add(role)

    try:
        await session.commit()
        await session.refresh(role)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exists"
        )

    return role


@router.get("/permissions", response_model=list[Permission])
async def list_permissions(
    admin: AdminUserDep, session: SessionDep
) -> Sequence[Permission]:
    result = await session.exec(select(Permission))
    return result.all()
