# ─────────────────────────────────────────────
# check06_orbits.py
# ─────────────────────────────────────────────
"""Check 6: brute-force orbit enumeration vs published class counts."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonjam import canonical_key, rows_for_option
import numpy as np
from itertools import product

EXPECTED = {
    1: {2: 2, 3: 4, 4: 10, 5: 25},
    2: {2: 5, 3: 21, 4: 120, 5: 666},
    3: {2: 5, 3: 21, 4: 120, 5: 666},
    4: {2: 16, 3: 144, 4: 1776, 5: 20736},
}

def count_orbits(n, option):
    seen = set()
    single = [tuple(r) for r in rows_for_option(option)]
    for combo in product(single, repeat=n):
        a = np.array(combo, dtype=object)
        seen.add(canonical_key(a, option))
    return len(seen)

ok = True
for option in [1, 2, 3, 4]:
    for n in [2, 3, 4, 5]:
        if n >= 5 and option == 4:
            print(f"option={option} n={n}: skipped (too large)")
            continue
        got = count_orbits(n, option)
        exp = EXPECTED[option][n]
        match = (got == exp)
        print(f"option={option} n={n}: {got} (expected {exp}) "
              f"{'OK' if match else 'MISMATCH'}")
        ok = ok and match
print("\nPASS" if ok else "\nFAIL")
sys.exit(0 if ok else 1)
