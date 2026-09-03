from apps.core.models import ApprovalAction
from apps.core.workflow.rules import WORKFLOW_TRANSITIONS


def get_next_status(current_status, action):
    transitions = WORKFLOW_TRANSITIONS.get(current_status, {})
    return transitions.get(action)


def transition(obj, action, user, notes=""):
    current_status = obj.status

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
