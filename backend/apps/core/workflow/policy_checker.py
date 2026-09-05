"""
Workflow Policy Checker

Validates if a user role is allowed
to perform a workflow action.
"""

from apps.core.workflow.policies import WORKFLOW_POLICIES


def can_perform_action(user_roles, request_type, action):
    """
    Check if any user role is allowed
    to perform the requested workflow action.
    """

    allowed_roles = WORKFLOW_POLICIES.get(
        request_type,
        {}
    ).get(
        action,
        []
    )

    return any(
        role in allowed_roles
        for role in user_roles
    )
