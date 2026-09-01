# PGMS Smart Dashboards and Mobile Design

Date: 2026-09-01  
Status: Approved  
Product: Postgraduate Studies Management System

## 1. Objective

Extend the existing postgraduate studies platform into a production-oriented bilingual system with Arabic as the default language, three role-specific executive dashboards, an embedded intelligent assistant, and one mobile application for Android and iOS.

## 2. Product Architecture

- Backend: Django + Django REST Framework.
- Database: PostgreSQL database named `postgraduate_studies_db`.
- Web dashboard: React with Arabic RTL enabled by default and optional English LTR.
- Mobile: React Native application sharing the same REST API and authentication model.
- Deployment: Docker-based local and server deployment.
- Security: Role-based access control, audit logging, protected endpoints, and explicit confirmation for sensitive actions.

## 3. User Roles and Dashboards

### Program Director

The Program Director dashboard supports daily postgraduate operations:

- Student records and enrollment lifecycle.
- Thesis and research-plan tracking.
- Supervisors, committees, defenses, and decisions.
- Overdue actions and deadline alerts.
- Operational reports and exports.
- Smart assistant access within the user's authorization scope.

### Dean

Dashboard identity: **الأستاذ الدكتور علاء عطية — عميد الكلية**

The Dean dashboard provides executive oversight:

- College-wide postgraduate indicators.
- Department comparison and trend summaries.
- Pending executive approvals.
- Registration, completion, and delayed-case summaries.
- Executive reports with drill-down access limited by role.

### Vice Dean for Postgraduate Studies and Research

Dashboard identity: **الأستاذ الدكتور محمد عبد الباسط خلاف — وكيل الكلية لشؤون الدراسات العليا والبحوث**

The Vice Dean dashboard provides academic and research governance:

- Research plans, theses, and supervision status.
- Committee formation and defense readiness.
- Department-level postgraduate performance.
- Pending decisions, escalations, and deadlines.
- Academic and research reports.

## 4. Intelligent Assistant

The assistant is available in both web and mobile applications.

Capabilities:

- Arabic-first conversational interface with English support.
- Search and summarize authorized system data.
- Identify overdue student cases and upcoming defenses.
- Explain dashboard indicators.
- Draft reports and administrative summaries.
- Navigate users to relevant records and workflows.
- Enforce role permissions on every assistant request.
- Require explicit confirmation before any sensitive or state-changing operation.
- Record assistant-triggered actions in the audit log.

The first production version uses a provider-agnostic assistant service so the AI provider can be configured through server environment variables without coupling business logic to one vendor.

## 5. Language and Localization

- Default locale: Arabic (`ar`).
- Default direction: RTL.
- Optional locale: English (`en`) with LTR.
- User preference is persisted per account.
- API validation messages, navigation, forms, reports, and notifications are localized.
- Proper names and official job titles remain exactly as approved.

## 6. Mobile Application

One React Native codebase targets Android and iOS.

Initial mobile scope:

- Secure authentication.
- Role-aware home dashboard.
- Student and thesis lookup.
- Notifications and deadline alerts.
- Committee and defense schedules.
- Smart assistant.
- Arabic RTL and English LTR.
- Responsive phone and tablet layouts.
- Secure token storage and session renewal.

## 7. Data and API Boundaries

The web dashboard and mobile app consume the same versioned API. Dashboard summaries use dedicated aggregate endpoints. The assistant calls a protected orchestration endpoint that retrieves only data authorized for the active user. Business rules remain in backend services rather than in web or mobile clients.

## 8. Reliability and Error Handling

- Standardized API error responses.
- Validation errors shown next to the relevant fields.
- Retry-safe reads and guarded writes.
- Session expiry handling on web and mobile.
- Offline-friendly mobile empty/error states for temporary connectivity loss.
- Server health checks and structured logging.
- Database migrations and seed data for development.

## 9. Verification

- Backend unit and API permission tests.
- Role isolation tests for all three dashboards.
- Arabic RTL and English LTR interface checks.
- Web responsive checks.
- Android and iOS build validation.
- Assistant authorization and confirmation tests.
- Docker startup and database migration test.
- End-to-end smoke tests for authentication, dashboard loading, assistant query, and key postgraduate workflows.

## 10. Delivery

The repository will contain:

- `backend/`
- `web/`
- `mobile/`
- `docs/`
- Docker and environment templates.
- Setup, development, testing, and server deployment instructions.
