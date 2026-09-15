# Academic Mission Control — Design Specification

## Objective

Upgrade the postgraduate studies management system into a cinematic, enterprise-grade academic operations experience while preserving the existing APIs, authentication, permission architecture, workflow rules, and database contracts.

The product serves two distinct contexts:

- Academic leadership needs a high-level command center for monitoring real institutional data and pending decisions.
- Operational staff need a fast daily workspace for search, review, and navigation without decorative motion slowing their work.

### Role-specific executive command centers

- **Program and Platform Director:** a digital operations room whose command destinations come only from permission-filtered API navigation. Platform governance appears solely when the account receives the settings capability.
- **Vice Dean for Postgraduate Studies:** an academic decision briefing centered on live pending decisions, workflow distribution, defenses, departments, and student records. Platform administration never appears in this surface.

Both variants share the existing dashboard contract. No frontend constant supplies a KPI. Gold identifies protected platform governance; medical teal identifies academic decision flow.

## Approved Direction

The approved design direction is **Academic Mission Control**: an institutional university and medical identity with restrained cinematic motion, permission-aware intelligence, and charts derived only from current backend responses.

The visual system uses deep institutional navy, medical teal, warm white, and limited gold accents. Cinematic effects are concentrated in entry sequences, chart transitions, assistant expansion, and key state changes. Tables, forms, search, and routine employee operations remain quiet and immediate.

## Experience Architecture

### Assistant Shell

The assistant remains globally available as a floating control and supports two display states:

- Compact chat panel for quick questions and navigation.
- Expanded intelligence panel for richer results without covering the active work context unnecessarily.

On mobile, the assistant becomes an accessible bottom sheet. It supports Arabic RTL and English LTR and retains keyboard navigation, labeled controls, focus visibility, and reduced-motion behavior.

### Assistant Intelligence UI

The assistant supports the existing academic domains:

- Students
- Theses
- Committees and defenses
- Approvals
- Workflow
- General authorized questions

Responses may include concise text, a result summary, and permission-safe navigation actions. Quick actions come from backend-provided capabilities or navigation. A visible action must lead to a working route or a real API-backed operation. Placeholder actions are not permitted.

The assistant does not infer or expose data outside the authenticated user's effective permissions.

### Platform Motion Layer

A centralized motion token layer defines:

- Page and section reveal durations.
- Card and row stagger limits.
- Assistant open and expand transitions.
- Chart update transitions.
- Hover and focus feedback.

Motion runs once when content appears or when data changes. Continuous decorative animation and excessive glow are excluded. `prefers-reduced-motion: reduce` removes transforms, stagger, and animated interpolation while preserving all content and functionality.

## Data Visualization

Charts are rendered only when the current API response contains enough data to support their stated meaning. Candidate visualizations are:

- Thesis status distribution.
- Student distribution by academic degree or department.
- Upcoming defense timeline.
- Workflow-stage distribution or funnel.

Each visualization must provide:

- A clear Arabic and English title.
- A backend-derived definition matching the displayed number.
- Accessible labels or an equivalent textual summary.
- Tooltips for exact values.
- A useful loading, error, and empty state.
- Responsive behavior without clipped labels.

No fixed KPI, fabricated series, demo total, or synthetic trend may be embedded in React. If the backend does not provide historical comparison data, no trend claim is displayed.

The implementation reuses an existing chart dependency if one is already installed and suitable. Otherwise it uses lightweight responsive SVG rather than adding an unnecessary dependency.

## Page-Level Treatment

### Executive Dashboard

The executive dashboard receives the richest presentation layer: ordered entry, animated real-data charts, decision emphasis, and compact institutional context. Animation supports hierarchy and does not delay access to information.

### Employee Workspace

The employee workspace keeps operational density and speed. Motion is limited to panel changes, search-result entry, status changes, and Student 360 transitions. Search fields, queues, tables, and actions remain immediately usable.

### Students, Theses, Committees, and Reports

All modules share the same typography, spacing, surface hierarchy, status language, and interaction feedback. Data tables remain stable while charts or summaries animate independently. Empty and loading states use the same bilingual vocabulary and never render `null`, `undefined`, or unexplained database codes.

## Data and Permission Flow

1. `/me/` supplies effective roles, permissions, and dashboard-management capability.
2. Dashboard navigation remains the authoritative frontend visibility input.
3. Existing dashboard and module APIs supply real metrics and records.
4. The assistant endpoint receives the question and returns an authorized answer.
5. The frontend renders only capabilities and actions supported by the returned data and visible navigation.

Frontend filtering improves usability but never replaces backend authorization.

## Error and Empty States

- Network failure: retain the active interface and show a clear retryable message when a retry action exists.
- Permission denial: explain that the information is outside the account's access without exposing hidden totals or records.
- Missing optional fields: use the existing bilingual fallback rules and display an em dash when neither value exists.
- Empty chart data: show a localized empty state instead of zero-filled or decorative chart marks.
- Assistant failure: preserve the conversation, identify the failed response, and allow the user to retry without duplicating their question.

## Performance and Accessibility

- Avoid animation on large table row sets.
- Animate transform and opacity where motion is appropriate.
- Lazy-load chart-heavy views if bundle analysis shows a material benefit.
- Preserve touch targets, focus states, semantic buttons, and screen-reader labels.
- Test desktop, tablet, and mobile layouts in RTL and LTR.
- Prevent assistant overlays from blocking critical page actions.

## Validation

Acceptance requires:

- Frontend production build succeeds.
- Existing backend contracts remain unchanged unless a separately approved gap requires backend work.
- Existing authentication, roles, permissions, and workflow behavior remain intact.
- Visible assistant quick actions work through real routes or APIs.
- Charts use backend-derived data and contain no hardcoded KPI values.
- Arabic and English labels render consistently.
- Keyboard navigation and reduced-motion behavior work.
- No regression occurs in executive dashboard or employee workspace routing.

## Delivery Sequence

1. Audit current assistant, dashboard datasets, chart dependencies, and global styles.
2. Establish motion and visualization tokens.
3. Upgrade the floating assistant shell and result presentation.
4. Add reusable real-data chart components.
5. Integrate charts into authorized dashboards and modules.
6. Apply restrained global cinematic transitions.
7. Validate localization, accessibility, responsiveness, tests, and production build.

## Out of Scope

- New database models.
- Changes to authentication or permission semantics.
- Changes to workflow transitions.
- Fabricated analytics or historical trends.
- Unapproved external LLM or analytics integrations.
- Merge into `main` or `enterprise-development`.
