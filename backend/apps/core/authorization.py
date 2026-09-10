"""Central permission normalization and authorization helpers."""

PERMISSION_ALIASES = {
    "thesis.view": "theses.view",
    "thesis.register": "theses.create",
    "thesis.freeze": "theses.update",
    "thesis.unfreeze": "theses.update",
    "committee.create": "committees.create",
}

LEGACY_ROLE_PERMISSIONS = {
    "PROGRAM_DIRECTOR": {
        "students.view",
        "students.create",
        "students.update",
        "students.manage",
        "theses.view",
        "theses.create",
        "theses.update",
        "theses.manage",
        "committees.view",
        "committees.create",
        "committees.update",
        "committees.manage",
        "reports.view",
        "reports.export",
        "registration.approve",
        "committee.approve",
    },
    "POSTGRADUATE_DIRECTOR": {
        "students.view",
        "students.manage",
        "theses.view",
        "theses.manage",
        "committees.view",
        "committees.manage",
        "reports.view",
        "reports.export",
        "registration.approve",
        "committee.approve",
    },
    "VICE_DEAN_POSTGRADUATE": {
        "students.view",
        "theses.view",
        "committees.view",
        "reports.view",
        "registration.approve",
        "committee.approve",
    },
    "VICE_DEAN": {"students.view", "theses.view", "committees.view", "reports.view"},
    "DEAN": {"students.view", "theses.view", "committees.view", "reports.view"},
    "VP_POSTGRADUATE_RESEARCH": {
        "students.view",
        "theses.view",
        "committees.view",
        "reports.view",
        "reports.export",
    },
    "STAFF": {
        "students.view",
        "students.create",
        "students.update",
        "students.manage",
        "theses.view",
        "committees.view",
        "committees.manage",
    },
    "REVIEWER": {
        "students.view",
        "theses.view",
        "committees.view",
        "registration.review",
    },
    "SUPERVISOR": {"students.view", "theses.view", "committees.view"},
    "STUDENT": set(),
}


def canonical_permission(code):
    return PERMISSION_ALIASES.get(code, code)


def effective_roles(user):
    dynamic = set(user.roles.filter(is_active=True).values_list("name", flat=True))
    if dynamic:
        return dynamic
    return {user.role} if getattr(user, "role", None) else set()


def effective_permissions(user):
    if user.is_superuser:
        return {"*"}

    dynamic_roles = user.roles.filter(is_active=True)
    if dynamic_roles.exists():
        codes = dynamic_roles.filter(permissions__is_active=True).values_list(
            "permissions__code", flat=True
        )
        return {canonical_permission(code) for code in codes if code}

    permissions = set()
    for role in effective_roles(user):
        permissions.update(LEGACY_ROLE_PERMISSIONS.get(role, set()))
    return {canonical_permission(code) for code in permissions}


def has_permission(user, code):
    permissions = effective_permissions(user)
    return "*" in permissions or canonical_permission(code) in permissions
