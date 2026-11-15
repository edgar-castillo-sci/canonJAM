# historical/

Scripts from the discovery and audit phases that preceded the current
implementation. They are kept in-tree for historical traceability only.

**These are not part of the library's test suite.** They may reference
old APIs, may break without notice, and are not covered by CI.

## Subdirectories

- **`exploration/`** — scripts used during the discovery phase to
  construct and verify the BPL/BU \(G\)-set isomorphism (Prop. 4.19 of
  the paper) and to explore the classification of \(X_n^\tau\) as a
  \(G\)-set, plus two files moved here from `tests/` for performance
  benchmarking (`benchmark_fast.py`, `benchmark_fast.csv`). The scripts
  assume the original `tests/exploration/` layout; see
  `exploration/README.md` for the full inventory and the path-drift
  note.

- **`audit/`** — 16 checks run during a single validation session
  against a draft manuscript. They surfaced five corrections (F1–F5)
  that were applied to the implementation and the paper; the check
  outputs are recorded verbatim in `audit/README.md`, together with the
  section-by-section map to the paper.

Both directories are excluded from pytest discovery via
`norecursedirs` in `pyproject.toml`. Neither is maintained.

## See also

- `../reproducibility/` — scripts that reproduce the published results
  (maintained).
- `../tests/` — formal test suite of the package.
- `../docs/adr/0004-test-layout.md` — the ADR that fixed this layout.
