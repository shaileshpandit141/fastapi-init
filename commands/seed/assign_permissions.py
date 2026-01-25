from typing import Sequence, cast

from click import command, echo
from sqlmodel import Session, select

from core.db.sessions import session
from domain.permission.models import Permission
from domain.role.constants import RoleType
from domain.role.models import Role, RolePermission


def _assign_permissions(
    db: Session,
    role_id: int,
    permissions: Sequence[Permission],
) -> None:
    """Shared helper to attach permissions to a role safely."""

    existing_links = {
        (
            rp.role_id,
            rp.permission_id,
        )
        for rp in db.exec(select(RolePermission)).all()
    }

    links: list[RolePermission] = []

    for perm in permissions:
        key = (role_id, cast(int, perm.id))
        if key not in existing_links:
            links.append(
                RolePermission(
                    role_id=key[0],
                    permission_id=key[1],
                )
            )

    if links:
        db.add_all(links)
        db.commit()


def assign_to_superuser(db: Session, role_id: int) -> None:
    """Superuser gets EVERYTHING"""
    permissions = db.exec(
        select(Permission).where(
            Permission.code.endswith(":*"),
        )
    ).all()
    _assign_permissions(db, role_id, permissions)
    echo("Superuser permissions assigned.")


def assign_to_admin(db: Session, role_id: int) -> None:
    """Admin gets unrestricted (wildcard) permissions"""
    pass


def assign_to_user(db: Session, role_id: int) -> None:
    """User gets ONLY restricted permissions"""
    pass


@command()
def assign_permissions() -> None:
    with session() as db:
        try:
            roles = db.exec(select(Role.id, Role.name)).all()

            for role_id, name in roles:
                role_id = cast(int, role_id)

                if name == RoleType.SUPERUSER.value:
                    assign_to_superuser(db, role_id)

                elif name == RoleType.ADMIN.value:
                    assign_to_admin(db, role_id)

                elif name == RoleType.USER.value:
                    assign_to_user(db, role_id)

            echo("Role permissions assignment completed.")
        except Exception as exc:
            db.rollback()
            echo(f"Role permission assignment failed: {exc}", err=True)
            raise
