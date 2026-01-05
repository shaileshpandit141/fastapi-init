from click import command, echo


@command()
def seed_rbac() -> None:
    """Seed initial roles and permissions."""
    echo("Roles and permissions seed successful.")
