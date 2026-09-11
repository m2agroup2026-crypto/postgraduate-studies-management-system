# Supervision Domain Data Model

## Version 1.0 — 2026

---

# 1. Purpose

This document defines the data model design for the Academic Supervision Domain.

The purpose is to establish the database structure before implementation.

The design supports:

- Supervisor assignment
- Multiple supervisors
- Supervisor replacement
- Historical tracking
- Approval workflows
- Capacity management
- Future SaaS expansion

---

# 2. Core Design Principle

A thesis must not store a direct supervisor reference.

Incorrect:

```text
Thesis
   |
   supervisor_id
```

Reason:

Academic supervision is a lifecycle relationship.

The system must preserve:

Previous supervisors
Current supervisors
Replacement history
Approval decisions
# 3. Domain Relationship Model
                    Thesis

                       |

        ThesisSupervisorAssignment

                       |

              SupervisorProfile
# 4. Entity: SupervisorProfile
Purpose

Represents the academic identity of a supervisor.

The entity is independent from authentication.

A supervisor may have:

Internal system account
External academic identity without login access
Attributes
id

user (optional)

name_ar

name_en

academic_rank

department

specialization

is_external

is_active

created_at

updated_at
# 5. Entity: ThesisSupervisorAssignment
Purpose

Represents the relationship between a thesis and supervisor.

This entity stores the complete supervision lifecycle.

Attributes
id

thesis

supervisor

role

status

start_date

end_date

approved_by

approved_at

created_at

updated_at
# 6. Supervisor Roles

Supported roles:

PRIMARY_SUPERVISOR

CO_SUPERVISOR

EXTERNAL_SUPERVISOR

ASSISTANT_SUPERVISOR
# 7. Assignment Status Lifecycle
PENDING_APPROVAL

ACTIVE

ENDED

REPLACED
# 8. Entity: SupervisorChangeRequest
Purpose

Handles formal supervisor replacement requests.

Changing a supervisor is an institutional decision.

It must pass through approval workflow.

Attributes
id

thesis

current_assignment

requested_supervisor

reason

status

requested_by

reviewed_by

decision_notes

created_at

updated_at
# 9. Change Request Lifecycle
DRAFT

↓

SUBMITTED

↓

UNDER_REVIEW

↓

APPROVED

↓

COMPLETED

Rejected flow:

UNDER_REVIEW

↓

REJECTED
# 10. Entity: SupervisorCapacityPolicy
Purpose

Controls supervisor workload limits.

Capacity rules must be configurable.

Attributes
id

academic_rank

maximum_active_theses

is_active

created_at

updated_at
# 11. Integration With Existing Domains
Thesis Domain

Relationship:

Thesis

1 ---- *

ThesisSupervisorAssignment
Academic Domain

Supervisor belongs to:

Department

↓

Faculty

↓

University
Accounts Domain

Authentication is separated:

User

optional

SupervisorProfile
Documents Domain

Supporting documents are managed by:

AcademicDocument

No duplicate document system is created.

Core Domain

Approval and audit are handled through:

ApprovalAction

No duplicate audit table is created.

# 12. Database Constraints

Required constraints:

A thesis may have only one active primary supervisor.
A supervisor can have multiple historical assignments.
External supervisors must be supported.
Historical assignments cannot be deleted.
Replacement actions require approval records.
# 13. Future Expansion

The design supports:

Multi-university deployment
SaaS tenancy
Supervisor analytics
Workload optimization
AI academic recommendations
Digital approval workflows
# Final Principle

The supervision domain represents an institutional process, not a simple database relationship.

The database must preserve history, accountability, and governance.
