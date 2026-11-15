# ─────────────────────────────────────────────
# check07_chiral.py
# ─────────────────────────────────────────────
"""Check 7: chiral/achiral split via sign-twisted Burnside."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from common import all_chains, fixed_counts_table
from canonjam import canonical_key, generate_group

def split_direct(n, option):
    ops = generate_group(option)
    seen = set()
    achiral = chiral = 0
    for a in all_chains(n, option):
        k = canonical_key(a, option)
        if k in seen:
            continue
        seen.add(k)
        stab = [i for i, op in enumerate(ops)
                if np.array_equal(op(a.copy()), a)]
        # z = 1 <=> index is odd
        if any(i % 2 == 1 for i in stab):
            achiral += 1
        else:
            chiral += 1
    return achiral, chiral

def split_formula(n, option):
    c = fixed_counts_table(n, option)
    sum_z0 = c["e"] + 3 * c["tau"] + 2 * c["omega"]
    sum_z1 = c["v"] + 3 * c["tau_v"] + 2 * c["omega_v"]
    achiral = 2 * sum_z1 // 12
    chiral = (sum_z0 - sum_z1) // 12
    return achiral, chiral

ok = True
for option in [1, 2, 3, 4]:
    for n in [2, 3, 4]:
        d_a, d_c = split_direct(n, option)
        f_a, f_c = split_formula(n, option)
        match = (d_a == f_a and d_c == f_c)
        print(f"option={option} n={n}: direct=(ach={d_a}, chir={d_c}), "
              f"formula=(ach={f_a}, chir={f_c}) "
              f"{'OK' if match else 'MISMATCH'}")
        ok = ok and match
print("\nPASS" if ok else "\nFAIL")
sys.exit(0 if ok else 1)
