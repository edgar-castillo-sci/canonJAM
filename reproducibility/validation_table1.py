import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import permutations
import numpy as np
from canonjam import filter_duplicates
from canonjam import rows_for_option

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
    """Same as validacion.generate_candidates, but uses the canonical
    filter for intermediate deduplication, making n=5 feasible."""
    single = [np.array(r) for r in rows_for_option(option)]
    uniques = single.copy()
    candidates = single
    for level in range(2, n + 1):
        if level == 2:
            candidates = [np.vstack([a, b]) for a in uniques for b in single]
        else:
            down = [np.vstack([a, b]) for a in uniques for b in single]
            up = [np.vstack([b, a]) for a in uniques for b in single]
            candidates = down + up
        uniques = filter_duplicates(candidates, option)
    return candidates

for option in range(1, 9):
    print(f"Option {option}:", flush=True)
    for n in [2, 3, 4, 5]:
        candidates = generate_candidates_canonical(n, option)
        unique = filter_duplicates(candidates, option)
        expected = TABLE1[option][n]
        mark = "PASS" if len(unique) == expected else "FAIL"
        print(f"  n={n}: {len(unique)} (expected {expected}) {mark}", flush=True)
