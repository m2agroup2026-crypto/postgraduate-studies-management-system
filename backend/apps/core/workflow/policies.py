"""
Workflow approval policies.

Defines role authorization for postgraduate workflow actions. Generic actions are
mapped in WORKFLOW_POLICIES, while ambiguous actions such as REJECT and RETURN
are constrained by the current workflow status in WORKFLOW_STATUS_POLICIES.
"""


WORKFLOW_POLICIES = {
    "THESIS": {
        "SUBMIT": [
            "STAFF",
        ],
        "REVIEW": [
            "REVIEWER",
        ],
        "DIRECTOR_APPROVE": [
            "POSTGRADUATE_DIRECTOR",
        ],
        "VICE_DEAN_APPROVE": [
            "VICE_DEAN_POSTGRADUATE",
        ],
        "DEAN_APPROVE": [
            "DEAN",
            "COLLEGE_COUNCIL",
        ],
        "FINAL_APPROVE": [
            "VP_POSTGRADUATE_RESEARCH",
        ],
    },
}


WORKFLOW_STATUS_POLICIES = {
    "THESIS": {
        "UNDER_REVIEW": {
            "REJECT": ["POSTGRADUATE_DIRECTOR"],
            "RETURN": ["POSTGRADUATE_DIRECTOR"],
        },
        "DIRECTOR_APPROVED": {
            "REJECT": ["VICE_DEAN_POSTGRADUATE"],
            "RETURN": ["VICE_DEAN_POSTGRADUATE"],
        },
        "VICE_DEAN_APPROVED": {
            "REJECT": ["DEAN", "COLLEGE_COUNCIL"],
            "RETURN": ["DEAN", "COLLEGE_COUNCIL"],
        },
        "DEAN_APPROVED": {
            "REJECT": ["VP_POSTGRADUATE_RESEARCH"],
            "RETURN": ["VP_POSTGRADUATE_RESEARCH"],
        },
    },
}
