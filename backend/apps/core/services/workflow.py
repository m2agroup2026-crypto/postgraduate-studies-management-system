from django.db import transaction

from apps.core.models import ApprovalAction
from apps.core.workflow.policy_checker import can_perform_action
from apps.core.workflow.rules import WORKFLOW_TRANSITIONS


def get_next_status(current_status, action):
    transitions = WORKFLOW_TRANSITIONS.get(current_status, {})
    return transitions.get(action)


def get_user_roles(user):
    """Prefer active database roles; use the legacy enum only as a migration fallback."""
    if hasattr(user, "roles"):
        dynamic_roles = list(
            user.roles.filter(is_active=True).values_list("name", flat=True)
        )
        if dynamic_roles:
            return dynamic_roles

    if getattr(user, "role", None):
        return [user.role]

    return []


@transaction.atomic
def transition(obj, action, user, notes=""):
    locked_obj = obj.__class__.objects.select_for_update().get(pk=obj.pk)
    current_status = locked_obj.status
    request_type = locked_obj.__class__.__name__.upper()

    if not can_perform_action(
        get_user_roles(user),
        request_type,
        action,
        current_status=current_status,
    ):
        raise PermissionError(
            f"User is not allowed to perform {action} on {request_type}"
        )

    next_status = get_next_status(current_status, action)
    if not next_status:
        raise ValueError(f"Invalid transition: {current_status} -> {action}")

    locked_obj.status = next_status
    locked_obj.save(update_fields=["status"])

    ApprovalAction.objects.create(
        request_type=locked_obj.__class__.__name__,
        object_id=locked_obj.id,
        action=action,
        from_status=current_status,
        to_status=next_status,
        performed_by=user,
        notes=notes,
    )

    return locked_obj
