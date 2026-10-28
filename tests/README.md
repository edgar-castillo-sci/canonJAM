# Tests and reproducibility scripts

This directory contains four kinds of scripts:

1. A **formal test suite** (`test_canonical.py`, `test_canonical_fast.py`)
   that validates the package itself. Does not require `xjam2`.
2. **Self-contained reproducibility scripts** for the theoretical
   results of the paper. Do not require `xjam2`.
3. **Comparison scripts** under `comparison/` that check the canonical
   filter against the original pairwise method of the JAM framework.
   **Require `xjam2`.** See `comparison/README.md` for details.
4. An **exploration** subdirectory (`exploration/`) with scripts used to
   construct and verify the BPL/BU G-set isomorphism and to explore the
   classification of G-sets. Not part of the reproducibility suite.

## Requirements

The formal test suite, the self-contained reproducibility scripts, and
the exploration scripts depend only on `numpy` and `canonjam`.

The three scripts under `comparison/` require `xjam2`, which is an
optional third-party package and is not distributed with canonJAM. See
`comparison/README.md` for installation instructions.

## Running the formal tests

```bash
cd ..
pip install -e ".[tests]"
pytest tests/test_canonical.py tests/test_canonical_fast.py -v
```

## Self-contained reproducibility scripts

These scripts reproduce the empirical checks of the paper using only
`numpy` and `canonjam`. Run any of them from the repository root or from
this directory.

### `validation_table1.py`

Checks the class counts against Table 1 of [Arcudia2023] for n=2,3,4,5
on all 8 options.

```bash
python3 validation_table1.py
```

### `scalability.py`

Scalability experiment for the planar case up to n=12. Uses the
canonical filter for intermediate deduplication, which is what makes
generation feasible at that scale.

```bash
python3 scalability.py
```

Expected output (approximately):
```
n=6:  m=150,     classes=70,     gen=0.05s, filter=0.03s
n=8:  m=1,176,   classes=574,    gen=0.41s, filter=0.27s
n=10: m=10,086,  classes=5,002,  gen=3.66s, filter=2.42s
n=12: m=89,304,  classes=44,530, gen=34.68s, filter=22.77s
```

### `recursion_check.py`

Verifies that the closed forms derived via Burnside's lemma agree with
the recursive formulas of [Arcudia2023] for n=2..30, for PL, BPL/BU,
and BBU.

```bash
python3 recursion_check.py
```

Expected output: `All match for N=2..30 (PL, BPL/BU, BBU)`.

### `burnside.py`, `burnside_all.py`

Compute the fixed-point counts \(|Fix(g)|\) for each conjugacy class of
\(G = S_3 \times \mathbb{Z}/2\). `burnside.py` covers PL; `burnside_all.py`
covers all 8 options.

```bash
python3 burnside.py
python3 burnside_all.py
```

### `structural.py`, `structural_all.py`

Verify that \(a \sim b\) iff the column multisets of \(a\) and \(b\)
coincide, or the column multiset of \(a\) equals that of \(v(b)\).
`structural.py` covers options 1–4; `structural_all.py` covers all 8
options.

```bash
python3 structural.py
python3 structural_all.py
```

### `kappa_equal_kappa_prime.py`

Verifies that the literal minimum over the 12 group elements equals the
\(O(k)\)-with-constant-2 computation. Covers all 8 options for n=2,3.

```bash
python3 kappa_equal_kappa_prime.py
```

Expected output: `kappa == kappa' for all options and n=2,3`.

## Comparison scripts (`comparison/`)

These scripts compare the canonical filter against the original
pairwise method of the JAM framework. They **require `xjam2`** (see
`comparison/README.md`).

### `comparison/validation.py`

Validates the canonical method against the original pairwise method for
all 8 JAM options, verifying that both produce the same equivalence
classes.

```bash
python3 comparison/validation.py
python3 comparison/validation.py --levels 2 3 4
```

Options:
- `--levels`: layer counts to validate (default: `2 3`).
  `n=2` and `n=3` are sufficient. `n>=4` is slow for the original method.
  `n>=5` is prohibitively slow.

### `comparison/full_report.py`

Generates a detailed report with all canonical keys produced by each
method, side by side.

```bash
python3 comparison/full_report.py
python3 comparison/full_report.py --levels 2 3 4 --output /tmp/report.txt
```

Options:
- `--levels`: layer counts to report (default: `2 3`).
- `--output`: output file path (default: `full_report_salida.txt`).

### `comparison/benchmark.py`

Measures the filtering time of both methods. The original method is
O(m²), so it is measured only while its estimated time stays below
`--max-time` (default: 30 s). Above that threshold, only the canonical
method is measured.

```bash
python3 comparison/benchmark.py
python3 comparison/benchmark.py --options 1 5 --levels 2 3 4 5 --max-time 60
```

Options:
- `--levels`: layer counts to benchmark (default: `2 3 4 5`).
- `--options`: JAM options to benchmark (default: `1 5 7`).
- `--max-time`: max estimated time for the original method, in seconds
  (default: 30).
- `--output`: output TSV file path (default: `benchmark_salida.tsv`).

## Exploration scripts (`exploration/`)

These scripts were used to construct and verify the BPL/BU G-set
isomorphism and to explore the classification of \(X_n^{\tau}\) as a
\(G\)-set. They are not part of the reproducibility suite, but are kept
for future work on canonical augmentation and on the classification of
\(G\)-sets.

| Script | Purpose |
|---|---|
| `build_bijection.py`, `build_bijection_v2.py`, `build_bijection_exact.py` | Construct the bijection \(\varphi_2\) between \(X_2^{BPL}\) and \(X_2^{BU}\) |
| `verify_bijection.py`, `verify_bijection_n4.py` | Verify that \(\varphi_2\) (and \(\varphi_4 = \varphi_2^{\otimes 2}\)) are \(G\)-equivariant bijections |
| `block_product_equiv.py` | Verify that \(\varphi_2^{\otimes m}\) is \(G\)-equivariant for m up to 3 |
| `orbit_sizes.py` | Compute the distribution of orbit sizes for BPL and BU |
| `stabilizer_types.py`, `stabilizer_conjclasses.py` | Compare the stabilizer distributions of BPL and BU |
| `pattern_search.py` | Search for a general pattern for \(\varphi_{2m}\) |

## Exit codes

All scripts exit with:
- `0` if all validations pass (or the experiment completes without error).
- `1` if any validation fails.
