"""
Workflow Approval Policies

Defines administrative approval stages
for postgraduate workflows.
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
