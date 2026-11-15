"""canonJAM — canonicalization of JAM chains for duplicate detection.

This package implements the **JAM instance** of the columnar G-sets
framework: canonicalization of JAM chains for the eight canonical options
(options 1–8), with symmetry group ``G = S₃ × ℤ/2`` (order 12), column
count ``r = 3``, and layer count ``k ≥ 2``.

Given a ``k × 3`` array of tokens (a "chain"), the package provides:

- **Canonical keys** (`canonical_key`, `canonical_key_fast`): a string
  invariant under the symmetry group. Two chains are equivalent if and
  only if they have the same key.
- **Duplicate filtering** (`filter_duplicates`): O(m) duplicate
  detection using canonical keys as dictionary keys, instead of the O(m²)
  of pairwise comparison.
- **Group operations** (`rot`, `transp`, `flip`, `sign`, `sort_cols`,
  `elements_S3`, `generate_group`): the generators of G, exposed for
  users who want to construct the group explicitly or compose operations
  by hand.
- **Chain conversion** (`array_to_chain`, `chain_to_array`): the bridge
  between the array representation (used for manipulation) and the
  string representation (used for hashing and lexicographic comparison).
- **Option data** (`rows_for_option`, `base_sets_for_option`,
  `base_tokens_for_option`): the single-layer row sets for the eight
  canonical options, self-contained in the package.

Scope
-----

This package implements **only** the JAM instance of columnar G-sets:
``P = S₃``, ``K = ℤ/2``, ``r = 3``, ``k ≥ 2``, options 1–8. It does not
implement the general framework (arbitrary ``P ≤ S_r``, arbitrary
``K``, ``r ≠ 3``); that is the subject of a separate artifact (a Lean 4
formalization). See ``DESIGN.md`` and ADR-0001 in ``docs/adr/`` for the
full rationale.

Runtime dependency: ``numpy`` only. The package does **not** depend on
``xjam2`` (the original JAM framework); scripts that optionally use
``xjam2`` for comparison are under ``tests/comparison/`` and
``examples/x_canonical.py``.

See Also
--------
- ``DESIGN.md``: architecture, public API surface, and "what this is
  NOT".
- ``docs/adr/``: the five Architectural Decision Records.
- ``docs/conventions.md``: project conventions.

Examples
--------
Basic usage: canonicalize a 3-layer structure and filter duplicates.

>>> import numpy as np
>>> from canonjam import canonical_key, filter_duplicates
>>> a = np.array([['+0', '+j', '+j'], ['+0', '+j', '+j'], ['+0', '+j', '+j']])
>>> key = canonical_key(a, optionx=1)
>>> isinstance(key, str)
True
>>> len(filter_duplicates([a, a, a], optionx=1))
1
"""

from .canonical import (
    array_to_chain,
    canonical_key,
    canonical_key_fast,
    chain_to_array,
    elements_S3,
    filter_duplicates,
    flip,
    generate_group,
    rot,
    sign,
    sort_cols,
    transp,
)
from .options import (
    base_sets_for_option,
    base_tokens_for_option,
    rows_for_option,
)

__all__ = [
    "array_to_chain",
    "base_sets_for_option",
    "base_tokens_for_option",
    "canonical_key",
    "canonical_key_fast",
    "chain_to_array",
    "elements_S3",
    "filter_duplicates",
    "flip",
    "generate_group",
    "rot",
    "rows_for_option",
    "sign",
    "sort_cols",
    "transp",
]

__version__ = "1.3.0"
