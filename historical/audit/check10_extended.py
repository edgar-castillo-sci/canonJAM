# ─────────────────────────────────────────────
# check10_extended.py
# ─────────────────────────────────────────────
"""Check 10: extended options 5–8 and q = |Σ_1|."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonjam import canonical_key, rows_for_option
from common import all_chains

EXPECTED = {
    5: {2: 5, 3: 21, 4: 120, 5: 666},
    6: {2: 5, 3: 21, 4: 120, 5: 666},
    7: {2: 16, 3: 144, 4: 1776, 5: 20736},
    8: {2: 16, 3: 144, 4: 1776, 5: 20736},
}
EXPECTED_Q = {5: 6, 6: 6, 7: 12, 8: 12}

def count_orbits(n, option):
    seen = set()
    for a in all_chains(n, option):
        seen.add(canonical_key(a, option))
    return len(seen)

ok = True
for option in [5, 6, 7, 8]:
    q = len(rows_for_option(option))
    q_ok = (q == EXPECTED_Q[option])
    print(f"Option {option}: q={q} "
          f"({'OK' if q_ok else f'MISMATCH expected {EXPECTED_Q[option]}'})")
    ok = ok and q_ok
    for n in [2, 3, 4]:
        if n >= 4 and option in (7, 8):
            print(f"  n={n}: skipped (n=4 too large for brute force)")
            continue
        got = count_orbits(n, option)
        exp = EXPECTED[option][n]
        match = (got == exp)
        print(f"  n={n}: {got} (expected {exp}) "
              f"{'OK' if match else 'MISMATCH'}")
        ok = ok and match
print("\nPASS" if ok else "\nFAIL")
sys.exit(0 if ok else 1)
