# ─────────────────────────────────────────────
# check08_bpl_bu.py
# ─────────────────────────────────────────────
"""Check 8: BPL/BU dichotomy — fixed points and stabilizer multisets."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from common import all_chains, fixed_count
from canonjam import canonical_key, generate_group

def v_fixed(n, option):
    return fixed_count(n, option, 0, 1)

def stabilizer_multiset(n, option):
    ops = generate_group(option)
    seen = set()
    multiset = {}
    for a in all_chains(n, option):
        k = canonical_key(a, option)
        if k in seen:
            continue
        seen.add(k)
        stab = frozenset(i for i, op in enumerate(ops)
                         if np.array_equal(op(a.copy()), a))
        multiset[stab] = multiset.get(stab, 0) + 1
    return multiset

ok = True
for n in [2, 3, 4]:
    fb = v_fixed(n, 2)
    fu = v_fixed(n, 3)
    sb = stabilizer_multiset(n, 2)
    su = stabilizer_multiset(n, 3)
    stab_equal = (sb == su)
    print(f"n={n}: |Fix_BPL(v)|={fb}, |Fix_BU(v)|={fu}, "
          f"stab multisets {'EQUAL' if stab_equal else 'DIFFER'}")
    if n % 2 == 0:
        if fb != fu:
            print(f"  FAIL: for even n, |Fix(v)| should be equal")
            ok = False
        if not stab_equal:
            print(f"  FAIL: for even n, stabilizer multisets should match")
            ok = False
    else:
        if fb == fu:
            print(f"  FAIL: for odd n, |Fix(v)| should differ")
            ok = False
        if stab_equal:
            print(f"  FAIL: for odd n, stabilizer multisets should differ")
            ok = False
print("\nPASS" if ok else "\nFAIL")
sys.exit(0 if ok else 1)
