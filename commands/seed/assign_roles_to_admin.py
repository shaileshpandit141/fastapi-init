from typing import cast

from click import command, echo
from sqlmodel import select

from core.db.sessions import session
from domain.permission.models import Permission
from domain.role.constants import RoleType
from domain.role.models import Role, RolePermission

# ===== Assign admin permissions ======


@command()
def assign_roles_to_admin() -> None:
    """Grant all permissions to the admin role."""

    with session() as db:
        try:
            admin = db.exec(
                select(Role).where(Role.name == RoleType.ADMIN.value)
            ).one_or_none()

            if not admin:
                echo("Admin role not found. Seed roles first.")
                return

            permissions = db.exec(select(Permission)).all()

            existing_links = {
                (rp.role_id, rp.permission_id)
                for rp in db.exec(select(RolePermission)).all()
            }

            links: list[RolePermission] = []

            for perm in permissions:
                key = (
                    cast(int, admin.id),
                    cast(int, perm.id),
                )
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

            echo("Admin permissions assigned successfully.")

        except Exception as exc:
            db.rollback()
            echo(f"Admin role assignment failed: {exc}")
            raise
