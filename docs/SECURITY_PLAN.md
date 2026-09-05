# Security Architecture Plan
# خطة المعمارية الأمنية

## Project

Postgraduate Studies Management System

نظام إدارة الدراسات العليا والبحوث


---

# 1. Security Vision

The system must provide a secure enterprise-level authorization architecture that supports:

- Multiple universities.
- Multiple faculties.
- Changing academic leadership.
- Dynamic user assignments.
- Full auditability.
- Workflow-based approvals.


النظام يجب أن يدعم:

- التوسع لعدة جامعات.
- التوسع لعدة كليات.
- تغير القيادات الأكاديمية.
- تغيير المستخدمين المسؤولين عن المناصب.
- تسجيل كامل لكل العمليات.
- اعتماد الإجراءات من خلال Workflow.


---

# 2. Current Security Architecture

Current structure:


User

↓

Role

↓

Permission


The system currently contains:

- User model.
- Role model.
- Permission model.
- ApprovalAction audit model.
- Workflow transition engine.


---

# 3. Identity vs Authorization Decision

## Identity Layer

Responsible for answering:

"Who is this user?"


Example:

Ahmed Abdelkhalek

Role:
PROGRAM_DIRECTOR


Current implementation:

User.role


---

## Authorization Layer

Responsible for answering:

"What can this user do?"


Example:


User:

Ahmed Abdelkhalek


Roles:

- PROGRAM_DIRECTOR
- PLATFORM_ADMIN


Permissions:

- workflow.configure
- users.manage
- reports.view


Implementation:

User

↓

Roles

↓

Permissions


---

# 4. Platform Administrator

## New Enterprise Role

Role:

PLATFORM_ADMIN


Purpose:

The platform administrator manages the digital platform, not academic decisions.


Responsibilities:

- Manage users.
- Assign roles.
- Manage permissions.
- Configure system settings.
- Monitor audit logs.
- Manage university/faculty configuration.


The Platform Administrator does NOT:

- Approve academic decisions.
- Replace dean authority.
- Replace vice dean authority.


---

# 5. Academic Roles

Academic roles represent positions, not permanent persons.


Examples:


DEAN

Assigned User:

Current Dean


VICE_DEAN_POSTGRADUATE

Assigned User:

Current Vice Dean


PROGRAM_DIRECTOR

Assigned User:

Current Program Director


Changing leadership must not require code modification.


---

# 6. Role Based Access Control (RBAC)

The system uses:

Role Based Access Control


Structure:


User

↓

Role

↓

Permission

↓

Action


Permissions must follow:

Least Privilege Principle.


---

# 7. Workflow Security Model


Workflow actions:


SUBMIT

REVIEW

APPROVE

REJECT

RETURN


Approval security requires more than permissions.


Final architecture:


User

↓

Role

↓

Permission

↓

Workflow Policy

↓

Approval Action

↓

Audit Log


---

# 8. Separation of Duties


The system must prevent conflicts of interest.


Examples:


Staff:

Create requests.


Reviewer:

Review requests.


Program Director:

Program level approval.


Vice Dean:

Postgraduate approval.


Dean:

Faculty approval.


No user should approve their own submitted request.


---

# 9. Audit Requirements


ApprovalAction currently records:


- Request type.
- Object ID.
- Action.
- Previous status.
- New status.
- User.
- Notes.
- Timestamp.


Future improvements:

- IP address.
- Device information.
- Change history.
- Approval level.
- Digital signature support.


---

# 10. AI Assistant Security


The AI Assistant is a controlled system component.


Architecture:


User

↓

Permission Check

↓

AI Assistant

↓

Authorized Data


The AI Assistant must respect user permissions.


Examples:


Student:

Can ask about personal requests.


Employee:

Can ask about assigned workflows.


Dean:

Can view faculty indicators.


Vice President:

Can view university-level indicators.


---

# 11. University Expansion Model


The system must support:


Faculty of Medicine

↓

Assiut University

↓

Multiple Universities


Security must support:

- University isolation.
- Faculty isolation.
- Role assignments per organization.


---

# 12. Security Development Roadmap


Phase 1:

Document security decisions.


Phase 2:

Introduce PLATFORM_ADMIN role.


Phase 3:

Create official permission matrix.


Phase 4:

Connect workflow actions with permissions.


Phase 5:

Create workflow policy engine.


Phase 6:

Improve audit logging.


Phase 7:

Integrate AI Assistant authorization.


---

# Security Principle

Never hardcode people names inside business logic.

Never depend only on roles.

Always validate:

User + Role + Permission + Workflow Rule.

