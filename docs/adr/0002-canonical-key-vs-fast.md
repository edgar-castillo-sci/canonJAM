# ADR-0002: `canonical_key` vs `canonical_key_fast`; `filter_duplicates` API

## Status

Accepted (2026-11-15)

## Context

Two implementations of the canonical key coexist:

- `canonical_key(a, option)` — the literal definition: minimum over
  the 12 group elements. Cost: 12 evaluations.
- `canonical_key_fast(a, option)` — the optimal computation: minimum
  of the sorted-column concatenations of `a` and its `v`-image.
  Cost: 2 evaluations.

Both are tested to agree for all eight options and `n = 2, 3`
(`tests/test_canonical_fast.py`, 5,655 chains).

A third function, `filter_duplicates(stackinglist, option)`, builds
a dict keyed by canonical key. It internally uses `canonical_key`
(not the fast variant). A draft proposal (now removed from the repo)
suggested adding a `key=` parameter so users could pass
`canonical_key_fast`. That proposal was rejected — see Decision.

Finally, `generate_group` is exported but does not appear in any
public example. Its status has to be settled.

## Decision

**Both implementations are exposed.** `canonical_key` is the
definition; `canonical_key_fast` is the optimal computation. Neither
is deprecated. The equivalence test is the contract.

**`filter_duplicates` does not accept `key=`.** Rationale: the
function performs *both* deduplication passes (`eqnum=1` and
`eqnum=2`) in a single call, matching the semantics of the original
`disc_equivalents`. A `key=` parameter would have to specify *to
which pass* it applies, leaking filter semantics into the interface.
Users who want the fast variant can build the dict themselves
(3 lines, shown in the README quickstart).

**`generate_group` is exported**, but is documented in `DESIGN.md`
as intended for advanced use, and may be deprecated in v2.0.0 if no
public consumer appears. It is not removed in v1.3.0 because doing
so would be a breaking change in a release that is otherwise
non-breaking for direct imports.

## Consequences

**Gains.**

- Both the definition and the implementation are visible to the
  reader; the test proves they agree.
- `filter_duplicates` has a single, clear semantics.
- `generate_group` is not silently broken; it is documented and
  given a deprecation path.

**Losses.**

- A user who benchmarks `filter_duplicates` sees the `canonical_key`
  cost (12 evals), not the fast cost (2 evals). This is intentional
  but should be documented; the README quickstart shows the fast
  path explicitly.
- `generate_group` remains exported as "soft-deprecated"; a future
  v2.0.0 could remove it.
