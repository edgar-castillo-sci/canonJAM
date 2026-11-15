"""Fixed-point counts per conjugacy class of G = S3 x Z/2.

For each option and each n, computes |Fix(g)| for each of the 12
elements g of G acting on the chain set X_n^option, and the orbit count
via Burnside's lemma (sum of |Fix(g)| divided by |G| = 12).

Reproduces the fixed-point table of the paper (Table 5.2 for the four
binary options, with the values for n = 2 and n = 3) and the orbit
counts of Table 1 of [Arcudia2023] for n = 2..5.

Usage
-----
    python3 burnside.py                    # options 1-4, n = 2..5
    python3 burnside.py --options 1 2      # only options 1 and 2
    python3 burnside.py --levels 2 3 4     # only n = 2, 3, 4

Self-contained: numpy + canonjam only. Does not require xjam2.
"""

import argparse
from itertools import product

import numpy as np

from canonjam import generate_group, rows_for_option

DEFAULT_OPTIONS = [1, 2, 3, 4]
DEFAULT_LEVELS = [2, 3, 4, 5]


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


def burnside_table(n, option):
    """Compute |Fix(g)| for each group element, and the Burnside sum.

    Parameters
    ----------
    n : int
        Number of layers, >= 2.
    option : int
        JAM option in 1..8.

    Returns
    -------
    tuple
        ``(counts, total, orbits)``, where ``counts`` is a list of 12
        integers (one per group element in the order of
        ``generate_group(option)``), ``total`` is their sum, and
        ``orbits`` is ``total // 12`` (Burnside's lemma).
    """
    G = generate_group(option)
    counts = [0] * len(G)
    for a in all_chains(n, option):
        for i, g in enumerate(G):
            if np.array_equal(g(a.copy()), a):
                counts[i] += 1
    total = sum(counts)
    orbits = total // len(counts)
    return counts, total, orbits


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Fixed-point counts per conjugacy class of G = S3 x Z/2, "
            "for each JAM option and each number of layers."
        ),
        epilog=(
            "Examples:\n"
            "  python3 burnside.py\n"
            "  python3 burnside.py --options 1 2 --levels 2 3 4\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--options",
        type=int,
        nargs="+",
        default=DEFAULT_OPTIONS,
        help=(
            "JAM options to process (default: %(default)s). "
            "Options 1-4 are the binary options; 5-8 are the extended "
            "options."
        ),
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
        print(f"Option {option}:")
        for n in args.levels:
            counts, total, orbits = burnside_table(n, option)
            print(f"  n={n:2d}  |Fix| = {counts}  sum = {total:8d}  "
                  f"orbits = {orbits}", flush=True)
