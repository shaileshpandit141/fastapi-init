from typing import cast
from uuid import UUID

from click import command, echo
from sqlmodel import select

from app.adapters.db.models.permission import Permission
from app.adapters.db.models.role import Role
from app.adapters.db.models.role_permission import RolePermission
from app.adapters.db.session import SyncSessionLocal
from app.shared.enums.permission import PermissionEnum
from app.shared.enums.role import RoleEnum

# =============================================================================
# Role Permission Map For Seeding Data to DB.
# =============================================================================

ROLE_PERMISSION_MAP: dict[RoleEnum, list[PermissionEnum]] = {
    RoleEnum.ADMIN: [
        PermissionEnum.USER_CREATE,
        PermissionEnum.USER_UPDATE,
        PermissionEnum.USER_DELETE,
    ],
    RoleEnum.USER: [
        PermissionEnum.USER_UPDATE,
    ],
}


# =============================================================================
# Sync role-permission seeder command.
# =============================================================================


@command(name="sync-role-permission")
def sync_role_permission_command() -> None:
    """Sync role-permission relationships based on the predefined ROLE_PERMISSION_MAP."""

    with SyncSessionLocal() as session:
        try:
            roles = session.exec(select(Role)).all()
            role_by_enum: dict[str, Role] = {role.name: role for role in roles}

            # Load all permissions
            permissions = session.exec(select(Permission)).all()

            # Map PermissionEnum -> Permission
            permission_by_enum: dict[PermissionEnum, Permission] = {
                perm.code: perm for perm in permissions
            }

            # Load ALL existing role-permission rows
            role_permissions = session.exec(select(RolePermission)).all()

            # Map role_id -> set(permission_id)
            existing_map: dict[UUID, set[str]] = {}

            for rp in role_permissions:
                existing_map.setdefault(rp.role_id, set()).add(rp.permission_id)  # type: ignore

            # Sync per role
            for role_enum, expected_permissions in ROLE_PERMISSION_MAP.items():

                role = role_by_enum.get(role_enum.value)
                if not role:
                    continue  # role missing, skip safely

                expected_permission_ids: set[UUID] = {
                    permission_by_enum[perm_enum].id
                    for perm_enum in expected_permissions
                    if perm_enum in permission_by_enum
                }

                current_permission_ids: set[UUID] = cast(
                    set[UUID], existing_map.get(role.id, set())
                )

                # Add Missing
                to_add = expected_permission_ids - current_permission_ids

                for permission_id in to_add:
                    session.add(
                        RolePermission(
                            role_id=role.id,
                            permission_id=permission_id,
                        )
                    )

                # Remove Stale
                to_remove = current_permission_ids - expected_permission_ids

                if to_remove:
                    for rp in role_permissions:
                        if rp.role_id == role.id and rp.permission_id in to_remove:
                            session.delete(rp)

            # Remove Orphaned Rows (Safety Cleanup)
            valid_role_ids = {role.id for role in roles}
            valid_permission_ids = {perm.id for perm in permissions}

            for rp in role_permissions:
                if (
                    rp.role_id not in valid_role_ids
                    or rp.permission_id not in valid_permission_ids
                ):
                    session.delete(rp)
        except Exception as exc:
            session.rollback()
            echo("Sync role-permission seeding failed: " + str(exc))
        else:
            session.commit()
            echo("Sync role-permission seeded successfully.")
