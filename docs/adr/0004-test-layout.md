# ADR-0004: Test layout — `tests/`, `reproducibility/`, `historical/`

## Status

Accepted (2026-11-15)

## Context

Before v1.3.0, `tests/` contained four heterogeneous categories:
formal tests (pytest), self-contained reproducibility scripts,
comparison scripts requiring `xjam2`, and historical exploration
scripts. Only the first category belongs in a test suite; the rest
either mislead `pytest` discovery or blur the meaning of "test".
After v1.3.0 the layout separates them by purpose.

## Decision

Four directories, each with a single purpose:

| Directory | Purpose | Collected by pytest? | Requires `xjam2`? | Maintained? |
|---|---|---|---|---|
| `tests/test_*.py` | Formal tests of the package API | yes | no | yes |
| `tests/comparison/` | Manual comparison against pairwise | no | yes | yes |
| `reproducibility/` | Paper-reproduction scripts (counts, closed forms) | no | no | yes |
| `historical/` | Discovery + audit scripts | no | no | no |

`pyproject.toml` enforces the split via `testpaths = ["tests"]` and
`norecursedirs = ["tests/comparison", "historical", "reproducibility", ...]`.

The `README.md` of each non-test directory states its purpose in the
first paragraph and links to the others.

## Consequences

**Gains.**

- `pytest` collects exactly what it should; no manual `--ignore`.
- Each directory has a single, discoverable purpose.
- Historical scripts are preserved for traceability without
  polluting the test suite.
- Reproducibility scripts are discoverable (a user looking for "how
  to reproduce Table 3" finds `reproducibility/validation_table1.py`
  in one step, not after digging through `tests/`).

**Losses.**

- New contributors must read `tests/README.md` to understand the
  four-way split. Accepted: this is a one-time cost of ~2 minutes.
- Moving scripts breaks external references. Accepted: CHANGELOG
  entries are not rewritten (see ADR-0005 conventions); only
  `README.md`, `README.es.md`, and `tests/comparison/README.md` are
  updated.
