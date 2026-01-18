from typing import cast

from click import command, echo

from core.db.sessions.session import session
from domain.rbac.models.permission import Permission
from domain.rbac.models.role import Role
from domain.rbac.models.role_permission import RolePermission

INITIAL_ROLES: list[Role] = [
    Role(name="admin", description="Administrator with full access."),
    Role(name="user", description="Regular user with limited access."),
]


INITIAL_PERMISSIONS: list[Permission] = [
    Permission(code="user:read", description="Permission to read user information."),
    Permission(code="user:create", description="Permission to create user."),
    Permission(
        code="user:update", description="Permission to modify user information."
    ),
    Permission(code="user:delete", description="Permission to delete user."),
]


@command()
def rbac() -> None:
    """Seed roles and permissions (SQLite dev, PostgreSQL prod)."""
    with session() as sessionx:
        try:
            # Add roles
            for role in INITIAL_ROLES:
                sessionx.add(role)
            sessionx.commit()

            # Refresh roles to get their IDs
            for role in INITIAL_ROLES:
                sessionx.refresh(role)

            # Add permissions
            for perm in INITIAL_PERMISSIONS:
                sessionx.add(perm)
            sessionx.commit()

            # Refresh permissions to get their IDs
            for perm in INITIAL_PERMISSIONS:
                sessionx.refresh(perm)

            # Link roles to permissions (example: admin gets all permissions)
            links: list[RolePermission] = []
            for role in INITIAL_ROLES:
                if role.name == "admin":
                    for perm in INITIAL_PERMISSIONS:
                        links.append(
                            RolePermission(
                                role_id=cast(int, role.id),
                                permission_id=cast(int, perm.id),
                            )
                        )

                elif role.name == "user":  # Example: user only gets read permission
                    read_perm = next(
                        p for p in INITIAL_PERMISSIONS if p.code == "user:read"
                    )
                    links.append(
                        RolePermission(
                            role_id=cast(int, role.id),
                            permission_id=cast(int, read_perm.id),
                        )
                    )

            sessionx.add_all(links)
            sessionx.commit()

            echo("Roles and permissions seeded successfully.")

        except Exception as err:
            sessionx.rollback()
            echo(f"RBAC seeding failed: {err}")
