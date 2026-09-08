"""Workflow policy authorization helpers."""

from apps.core.workflow.policies import WORKFLOW_POLICIES, WORKFLOW_STATUS_POLICIES


def can_perform_action(user_roles, request_type, action, current_status=None):
    """Return whether any effective user role may perform the workflow action."""
    allowed_roles = WORKFLOW_POLICIES.get(request_type, {}).get(action, [])

    if current_status:
        status_roles = (
            WORKFLOW_STATUS_POLICIES.get(request_type, {})
            .get(current_status, {})
            .get(action)
        )
        if status_roles is not None:
            allowed_roles = status_roles

    return any(role in allowed_roles for role in user_roles)
