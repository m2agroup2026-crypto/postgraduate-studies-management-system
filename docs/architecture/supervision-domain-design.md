# Academic Supervision Domain Design

## Version 1.0 — 2026

---

# 1. Purpose

The Academic Supervision Domain manages the complete lifecycle of postgraduate thesis supervision.

The domain is responsible for:

- Supervisor assignment
- Co-supervisor management
- Supervisor replacement
- Supervisor withdrawal
- Approval workflow
- Historical tracking
- Capacity management

---

# 2. Design Principle

A thesis must not directly store a single supervisor reference.

Incorrect approach:

```text
Thesis
 |
 supervisor_id
Reason:

Academic supervision is a historical relationship.

A student may have:

Current supervisor
Previous supervisor
Co-supervisor
Replacement supervisor
Pending assignment
3. Core Relationship Model
Student

    |

Thesis

    |

ThesisSupervisorAssignment

    |

SupervisorProfile
4. Main Entities
SupervisorProfile

Represents the academic supervisor.

Responsibilities:

Academic identity
Department association
Specialization
Supervision capacity
Active status
ThesisSupervisorAssignment

Represents the relationship between a thesis and supervisor.

Responsibilities:

Assignment lifecycle
Supervisor role
Start date
End date
Status tracking

Possible statuses:

PENDING_APPROVAL

ACTIVE

ENDED

REPLACED
SupervisorChangeRequest

Handles supervisor replacement requests.

Reason:

Changing a supervisor is an administrative decision, not a direct database update.

Workflow:

Request

↓

Review

↓

Approval

↓

Activation
SupervisorAssignmentHistory

Preserves complete supervision history.

Records:

Previous supervisor
New supervisor
Date
Reason
Approval reference
5. Supervisor Roles

The system should support:

PRIMARY_SUPERVISOR

CO_SUPERVISOR

EXTERNAL_SUPERVISOR

ASSISTANT_SUPERVISOR
6. Capacity Management

Supervisor capacity must not be hard-coded.

The system should support configurable policies.

Example:

Professor:
10 theses

Associate Professor:
7 theses

Lecturer:
5 theses

Future implementation:

SupervisorCapacityPolicy
7. Approval Governance

Important actions require approval.

Examples:

New supervisor assignment
Supervisor replacement
Supervisor removal

Each action must record:

Requested by
Approved by
Date
Decision
Notes
8. Security Requirements

Suggested permissions:

supervision.view

supervision.assign

supervision.change

supervision.approve

supervision.manage
9. Future Expansion

The domain should support:

Multiple universities
Multiple faculties
External supervisors
Digital approvals
AI supervision analytics
Workload optimization
Final Principle

Academic supervision is not a simple relationship.

It is a governed institutional process with history, approvals, and accountability.
