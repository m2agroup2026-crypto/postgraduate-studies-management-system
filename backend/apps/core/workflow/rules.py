WORKFLOW_TRANSITIONS = {
    "REGISTERED": {
        "SUBMIT": "SUBMITTED",
    },

    "DRAFT": {
        "SUBMIT": "SUBMITTED",
    },

    "SUBMITTED": {
        "REVIEW": "UNDER_REVIEW",
    },

    "UNDER_REVIEW": {
        "APPROVE": "APPROVED",
        "REJECT": "REJECTED",
        "RETURN": "RETURNED",
    },

    "RETURNED": {
        "SUBMIT": "SUBMITTED",
    },
}
