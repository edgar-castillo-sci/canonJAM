# historical/

Scripts from the discovery and audit phases that preceded the current
implementation. They are kept in-tree for historical traceability only.

**These are not part of the library's test suite.** They may reference old
APIs, may break without notice, and are not covered by CI.

## Subdirectories

- **`exploration/`** — scripts used to construct and verify the BPL/BU
  \(G\)-set isomorphism and to explore the classification of \(X_n^\tau\)
  as a \(G\)-set. These scripts informed the discovery phase that led to
  the current canonicalization method and to the paper that describes it.

- **`audit/`** — 16 checks run during a single validation session against
  a draft manuscript. They surfaced five corrections (F1–F5) that were
  subsequently folded into the implementation and the paper. See
  `audit/README.md` for the per-check map and the list of findings.

Both directories are excluded from pytest discovery via
`norecursedirs` in `pyproject.toml`.
