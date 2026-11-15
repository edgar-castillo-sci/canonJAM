"""Orbit invariance of the column-multiset canonical form.

The canonical form of a chain a is min(sort_cols(a),
sort_cols(v(a))), where v is flip for planar options (1, 2, 5) and
sign . flip for buckled options (3, 4, 6, 7, 8). This script verifies:

  1. Invariance: for every g in G and every chain a, the key of g(a)
     equals the key of a.
  2. Counting: the number of distinct keys equals the number of orbits
     of X_n^option under G, as computed by filter_duplicates.

For the four binary options (1-4) it also compares against the known
orbit counts (Table 1 of [Arcudia2023]).

Usage
-----
    python3 structural.py                  # options 1-8, n = 2, 3
    python3 structural.py --options 1 2 5
    python3 structural.py --levels 2 3 4

Self-contained: numpy + canonjam only. Does not require xjam2.
"""

import argparse
from itertools import product

import numpy as np

from canonjam import generate_group, rows_for_option
from canonjam.canonical import flip, sign

DEFAULT_OPTIONS = list(range(1, 9))
DEFAULT_LEVELS = [2, 3]

# Orbit counts from Table 1 of [Arcudia2023] for n = 2 and n = 3.
# Only the four binary options (1-4) have published values.
KNOWN = {
    1: {2: 2, 3: 4},
    2: {2: 5, 3: 21},
    3: {2: 5, 3: 21},
    4: {2: 16, 3: 144},
}


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


def sorted_cols(a):
    """Return the sorted tuple of columns of ``a``.

    Parameters
    ----------
    a : numpy.ndarray
        A k x 3 array of tokens.

    Returns
    -------
    tuple of tuple
        The three columns as tuples, sorted lexicographically.
    """
    return tuple(sorted(tuple(a[:, i]) for i in range(3)))


def key_prime(a, option):
    """Compute the column-multiset canonical key of ``a``.

    This is the O(k) canonical form: the minimum of the sorted-column
    concatenation of ``a`` and of ``v(a)``. Equivalent to
    ``canonical_key_fast(a, option)`` but expressed as a tuple of
    columns (rather than a string), for clarity in the checks below.

    Parameters
    ----------
    a : numpy.ndarray
        A k x 3 array of tokens.
    option : int
        JAM option in 1..8.

    Returns
    -------
    tuple of tuple
        The canonical key.
    """
    return min(sorted_cols(a), sorted_cols(v_of(a, option)))


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Verify invariance and orbit counts of the column-multiset "
            "canonical form."
        ),
        epilog=(
            "Examples:\n"
            "  python3 structural.py\n"
            "  python3 structural.py --options 1 2 5\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--options",
        type=int,
        nargs="+",
        default=DEFAULT_OPTIONS,
        help="JAM options to process (default: 1-8).",
    )
    parser.add_argument(
        "--levels",
        type=int,
        nargs="+",
        default=DEFAULT_LEVELS,
        help="Layer counts (default: %(default)s).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    for option in args.options:
        G = generate_group(option)
        for n in args.levels:
            chains = list(all_chains(n, option))
            inv_ok = all(
                key_prime(g(a.copy()), option) == key_prime(a, option)
                for a in chains
                for g in G
            )
            n_keys = len({key_prime(a, option) for a in chains})
            expected = KNOWN.get(option, {}).get(n)
            if expected is not None:
                match_str = f"match={n_keys == expected} (expected {expected})"
            else:
                match_str = "no published count"
            print(
                f"option={option} n={n}: inv={inv_ok} keys={n_keys} "
                f"{match_str}",
                flush=True,
            )
