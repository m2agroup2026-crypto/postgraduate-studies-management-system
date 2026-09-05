# Workflow Documentation
# توثيق سير العمل والاعتمادات

# Postgraduate Studies Management System
# نظام إدارة الدراسات العليا والبحوث

---

# 1. Introduction | مقدمة

## English

This document defines the workflow architecture and approval processes of the Postgraduate Studies Management System.

The workflow engine represents real academic and administrative procedures and converts them into controlled digital processes.

The goal is to provide:

- Clear approval paths.
- Full traceability.
- Secure decision management.
- Flexible expansion for different universities.

---

## العربية

هذا الملف يوضح معمارية سير العمل ومسارات الاعتماد داخل نظام إدارة الدراسات العليا والبحوث.

يقوم محرك سير العمل بتحويل الإجراءات الأكاديمية والإدارية الحقيقية إلى إجراءات رقمية منظمة ومؤمنة.

الأهداف:

- تحديد مسارات الاعتماد بوضوح.
- تسجيل جميع الإجراءات.
- حماية القرارات.
- دعم التوسع للجامعات المختلفة.

---

# 2. Workflow Concept | مفهوم سير العمل


## English

A workflow represents the lifecycle of a request from creation until final approval.

Each workflow contains:

- Request
- Statuses
- Actions
- Approval Steps
- Responsible Users
- Audit Records


---

## العربية

يمثل سير العمل دورة حياة الطلب منذ إنشائه حتى الاعتماد النهائي.

يتكون كل Workflow من:

- الطلب
- الحالات
- الإجراءات
- مراحل الاعتماد
- المسؤولين
- سجل الإجراءات

---

# 3. Workflow Architecture | معمارية سير العمل


The system separates workflow rules from execution logic.


Structure:

core/

workflow/
rules.py
services/
workflow.py


Purpose:

- Easy maintenance.
- Clear business rules.
- Future configuration.
- Support multiple universities.


---

# 4. Request Lifecycle | دورة حياة الطلب


General lifecycle:

Created

↓

Submitted

↓

Under Review

↓

Approved / Rejected / Returned

↓

Completed


---

# 5. Official Approval Hierarchy

# التسلسل الرسمي للاعتمادات


The current organizational approval chain:

Staff Member

الموظف المختص
    ↓
    Reviewer

المراجع
    ↓
Vice Dean for Postgraduate Studies

وكيل الكلية لشئون الدراسات العليا والبحوث

Prof. Mohamed Abdel Baset Khalaf
    ↓
Dean

عميد الكلية

Prof. Alaa Attia
    ↓
Vice President for Postgraduate Studies

نائب رئيس الجامعة لشئون الدراسات العليا والبحوث

Prof. Gamal Badr
    ↓
Faculty Council / University Council

مجلس الكلية / مجلس الجامعة حسب نوع القرار

---

# 6. User Responsibilities | مسؤوليات المستخدمين


# Staff Member

## الموظف المختص


Responsibilities:

- Create requests.
- Enter information.
- Upload documents.
- Verify completeness.


---

# Reviewer

## المراجع


Responsibilities:

- Check submitted data.
- Review documents.
- Add comments.
- Return incomplete requests.


---

# Program Director

## مدير البرنامج


Responsibilities:

- Academic review.
- Workflow supervision.
- Request monitoring.
- Forward approval requests.


---

# Vice Dean

## وكيل الكلية


Responsibilities:

- Main postgraduate approval.
- Review academic decisions.
- Approve postgraduate processes.


---

# Dean

## العميد


Responsibilities:

- Final faculty approval.
- Executive decisions.
- Faculty governance.


---

# Vice President

## نائب رئيس الجامعة


Responsibilities:

- University-level governance.
- Strategic monitoring.
- University-wide approvals.


---

# 7. Thesis Workflow Example

# مثال: تسجيل رسالة علمية


Current planned flow:

Student Request

↓

Staff Data Entry

↓

Reviewer Verification

↓

Program Director Review

↓

Vice Dean Approval

↓

Dean Approval

↓

University Approval if required

---

# 8. Workflow Status Design

## Example Thesis Statuses

REGISTERED

SUBMITTED

UNDER_REVIEW

PENDING_VICE_DEAN_APPROVAL

PENDING_DEAN_APPROVAL

APPROVED

REJECTED

RETURNED

COMPLETED


---

# 9. Actions


Available workflow actions:

SUBMIT

REVIEW

APPROVE

REJECT

RETURN

FINAL_APPROVE

---

# 10. ApprovalAction Audit Trail


Every workflow action creates an audit record.


Stored information:

Request Type

Object ID

Action

Previous Status

New Status

Performed User

Notes

Timestamp


Purpose:


- Accountability.
- Compliance.
- Decision history.
- Reports.


---

# 11. Adding New Workflow


When adding a new process:


Example:

Defense Committee Formation


Required steps:


1. Define request type.

2. Define statuses.

3. Define approval steps.

4. Define responsible roles.

5. Add permissions.

6. Create APIs.

7. Test workflow.

8. Update documentation.


---

# 12. Configurable Workflow Future


The future architecture will support database-driven workflows.


Instead of coding:

IF role == DEAN


The system will use:

Workflow Template

Approval Steps

Approval Policies


This allows different universities to configure their own procedures.

---

# 13. Multi University Support


Each university may have:


- Different approval hierarchy.
- Different regulations.
- Different documents.
- Different workflows.


The system should support this through configuration, not code changes.


Example:


University A:
Staff
Reviewer
Director
Vice Dean
Dean


University B:
Staff
Department Head
Vice Dean
Dean
University Approval


---

# 14. Workflow Security Rules


Important principles:


1. User identity must be verified.

2. User role must allow the action.

3. Every action must be logged.

4. Unauthorized transitions must be blocked.


Example:


Invalid:

APPROVED → REVIEW


Result:

Blocked

Invalid Transition


---

# 15. Future Enhancements


Planned improvements:


- Dynamic Workflow Designer.
- Approval delegation.
- Escalation rules.
- Automatic reminders.
- SLA monitoring.
- AI workflow recommendations.


---

# Document Information


Document:

Workflow Documentation


System:

Postgraduate Studies Management System


Designed & Developed by:


Engineer Ahmed Abdelkhalek

Digital Experience & Automation Engineer


Website:

https://ahmed.m2agroupeg.com/


---

END OF DOCUMENT


