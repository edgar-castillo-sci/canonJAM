"""
Formal test suite for the canonjam package.

These tests are fast, deterministic, and do not measure time.
They verify the core properties of the canonicalization method:

  - The symmetry group has the expected size for every JAM option.
  - Array ↔ chain conversions are inverse.
  - Equivalent structures produce the same canonical key.
  - Non-equivalent structures produce different canonical keys.
  - Duplicate filtering collapses equivalent structures.
  - The sign operation behaves correctly on 2- and 6-character tokens.

Run with:

    pytest tests/test_canonical.py -v
"""

import numpy as np
import pytest

from canonjam import (
    array_to_chain,
    canonical_key,
    chain_to_array,
    elements_S3,
    filter_duplicates,
    flip,
    generate_group,
    rot,
    sign,
    transp,
)

# ─────────────────────────────────────────────
# Group
# ─────────────────────────────────────────────

@pytest.mark.parametrize("option", range(1, 9))
def test_group_has_12_elements(option):
    """Every JAM option has a symmetry group of order 12."""
    ops = generate_group(option)
    assert len(ops) == 12, f"option {option}: got {len(ops)} ops"


def test_elements_S3_has_6_elements():
    """S3 has 6 elements."""
    assert len(elements_S3()) == 6


# ─────────────────────────────────────────────
# Array ↔ chain
# ─────────────────────────────────────────────

def test_roundtrip_simple():
    """array_to_chain and chain_to_array are inverse (2-char tokens)."""
    a = np.array([['+0', '+j', '+j'], ['+0', '+j', '+j']])
    assert np.array_equal(chain_to_array(array_to_chain(a)), a)


def test_roundtrip_with_parentheses():
    """Roundtrip works with 6-character tokens."""
    a = np.array([['(+k-k)', '*j', '+0']])
    assert np.array_equal(chain_to_array(array_to_chain(a)), a)


def test_array_to_chain_example():
    """Known example: a 2-layer planar structure."""
    a = np.array([['+0', '+j', '+j'], ['+0', '+j', '+j']])
    assert array_to_chain(a) == "+0+0/+j+j/+j+j"


# ─────────────────────────────────────────────
# Canonical key
# ─────────────────────────────────────────────

def test_equivalent_structures_same_key():
    """Rotated structures produce the same canonical key."""
    a = np.array([['+0', '+j', '+j'], ['+0', '+j', '+j']])
    b = np.array([['+j', '+j', '+0'], ['+j', '+j', '+0']])
    assert canonical_key(a, 1) == canonical_key(b, 1)


def test_key_invariant_under_rot():
    """canonical_key(rot(a)) == canonical_key(a)."""
    a = np.array([['+0', '+j', '+j'], ['+j', '+0', '+j']])
    assert canonical_key(rot(a), 1) == canonical_key(a, 1)


def test_key_invariant_under_flip():
    """canonical_key(flip(a)) == canonical_key(a)."""
    a = np.array([['+0', '+j', '+j'], ['+j', '+0', '+j']])
    assert canonical_key(flip(a), 1) == canonical_key(a, 1)


def test_non_equivalent_structures_different_key():
    """Different structures produce different canonical keys."""
    a = np.array([['+0', '+j', '+j'], ['+0', '+j', '+j']])
    c = np.array([['+0', '+j', '+j'], ['+j', '+0', '+j']])
    assert canonical_key(a, 1) != canonical_key(c, 1)


# ─────────────────────────────────────────────
# Duplicate filtering
# ─────────────────────────────────────────────

def test_filter_duplicates_collapses_equivalents():
    """Equivalent structures collapse into one unique representative."""
    a = np.array([['+0', '+j', '+j'], ['+0', '+j', '+j']])
    b = np.array([['+j', '+j', '+0'], ['+j', '+j', '+0']])
    c = np.array([['+0', '+j', '+j'], ['+j', '+0', '+j']])
    unique = filter_duplicates([a, b, c], 1)
    assert len(unique) == 2


def test_filter_duplicates_keeps_all_distinct():
    """All distinct structures are kept."""
    a = np.array([['+0', '+j', '+j'], ['+0', '+j', '+j']])
    b = np.array([['+0', '+j', '+j'], ['+j', '+0', '+j']])
    unique = filter_duplicates([a, b], 1)
    assert len(unique) == 2


def test_filter_duplicates_empty_input():
    """Empty input returns empty output."""
    assert filter_duplicates([], 1) == []


# ─────────────────────────────────────────────
# Sign operation
# ─────────────────────────────────────────────

def test_sign_simple_tokens():
    """+j → -j, -j → +j, +0 unchanged, *j unchanged."""
    a = np.array([['+j', '-j', '+0', '*j']])
    expected = np.array([['-j', '+j', '+0', '*j']])
    assert np.array_equal(sign(a), expected)


def test_sign_parentheses_different_elements():
    """(+k-l) flips to (-k+l) because k != l."""
    a = np.array([['(+k-l)', '+0', '+0']])
    expected = np.array([['(-k+l)', '+0', '+0']])
    assert np.array_equal(sign(a), expected)


def test_sign_parentheses_same_elements():
    """(+k-k) stays the same because k == k."""
    a = np.array([['(+k-k)', '+0', '+0']])
    expected = np.array([['(+k-k)', '+0', '+0']])
    assert np.array_equal(sign(a), expected)


# ─────────────────────────────────────────────
# Basic operations (sanity checks)
# ─────────────────────────────────────────────

def test_rot_cycle():
    """rot applied three times is the identity."""
    a = np.array([['+0', '+j', '+k']])
    assert np.array_equal(rot(rot(rot(a))), a)


def test_transp_involution():
    """transp applied twice is the identity."""
    a = np.array([['+0', '+j', '+k']])
    assert np.array_equal(transp(transp(a)), a)


def test_flip_involution():
    """flip applied twice is the identity."""
    a = np.array([['+0', '+j', '+k'], ['+j', '+k', '+0']])
    assert np.array_equal(flip(flip(a)), a)
