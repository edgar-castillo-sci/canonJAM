# historical/exploration/

Scripts from the discovery phase that preceded the current
implementation. They are kept in-tree for historical traceability only.

**Not part of the library's test suite.** May break without notice.

## Contents

### BPL/BU G-set isomorphism (Prop. 4.19 of the paper)

Scripts that construct and verify the bijection between `X_2^BPL` and
`X_2^BU`, and its blockwise extension to even `n`:

| Script | Purpose |
|---|---|
| `build_bijection.py` | First attempt: match orbits by exact stabilizer index set |
| `build_bijection_exact.py` | Find a chain with a given exact stabilizer in the other option |
| `build_bijection_v2.py` | Match orbits by conjugacy class of stabilizer (more robust) |
| `verify_bijection.py` | Verify the bijection is well-defined, injective, surjective, and equivariant (n = 2) |
| `verify_bijection_n4.py` | Same for n = 4, using the blockwise extension |
| `block_product_equiv.py` | Verify the blockwise extension is equivariant for n = 2, 4, 6 |
| `pattern_search.py` | Search for a general pattern for the blockwise extension |

### Classification of X_n as a G-set

Scripts that explore how the chain set X_n decomposes into orbits of the
symmetry group, by orbit size and by stabilizer type:

| Script | Purpose |
|---|---|
| `orbit_sizes.py` | Orbit size distribution for BPL and BU at n = 2, 4 |
| `stabilizer_types.py` | Stabilizer distribution (exact index sets) |
| `stabilizer_conjclasses.py` | Stabilizer distribution (conjugacy classes) |

### Benchmarking (moved here from `tests/`)

| Script | Purpose |
|---|---|
| `benchmark_fast.py` | Compare `filter_duplicates` (literal key) vs a fast filter using `canonical_key_fast` |
| `benchmark_fast.csv` | Output of one run of `benchmark_fast.py` (option 7, k = 5) |

## Status

These scripts **are not re-executable as-is** in the current layout.
They were written for `tests/exploration/` (one level below the
repository root), where `sys.path.insert(0, os.path.dirname(__file__))`
correctly pointed to the exploration directory. Now they live in
`historical/exploration/` (two levels below), so the `sys.path` insert
points one level short of the repository root. `from canonjam import
...` may therefore fail unless `canonJAM` is installed (e.g.,
`pip install -e .` from the repository root).

They are preserved for reference: the paper records the results they
produced, and the git log records how the bijection was found.

## See also

- `../audit/README.md` — validation session against a draft manuscript,
  findings F1-F5, applied to the paper.
- `../../reproducibility/README.md` — scripts that reproduce the
  published results (maintained).
- `../../tests/` — formal test suite of the package.
