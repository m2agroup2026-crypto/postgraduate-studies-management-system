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
        "DIRECTOR_APPROVE": "DIRECTOR_APPROVED",
        "REJECT": "REJECTED",
        "RETURN": "RETURNED",
    },

    "DIRECTOR_APPROVED": {
        "VICE_DEAN_APPROVE": "VICE_DEAN_APPROVED",
        "REJECT": "REJECTED",
        "RETURN": "RETURNED",
    },

    "VICE_DEAN_APPROVED": {
        "DEAN_APPROVE": "DEAN_APPROVED",
        "REJECT": "REJECTED",
        "RETURN": "RETURNED",
    },

    "DEAN_APPROVED": {
        "FINAL_APPROVE": "FINAL_APPROVED",
        "REJECT": "REJECTED",
        "RETURN": "RETURNED",
    },

    "RETURNED": {
        "SUBMIT": "SUBMITTED",
    },
}
