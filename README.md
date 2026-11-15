# canonJAM
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23471387.svg)](https://doi.org/10.5281/zenodo.23471387)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
[![Tests](https://github.com/edgar-castillo-sci/canonJAM/actions/workflows/tests.yml/badge.svg)](https://github.com/edgar-castillo-sci/canonJAM/actions/workflows/tests.yml)
![License](https://img.shields.io/badge/license-MIT-green)

*[Leer en español](README.es.md)*

Canonicalization of JAM chains (options 1–8) for duplicate detection
in layered structures. Implements the JAM instance of the columnar
G-sets framework (`P = S₃`, `K = ℤ/2`, `r = 3`, `k ≥ 2`); does **not**
implement the general framework. Runtime depends only on `numpy`.

## Author

Edgar Castillo (Independent Researcher)

## Scientific basis

The JAM notation is described in:

> Arcudia, J., Ortiz-Chi, F., Sanchez-Valenzuela, A., Aspuru-Guzik, A.,
> Merino, G. (2023). "Joining and arrangement of multilayers: A string
> representation for honeycomb layered materials." *Matter*, 6(5),
> 1503–1513. doi: [10.1016/j.matt.2023.02.014](https://doi.org/10.1016/j.matt.2023.02.014)

## Install

```bash
pip install -e .
pip install -e ".[tests]"   # for the test suite
```

## Quickstart

```python
from canonjam import canonical_key, canonical_key_fast, filter_duplicates
import numpy as np

# A 3-layer structure
a = np.array([['+0', '+j', '+j'],
              ['+0', '+j', '+j'],
              ['+0', '+j', '+j']])

# Literal computation: 12 group evaluations
print(canonical_key(a, optionx=1))

# Optimal computation: 2 evaluations, O(k)
print(canonical_key_fast(a, optionx=1))

# Filter a list of structures in O(m) instead of O(m²)
unique = filter_duplicates([a, a, a], optionx=1)
print(len(unique))   # 1
```

## Public API

| Function | Purpose |
|---|---|
| `canonical_key(a, option)` | Literal definition: minimum over 12 group elements |
| `canonical_key_fast(a, option)` | Optimal computation: column sorting, 2 evaluations |
| `filter_duplicates(list, option)` | Deduplicate a list via canonical keys |
| `rows_for_option(option)` | All valid single-layer rows for options 1–8 |
| `rot`, `transp`, `flip`, `sign`, `sort_cols`, `elements_S3` | Group operations |
| `array_to_chain`, `chain_to_array` | Conversion between matrix and JAM string |

The full API surface is listed in [`DESIGN.md`](DESIGN.md#public-api-surface).

## Self-contained vs. `xjam2`

`canonJAM` does **not** depend on `xjam2`, and does **not** vendor or
modify its code. Only two places use `xjam2`, and both are optional:

- `tests/comparison/` — manual validation against the original
  pairwise method. Requires `xjam2`; fails with a clear message if
  missing.
- `examples/x_canonical.py` — optional integration example
  (monkey-patches `xjam2`'s public API).

See [`tests/comparison/README.md`](tests/comparison/README.md) for
installation instructions.

## What's in this repo

| Directory | Purpose |
|---|---|
| `canonjam/` | The package |
| `tests/` | Formal test suite (pytest) |
| `tests/comparison/` | Manual validation against `xjam2` (optional) |
| `reproducibility/` | Scripts that reproduce published counts and closed forms |
| `examples/` | Usage examples |
| `historical/` | Discovery and audit scripts (not maintained) |
| `docs/` | ADRs and conventions |

## Related artifacts

- Paper: *Canonical Forms and Burnside Enumeration for Columnar
  G-Sets* — forthcoming.
- Lean 4 formalization: `columnar-gsets` — forthcoming.

## Cite this repository

See [`CITATION.cff`](CITATION.cff). Concept DOI
[10.5281/zenodo.23471387](https://doi.org/10.5281/zenodo.23471387)
always resolves to the latest version.

## License

MIT (see [`LICENSE`](LICENSE)).
