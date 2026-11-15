"""Class counts against Table 1 of [Arcudia2023].

For each of the 8 JAM options and n = 2..5, computes the number of
canonical classes and compares against Table 1 of [Arcudia2023]. Uses
the canonical filter for intermediate deduplication, making n = 5
feasible.

Usage
-----
    python3 validation_table1.py

The script prints, per option and per n, the computed count and the
expected count, with a PASS/FAIL mark.

Self-contained: numpy + canonjam only. Does not require xjam2.
"""

import numpy as np

from canonjam import filter_duplicates, rows_for_option

# Class counts from Table 1 of [Arcudia2023].
TABLE1 = {
    1: {2: 2, 3: 4, 4: 10, 5: 25},
    2: {2: 5, 3: 21, 4: 120, 5: 666},
    3: {2: 5, 3: 21, 4: 120, 5: 666},
    4: {2: 16, 3: 144, 4: 1776, 5: 20736},
    5: {2: 5, 3: 21, 4: 120, 5: 666},
    6: {2: 5, 3: 21, 4: 120, 5: 666},
    7: {2: 16, 3: 144, 4: 1776, 5: 20736},
    8: {2: 16, 3: 144, 4: 1776, 5: 20736},
}


def generate_candidates_canonical(n, option):
    """Generate candidates for n layers, filtering at each level.

    Uses the canonical filter for intermediate deduplication, making
    n = 5 feasible. The candidate set at level n is returned before the
    final filtering.

    Parameters
    ----------
    n : int
        Number of layers, >= 2.
    option : int
        JAM option in 1..8.

    Returns
    -------
    list of numpy.ndarray
        All candidate chains at level n, before the final filtering.
    """
    single = [np.array(r) for r in rows_for_option(option)]
    uniques = single.copy()
    candidates = single
    for level in range(2, n + 1):
        if level == 2:
            candidates = [
                np.vstack([a, b]) for a in uniques for b in single
            ]
        else:
            down = [np.vstack([a, b]) for a in uniques for b in single]
            up = [np.vstack([b, a]) for a in uniques for b in single]
            candidates = down + up
        uniques = filter_duplicates(candidates, option)
    return candidates


if __name__ == "__main__":
    for option in range(1, 9):
        print(f"Option {option}:", flush=True)
        for n in [2, 3, 4, 5]:
            candidates = generate_candidates_canonical(n, option)
            unique = filter_duplicates(candidates, option)
            expected = TABLE1[option][n]
            mark = "PASS" if len(unique) == expected else "FAIL"
            print(
                f"  n={n}: {len(unique)} (expected {expected}) {mark}",
                flush=True,
            )
