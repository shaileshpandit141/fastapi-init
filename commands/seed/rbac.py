from typing import cast

from click import command, echo

from db.connections import sessions
from models.permission import Permission
from models.role import Role
from models.role_permission_link import RolePermissionLink

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
    with sessions.SyncSessionLocal() as session:
        try:
            # Add roles
            for role in INITIAL_ROLES:
                session.add(role)
            session.commit()

            # Refresh roles to get their IDs
            for role in INITIAL_ROLES:
                session.refresh(role)

            # Add permissions
            for perm in INITIAL_PERMISSIONS:
                session.add(perm)
            session.commit()

            # Refresh permissions to get their IDs
            for perm in INITIAL_PERMISSIONS:
                session.refresh(perm)

            # Link roles to permissions (example: admin gets all permissions)
            links: list[RolePermissionLink] = []
            for role in INITIAL_ROLES:
                if role.name == "admin":
                    for perm in INITIAL_PERMISSIONS:
                        links.append(
                            RolePermissionLink(
                                role_id=cast(int, role.id),
                                permission_id=cast(int, perm.id),
                            )
                        )

                elif role.name == "user":  # Example: user only gets read permission
                    read_perm = next(
                        p for p in INITIAL_PERMISSIONS if p.code == "user:read"
                    )
                    links.append(
                        RolePermissionLink(
                            role_id=cast(int, role.id),
                            permission_id=cast(int, read_perm.id),
                        )
                    )

            session.add_all(links)
            session.commit()

            echo("Roles and permissions seeded successfully.")

        except Exception as err:
            session.rollback()
            echo(f"RBAC seeding failed: {err}")
