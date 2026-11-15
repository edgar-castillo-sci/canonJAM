"""Literal vs optimal computation of the canonical key.

The canonical key kappa(a) can be computed in two ways:

  1. Literal: minimum over the 12 elements of the symmetry group G.
     Cost: 12 group evaluations, O(k) each.
  2. Optimal: minimum of the sorted-column concatenations of a and of
     v(a), where v is the non-trivial element of the Z/2 factor
     (flip for planar options, sign . flip for buckled options).
     Cost: 2 evaluations, O(k) each.

This script verifies that the two computations agree for all 8 JAM
options and n = 2, 3, i.e. that kappa == kappa' as stated in the paper.

Usage
-----
    python3 kappa_equal_kappa_prime.py

Self-contained: numpy + canonjam only. Does not require xjam2.
"""

from itertools import product

import numpy as np

from canonjam import rows_for_option
from canonjam.canonical import array_to_chain, flip, generate_group, sign


def all_chains(n, option):
    """Yield all chains of n layers for the given option.

    Parameters
    ----------
    n : int
        Number of layers, >= 2.
    option : int
        JAM option in 1..8.

    Yields
    ------
    numpy.ndarray
        A k x 3 array of tokens.
    """
    single = [tuple(r) for r in rows_for_option(option)]
    for combo in product(single, repeat=n):
        yield np.array(combo, dtype=object)


def v_of(a, option):
    """Apply the non-trivial element of the Z/2 factor.

    ``flip`` for planar options (1, 2, 5), ``sign . flip`` for buckled
    options (3, 4, 6, 7, 8).

    Parameters
    ----------
    a : numpy.ndarray
        A k x 3 array of tokens.
    option : int
        JAM option in 1..8.

    Returns
    -------
    numpy.ndarray
        The image of ``a`` under ``v``.
    """
    if option in [1, 2, 5]:
        return flip(a.copy())
    return sign(flip(a.copy()))


def sort_cols(a):
    """Return a copy of ``a`` with its columns sorted lexicographically.

    Parameters
    ----------
    a : numpy.ndarray
        A k x 3 array of tokens.

    Returns
    -------
    numpy.ndarray
        A new array of the same shape with sorted columns.
    """
    cols = sorted([tuple(a[:, i]) for i in range(3)])
    return np.array(cols).T


def kappa_literal(a, option):
    """Compute the canonical key via the 12 group evaluations.

    Parameters
    ----------
    a : numpy.ndarray
        A k x 3 array of tokens.
    option : int
        JAM option in 1..8.

    Returns
    -------
    str
        The canonical key.
    """
    G = generate_group(option)
    return min(array_to_chain(g(a.copy())) for g in G)


def kappa_fast(a, option):
    """Compute the canonical key via the column-sorting trick.

    Parameters
    ----------
    a : numpy.ndarray
        A k x 3 array of tokens.
    option : int
        JAM option in 1..8.

    Returns
    -------
    str
        The canonical key.
    """
    return min(
        array_to_chain(sort_cols(a)),
        array_to_chain(sort_cols(v_of(a, option))),
    )


if __name__ == "__main__":
    ok = True
    for option in range(1, 9):
        for n in [2, 3]:
            for a in all_chains(n, option):
                if kappa_literal(a, option) != kappa_fast(a, option):
                    print(f"MISMATCH option={option} n={n} "
                          f"a={array_to_chain(a)}")
                    ok = False
    if ok:
        print("kappa == kappa' for all options and n=2,3")
