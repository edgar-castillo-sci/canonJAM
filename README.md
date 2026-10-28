# canonJAM
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23471387.svg)](https://doi.org/10.5281/zenodo.23471387)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Tests](https://img.shields.io/badge/tests-33%20passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

*[Leer en español](README.es.md)*

Canonicalization method for duplicate detection in layered structures
represented with the JAM notation.

## Author

Edgar Castillo (Independent Researcher)

## Scientific basis

The JAM notation is described in:

> Arcudia, J., Ortiz-Chi, F., Sanchez-Valenzuela, A., Aspuru-Guzik, A.,
> Merino, G. (2023). "Joining and arrangement of multilayers: A string
> representation for honeycomb layered materials." Matter, 6(5),
> 1503–1513. doi: 10.1016/j.matt.2023.02.014

canonJAM itself is self-contained: it depends only on `numpy` at
runtime. It does **not** require `xjam2`, and it does **not** vendor or
modify any xjam2 code.

`xjam2` is used only by:

- the comparison scripts in `tests/comparison/`, which check the
  canonical filter against the original pairwise method;
- the optional integration example `examples/x_canonical.py`.

Those scripts fail with a clear message if `xjam2` is missing.

> **Note on the formalization.** The PDF in `docs/` is the initial
> formalization of the method. The current implementation reflects a
> later correction (confirmed by Dr. Jessica Arcudia): for buckled
> options, the vertical symmetry is the composition `sign·flip`, not
> `sign` and `flip` independently. The group for all options has order
> 12. See `canonjam/canonical.py` and the section "The symmetry
> group" below for the current version.

## Installation

```bash
pip install -e .
```

For running the formal tests:

```bash
pip install -e ".[tests]"
```

`xjam2` is **not** installable via PyPI. The comparison scripts and the
integration example expect it on `PYTHONPATH` or installed from source;
see `tests/comparison/README.md`.

## Usage

```python
from canonjam import canonical_key, canonical_key_fast, filter_duplicates
import numpy as np

# A 3-layer structure
a = np.array([['+0', '+j', '+j'],
              ['+0', '+j', '+j'],
              ['+0', '+j', '+j']])

# Literal computation: 12 group evaluations
key = canonical_key(a, optionx=1)
print(key)

# Optimal computation: 2 evaluations, O(k)
key = canonical_key_fast(a, optionx=1)
print(key)

# Filter a list of structures
unique = filter_duplicates([a, a, a], optionx=1)
print(len(unique))
```

## What it does

JAM generates all possible stacking configurations for an n-layer
system. Many of them are equivalent under symmetry (column rotation,
column swap, layer inversion). The original method detects duplicates
by pairwise comparison, which is O(m²). This package replaces that
with a dictionary of canonical keys, which is O(m).

The canonical key of a structure is the lexicographic minimum of its
orbit under the symmetry group. Two equivalent structures produce the
same key.

The package provides two implementations:

- `canonical_key`: the literal definition (minimum over the 12 group
  elements). Used in the benchmarks for direct correspondence with the
  theory.
- `canonical_key_fast`: the optimal computation via column sorting
  (minimum of the sorted-column concatenations of the chain and its
  v-image). O(k) with a constant of 2. Verified to agree with
  `canonical_key` for all 8 options and n=2,3.

## The symmetry group

For option 1 (planar monoelemental), option 2 (planar binary), and
option 5 (planar with an extended site-occupancy token):

    G = S3 × {e, flip}

For options 3, 4, 6, 7, 8 (buckled and Janus variants):

    G = S3 × {e, sign·flip}

In all cases, |G| = 12.

The vertical symmetry is the composition `sign·flip` (global reflection),
not `sign` and `flip` independently. This was confirmed by Dr. Jessica
Arcudia.

## Contents

- `canonjam/` — the package (`canonical.py`, `options.py`).
- `tests/` — formal test suite (`test_canonical.py`,
  `test_canonical_fast.py`) and self-contained reproducibility scripts
  (no `xjam2` required).
- `tests/comparison/` — scripts that compare against the original
  pairwise method. **Require `xjam2`.**
- `tests/exploration/` — exploratory scripts for the BPL/BU dichotomy
  and the classification of G-sets (companion work; self-contained).
- `examples/` — usage examples. `pipeline.py` is self-contained;
  `x_canonical.py` is the integration example and requires `xjam2`.
- `docs/` — formal mathematical description (PDF).

## Integration with xjam2 (monkey patching)

If you already have `xjam2` installed and want to use canonJAM as a
drop-in replacement for its pairwise filter, `examples/x_canonical.py`
shows how. It monkey-patches `disc_equivalents` in `xjam.libjamstd`
and `xjam.libjamtdm` to use `filter_duplicates` from canonJAM, then
runs `x.jam` from the current directory.

```bash
# 1. Install xjam2 (from source; it is not on PyPI)
pip install git+https://github.com/Theochem-merida/xjam2.git
# or:  export PYTHONPATH=/path/to/xjam2:$PYTHONPATH

# 2. From a directory with x.jam and JAM.inp:
python3 /path/to/canonJAM/examples/x_canonical.py
```

The canonical method performs both the `eqnum=1` and `eqnum=2` passes
in a single call, so `eqnum` is ignored by the replacement.

**Important:** this is a monkey patch of xjam2's public API. canonJAM
does not modify or vendor xjam2's source. If xjam2's internal API
changes, the patch may need updating. See `examples/README.md` for
details and caveats.

## Reproducing the theoretical results

### Self-contained (no `xjam2` required)

These scripts reproduce the class counts, the closed forms, the
structural theorems, and the κ = κ' check. They need only `numpy`
and `canonjam`.

| Script | Reproduces |
|---|---|
| `tests/validation_table1.py` | Class counts against Table 1 of [Arcudia2023] for n=4,5 |
| `tests/scalability.py` | Scalability experiment for n=6,8,10,12 (planar) |
| `tests/recursion_check.py` | Closed forms vs. recursive formulas up to n=30 |
| `tests/burnside.py`, `tests/burnside_all.py` | Fixed-point counts per conjugacy class |
| `tests/structural.py`, `tests/structural_all.py` | Orbits vs. column multisets |
| `tests/kappa_equal_kappa_prime.py` | Literal vs. optimal computation of κ |

Run any of them from the repository root:

```bash
python3 tests/validation_table1.py
python3 tests/scalability.py
python3 tests/recursion_check.py
```

### Comparison (require `xjam2`)

These scripts check the canonical filter against the original pairwise
method of the JAM framework. They require `xjam2`; see
`tests/comparison/README.md`.

| Script | Reproduces |
|---|---|
| `tests/comparison/validation.py` | Pairwise vs. canonical, per option and n |
| `tests/comparison/full_report.py` | Detailed key-by-key report |
| `tests/comparison/benchmark.py` | Filtering-time comparison |

## Running the formal tests

```bash
pytest tests/test_canonical.py tests/test_canonical_fast.py -v
```

## License

MIT (see `LICENSE`).
