# Developer Guide
# دليل المطور

## Postgraduate Studies Management System

---

# 1. Introduction | مقدمة

## English

This document explains the technical architecture, development rules, and maintenance guidelines for the Postgraduate Studies Management System.

The purpose is to allow developers to understand, maintain, and extend the system safely.

---

## العربية

هذا الملف يشرح الهيكل البرمجي وقواعد التطوير والصيانة لنظام إدارة الدراسات العليا والبحوث.

الهدف هو تمكين أي مطور من فهم النظام وتطويره بدون التأثير على الأجزاء الحالية.

---

# 2. Technology Stack

Backend:

- Django
- Django REST Framework
- PostgreSQL
- Docker


Frontend:

- React Dashboard


Mobile:

- Android / iOS


Authentication:

- JWT


---

# 3. Project Structure

backend/

apps/
accounts/

academics/

students/

theses/

committees/

core/
---

# 4. Application Responsibilities


## accounts

Responsible for:

- User management
- Authentication
- Roles
- Permissions


Important concepts:

User Role

User Identity

Authorization


---

## academics

Responsible for academic structure:


Examples:

University

Faculty

Department

Program

Academic Degree


Future:

Multi University Support


---

## students

Responsible for:

- Student profiles
- Academic information
- Student lifecycle


---

## theses

Responsible for:

- Thesis registration
- Thesis workflow
- Thesis status


---

## committees

Responsible for:

- Defense committees
- Examiner information
- Defense process


---

## core

The heart of the platform.


Responsible for:

- Shared services
- Workflow Engine
- Approval System
- Audit Logs


---

# 5. Workflow Engine Architecture


The workflow system is separated into two layers:


## Rules Layer


Location:

Purpose:

Contains business transitions only.


Example:

core/workflow/rules.py
REGISTERED

SUBMIT

↓

SUBMITTED

REVIEW

↓

UNDER_REVIEW

APPROVE

↓

APPROVED


---

## Execution Layer


Location:
core/services/workflow.py


Responsibilities:

- Validate transition
- Update status
- Create audit record


---

# 6. ApprovalAction Audit System


Every important workflow action must create an audit record.


Stores:

- Request type
- Object ID
- Action
- Previous status
- New status
- User
- Notes
- Timestamp


Purpose:

- Compliance
- Tracking
- Investigation
- Reports


---

# 7. Development Rules


## Business Logic


Never put business rules inside:

- API Views
- Serializers


Correct approach:

↓

Service Layer

↓

Business Logic

↓

Database


---

# 8. Adding a New Feature


Every feature should contain:


## 1. Model

Database structure


## 2. Service

Business logic


## 3. API

External communication


## 4. Permission

Who can use it


## 5. Documentation

Explain the feature


---

# 9. Adding New Workflow


Steps:


1. Define statuses


Example:

PENDING

APPROVED

REJECTED


2. Add transitions


3. Add permissions


4. Add API actions


5. Test workflow


6. Update documentation



---

# 10. Multi University Design Rules


Never create university-specific code.


Wrong:

if university == "Assiut":


Correct:


Use configuration:

University Settings

Workflow Templates

Approval Policies


---

# 11. Security Development Rules


Required:


- Permission checks
- Authentication
- Audit logs
- Input validation
- Secure API access


Never trust frontend permissions only.


Backend must always validate.


---

# 12. Code Documentation Rules


Important sections must contain comments explaining:


- Why this code exists
- Business purpose
- Future extension


Avoid unnecessary comments explaining obvious code.


---

# 13. Git Workflow


Before changes:


Check current branch.


After changes:


Run tests.


Commit message example:

feat: add thesis approval workflow


or:

refactor: separate workflow rules


---

# 14. Testing Rules


Before accepting any feature:


Check:

- API works
- Workflow works
- Permissions work
- Existing features are not broken


---

# 15. Future Architecture Goals


The system will evolve into:


Enterprise University Platform


Supporting:


- Multiple Universities
- Configurable Workflows
- AI Assistant
- Mobile Applications
- Advanced Analytics


---

# Developer Identity


Designed & Developed by:

Engineer Ahmed Abdelkhalek

Digital Experience & Automation Engineer


Website:

https://ahmed.m2agroupeg.com/


---

END OF DOCUMENT


