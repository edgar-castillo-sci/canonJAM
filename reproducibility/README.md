# reproducibility/

Scripts that reproduce the published results of the paper using only
`numpy` and `canonJAM`. They are **not** part of the library's test suite
and are **not** collected by pytest.

Each script has a module docstring identifying which result of the paper
it reproduces (Table number, theorem, or proposition). Run any of them
from this directory or from the repository root.

## Contents

| Script | Reproduces |
|---|---|
| `validation_table1.py` | Class counts of Table 1 of [Arcudia2023], n = 2..5, all 8 options |
| `recursion_check.py` | Closed forms (Theorem 5.5) vs recursive formulas (Table S1), n = 2..30 |
| `scalability.py` | Scalability experiment, planar case, n = 6..12 |
| `burnside.py` | Fixed-point counts per conjugacy class (Table 5.2), and orbit counts via Burnside's lemma |
| `structural.py` | Invariance and orbit counts of the column-multiset canonical form |
| `kappa_equal_kappa_prime.py` | Literal vs optimal computation of the canonical key (Theorem 4.10) |

## Usage

Each script can be run directly:

```bash
python3 validation_table1.py
python3 recursion_check.py
python3 scalability.py
python3 kappa_equal_kappa_prime.py
```

The two scripts that process multiple options and/or levels accept
`--options` and `--levels`:

```bash
# Fixed-point counts and orbit counts for options 1 and 2, n = 2, 3, 4
python3 burnside.py --options 1 2 --levels 2 3 4

# Invariance and orbit counts for options 1, 2, 5 (the planar options)
python3 structural.py --options 1 2 5 --levels 2 3
```

## Expected outputs

| Script | Expected final line |
|---|---|
| `validation_table1.py` | All options report `PASS` for n = 2..5 |
| `recursion_check.py` | `All match for N=2..30 (PL, BPL/BU, BBU)` |
| `scalability.py` | 4 lines, one per n (see example below) |
| `kappa_equal_kappa_prime.py` | `kappa == kappa' for all options and n=2,3` |
| `burnside.py` | One line per (option, n) with `|Fix|`, sum, and `orbits` |
| `structural.py` | One line per (option, n) with `inv=True` and `match=True` |

`scalability.py` takes about 30 seconds at n = 12. Approximate output:

```
n=6:  m=150,     classes=70,     gen=0.05s, filter=0.03s
n=8:  m=1,176,   classes=574,    gen=0.41s, filter=0.27s
n=10: m=10,086,  classes=5,002,  gen=3.66s, filter=2.42s
n=12: m=89,304,  classes=44,530, gen=34.68s, filter=22.77s
```

## Relationship to the paper

`canonJAM` implements the **JAM instance** of the columnar G-sets
framework. These scripts reproduce the numerical claims of the paper for
the JAM instance only. The general framework (arbitrary column group
`P <= S_r`, arbitrary alphabet group `K`) is the subject of a separate
artifact (a Lean 4 formalization).

## Relationship to `tests/` and `historical/`

- `tests/` contains the **formal test suite** of the package. It is
  collected by pytest and verifies the public API.
- `tests/comparison/` contains scripts that compare the canonical method
  against the **original pairwise method**. They require `xjam2`
  (optional, not a dependency). See `tests/comparison/README.md`.
- `historical/` contains **discovery and audit scripts** from the phase
  that preceded the current implementation. They are not maintained.
  See `historical/README.md`.

## Requirements

Only `numpy` and `canonJAM`. None of these scripts requires `xjam2`.

To run them, install the package in editable mode from the repository
root:

```bash
pip install -e .
```

Then run any script from this directory:

```bash
python3 validation_table1.py
```
