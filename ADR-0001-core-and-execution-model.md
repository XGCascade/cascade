# ADR-0001: Core Architecture and Execution Model

## Status
Accepted

## Date
2025-12-16

## Context

Cascade is designed as an explicit runtime validation framework.
The framework prioritizes determinism, minimal magic, and clear separation
of responsibilities over convenience abstractions.

During early v1 development, several design decisions were implicitly present
in the codebase. This ADR exists to make those decisions explicit, final,
and enforceable.

This document defines the architectural contract for Cascade v1.

---

## Decision 1 — Core Is Always Strict

The Cascade Core (`cascade.core`) performs strictly deterministic
type validation.

- No implicit coercion
- No lenient mode
- No context-aware behavior
- No policy-level decisions

As a result:
- The `validate_type` API has no `strict` or mode parameters
- Any non-strict behavior is considered a higher-layer concern

This decision ensures that Core behavior is predictable and
semantically frozen for v1.

---

## Decision 2 — Core Does Not Execute Rules

Rules are never executed by the Core layer.

Core responsibilities are limited to:
- Type checking
- Custom type validator dispatch
- Error construction

Rule execution belongs to explicit execution policies
such as validated dataclasses or user-defined workflows.

---

## Decision 3 — Global Registries Are a Conscious Trade-off

Type validators and coercers are registered in process-global registries.

This is a deliberate design choice with the following implications:

- Deterministic lookup
- Low cognitive overhead
- Simple mental model

Limitations are explicitly accepted:
- No request-local isolation
- No per-context registry overrides
- Not suitable for multi-tenant plugin systems

Registry clearing functions exist strictly for test isolation.

---

## Decision 4 — Rules Are Defined by Behavior, Not Inheritance

A rule is defined as:

- A callable accepting a single value
- Raising `RuleValidationError` on failure
- Exposing a public `name` attribute

The `Rule` base class is a reference implementation only.
Inheritance from `Rule` is optional.

Execution layers must not enforce rule inheritance.
They may only validate the callable contract.

---

## Decision 5 — Validated Dataclasses Are an Execution Policy

The `validated_dataclass` decorator defines a specific and opinionated
execution model.

Execution order is fixed for v1:

1. Type validation
2. Field rule execution (in declaration order)

Additional characteristics:

- No validation on initialization
- No validation on assignment
- No implicit triggers

Validated dataclasses are one execution policy among many.
They are not the only supported way to use Cascade.

---

## Decision 6 — Public API Is Explicit and Minimal

Only symbols exported through `cascade.api` are considered public
and stable for v1.

Internal modules may change freely as long as the public API contract
is preserved.

No experimental or future-facing parameters are exposed in the v1 API.

---

## Consequences

- Cascade v1 behavior is explicit and irreversible without a major version bump
- Extension points are intentional and limited
- Architectural boundaries are enforceable via tests
- Users must opt in to all behavior explicitly

These constraints are considered features, not limitations.

---

## Enforcement

This ADR is enforced by:

- Architecture-level tests
- Strict public API curation
- Explicit documentation
- Code review policy

Any change that violates this ADR requires:
- A new ADR
- A major version increment
