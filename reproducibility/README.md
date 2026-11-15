# reproducibility/

Scripts that reproduce the published results of the paper using only
`numpy` and `canonJAM`. They are **not** part of the library's test suite
and are **not** collected by pytest.

## Contents

| Script | Reproduces |
|---|---|
| `validation_table1.py` | Class counts of Table 3 (n=2,3,4,5) |
| `recursion_check.py` | Closed forms vs. recursive formulas, n=2..30 |
| `scalability.py` | Scalability experiment, planar, n=6..12 |
| `burnside.py`, `burnside_all.py` | Fixed-point counts per conjugacy class |
| `structural.py`, `structural_all.py` | Orbits vs. column multisets |
| `kappa_equal_kappa_prime.py` | Literal vs. optimal computation of κ |

All scripts run from this directory or from the repository root:

```bash
python3 reproducibility/validation_table1.py
```

For scripts that compare against the original pairwise method of the JAM
framework, see `tests/comparison/` (they require `xjam2`). For scripts
from the pre-paper discovery phase, see `historical/`.
