from apps.core.models import ApprovalAction
from apps.core.workflow.rules import WORKFLOW_TRANSITIONS
from apps.core.workflow.policy_checker import can_perform_action


def get_next_status(current_status, action):
    transitions = WORKFLOW_TRANSITIONS.get(current_status, {})
    return transitions.get(action)


def get_user_roles(user):
    roles = []

    if getattr(user, "role", None):
        roles.append(user.role)

    if hasattr(user, "roles"):
        roles.extend(
            user.roles.values_list("name", flat=True)
        )

    return roles


def transition(obj, action, user, notes=""):
    current_status = obj.status

    request_type = obj.__class__.__name__.upper()

    if not can_perform_action(
        get_user_roles(user),
        request_type,
        action
    ):
        raise PermissionError(
            f"User is not allowed to perform {action} on {request_type}"
        )

    next_status = get_next_status(
        current_status,
        action
    )

    if not next_status:
        raise ValueError(
            f"Invalid transition: {current_status} -> {action}"
        )

    obj.status = next_status
    obj.save(update_fields=["status"])

    ApprovalAction.objects.create(
        request_type=obj.__class__.__name__,
        object_id=obj.id,
        action=action,
        from_status=current_status,
        to_status=next_status,
        performed_by=user,
        notes=notes,
    )

    return obj
