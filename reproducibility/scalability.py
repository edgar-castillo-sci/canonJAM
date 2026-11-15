"""Scalability experiment for the planar case.

Generates canonical classes for the planar option (option 1) at
n = 6, 8, 10, 12, using the canonical filter for intermediate
deduplication (which is what makes generation feasible at that scale).
Reports the number of candidates, the number of canonical classes, and
the time spent in generation and filtering.

Usage
-----
    python3 scalability.py

The expected output is reported in reproducibility/README.md.

Self-contained: numpy + canonjam only. Does not require xjam2.
"""

import time

import numpy as np

from canonjam import filter_duplicates, rows_for_option


def gen_candidates_canonical(n, option):
    """Generate candidates for n layers, filtering at each level.

    Uses the canonical filter for intermediate deduplication, making
    high n values (>= 6) reachable in reasonable time.

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
    for n in [6, 8, 10, 12]:
        t0 = time.perf_counter()
        cands = gen_candidates_canonical(n, 1)
        t_gen = time.perf_counter() - t0
        m = len(cands)
        t0 = time.perf_counter()
        unique = filter_duplicates(cands, 1)
        t_filt = time.perf_counter() - t0
        print(
            f"n={n}: m={m}, classes={len(unique)}, "
            f"gen={t_gen:.2f}s, filter={t_filt:.2f}s",
            flush=True,
        )
