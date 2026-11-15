# ─────────────────────────────────────────────
# check12_subgroups.py
# ─────────────────────────────────────────────
"""Check 12: order, |N_G|, and class size for U1..U10."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import U_REPS, normalizer, all_conjugates

EXPECTED = {
    1:  (1, 12, 1),  2:  (2, 12, 1),  3:  (2, 4, 3),  4:  (2, 4, 3),
    5:  (3, 12, 1),  6:  (4, 4, 3),   7:  (6, 12, 1), 8:  (6, 12, 1),
    9:  (6, 12, 1), 10:  (12, 12, 1),
}

ok = True
for i in range(1, 11):
    U = U_REPS[i]
    order = len(U)
    N = normalizer(U)
    class_size = len(all_conjugates(U))
    exp = EXPECTED[i]
    match = (order, len(N), class_size) == exp
    print(f"U{i:2d}: |U|={order:2d} (exp {exp[0]:2d}), "
          f"|N|={len(N):2d} (exp {exp[1]:2d}), "
          f"class={class_size:2d} (exp {exp[2]:2d}) "
          f"{'OK' if match else 'MISMATCH'}")
    ok = ok and match
print("\nPASS" if ok else "\nFAIL")
sys.exit(0 if ok else 1)
