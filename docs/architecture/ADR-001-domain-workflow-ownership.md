# ADR-001: Domain Workflow Ownership

## Status

Accepted

## Date

2026

---

# Context

The platform contains multiple business domains:

- Thesis Management
- Academic Supervision
- Defense Committees
- Future Enterprise Modules

Each domain has its own business lifecycle and approval requirements.

A common mistake is placing all workflow states inside a central workflow model, causing the core platform to become dependent on individual business domains.

---

# Decision

The platform separates:

## Workflow Infrastructure

Owned by:
Core Domain


Responsible for:

- Workflow execution engine
- Approval actions
- Permission evaluation
- Audit records
- Generic workflow services

---

## Business Workflow States

Owned by:


Each Business Domain


Examples:

### Thesis Domain

Owns:

- REGISTERED
- SUBMITTED
- UNDER_REVIEW
- APPROVED

---

### Supervision Domain

Owns:

Supervisor assignment lifecycle:

- PENDING
- ACTIVE
- ENDED
- REPLACED

Supervisor change request lifecycle:

- DRAFT
- SUBMITTED
- UNDER_REVIEW
- APPROVED
- REJECTED
- COMPLETED

---

# Rationale

Business rules belong to the domain that understands them.

The Core domain should know:

"How to execute approval"

but should not know:

"What does changing a supervisor mean?"

---

# Benefits

This architecture provides:

- Clear domain ownership
- Better maintainability
- Independent module evolution
- SaaS scalability
- Easier testing
- Reduced coupling

---

# Consequences

Future domains must define their own:

- Business states
- Domain rules
- Lifecycle transitions

while reusing:

- Core workflow engine
- Approval infrastructure
- Security architecture

---

# Final Principle

Core provides the engine.

Domains provide the meaning.

Enterprise systems scale when responsibilities remain separated.
