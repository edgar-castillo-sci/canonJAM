"""Tests for canonical_key_fast (optimal computation of κ via column sorting)."""

import itertools

import numpy as np
import pytest

from canonjam import canonical_key, canonical_key_fast, rows_for_option


def all_chains(n, option):
    rows = rows_for_option(option)
    for combo in itertools.product(rows, repeat=n):
        yield np.array(combo, dtype=object)


@pytest.mark.parametrize("option", range(1, 9))
def test_canonical_key_fast_matches_literal(option):
    """canonical_key_fast agrees with canonical_key."""
    for n in [2, 3]:
        for a in all_chains(n, option):
            fast = canonical_key_fast(a, option)
            literal = canonical_key(a, option)
            assert fast == literal, (
                f"Mismatch: option={option}, n={n}, "
                f"chain={a.tolist()}, fast={fast!r}, literal={literal!r}"
            )
