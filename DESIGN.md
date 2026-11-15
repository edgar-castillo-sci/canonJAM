# Design

This document is the mid-level layer of documentation for `canonJAM`.
For the top-level orientation see `README.md`; for the detailed
architectural decisions see `docs/adr/`.

## Scope

`canonJAM` implements the **JAM instance** of the columnar G-sets
framework: canonicalization of JAM chains for the eight canonical
options (1–8), with group `G = S₃ × ℤ/2`, `r = 3`, `k ≥ 2`, and
duplicate detection in `O(m)` via canonical keys. The runtime
depends only on `numpy`.

It does **not** implement the general framework (`P = D₄`, `P = D₂`,
`r ≠ 3`); that is the subject of a separate artifact. See ADR-0001.

## Architecture

```
canonjam/
  canonical.py    core: group actions, canonical keys, filter
  options.py      data: single-layer rows for the 8 options
  __init__.py     public API surface
tests/            formal tests (pytest); not paper artifacts
reproducibility/  paper-reproduction scripts (numpy + canonJAM only)
historical/       discovery + audit scripts; not maintained
examples/         usage examples (pipeline.py self-contained)
docs/adr/         architectural decisions
```

`canonjam/canonical.py` and `canonjam/options.py` are independent:
`options.py` has no imports from `canonical.py`, and `canonical.py`
imports only `numpy`. This is intentional (ADR-0003).

## Public API surface

Exported by `canonjam/__init__.py`:

- **Canonicalization**: `canonical_key`, `canonical_key_fast`,
  `filter_duplicates`.
- **Group operations**: `rot`, `transp`, `flip`, `sign`,
  `sort_cols`, `elements_S3`, `generate_group`.
- **Chain conversion**: `array_to_chain`, `chain_to_array`.
- **Option data**: `rows_for_option`, `base_sets_for_option`,
  `base_tokens_for_option`.

Everything else in `canonjam/` is internal and may change without a
major version bump. `generate_group` is exported but is intended for
advanced use; see ADR-0002 for its deprecation path.

## Index of ADRs

| ADR | Decision |
|---|---|
| [0001](docs/adr/0001-scope.md) | JAM instance, not general columnar G-sets; self-sufficiency of options |
| [0002](docs/adr/0002-canonical-key-vs-fast.md) | Both `canonical_key` and `canonical_key_fast` exposed; no `key=` in `filter_duplicates` |
| [0003](docs/adr/0003-numpy-only-xjam2-optional.md) | Runtime: numpy only; `xjam2` is optional and never vendored |
| [0004](docs/adr/0004-test-layout.md) | `tests/`, `tests/comparison/`, `reproducibility/`, `historical/` |
| [0005](docs/adr/0005-versioning-doi.md) | SemVer, CHANGELOG, Zenodo DOI policy, no `version` in `.zenodo.json` |

## What this is NOT

1. **Not a general columnar G-sets framework.** No `P = D₄`,
   `P = D₂`, `r ≠ 3`. That is scope, not a bug.
2. **Not the reproducibility artifact of a specific paper.** Scripts
   that reproduce published counts live in `reproducibility/`; they
   are self-contained but not the interface of the library.
3. **Not dependent on `xjam2`.** Scripts that require it fail with a
   clear error and never block the core package.

## Related artifacts

- Paper: *Canonical Forms and Burnside Enumeration for Columnar
  G-Sets* — forthcoming.
- Lean 4 formalization: `columnar-gsets` — forthcoming.

## Versioning

SemVer; CHANGELOG entries are never retroactively edited; `.zenodo.json`
contains no `version` field (the git tag is the single source of
truth). See ADR-0005.
