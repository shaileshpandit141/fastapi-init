from typing import Sequence

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from dependencies.authorization.roles import AdminUserDep
from dependencies.connections.session import SessionDep
from models.permission import Permission
from models.role import Role
from models.role_permission_link import RolePermissionLink
from schemas.message import MessageRead
from schemas.rbac import PermissionCreate, RoleCreate, RoleRead
from schemas.user import RolePermissionCreate

router = APIRouter(prefix="/rbac", tags=["rbac"])


@router.get("/roles", response_model=list[RoleRead])
async def list_roles(admin: AdminUserDep, session: SessionDep) -> Sequence[Role]:
    result = await session.exec(select(Role))
    return result.all()


@router.post("/roles", response_model=Role, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_in: RoleCreate, admin: AdminUserDep, session: SessionDep
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


@router.post(
    "/permissions", response_model=Permission, status_code=status.HTTP_201_CREATED
)
async def create_permission(
    perm_in: PermissionCreate, admin: AdminUserDep, session: SessionDep
) -> Permission:
    permission = Permission.model_validate(perm_in)
    session.add(permission)

    try:
        await session.commit()
        await session.refresh(permission)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Permission already exists"
        )

    return permission


@router.post(
    "/roles/permissions",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
)
async def set_role_permission(
    body: RolePermissionCreate, admin: AdminUserDep, session: SessionDep
) -> MessageRead:
    role = await session.get(Role, body.role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    permission = await session.get(Permission, body.permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    try:
        role_perm = RolePermissionLink(
            role_id=body.role_id,
            permission_id=body.permission_id,
        )
        session.add(role_perm)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Permission already assigned to role",
        )

    return MessageRead(
        detail="Permission assigned to role",
    )
