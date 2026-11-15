# ADR-0001: Scope — JAM instance, not general columnar G-sets

## Status

Accepted (2026-11-15)

## Context

`canonJAM` was born as a JAM-specific library: canonicalization of
JAM chains for the eight canonical options described in
[Arcudia2023]. Later work generalized the underlying structure to
*columnar G-sets* with group `G = P × K`, arbitrary column group
`P ≤ S_r` and alphabet group `K ≤ Sym(Σ)`. That generalization lives
in a separate artifact (a Lean 4 formalization) and in a paper. The
scope of `canonJAM` must be fixed explicitly, or it will drift toward
implementing the general framework, which is out of scope for a
Python package whose value is a small, tested, dependency-free API.

A second scope question is *self-sufficiency*: before v1.2.0, the
single-layer row sets for the eight options lived in
`tests/validacion.py`, forcing users who wanted the row sets to
depend on a test file. v1.2.0 moved them into `canonjam/options.py`.

## Decision

`canonJAM` implements **only** the JAM instance of columnar G-sets:

- `P = S_3`, `K = ℤ/2`, `r = 3`, `k ≥ 2`.
- All eight canonical options (1–8).
- The package is **self-sufficient** in its own definition of the
  options: `rows_for_option` lives in `canonjam/options.py`, not in
  a test file.
- `canonJAM` does **not** implement the general framework. If the
  need arises (`P = D_4`, `r ≠ 3`, etc.), that belongs to a new
  package, not to `canonJAM`.

## Consequences

**Gains.**

- Clear, maintainable, testable scope.
- A user who needs `P = D_4` reads `DESIGN.md`, understands it is
  out of scope, and does not open an issue.
- The package no longer depends on any test file for its public
  surface.

**Losses.**

- Generalization requires a new repo (the Lean formalization or a
  future Python package), not a modification of `canonJAM`.
- The paper must declare explicitly that `canonJAM` is a
  specialization of the general framework.
- If the general framework later wants a Python implementation,
  some code from `canonjam/canonical.py` will be duplicated or
  refactored; this is accepted as a future cost, not a present
  blocker.

