from enum import StrEnum

# ===== Enums =====


class Action(StrEnum):
    CREATE = "create"
    LIST = "list"
    RETRIEVE = "retrieve"
    UPDATE = "update"
    DELETE = "delete"


class Access(StrEnum):
    PUBLIC = "public"
    AUTHENTICATED = "authenticated"


class ResponseSpec(StrEnum):
    PUBLIC_READ = "public_read"
    PUBLIC_WRITE = "public_write"
    AUTHENTICATED_READ = "authenticated_read"
    AUTHENTICATED_WRITE = "authenticated_write"
    AUTHENTICATED_DELETE = "authenticated_delete"


# ===== Template Maps =====


SUMMARY_MAP: dict[Action, str] = {
    Action.CREATE: "Create {resource}",
    Action.LIST: "List {resource}",
    Action.RETRIEVE: "Retrieve {resource}",
    Action.UPDATE: "Update {resource}",
    Action.DELETE: "Delete {resource}",
}

DESCRIPTION_MAP: dict[Action, str] = {
    Action.CREATE: "Create a new {name}.",
    Action.LIST: "List all {name} with pagination.",
    Action.RETRIEVE: "Retrieve a specific {name} by its ID.",
    Action.UPDATE: "Update a specific {name} by its ID.",
    Action.DELETE: "Delete a specific {name} by its ID.",
}

ACCESS_MAP: dict[Access, str] = {
    Access.PUBLIC: "Public endpoint.",
    Access.AUTHENTICATED: "Accessible by authenticated users only.",
}


RESPONSE_KEY_MAP: dict[tuple[Action, Access], ResponseSpec] = {
    # -------- PUBLIC --------
    (Action.LIST, Access.PUBLIC): ResponseSpec.PUBLIC_READ,
    (Action.RETRIEVE, Access.PUBLIC): ResponseSpec.PUBLIC_READ,
    (Action.CREATE, Access.PUBLIC): ResponseSpec.PUBLIC_WRITE,
    # -------- AUTH --------
    (Action.LIST, Access.AUTHENTICATED): ResponseSpec.AUTHENTICATED_READ,
    (Action.RETRIEVE, Access.AUTHENTICATED): ResponseSpec.AUTHENTICATED_READ,
    (Action.CREATE, Access.AUTHENTICATED): ResponseSpec.AUTHENTICATED_WRITE,
    (Action.UPDATE, Access.AUTHENTICATED): ResponseSpec.AUTHENTICATED_WRITE,
    (Action.DELETE, Access.AUTHENTICATED): ResponseSpec.AUTHENTICATED_DELETE,
}
