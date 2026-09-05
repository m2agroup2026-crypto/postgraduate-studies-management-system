"""
Workflow Approval Policies

Defines who can perform workflow actions
based on administrative hierarchy.

This file contains business rules only.
No database operations here.
"""


WORKFLOW_POLICIES = {

    "THESIS": {

        "SUBMIT": [
            "STAFF",
        ],

        "REVIEW": [
            "REVIEWER",
        ],

        "APPROVE": [
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
