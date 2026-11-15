# tests/

Formal test suite of `canonJAM`. Only `test_*.py` files are collected by
pytest. Run with:

```bash
pip install -e ".[tests]"
pytest -v
```

## Contents

- **`test_canonical.py`** — formal tests of the public API:
  group order, array↔chain roundtrip, canonical key invariance,
  duplicate filtering, sign operation, basic group operations.
- **`test_canonical_fast.py`** — parametrized check that
  `canonical_key_fast(a, option) == canonical_key(a, option)` for all
  eight JAM options and `n=2,3`.
- **`comparison/`** — scripts that compare the canonical filter against
  the original pairwise method of the JAM framework. **Require `xjam2`**
  (optional, not a dependency). See `comparison/README.md`.

## Out of scope

- **`reproducibility/`** — scripts that reproduce the published counts
  and closed forms of the paper. Self-contained (numpy + canonJAM only),
  not collected by pytest. See `../reproducibility/README.md`.
- **`historical/`** — discovery and audit scripts that preceded the
  current implementation. Not maintained. See `../historical/README.md`.
- **`examples/`** — usage examples (`pipeline.py` self-contained,
  `x_canonical.py` requires `xjam2`). See `../examples/README.md`.
