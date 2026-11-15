# ADR-0003: Runtime depends only on numpy; `xjam2` is optional

## Status

Accepted (2026-11-15)

## Context

`xjam2` is the original JAM framework (not distributed via PyPI).
`canonJAM` was designed from the start to be usable *without*
`xjam2`, because the canonicalization method is independent of the
original pairwise method that `xjam2` implements. Two questions
arise: (i) should `canonJAM` depend on `xjam2` at all? (ii) if some
scripts need it, how should they fail?

## Decision

**Runtime dependency: `numpy` only.** `xjam2` is never a dependency
of the package.

**Scripts that require `xjam2`** (`tests/comparison/*.py`,
`examples/x_canonical.py`) **fail with a clear error message** if
`xjam2` is not importable, instead of raising `ModuleNotFoundError`.
The message points to `tests/comparison/README.md` for installation
instructions.

**`canonJAM` does not vendor or modify `xjam2`.** Only its public
API is used, and only in the comparison scripts and the optional
integration example.

## Consequences

**Gains.**

- `pip install canonJAM` works for any user with `numpy`.
- Tests are self-contained; CI does not need `xjam2`.
- The canonical filter is validated against the original method
  only when the user chooses to install `xjam2`, not as a condition
  of using `canonJAM`.

**Losses.**

- The comparison scripts cannot run in CI without an additional
  `xjam2` setup step. This is accepted: they are manual validation
  scripts, not part of `pytest`.
- Users who want to validate against the original pairwise method
  must install `xjam2` from source and set `PYTHONPATH` or use the
  Git URL; the README explains this.
